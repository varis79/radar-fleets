#!/usr/bin/env python3
"""
unify_navigation.py — Unifica el <header class="topbar"> y añade un <footer>
canónico global a todas las páginas HTML del sitio.

Header canónico:
  Última · Archivo · Mercados · Temas · Casos de uso · Sectores · Recursos · Pulpo ↗

Footer canónico:
  - Brand block (logo + tagline)
  - Secciones (Mercados, Temas, Casos uso, Sectores, Ciudades, Recursos)
  - Legal (Privacidad, Términos)
  - Contacto (hola@getpulpo.com)
  - Pulpo ↗

Estrategia:
  - Reemplaza `<header class="topbar">…</header>` con la versión canónica
    SOLO si el contenido difiere (idempotente)
  - Si la página tiene <header class="topbar"> pero faltan links, los inyecta
  - Si la página NO tiene <footer>, añade el canónico antes de </body>
  - Preserva `topbar-meta` y el contexto-específico de cada página
  - Excluye: 404.html, styleguide.html (mantienen su propio chrome)

Uso:
    python3 scripts/unify_navigation.py [--dry-run]
"""
import sys
import re
from pathlib import Path
from bs4 import BeautifulSoup, Tag, NavigableString

DRY_RUN = "--dry-run" in sys.argv
ROOT = Path(__file__).parent.parent

# Páginas que no se tocan
SKIP_NAMES = {"404.html", "styleguide.html"}

# Plantilla del nav canónico (los enlaces)
CANONICAL_NAV_LINKS = [
    ('/',                   "Última",         None),
    ('/archive.html',       "Archivo",        None),
    ('/mercados/',          "Mercados",       None),
    ('/temas/',             "Temas",          None),
    ('/casos-uso/',         "Casos de uso",   None),
    ('/sectores/',          "Sectores",       None),
    ('/evergreen/',         "Recursos",       None),
    ('https://www.getpulpo.com/', "Pulpo ↗",  "cta"),
]

FOOTER_HTML = """
<footer class="site-footer">
  <div class="footer-grid">
    <div class="footer-brand">
      <a class="footer-brand-link" href="/">The Fleet Radar <span>by Pulpo</span></a>
      <p class="footer-tagline">Inteligencia semanal de mercado para el sector de gestión de flotas en México, España y LatAm.</p>
    </div>
    <div class="footer-col">
      <h4>Secciones</h4>
      <ul>
        <li><a href="/mercados/">Mercados</a></li>
        <li><a href="/temas/">Temas</a></li>
        <li><a href="/casos-uso/">Casos de uso</a></li>
        <li><a href="/sectores/">Sectores</a></li>
        <li><a href="/ciudades/">Ciudades</a></li>
        <li><a href="/evergreen/">Recursos</a></li>
      </ul>
    </div>
    <div class="footer-col">
      <h4>Ediciones</h4>
      <ul>
        <li><a href="/">Última edición</a></li>
        <li><a href="/archive.html">Archivo</a></li>
        <li><a href="/rss.xml">RSS</a></li>
      </ul>
    </div>
    <div class="footer-col">
      <h4>Legal</h4>
      <ul>
        <li><a href="/legal/privacidad/">Privacidad</a></li>
        <li><a href="/legal/terminos/">Términos</a></li>
        <li><a href="mailto:hola@getpulpo.com">Contacto</a></li>
      </ul>
    </div>
    <div class="footer-col">
      <h4>Pulpo</h4>
      <ul>
        <li><a href="https://www.getpulpo.com/" rel="noopener" target="_blank">getpulpo.com ↗</a></li>
        <li><a href="https://www.linkedin.com/company/getpulpo" rel="noopener" target="_blank">LinkedIn ↗</a></li>
      </ul>
    </div>
  </div>
  <div class="footer-bottom">
    <span>© 2026 Pulpo · The Fleet Radar</span>
    <span class="footer-meta">Publicación editorial independiente. Análisis no constituye asesoría.</span>
  </div>
</footer>
"""


