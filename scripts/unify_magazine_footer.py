#!/usr/bin/env python3
"""
unify_magazine_footer.py — Elimina <section class="closing"> redundante
de TODAS las páginas HTML del sitio. Esa sección era el "footer legacy"
con info duplicada que ahora cubre el <footer class="site-footer"> global.

Idempotente.

Uso:
    python3 scripts/unify_magazine_footer.py [--dry-run]
"""
import sys
from pathlib import Path
from bs4 import BeautifulSoup

DRY_RUN = "--dry-run" in sys.argv
ROOT = Path(__file__).parent.parent

# Excluir páginas que conviene mantener el closing (ej: styleguide para mostrar todos los componentes)
SKIP_FILES = {"styleguide.html"}


def process(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    soup = BeautifulSoup(text, "html.parser")
    changed = False
    # Puede haber más de un closing (defensivo)
    for closing in soup.find_all("section", class_="closing"):
        closing.decompose()
        changed = True
    if changed and not DRY_RUN:
        path.write_text(str(soup), encoding="utf-8")
    return changed


def main():
    mode = "[DRY-RUN]" if DRY_RUN else "[LIVE]"
    print(f"\nunify_magazine_footer.py {mode}\n")

    # Recorrer TODAS las páginas HTML del sitio
    files = []
    for sub in ("temas", "mercados", "casos-uso", "sectores", "ciudades",
                "evergreen", "corredores", "players", "about", "legal"):
        d = ROOT / sub
        if d.exists():
            files.extend(d.rglob("index.html"))
    files.extend((ROOT / "magazines").glob("*.html"))
    files.extend([ROOT / "index.html", ROOT / "archive.html",
                  ROOT / "404.html"])

    n = 0
    for p in sorted(set(files)):
        if not p.exists() or p.name in SKIP_FILES:
            continue
        if process(p):
            n += 1
            rel = p.relative_to(ROOT)
            marker = "[DRY]" if DRY_RUN else "  ✅"
            print(f"  {marker} {rel}: closing eliminado")
    print(f"\n  Total páginas limpiadas: {n}")


if __name__ == "__main__":
    main()
