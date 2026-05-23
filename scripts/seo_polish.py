#!/usr/bin/env python3
"""
seo_polish.py — Polish final de SEO técnico:

  1. og:title/twitter:title sincronizados con <title>
  2. BreadcrumbList schema en magazines (faltaba en los 7) + evergreens nuevos
  3. hreflang reciprocity MX↔ES en pares paralelos (casos-uso, sectores, temas)
  4. ItemList JSON-LD en home con últimas 5 ediciones
  5. Breadcrumb visual en magazines (Home › Ediciones › Nº X)

Idempotente: si ya existe el tag/schema correcto, no toca.

Uso:
    python3 scripts/seo_polish.py [--dry-run]
"""
import sys
import re
import json
import datetime as dt
from pathlib import Path
from bs4 import BeautifulSoup, Tag

DRY_RUN = "--dry-run" in sys.argv
ROOT = Path(__file__).parent.parent
SITE = "https://thefleetradar.com"


# ── 1. og:title / twitter:title sync ─────────────────────────────────────────

def sync_titles(soup: BeautifulSoup) -> bool:
    title = soup.find("title")
    if not title:
        return False
    title_text = title.get_text(strip=True)
    changed = False

    for meta in soup.find_all("meta", attrs={"property": "og:title"}):
        if meta.get("content") != title_text:
            meta["content"] = title_text
            changed = True

    for meta in soup.find_all("meta", attrs={"name": "twitter:title"}):
        if meta.get("content") != title_text:
            meta["content"] = title_text
            changed = True

    return changed


# ── 2. BreadcrumbList schema ─────────────────────────────────────────────────

def _build_breadcrumb(items: list[tuple[str, str]]) -> str:
    """items: [(name, url)]"""
    list_items = []
    for i, (name, url) in enumerate(items, start=1):
        list_items.append({
            "@type": "ListItem",
            "position": i,
            "name": name,
            "item": url,
        })
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": list_items,
    }, ensure_ascii=False, separators=(",", ":"))


def add_magazine_breadcrumb(soup: BeautifulSoup, mag_path: Path) -> bool:
    """Añade BreadcrumbList schema a magazine si falta."""
    if soup.find("script", string=re.compile(r"BreadcrumbList")):
        return False
    head = soup.find("head")
    if not head:
        return False

    # Derivar nº de edición y fecha del filename: 2026-05-18-radar-fleet-by-pulpo.html
    fname = mag_path.name
    m = re.match(r"(\d{4}-\d{2}-\d{2})", fname)
    if not m:
        return False
    date_str = m.group(1)
    date_obj = dt.date.fromisoformat(date_str)
    # Detectar Nº edición desde el title si está disponible
    title_text = (soup.find("title").get_text(strip=True) if soup.find("title") else "")
    n_match = re.search(r"Nº\s*(\d+)", title_text)
    n_label = f"Nº {n_match.group(1)}" if n_match else f"Edición {date_str}"

    items = [
        ("The Fleet Radar", f"{SITE}/"),
        ("Archivo", f"{SITE}/archive.html"),
        (n_label, f"{SITE}/magazines/{fname}"),
    ]
    bc = soup.new_tag("script", type="application/ld+json")
    bc.string = _build_breadcrumb(items)
    head.append(bc)
    return True


def add_evergreen_breadcrumb(soup: BeautifulSoup, page_path: Path) -> bool:
    """Añade BreadcrumbList a evergreen si falta."""
    if soup.find("script", string=re.compile(r"BreadcrumbList")):
        return False
    head = soup.find("head")
    if not head:
        return False
    rel = page_path.parent.relative_to(ROOT)
    parts = rel.parts  # evergreen, checklists, slug

    items = [
        ("The Fleet Radar", f"{SITE}/"),
        ("Recursos", f"{SITE}/evergreen/"),
    ]
    if len(parts) >= 2:
        cat = parts[1]
        cat_label = {"checklists": "Checklists", "guias": "Guías"}.get(cat, cat.title())
        items.append((cat_label, f"{SITE}/{parts[0]}/{parts[1]}/"))
    title_tag = soup.find("title")
    page_name = (title_tag.get_text(strip=True).split("·")[0].strip()
                 if title_tag else rel.name)
    items.append((page_name, f"{SITE}/{rel.as_posix()}/"))

    bc = soup.new_tag("script", type="application/ld+json")
    bc.string = _build_breadcrumb(items)
    head.append(bc)
    return True


