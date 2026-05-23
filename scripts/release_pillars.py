#!/usr/bin/env python3
"""
release_pillars.py — Libera (de noindex a index) las páginas pilar que han
superado el threshold de contenido.

Las pillars se generan con `<meta name="robots" content="noindex, follow">`
como stubs. Cuando alcanzan suficiente cuerpo editorial, deben liberarse
para que Google las indexe.

Estrategia:
  - Recorre temas/*/index.html
  - Si word_count(body) >= MIN_WORDS, reemplaza noindex,follow → index,follow,…
  - Idempotente: si ya está liberada (index,follow), no toca
  - Bajo umbral: muestra warning y no libera

Uso:
    python3 scripts/release_pillars.py [--dry-run] [--min-words 600]
"""
import re
import sys
from pathlib import Path
from bs4 import BeautifulSoup

DRY_RUN = "--dry-run" in sys.argv

MIN_WORDS = 600
for i, arg in enumerate(sys.argv):
    if arg == "--min-words" and i + 1 < len(sys.argv):
        MIN_WORDS = int(sys.argv[i + 1])

ROOT = Path(__file__).parent.parent

NOINDEX_RX = re.compile(
    r'<meta\s+(?:name="robots"\s+content="noindex,\s*follow"|'
    r'content="noindex,\s*follow"\s+name="robots")\s*/?>',
    re.IGNORECASE,
)
INDEX_TAG = (
    '<meta name="robots" '
    'content="index, follow, max-snippet:-1, max-image-preview:large">'
)


def _body_word_count(html: str) -> int:
    """Cuenta palabras en el cuerpo editorial principal (excluyendo nav/header/footer)."""
    soup = BeautifulSoup(html, "html.parser")
    # Quitar bloques no editoriales para el conteo
    for sel in ("header", "footer", "nav", "script", "style"):
        for el in soup.find_all(sel):
            el.decompose()
    text = soup.get_text(separator=" ", strip=True)
    return len(text.split())


def _release(path: Path) -> tuple[str, int]:
    """Devuelve (status, word_count). status ∈ {released, already, below, no-noindex}."""
    text = path.read_text(encoding="utf-8")
    wc = _body_word_count(text)

    # Ya liberada (idempotencia)
    if "noindex" not in text:
        return ("already", wc)

    if not NOINDEX_RX.search(text):
        return ("no-noindex", wc)

    if wc < MIN_WORDS:
        return ("below", wc)

    new_text = NOINDEX_RX.sub(INDEX_TAG, text, count=1)
    if not DRY_RUN:
        path.write_text(new_text, encoding="utf-8")
    return ("released", wc)


def main():
    mode = "[DRY-RUN]" if DRY_RUN else "[LIVE]"
    print(f"\nrelease_pillars.py {mode}  (min_words={MIN_WORDS})\n")

    targets = []
    for section in ("temas", "casos-uso", "sectores", "ciudades"):
        targets.extend(sorted((ROOT / section).glob("*/index.html")))
    stats = {"released": 0, "already": 0, "below": 0, "no-noindex": 0}

    for path in targets:
        status, wc = _release(path)
        stats[status] += 1
        rel = path.relative_to(ROOT)
        if status == "released":
            marker = "  ✅ " if not DRY_RUN else "  [DRY]"
            print(f"{marker} {rel}  ({wc} palabras)")
        elif status == "below":
            print(f"  ⚠️  {rel}  ({wc} palabras — bajo umbral, sigue noindex)")

    print()
    print(f"Resumen: {stats['released']} liberadas, "
          f"{stats['already']} ya indexadas, "
          f"{stats['below']} debajo del umbral, "
          f"{stats['no-noindex']} sin meta robots.")


if __name__ == "__main__":
    main()
