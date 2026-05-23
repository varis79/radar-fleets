#!/usr/bin/env python3
"""
refresh_freshness.py — Marca páginas pillar como "vivas" para Google.

Cada vez que corre (cron semanal):
  1. Selecciona ~30 páginas (rotación: (epoch_week + page_hash) % CYCLE_WEEKS)
  2. Para cada una, actualiza:
     - <meta property="article:modified_time" content="ISO8601">
     - <meta property="article:published_time"> si no existe
     - <time datetime="ISO">Actualizado el DD de MMM de AAAA</time> en el hero
     - JSON-LD Article.dateModified
  3. Regenera sitemap.xml entero (lastmod = mtime real)

Estrategia anti-spam:
  - NO toca todas las páginas a la vez (Google penaliza updates masivos sin cambio real)
  - Rota: cada página recibe ~1 refresh cada CYCLE_WEEKS semanas (~6)
  - El refresh es un "touch" semántico: marca que el equipo editorial revisó la página
  - Combinable con rotate_facts.py para inyectar cambios de contenido reales

Uso:
    python3 scripts/refresh_freshness.py [--dry-run] [--all]
    --all: ignora rotación, refresca todas las páginas (solo para inicialización)
"""
import sys
import json
import re
import hashlib
import datetime as dt
from pathlib import Path
from bs4 import BeautifulSoup, Tag

DRY_RUN = "--dry-run" in sys.argv
REFRESH_ALL = "--all" in sys.argv

ROOT = Path(__file__).parent.parent

CYCLE_WEEKS = 6  # ~30 pages × 6 weeks = ~180 page-refreshes/cycle for ~170 pages

MONTH_NAMES_ES = ["enero", "febrero", "marzo", "abril", "mayo", "junio",
                  "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]


def _format_es_date(d: dt.date) -> str:
    return f"{d.day} de {MONTH_NAMES_ES[d.month - 1]} de {d.year}"


def _page_should_refresh(rel_path: str, today: dt.date) -> bool:
    """True si la página le toca refresh esta semana."""
    if REFRESH_ALL:
        return True
    iso_year, iso_week, _ = today.isocalendar()
    page_hash = int(hashlib.sha1(rel_path.encode()).hexdigest(), 16)
    return (iso_week + page_hash) % CYCLE_WEEKS == 0


def _inject_meta(soup: BeautifulSoup, today_iso: str) -> bool:
    """Asegura <meta property='article:modified_time'> en <head>. Devuelve True si tocó."""
    head = soup.find("head")
    if head is None:
        return False
    changed = False

    # article:modified_time
    mod = soup.find("meta", attrs={"property": "article:modified_time"})
    if mod:
        if mod.get("content") != today_iso:
            mod["content"] = today_iso
            changed = True
    else:
        tag = soup.new_tag("meta", attrs={
            "property": "article:modified_time",
            "content": today_iso,
        })
        head.append(tag)
        changed = True

    # article:published_time (si no existe, derivar de Article JSON-LD o usar mtime)
    pub = soup.find("meta", attrs={"property": "article:published_time"})
    if not pub:
        pub_date = _extract_published_from_jsonld(soup) or today_iso
        tag = soup.new_tag("meta", attrs={
            "property": "article:published_time",
            "content": pub_date,
        })
        head.append(tag)
        changed = True

    return changed


def _extract_published_from_jsonld(soup: BeautifulSoup) -> str | None:
    for sc in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(sc.string or "")
        except Exception:
            continue
        if isinstance(data, dict) and data.get("datePublished"):
            return data["datePublished"]
    return None


def _inject_time_tag(soup: BeautifulSoup, today: dt.date) -> bool:
    """Inyecta o actualiza <time> visible en hero/encabezado. Devuelve True si tocó."""
    iso = today.isoformat()
    pretty = _format_es_date(today)

    existing = soup.find("time", class_="page-updated")
    if existing:
        if existing.get("datetime") != iso:
            existing["datetime"] = iso
            existing.string = f"Actualizado el {pretty}"
            return True
        return False

    # Inyectar en pillar-hero o mkt-hero o equivalente
    hero = (soup.find(class_="pillar-hero") or soup.find(class_="mkt-hero")
            or soup.find(class_="e-hero") or soup.find("header", class_="hero"))
    if hero is None:
        return False

    time_tag = soup.new_tag("time", attrs={
        "class": "page-updated",
        "datetime": iso,
    })
    time_tag.string = f"Actualizado el {pretty}"
    hero.append(time_tag)
    return True


def _update_jsonld_modified(soup: BeautifulSoup, today_iso: str) -> bool:
    """Actualiza dateModified en cualquier JSON-LD Article/WebPage."""
    changed = False
    for sc in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(sc.string or "")
        except Exception:
            continue
        if not isinstance(data, dict):
            continue
        type_ = data.get("@type")
        if type_ in ("Article", "NewsArticle", "BlogPosting", "WebPage", "CollectionPage"):
            if data.get("dateModified") != today_iso:
                data["dateModified"] = today_iso
                if not data.get("datePublished"):
                    data["datePublished"] = today_iso
                sc.string = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
                changed = True
    return changed


def process_file(path: Path, today: dt.date) -> bool:
    """Devuelve True si tocó el archivo."""
    text = path.read_text(encoding="utf-8")
    soup = BeautifulSoup(text, "html.parser")

    today_iso = today.isoformat()
    changed = False
    if _inject_meta(soup, today_iso):
        changed = True
    if _inject_time_tag(soup, today):
        changed = True
    if _update_jsonld_modified(soup, today_iso):
        changed = True

    if changed and not DRY_RUN:
        path.write_text(str(soup), encoding="utf-8")
    return changed


def main():
    today = dt.date.today()
    mode = "[DRY-RUN]" if DRY_RUN else "[LIVE]"
    scope = "[ALL]" if REFRESH_ALL else f"[rotation cycle={CYCLE_WEEKS}w]"
    print(f"\nrefresh_freshness.py {mode} {scope}  today={today.isoformat()}\n")

    # Páginas elegibles: contenido editorial (no legal, no 404, no styleguide)
    files = []
    for section in ("temas", "mercados", "casos-uso", "sectores", "ciudades"):
        d = ROOT / section
        if d.exists():
            files.extend(sorted(d.rglob("index.html")))
    for sub in ("evergreen/checklists", "evergreen/guias"):
        d = ROOT / sub
        if d.exists():
            files.extend(sorted(d.rglob("index.html")))

    selected = [p for p in files
                if _page_should_refresh(str(p.relative_to(ROOT)), today)]
    print(f"  Páginas candidatas: {len(files)}")
    print(f"  Seleccionadas esta semana: {len(selected)}")
    print()

    touched = 0
    for path in selected:
        if process_file(path, today):
            touched += 1
            marker = "[DRY]" if DRY_RUN else "  ✅"
            print(f"  {marker} {path.relative_to(ROOT)}")

    print()
    print(f"  Total refrescadas: {touched} / {len(selected)} seleccionadas")

    # Trigger sitemap regen (importamos en runtime para evitar coste si no toca)
    if not DRY_RUN and touched > 0:
        print("\n  Regenerando sitemap.xml…")
        # Import perezoso del rebuild_sitemap como módulo
        sys.path.insert(0, str(ROOT / "scripts"))
        import importlib
        rs = importlib.import_module("rebuild_sitemap")
        entries = rs._collect()
        xml = rs._serialize(entries)
        (ROOT / "sitemap.xml").write_text(xml, encoding="utf-8")
        print(f"  ✅ sitemap.xml regenerado con {len(entries)} URLs")


if __name__ == "__main__":
    main()