# ── 3. hreflang reciprocity ──────────────────────────────────────────────────

def _existing_alternates(soup: BeautifulSoup) -> set[str]:
    return {l.get("href", "") for l in soup.find_all("link", rel="alternate")
            if l.get("hreflang")}


def add_hreflang_pair(soup: BeautifulSoup, sibling_url: str, sibling_lang: str) -> bool:
    head = soup.find("head")
    if not head:
        return False
    if sibling_url in _existing_alternates(soup):
        return False
    tag = soup.new_tag("link", rel="alternate")
    tag["hreflang"] = sibling_lang
    tag["href"] = sibling_url
    head.append(tag)
    return True


# ── 4. Home ItemList JSON-LD ─────────────────────────────────────────────────

def add_home_itemlist(soup: BeautifulSoup) -> bool:
    """Añade ItemList con últimas 5 ediciones al home si falta."""
    for sc in soup.find_all("script", type="application/ld+json"):
        if '"ItemList"' in (sc.string or ""):
            return False
    head = soup.find("head")
    if not head:
        return False

    mags = sorted((ROOT / "magazines").glob("*.html"), reverse=True)[:5]
    items = []
    for i, m in enumerate(mags, start=1):
        # Extract title from file
        s = BeautifulSoup(m.read_text(encoding="utf-8"), "html.parser")
        t = s.find("title")
        name = t.get_text(strip=True) if t else m.name
        items.append({
            "@type": "ListItem",
            "position": i,
            "url": f"{SITE}/magazines/{m.name}",
            "name": name,
        })
    schema = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "Últimas ediciones · The Fleet Radar",
        "description": "Las 5 ediciones más recientes de la publicación editorial semanal.",
        "numberOfItems": len(items),
        "itemListElement": items,
    }
    sc = soup.new_tag("script", type="application/ld+json")
    sc.string = json.dumps(schema, ensure_ascii=False, separators=(",", ":"))
    head.append(sc)
    return True


# ── Process pages ────────────────────────────────────────────────────────────

def process_magazine(path: Path) -> dict:
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    changes = {
        "titles": sync_titles(soup),
        "breadcrumb": add_magazine_breadcrumb(soup, path),
    }
    if any(changes.values()) and not DRY_RUN:
        path.write_text(str(soup), encoding="utf-8")
    return changes


def process_evergreen(path: Path) -> dict:
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    changes = {
        "titles": sync_titles(soup),
        "breadcrumb": add_evergreen_breadcrumb(soup, path),
    }
    if any(changes.values()) and not DRY_RUN:
        path.write_text(str(soup), encoding="utf-8")
    return changes


def process_with_hreflang_pair(mx_path: Path, es_path: Path) -> tuple[bool, bool]:
    """Garantiza que MX y ES se enlacen mutuamente via hreflang."""
    mx_url = f"{SITE}/{mx_path.parent.relative_to(ROOT).as_posix()}/"
    es_url = f"{SITE}/{es_path.parent.relative_to(ROOT).as_posix()}/"
    mx_soup = BeautifulSoup(mx_path.read_text(encoding="utf-8"), "html.parser")
    es_soup = BeautifulSoup(es_path.read_text(encoding="utf-8"), "html.parser")

    mx_changed = add_hreflang_pair(mx_soup, es_url, "es-ES")
    es_changed = add_hreflang_pair(es_soup, mx_url, "es-MX")
    # x-default opcional (apunta al MX por defecto en LatAm)
    if mx_changed:
        sync_titles(mx_soup)
    if es_changed:
        sync_titles(es_soup)

    if mx_changed and not DRY_RUN:
        mx_path.write_text(str(mx_soup), encoding="utf-8")
    if es_changed and not DRY_RUN:
        es_path.write_text(str(es_soup), encoding="utf-8")
    return mx_changed, es_changed


