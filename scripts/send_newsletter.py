"""
send_newsletter.py — Crea y envía un broadcast semanal en Resend.

Flujo:
  1. Carga el compose-info de la edición (por fecha o el más reciente)
  2. Genera el HTML del email via generate_email.py
  3. Crea un broadcast en Resend (POST /broadcasts)
  4. Lo envía inmediatamente (POST /broadcasts/{id}/send)
  5. Imprime JSON de resultado al stdout (para integración con el pipeline)

Uso:
  python -m scripts.send_newsletter --date 2026-05-26
  python -m scripts.send_newsletter  # usa la edición más reciente

Variables de entorno requeridas:
  RESEND_API_KEY         — API key de Resend (re_xxx)
  RESEND_AUDIENCE_ID     — UUID de la audience en Resend
  RESEND_FROM_EMAIL      — From address verificada (default: team@thefleetradar.com)

Nota sobre el dominio sender:
  Resend requiere que el dominio del from email esté verificado.
  Antes de usar thefleetradar.com como from, hay que:
    1. Resend → Domains → Add domain → thefleetradar.com
    2. Añadir registros SPF/DKIM/DMARC donde tengas el DNS
    3. Esperar ~30 min a que quede "Verified"
  Mientras no esté verificado, usa la dirección por defecto de Resend
  (onboarding@resend.dev o similar) para pruebas.
"""
from __future__ import annotations
import argparse
import datetime as dt
import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path

# Make scripts/ importable
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.generate_email import generate_email_html, generate_text, load_compose_info
from scripts.lib.templating import human_date_es, FLAGS, MARKET_LABELS


RESEND_API = "https://api.resend.com"
DEFAULT_FROM = "The Fleet Radar <team@thefleetradar.com>"


def _post(url: str, payload: dict, api_key: str) -> tuple[int, dict]:
    """Simple HTTP POST usando urllib (sin dependencias extra)."""
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = {}
        try:
            body = json.loads(e.read().decode("utf-8"))
        except Exception:
            pass
        return e.code, body


def send_newsletter(
    compose_info: dict,
    api_key: str,
    audience_id: str,
    from_email: str = DEFAULT_FROM,
    dry_run: bool = False,
) -> dict:
    """Crea y envía el broadcast. Devuelve dict con status y detalles."""
    edition_date = compose_info.get("edition_date", "")
    number = compose_info.get("number", 1)
    cover_headline = compose_info.get("cover_headline", "")
    date_obj = dt.date.fromisoformat(edition_date) if edition_date else dt.date.today()
    human_date = human_date_es(date_obj)

    subject = f"Nº {number:02d} · {cover_headline} · The Fleet Radar"
    html = generate_email_html(compose_info)
    text = generate_text(compose_info)

    if dry_run:
        print(f"[DRY-RUN] Subject: {subject}", file=sys.stderr)
        print(f"[DRY-RUN] From: {from_email}", file=sys.stderr)
        print(f"[DRY-RUN] Audience: {audience_id}", file=sys.stderr)
        print(f"[DRY-RUN] HTML length: {len(html)} chars", file=sys.stderr)
        return {
            "status": "dry-run",
            "subject": subject,
            "edition_date": edition_date,
            "number": number,
        }

    # 1. Crear broadcast
    print(f"Creando broadcast: {subject}", file=sys.stderr)
    status, body = _post(
        f"{RESEND_API}/broadcasts",
        {
            "name": f"The Fleet Radar · Nº {number:02d} · {edition_date}",
            "audience_id": audience_id,
            "from": from_email,
            "subject": subject,
            "html": html,
            "text": text,
            "reply_to": "hola@getpulpo.com",
        },
        api_key,
    )

    if status not in (200, 201):
        msg = body.get("message", body.get("error", "Error desconocido"))
        print(f"ERROR creando broadcast: {status} — {msg}", file=sys.stderr)
        return {
            "status": "error",
            "step": "create",
            "http_status": status,
            "error": msg,
        }

    broadcast_id = body.get("id")
    print(f"Broadcast creado: {broadcast_id}", file=sys.stderr)

    # 2. Enviar broadcast
    print("Enviando broadcast…", file=sys.stderr)
    send_status, send_body = _post(
        f"{RESEND_API}/broadcasts/{broadcast_id}/send",
        {},
        api_key,
    )

    if send_status not in (200, 201):
        msg = send_body.get("message", send_body.get("error", "Error desconocido"))
        print(f"ERROR enviando broadcast: {send_status} — {msg}", file=sys.stderr)
        return {
            "status": "error",
            "step": "send",
            "broadcast_id": broadcast_id,
            "http_status": send_status,
            "error": msg,
        }

    print(f"✓ Broadcast enviado. ID: {broadcast_id}", file=sys.stderr)
    return {
        "status": "sent",
        "broadcast_id": broadcast_id,
        "subject": subject,
        "edition_date": edition_date,
        "number": number,
        "from": from_email,
        "audience_id": audience_id,
    }


def main(argv=None):
    p = argparse.ArgumentParser(description="Envía el newsletter semanal vía Resend.")
    p.add_argument("--date", help="YYYY-MM-DD de la edición")
    p.add_argument("--dry-run", action="store_true",
                   help="Genera el email pero no lo envía")
    p.add_argument("--from", dest="from_email", default=None,
                   help=f"From address (default: {DEFAULT_FROM})")
    args = p.parse_args(argv)

    api_key = os.environ.get("RESEND_API_KEY", "")
    audience_id = os.environ.get("RESEND_AUDIENCE_ID", "")

    if not api_key or not audience_id:
        if not args.dry_run:
            print(json.dumps({
                "status": "error",
                "error": "Faltan RESEND_API_KEY o RESEND_AUDIENCE_ID"
            }))
            return 1
        else:
            print("WARN: Variables de entorno no configuradas — modo dry-run", file=sys.stderr)

    date = dt.date.fromisoformat(args.date) if args.date else None
    info = load_compose_info(date)
    if not info:
        result = {"status": "error", "error": "No se encontró compose-info"}
        print(json.dumps(result))
        return 1

    if info.get("status") == "pause":
        result = {"status": "pause", "message": "Semana de pausa editorial — no se envía newsletter"}
        print(json.dumps(result))
        return 0

    from_email = args.from_email or DEFAULT_FROM
    result = send_newsletter(
        compose_info=info,
        api_key=api_key,
        audience_id=audience_id,
        from_email=from_email,
        dry_run=args.dry_run,
    )

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("status") in ("sent", "dry-run") else 1


if __name__ == "__main__":
    sys.exit(main())
