"""
send_newsletter.py — Crea y envía un broadcast semanal en Resend.

Flujo:
  1. Carga el compose-info de la edición (por fecha o el más reciente)
  2. Comprueba deduplicación: si ya se envió esta semana, sale sin hacer nada
  3. Genera copy editorial via generate_newsletter_copy.py (Claude)
  4. Genera el HTML del email via generate_email.py
  5. Crea un broadcast en Resend (POST /broadcasts)
  6. Lo envía inmediatamente (POST /broadcasts/{id}/send)
  7. Guarda registro de envío en content/decisions/{week}-newsletter.json
  8. Imprime JSON de resultado al stdout (para integración con el pipeline)

Uso:
  python -m scripts.send_newsletter --date 2026-05-26
  python -m scripts.send_newsletter  # usa la edición más reciente
  python -m scripts.send_newsletter --dry-run  # genera email pero no envía
  python -m scripts.send_newsletter --no-claude  # salta Claude, usa fallback

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
from pathlib import Path

import requests

# Make scripts/ importable
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.generate_email import generate_email_html, generate_text, load_compose_info
from scripts.lib.paths import DECISIONS_DIR, iso_week_key
from scripts.lib.templating import human_date_es, FLAGS, MARKET_LABELS


RESEND_API = "https://api.resend.com"
DEFAULT_FROM = "The Fleet Radar <team@thefleetradar.com>"


def _post(url: str, payload: dict, api_key: str) -> tuple[int, dict]:
    """HTTP POST a la API de Resend usando requests (maneja SSL correctamente en macOS)."""
    resp = requests.post(
        url,
        json=payload,
        headers={"Authorization": f"Bearer {api_key}"},
        timeout=30,
    )
    try:
        body = resp.json()
    except Exception:
        body = {}
    return resp.status_code, body


def _newsletter_record_path(date: dt.date | None = None) -> Path:
    week = iso_week_key(date)
    return DECISIONS_DIR / f"{week}-newsletter.json"


def _already_sent(date: dt.date | None = None) -> dict | None:
    """Devuelve el registro de envío si ya se mandó esta semana, o None."""
    path = _newsletter_record_path(date)
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return None


def _save_record(record: dict, date: dt.date | None = None) -> None:
    """Guarda el registro de envío para deduplicación futura."""
    DECISIONS_DIR.mkdir(parents=True, exist_ok=True)
    path = _newsletter_record_path(date)
    path.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")


def send_newsletter(
    compose_info: dict,
    api_key: str,
    audience_id: str,
    from_email: str = DEFAULT_FROM,
    dry_run: bool = False,
    no_claude: bool = False,
) -> dict:
    """Genera copy (Claude), crea y envía el broadcast. Devuelve dict con status y detalles."""
    edition_date = compose_info.get("edition_date", "")
    number = compose_info.get("number", 1)
    cover_headline = compose_info.get("cover_headline", "")
    date_obj = dt.date.fromisoformat(edition_date) if edition_date else dt.date.today()

    # ── 1. Generar copy editorial con Claude ──────────────────────────────────
    newsletter_copy = None
    if not no_claude:
        try:
            from scripts.generate_newsletter_copy import generate_copy
            print("  Generando copy editorial con Claude…", file=sys.stderr)
            newsletter_copy = generate_copy(compose_info)
        except Exception as e:
            print(f"  WARN: generate_copy falló ({e}) — usando fallback", file=sys.stderr)

    # ── 2. Construir subject y contenido del email ────────────────────────────
    # Usa subject_line de Claude si está disponible; si no, genera uno básico
    subject_from_claude = (newsletter_copy or {}).get("subject_line", "")
    if subject_from_claude:
        subject = subject_from_claude
        # Añadir número de edición si no está ya
        if f"Nº {number:02d}" not in subject and "Fleet Radar" not in subject:
            subject = f"Nº {number:02d} · {subject}"
    else:
        subject = f"Nº {number:02d} · {cover_headline} · The Fleet Radar"

    html = generate_email_html(compose_info, newsletter_copy)
    text = generate_text(compose_info, newsletter_copy)

    if dry_run:
        print(f"[DRY-RUN] Subject: {subject}", file=sys.stderr)
        print(f"[DRY-RUN] From: {from_email}", file=sys.stderr)
        print(f"[DRY-RUN] Audience: {audience_id}", file=sys.stderr)
        print(f"[DRY-RUN] HTML length: {len(html)} chars", file=sys.stderr)
        stories_count = len((newsletter_copy or {}).get("stories", []))
        print(f"[DRY-RUN] Historias teaser: {stories_count}", file=sys.stderr)
        return {
            "status": "dry-run",
            "subject": subject,
            "edition_date": edition_date,
            "number": number,
            "copy_source": (newsletter_copy or {}).get("_source", "fallback"),
        }

    # ── 3. Crear broadcast ────────────────────────────────────────────────────
    print(f"  Creando broadcast: {subject}", file=sys.stderr)
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
        print(f"  ERROR creando broadcast: {status} — {msg}", file=sys.stderr)
        return {
            "status": "error",
            "step": "create",
            "http_status": status,
            "error": msg,
        }

    broadcast_id = body.get("id")
    print(f"  Broadcast creado: {broadcast_id}", file=sys.stderr)

    # ── 4. Enviar broadcast ───────────────────────────────────────────────────
    print("  Enviando broadcast…", file=sys.stderr)
    send_status, send_body = _post(
        f"{RESEND_API}/broadcasts/{broadcast_id}/send",
        {},
        api_key,
    )

    if send_status not in (200, 201):
        msg = send_body.get("message", send_body.get("error", "Error desconocido"))
        print(f"  ERROR enviando broadcast: {send_status} — {msg}", file=sys.stderr)
        return {
            "status": "error",
            "step": "send",
            "broadcast_id": broadcast_id,
            "http_status": send_status,
            "error": msg,
        }

    print(f"  ✓ Broadcast enviado. ID: {broadcast_id}", file=sys.stderr)

    result = {
        "status": "sent",
        "broadcast_id": broadcast_id,
        "subject": subject,
        "edition_date": edition_date,
        "number": number,
        "from": from_email,
        "audience_id": audience_id,
        "copy_source": (newsletter_copy or {}).get("_source", "fallback"),
        "sent_at": dt.datetime.utcnow().isoformat() + "Z",
    }
    return result


def main(argv=None):
    p = argparse.ArgumentParser(description="Envía el newsletter semanal vía Resend.")
    p.add_argument("--date", help="YYYY-MM-DD de la edición")
    p.add_argument("--dry-run", action="store_true",
                   help="Genera el email pero no lo envía")
    p.add_argument("--no-claude", action="store_true",
                   help="Salta la generación de copy con Claude (usa fallback)")
    p.add_argument("--force", action="store_true",
                   help="Envía aunque ya se haya enviado esta semana (sobreescribe dedup)")
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
            print("  WARN: Variables de entorno no configuradas — modo dry-run", file=sys.stderr)

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

    # ── Deduplicación ─────────────────────────────────────────────────────────
    if not args.dry_run and not args.force:
        existing = _already_sent(date)
        if existing:
            broadcast_id = existing.get("broadcast_id", "?")
            sent_at = existing.get("sent_at", "?")
            print(f"  INFO: Newsletter ya enviado esta semana "
                  f"(broadcast_id={broadcast_id}, sent_at={sent_at}) — saliendo.",
                  file=sys.stderr)
            result = {
                "status": "already-sent",
                "broadcast_id": broadcast_id,
                "sent_at": sent_at,
                "edition_date": existing.get("edition_date"),
                "number": existing.get("number"),
            }
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 0

    from_email = args.from_email or DEFAULT_FROM
    result = send_newsletter(
        compose_info=info,
        api_key=api_key,
        audience_id=audience_id,
        from_email=from_email,
        dry_run=args.dry_run,
        no_claude=args.no_claude,
    )

    # ── Guardar registro de envío (dedup) ─────────────────────────────────────
    if result.get("status") == "sent":
        _save_record(result, date)
        print(f"  ✓ Registro guardado en decisions/{iso_week_key(date)}-newsletter.json",
              file=sys.stderr)

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("status") in ("sent", "dry-run", "already-sent") else 1


if __name__ == "__main__":
    sys.exit(main())
