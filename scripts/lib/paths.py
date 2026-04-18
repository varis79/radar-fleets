"""Rutas canónicas del repo. Todas relativas al ROOT del repo."""
from __future__ import annotations
from pathlib import Path
import datetime as dt

ROOT = Path(__file__).resolve().parents[2]

CONFIG_FILE = ROOT / "pipeline-config.yml"
PROMPTS_DIR = ROOT / "prompts"
MASTER_PROMPT = PROMPTS_DIR / "radar-master-prompt.md"
QA_CHECKLIST = PROMPTS_DIR / "qa-checklist.md"

CONTENT_DIR = ROOT / "content"
TAXONOMY_DIR = CONTENT_DIR / "taxonomy"
RAW_DIR = CONTENT_DIR / "raw"
QA_DIR = CONTENT_DIR / "qa"
DECISIONS_DIR = CONTENT_DIR / "decisions"
EDITORIAL_MEMORY = CONTENT_DIR / "editorial-memory.md"
MARKET_WATCH = CONTENT_DIR / "market-watch.md"
PULPO_UPDATE = CONTENT_DIR / "pulpo-update.md"
PULPO_FACTS = CONTENT_DIR / "pulpo-facts.md"

MAGAZINES_DIR = ROOT / "magazines"
INDEX_HTML = ROOT / "index.html"
ARCHIVE_HTML = ROOT / "archive.html"
SITEMAP_XML = ROOT / "sitemap.xml"
RSS_XML = ROOT / "rss.xml"


def iso_week_key(d: dt.date | None = None) -> str:
    """Devuelve la clave ISO-semana YYYY-WW para agrupar artefactos del pipeline."""
    d = d or dt.date.today()
    y, w, _ = d.isocalendar()
    return f"{y}-W{w:02d}"


def ensure_dirs() -> None:
    for p in (RAW_DIR, QA_DIR, DECISIONS_DIR):
        p.mkdir(parents=True, exist_ok=True)


def next_monday(from_date: dt.date | None = None) -> dt.date:
    """Lunes siguiente (o hoy si ya es lunes)."""
    d = from_date or dt.date.today()
    offset = (7 - d.weekday()) % 7
    offset = 7 if offset == 0 and d.weekday() != 0 else offset
    if d.weekday() == 0:
        return d
    return d + dt.timedelta(days=offset)


def magazine_paths(edition_date: dt.date) -> dict:
    slug = f"{edition_date.isoformat()}-radar-fleet-by-pulpo"
    return {
        "slug": slug,
        "html": MAGAZINES_DIR / f"{slug}.html",
        "summary": MAGAZINES_DIR / f"{slug}-summary.txt",
        "permalink": f"/magazines/{slug}.html",
    }
