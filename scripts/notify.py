"""
Notificación Slack al terminar la edición semanal.

Lee el slack_summary generado por compose y lo postea al webhook de Slack.

Requiere:
  SLACK_WEBHOOK_URL  — webhook de Slack (secreto de GitHub).
                       Si no está definido, el paso se omite silenciosamente.

El webhook apunta al canal #general de Pulpo (o el que se configure).
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

from scripts.lib.paths import DECISIONS_DIR, iso_week_key, magazine_paths, next_monday


def notify(today: dt.date | None = None) -> dict:
    webhook_url = os.environ.get("SLACK_WEBHOOK_URL", "").strip()
    if not webhook_url:
        return {"status": "skipped", "reason": "no SLACK_WEBHOOK_URL"}

    week = iso_week_key(today)

    # Leer compose info para metadatos
    compose_path = DECISIONS_DIR / f"{week}-compose.json"
    if not compose_path.exists():
        return {"status": "skipped", "reason": "no compose info"}
    compose_info = json.loads(compose_path.read_text(encoding="utf-8"))

    if compose_info.get("status") == "pause":
        return {"status": "skipped", "reason": "pause week"}

    # Leer slack_summary
    slack_path = DECISIONS_DIR / f"{week}-slack.txt"
    if slack_path.exists():
        message = slack_path.read_text(encoding="utf-8").strip()
    else:
        # Fallback: mensaje mínimo si compose no generó el campo
        edition_date = dt.date.fromisoformat(compose_info["edition_date"])
        number = compose_info.get("number", "?")
        paths = magazine_paths(edition_date)
        permalink = f"https://thefleetradar.com{paths['permalink']}"
        message = (
            f"Ya está fuera la nueva edición de The Fleet Radar by Pulpo - "
            f"Nº {number:02d} · {edition_date.strftime('%d %b %Y')}\n\n"
            f"{permalink}"
        )

    # Añadir enlace al final si no está ya en el mensaje
    edition_date = dt.date.fromisoformat(compose_info["edition_date"])
    paths = magazine_paths(edition_date)
    permalink = f"https://thefleetradar.com{paths['permalink']}"
    if permalink not in message:
        message = message + f"\n\n🔗 {permalink}"

    # POST al webhook
    payload = json.dumps({"text": message}).encode("utf-8")
    req = urllib.request.Request(
        webhook_url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            status_code = resp.getcode()
    except urllib.error.HTTPError as e:
        return {"status": "error", "reason": f"HTTP {e.code}: {e.reason}"}
    except urllib.error.URLError as e:
        return {"status": "error", "reason": str(e.reason)}

    if status_code == 200:
        return {
            "status": "sent",
            "week": week,
            "edition_date": compose_info["edition_date"],
            "number": compose_info.get("number"),
            "chars": len(message),
        }
    return {"status": "error", "reason": f"unexpected HTTP {status_code}"}


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--date", help="YYYY-MM-DD (default: hoy)")
    args = p.parse_args(argv)
    today = dt.date.fromisoformat(args.date) if args.date else None
    result = notify(today)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0  # nunca bloquea el pipeline


if __name__ == "__main__":
    sys.exit(main())
