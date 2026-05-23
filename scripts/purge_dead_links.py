#!/usr/bin/env python3
"""
purge_dead_links.py — Elimina <a> internos que apuntan a páginas que no existen
en disco. Limpia los <li> vacíos resultantes y los <ul> que queden sin items.
También elimina <div class="related-group"> que queden sin lista.

Idempotente: si no hay links rotos, no hace nada.

Uso:
    python3 scripts/purge_dead_links.py [--dry-run]
"""
import sys
from pathlib import Path
from bs4 import BeautifulSoup

DRY_RUN = "--dry-run" in sys.argv
ROOT = Path(__file__).parent.parent


def _target_exists(href: str) -> bool:
    """True si el href interno resuelve a un archivo existente."""
    if not href.startswith("/"):
        return True  # external or relative, leave alone
    href = href.split("#", 1)[0].split("?", 1)[0]
    if href.endswith("/"):
        target = ROOT / href.lstrip("/") / "index.html"
    elif href.endswith(".html"):
        target = ROOT / href.lstrip("/")
    else:
        return True  # assets/json/etc — assume ok
    return target.exists()


def purge_soup(soup: BeautifulSoup) -> int:
    """Elimina <a> internos rotos. Devuelve nº de links eliminados."""
    removed = 0

    for a in list(soup.find_all("a", href=True)):
        if _target_exists(a["href"]):
            continue
        # Si el <a> está dentro de un <li>, removemos el <li> entero
        parent_li = a.find_parent("li")
        if parent_li is not None:
            parent_li.decompose()
        else:
            # Sustituimos por su texto plano para no romper el flujo
            a.replace_with(a.get_text())
        removed += 1

    # Limpieza: <ul>/<ol> vacíos
    for ul in list(soup.find_all(["ul", "ol"])):
        if not ul.find("li"):
            ul.decompose()

    # Limpieza: related-group sin <ul>
    for grp in list(soup.find_all("div", class_="related-group")):
        if not grp.find(["ul", "ol"]):
            grp.decompose()

    # Limpieza: related-grid sin grupos
    for grid in list(soup.find_all("div", class_="related-grid")):
        if not grid.find("div", class_="related-group"):
            grid.decompose()

    # Limpieza: pillar-related entera si quedó sin contenido útil
    for sec in list(soup.find_all("section", class_="pillar-related")):
        if not sec.find("div", class_="related-grid"):
            sec.decompose()

    return removed


def main():
    mode = "[DRY-RUN]" if DRY_RUN else "[LIVE]"
    print(f"\npurge_dead_links.py {mode}\n")

    # Escanea todos los HTML del sitio
    files = []
    for sub in ("temas", "mercados", "casos-uso", "sectores", "ciudades", "evergreen", "magazines"):
        d = ROOT / sub
        if not d.exists():
            continue
        if sub == "magazines":
            files.extend(d.glob("*.html"))
        else:
            files.extend(d.rglob("index.html"))
    files.extend([ROOT / "index.html", ROOT / "archive.html"])

    total_removed = 0
    total_files = 0
    for path in sorted(files):
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        soup = BeautifulSoup(text, "html.parser")
        n = purge_soup(soup)
        if n > 0:
            total_removed += n
            total_files += 1
            rel = path.relative_to(ROOT)
            marker = "[DRY]" if DRY_RUN else "  ✅"
            print(f"  {marker} {rel}: -{n} links rotos")
            if not DRY_RUN:
                path.write_text(str(soup), encoding="utf-8")

    print()
    print(f"Total: {total_removed} links rotos eliminados en {total_files} archivos")


if __name__ == "__main__":
    main()
