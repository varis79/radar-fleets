#!/usr/bin/env python3
"""
unify_magazine_footer.py — Elimina <section class="closing"> redundante
de los magazines. Esa sección era el "footer del magazine" legacy con
info duplicada que ahora cubre el <footer class="site-footer"> global.

Se preserva la metadata útil ("Próxima edición: ..." y la frase de
contexto editorial) movida a un párrafo discreto antes del footer global
si así se desea — por ahora simplemente eliminamos el bloque y dejamos
que el footer global haga su trabajo.

Idempotente.

Uso:
    python3 scripts/unify_magazine_footer.py [--dry-run]
"""
import sys
from pathlib import Path
from bs4 import BeautifulSoup

DRY_RUN = "--dry-run" in sys.argv
ROOT = Path(__file__).parent.parent


def process(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    soup = BeautifulSoup(text, "html.parser")
    closing = soup.find("section", class_="closing")
    if closing is None:
        return False
    closing.decompose()
    if not DRY_RUN:
        path.write_text(str(soup), encoding="utf-8")
    return True


def main():
    mode = "[DRY-RUN]" if DRY_RUN else "[LIVE]"
    print(f"\nunify_magazine_footer.py {mode}\n")
    files = sorted((ROOT / "magazines").glob("*.html"))
    n = 0
    for p in files:
        if process(p):
            n += 1
            marker = "[DRY]" if DRY_RUN else "  ✅"
            print(f"  {marker} {p.relative_to(ROOT)}: closing eliminado")
    print(f"\n  Total magazines limpiados: {n} / {len(files)}")


if __name__ == "__main__":
    main()
