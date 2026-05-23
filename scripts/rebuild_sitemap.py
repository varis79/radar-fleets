#!/usr/bin/env python3
"""
rebuild_sitemap.py — Regenera sitemap.xml entero recorriendo el filesystem.

Incluye TODAS las páginas publicadas:
  - Home, archive, about
  - magazines/*.html
  - temas/*/, mercados/*/, casos-uso/*/, sectores/*/, ciudades/*/
  - evergreen/checklists/*/, evergreen/guias/*/

Excluye:
  - Páginas con <meta name="robots" content="noindex...">
  - 404.html, styleguide.html
  - Drafts (cualquier path con "draft")

lastmod = mtime real del index.html.
Priority/changefreq deducidos por tipo.

Uso:
    python3 scripts/rebuild_sitemap.py [--dry-run]
"""
import sys
import datetime as dt
from pathlib import Path

ROOT = Path(__file__).parent.parent
SITE = "https://thefleetradar.com"
DRY_RUN = "--dry-run" in sys.argv

EXCLUDE_NAMES = {"404.html", "styleguide.html"}


def _is_noindex(path: Path) -> bool:
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return True
    # Simple grep; cubre ambos orderings de attrs
    return 'content="noindex' in text or "content='noindex" in text


def _meta_for(path: Path) -> tuple[str, float, str]:
    """Devuelve (url, priority, changefreq) según el tipo de página."""
    rel = path.relative_to(ROOT)
    parts = rel.parts

    # Home
    if rel == Path("index.html"):
        return (f"{SITE}/", 1.0, "weekly")
    if rel == Path("archive.html"):
        return (f"{SITE}/archive.html", 0.8, "weekly")

    # magazine HTML files
    if parts[0] == "magazines" and rel.suffix == ".html":
        # Determinar si es la más reciente
        return (f"{SITE}/{rel.as_posix()}", 0.9, "monthly")

    # Directory-style URL (index.html in subdir)
    if rel.name == "index.html":
        url = f"{SITE}/{'/'.join(parts[:-1])}/"
        section = parts[0]
        priority = {
            "mercados":   0.85,
            "temas":      0.8,
            "evergreen":  0.8,
            "casos-uso":  0.75,
            "sectores":   0.75,
            "ciudades":   0.7,
            "about":      0.6,
        }.get(section, 0.6)
        changefreq = "weekly" if section == "mercados" else "monthly"
        return (url, priority, changefreq)

    return (f"{SITE}/{rel.as_posix()}", 0.5, "monthly")


def _collect() -> list[tuple[str, dt.date, float, str]]:
    """Devuelve lista de (loc, lastmod, priority, changefreq)."""
    out = []

    # Top-level files
    for name in ("index.html", "archive.html"):
        p = ROOT / name
        if p.exists():
            loc, prio, freq = _meta_for(p)
            out.append((loc, dt.date.fromtimestamp(p.stat().st_mtime), prio, freq))

    # about/
    about = ROOT / "about" / "index.html"
    if about.exists():
        loc, prio, freq = _meta_for(about)
        out.append((loc, dt.date.fromtimestamp(about.stat().st_mtime), prio, freq))

    # magazines/*.html
    for p in sorted((ROOT / "magazines").glob("*.html")):
        loc, prio, freq = _meta_for(p)
        out.append((loc, dt.date.fromtimestamp(p.stat().st_mtime), prio, freq))

    # Subdir sections
    for section in ("temas", "mercados", "casos-uso", "sectores", "ciudades"):
        d = ROOT / section
        if not d.exists():
            continue
        for p in sorted(d.rglob("index.html")):
            if "draft" in str(p):
                continue
            if _is_noindex(p):
                continue
            loc, prio, freq = _meta_for(p)
            out.append((loc, dt.date.fromtimestamp(p.stat().st_mtime), prio, freq))

    # evergreen
    d = ROOT / "evergreen"
    if d.exists():
        for p in sorted(d.rglob("index.html")):
            if _is_noindex(p):
                continue
            loc, prio, freq = _meta_for(p)
            out.append((loc, dt.date.fromtimestamp(p.stat().st_mtime), prio, freq))

    return out


def _serialize(entries) -> str:
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    # Sort: highest priority first, then by lastmod desc
    entries.sort(key=lambda e: (-e[2], -e[1].toordinal()))
    for loc, lastmod, priority, changefreq in entries:
        lines.append("  <url>")
        lines.append(f"    <loc>{loc}</loc>")
        lines.append(f"    <lastmod>{lastmod.isoformat()}</lastmod>")
        lines.append(f"    <changefreq>{changefreq}</changefreq>")
        lines.append(f"    <priority>{priority:.2f}</priority>")
        lines.append("  </url>")
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def main():
    mode = "[DRY-RUN]" if DRY_RUN else "[LIVE]"
    print(f"\nrebuild_sitemap.py {mode}\n")

    entries = _collect()
    xml = _serialize(entries)

    sitemap = ROOT / "sitemap.xml"
    if DRY_RUN:
        # Conteo comparativo
        old = sitemap.read_text(encoding="utf-8") if sitemap.exists() else ""
        old_count = old.count("<url>")
        print(f"  Antes: {old_count} URLs en sitemap.xml")
        print(f"  Después: {len(entries)} URLs")
        # Mostrar distribución por sección
        from collections import Counter
        sections = Counter()
        for loc, *_ in entries:
            parts = loc.replace(SITE, "").strip("/").split("/")
            sections[parts[0] if parts and parts[0] else "home"] += 1
        print("\n  Por sección:")
        for s, n in sorted(sections.items(), key=lambda x: -x[1]):
            print(f"    {s:20} {n}")
    else:
        sitemap.write_text(xml, encoding="utf-8")
        print(f"  ✅ sitemap.xml regenerado con {len(entries)} URLs")


if __name__ == "__main__":
    main()