def _build_canonical_nav(meta_text: str | None) -> Tag:
    """Construye el <header class='topbar'> canónico. Preserva topbar-meta si se da."""
    soup = BeautifulSoup("", "html.parser")
    header = soup.new_tag("header", **{"class": "topbar"})

    brand = soup.new_tag("a", **{"class": "topbar-brand", "href": "/"})
    brand.append(NavigableString("The Fleet Radar "))
    span = soup.new_tag("span")
    span.string = "by Pulpo"
    brand.append(span)
    header.append(brand)

    if meta_text:
        meta = soup.new_tag("div", **{"class": "topbar-meta"})
        meta.string = meta_text
        header.append(meta)

    nav = soup.new_tag("nav", **{"class": "topbar-nav"})
    for href, label, css in CANONICAL_NAV_LINKS:
        attrs = {"href": href}
        if css:
            attrs["class"] = css
        if href.startswith("http"):
            attrs["target"] = "_blank"
            attrs["rel"] = "noopener"
        a = soup.new_tag("a", **attrs)
        a.string = label
        nav.append(a)
    header.append(nav)
    return header


def _existing_meta_text(header: Tag) -> str | None:
    m = header.find("div", class_="topbar-meta") if header else None
    return m.get_text(strip=True) if m else None


def _nav_is_canonical(header: Tag) -> bool:
    """True si el nav del header ya tiene exactamente los links canónicos."""
    if not header:
        return False
    nav = header.find("nav", class_="topbar-nav")
    if not nav:
        return False
    existing = [(a.get("href",""), a.get_text(strip=True))
                for a in nav.find_all("a")]
    canonical = [(h, l) for h, l, _ in CANONICAL_NAV_LINKS]
    return existing == canonical


def process_file(path: Path) -> dict:
    """Devuelve {'header': bool, 'footer': bool} indicando cambios."""
    text = path.read_text(encoding="utf-8")
    soup = BeautifulSoup(text, "html.parser")

    changed = {"header": False, "footer": False}

    # ── HEADER ──
    body = soup.find("body")
    if body is None:
        return changed

    existing_header = soup.find("header", class_="topbar")
    if existing_header and _nav_is_canonical(existing_header):
        pass  # idempotente
    else:
        meta_text = _existing_meta_text(existing_header)
        new_header = _build_canonical_nav(meta_text)
        if existing_header:
            existing_header.replace_with(new_header)
        else:
            body.insert(0, new_header)
        changed["header"] = True

    # ── FOOTER ──
    if not soup.find("footer", class_="site-footer"):
        footer_soup = BeautifulSoup(FOOTER_HTML, "html.parser")
        # Si hay un footer viejo (sin nuestra class), lo dejamos y añadimos el nuestro
        # antes de </body>. Si quieres reemplazarlo, descomenta:
        # for old in soup.find_all("footer"):
        #     old.decompose()
        body.append(footer_soup)
        changed["footer"] = True

    if (changed["header"] or changed["footer"]) and not DRY_RUN:
        path.write_text(str(soup), encoding="utf-8")

    return changed


def main():
    mode = "[DRY-RUN]" if DRY_RUN else "[LIVE]"
    print(f"\nunify_navigation.py {mode}\n")

    files = []
    for sub in ("temas", "mercados", "casos-uso", "sectores", "ciudades",
                "evergreen", "about", "legal"):
        d = ROOT / sub
        if d.exists():
            files.extend(d.rglob("index.html"))
    files.extend((ROOT / "magazines").glob("*.html"))
    files.append(ROOT / "index.html")
    files.append(ROOT / "archive.html")

    stats = {"header_changed": 0, "footer_added": 0, "no_change": 0}
    for path in sorted(set(files)):
        if path.name in SKIP_NAMES:
            continue
        if not path.exists():
            continue
        r = process_file(path)
        if r["header"]:
            stats["header_changed"] += 1
        if r["footer"]:
            stats["footer_added"] += 1
        if not (r["header"] or r["footer"]):
            stats["no_change"] += 1

    print(f"  headers actualizados: {stats['header_changed']}")
    print(f"  footers añadidos:     {stats['footer_added']}")
    print(f"  sin cambios:          {stats['no_change']}")


if __name__ == "__main__":
    main()
