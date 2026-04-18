"""
Ingesta de noticias desde fuentes RSS/Atom.

Lee `pipeline-config.yml` → sources, filtra por ventana temporal
(`lookback_days`) y escribe items normalizados en
`content/raw/YYYY-WW-raw.jsonl`.

Cada item: {id, title, link, summary, published_iso, source_name, source_geo, source_lang, source_topic_hint}

Uso:
    python -m scripts.ingest [--date YYYY-MM-DD]

Si no se pasa --date, toma la fecha de hoy para calcular la clave ISO-semana.
"""
from __future__ import annotations
import argparse
import datetime as dt
import hashlib
import json
import sys
from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode

import feedparser

from scripts.lib.config import config
from scripts.lib.paths import RAW_DIR, ensure_dirs, iso_week_key


def canon_url(url: str) -> str:
    """URL canónica mínima: quita utm_* y fragmentos."""
    if not url:
        return ""
    try:
        p = urlparse(url.strip())
        q = [(k, v) for k, v in parse_qsl(p.query) if not k.lower().startswith("utm_") and k.lower() not in ("fbclid", "gclid", "mc_cid", "mc_eid")]
        return urlunparse(p._replace(query=urlencode(q), fragment=""))
    except Exception:
        return url


def item_id(title: str, url: str) -> str:
    return hashlib.sha1(f"{canon_url(url)}|{(title or '').strip().lower()}".encode("utf-8")).hexdigest()[:16]


def parse_published(entry) -> dt.datetime | None:
    for field in ("published_parsed", "updated_parsed"):
        t = getattr(entry, field, None)
        if t:
            try:
                return dt.datetime(*t[:6], tzinfo=dt.timezone.utc)
            except Exception:
                pass
    return None


def ingest(today: dt.date | None = None) -> dict:
    ensure_dirs()
    cfg = config()
    ingest_cfg = cfg.get("ingest", {})
    lookback = dt.timedelta(days=int(ingest_cfg.get("lookback_days", 8)))
    cutoff_utc = dt.datetime.now(dt.timezone.utc) - lookback
    blocklist = set(d.lower() for d in cfg.get("blocklist_domains", []))

    week = iso_week_key(today)
    out_path = RAW_DIR / f"{week}-raw.jsonl"

    collected: list[dict] = []
    per_source: dict[str, int] = {}
    errors: list[dict] = []

    for src in cfg.get("sources", []):
        name = src.get("name", src.get("url"))
        try:
            feed = feedparser.parse(src["url"], agent=ingest_cfg.get("user_agent", "TheFleetRadarBot/1.0"))
        except Exception as e:
            errors.append({"source": name, "error": f"parse-failed: {e}"})
            continue

        if getattr(feed, "bozo", False) and not getattr(feed, "entries", None):
            errors.append({"source": name, "error": f"feed-bozo: {getattr(feed, 'bozo_exception', 'unknown')}"})
            continue

        count = 0
        max_per = int(ingest_cfg.get("max_items_per_source", 30))
        for entry in feed.entries[:max_per]:
            link = entry.get("link") or ""
            if not link:
                continue
            host = urlparse(link).hostname or ""
            if any(host.endswith(bad) for bad in blocklist):
                continue

            published = parse_published(entry)
            if published and published < cutoff_utc:
                continue

            title = (entry.get("title") or "").strip()
            summary = (entry.get("summary") or entry.get("description") or "").strip()
            # Limpieza simple HTML
            summary = summary.replace("\n", " ").strip()
            if len(summary) > 800:
                summary = summary[:797] + "..."

            item = {
                "id": item_id(title, link),
                "title": title,
                "link": canon_url(link),
                "summary": summary,
                "published_iso": published.isoformat() if published else None,
                "source_name": name,
                "source_geo": src.get("geo", "global"),
                "source_lang": src.get("lang", "en"),
                "source_topic_hint": src.get("topic_hint", ""),
            }
            collected.append(item)
            count += 1
        per_source[name] = count

    # Dedupe grueso por id antes de escribir
    seen = set()
    unique = []
    for it in collected:
        if it["id"] in seen:
            continue
        seen.add(it["id"])
        unique.append(it)

    with out_path.open("w", encoding="utf-8") as f:
        for it in unique:
            f.write(json.dumps(it, ensure_ascii=False) + "\n")

    return {
        "week": week,
        "path": str(out_path),
        "total_items": len(unique),
        "per_source": per_source,
        "errors": errors,
    }


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--date", help="YYYY-MM-DD (default: hoy)")
    args = p.parse_args(argv)
    today = dt.date.fromisoformat(args.date) if args.date else None
    result = ingest(today)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