def process_home() -> dict:
    path = ROOT / "index.html"
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    changes = {
        "titles": sync_titles(soup),
        "itemlist": add_home_itemlist(soup),
    }
    if any(changes.values()) and not DRY_RUN:
        path.write_text(str(soup), encoding="utf-8")
    return changes


def process_other(path: Path) -> dict:
    """Pages generales: solo sync titles."""
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    changes = {"titles": sync_titles(soup)}
    if changes["titles"] and not DRY_RUN:
        path.write_text(str(soup), encoding="utf-8")
    return changes


def main():
    mode = "[DRY-RUN]" if DRY_RUN else "[LIVE]"
    print(f"\nseo_polish.py {mode}\n")

    stats = {"title_sync": 0, "breadcrumb_added": 0,
             "hreflang_added": 0, "itemlist_added": 0}

    # 1. Home
    print("── Home ──")
    ch = process_home()
    if ch["titles"]: stats["title_sync"] += 1
    if ch["itemlist"]:
        stats["itemlist_added"] += 1
        print("  ✅ ItemList JSON-LD añadida")
    print()

    # 2. Magazines (breadcrumb + title sync)
    print("── Magazines ──")
    for m in sorted((ROOT / "magazines").glob("*.html")):
        ch = process_magazine(m)
        if ch["titles"]: stats["title_sync"] += 1
        if ch["breadcrumb"]:
            stats["breadcrumb_added"] += 1
            print(f"  ✅ {m.name}: BreadcrumbList añadido")
    print()

    # 3. Evergreens (breadcrumb + title sync)
    print("── Evergreen ──")
    for p in sorted((ROOT / "evergreen").rglob("index.html")):
        ch = process_evergreen(p)
        if ch["titles"]: stats["title_sync"] += 1
        if ch["breadcrumb"]:
            stats["breadcrumb_added"] += 1
            print(f"  ✅ {p.relative_to(ROOT)}: BreadcrumbList añadido")
    print()

    # 4. hreflang MX↔ES en casos-uso/sectores/temas
    print("── hreflang MX↔ES ──")
    for section in ("casos-uso", "sectores", "temas"):
        d = ROOT / section
        if not d.exists():
            continue
        for mx_path in sorted(d.glob("*-mexico-*/index.html")):
            es_path = Path(str(mx_path).replace("-mexico-", "-espana-"))
            if not es_path.exists():
                continue
            mc, ec = process_with_hreflang_pair(mx_path, es_path)
            if mc: stats["hreflang_added"] += 1
            if ec: stats["hreflang_added"] += 1
    print(f"  hreflang tags añadidos: {stats['hreflang_added']}")
    print()

    # 5. Title sync on all other content pages
    print("── Title sync resto de páginas ──")
    other_paths = []
    for section in ("temas", "mercados", "casos-uso", "sectores", "ciudades"):
        d = ROOT / section
        if d.exists():
            other_paths.extend(d.rglob("index.html"))
    other_paths.extend([ROOT / "about/index.html", ROOT / "archive.html"])
    for p in sorted(set(other_paths)):
        if not p.exists():
            continue
        ch = process_other(p)
        if ch["titles"]: stats["title_sync"] += 1
    print(f"  títulos sincronizados (total): {stats['title_sync']}")

    print()
    print(f"Resumen: titles={stats['title_sync']}  breadcrumbs={stats['breadcrumb_added']}  "
          f"hreflang={stats['hreflang_added']}  itemlist={stats['itemlist_added']}")


if __name__ == "__main__":
    main()
