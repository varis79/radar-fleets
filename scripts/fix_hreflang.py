#!/usr/bin/env python3
"""
fix_hreflang.py — Asegura hreflang reciprocity completo en pares MX↔ES.

Audit 2026-05-24 reveló que ~106 páginas de temas/, casos-uso/ y sectores/
declaran únicamente el "otro" mercado en hreflang, omitiendo el self-tag y
el x-default. Esto reduce el valor SEO de la señal de internacionalización.

Patrón ACTUAL incorrecto en una página MX:
  <link rel="alternate" hreflang="es-ES" href="{ES url}"/>

Patrón CORRECTO (este script lo aplica):
  <link rel="alternate" hreflang="es-MX" href="{MX url}"/>   (self)
  <link rel="alternate" hreflang="es-ES" href="{ES url}"/>   (alternate)
  <link rel="alternate" hreflang="x-default" href="{MX url}"/>  (x-default → MX)

Idempotente: no añade duplicados. Procesa todos los `index.html` bajo
temas/, casos-uso/ y sectores/. Solo modifica páginas con par MX↔ES
(es decir, las que ya tienen al menos un hreflang declarado).

Uso:
  python3 scripts/fix_hreflang.py
  python3 scripts/fix_hreflang.py --dry-run
"""
import argparse
import re
import sys
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).parent.parent
SECTIONS = ("temas", "casos-uso", "sectores")
BASE = "https://thefleetradar.com"


def page_url(rel_path: Path) -> str:
    """rel_path es algo como temas/foo/index.html → https://.../temas/foo/"""
    parts = rel_path.parent.as_posix().rstrip("/")
    return f"{BASE}/{parts}/"


def detect_market(path: Path) -> str | None:
    """Detect 'mx' / 'es' por slug. Devuelve None si no detectable."""
    name = path.parent.name
    if "mexico" in name:
        return "mx"
    if "espana" in name:
        return "es"
    return None


def pair_path(path: Path, my_market: str) -> Path | None:
    """Devuelve la ruta del par MX↔ES si existe en disco."""
    other = "espana" if my_market == "mx" else "mexico"
    new_name = path.parent.name.replace(
        "mexico" if my_market == "mx" else "espana", other
    )
    candidate = path.parent.parent / new_name / "index.html"
    return candidate if candidate.exists() else None


def fix_file(path: Path, dry_run: bool = False) -> dict:
    """Devuelve dict con cambios aplicados."""
    market = detect_market(path)
    if market is None:
        return {"skipped": "no_market"}
    pair = pair_path(path, market)
    if pair is None:
        return {"skipped": "no_pair"}

    text = path.read_text(encoding="utf-8")
    soup = BeautifulSoup(text, "html.parser")
    head = soup.find("head")
    if head is None:
        return {"skipped": "no_head"}

    # URLs canónicas
    rel = path.relative_to(ROOT)
    pair_rel = pair.relative_to(ROOT)
    self_url = page_url(rel)
    pair_url = page_url(pair_rel)
    mx_url = self_url if market == "mx" else pair_url

    # Inventariamos los hreflangs existentes
    existing = {}
    for link in head.find_all("link", attrs={"rel": "alternate"}):
        hl = link.get("hreflang")
        if hl:
            existing[hl] = link

    self_tag = "es-MX" if market == "mx" else "es-ES"
    other_tag = "es-ES" if market == "mx" else "es-MX"

    added = []
    # 1) self
    if self_tag not in existing:
        tag = soup.new_tag(
            "link", rel="alternate", hreflang=self_tag, href=self_url
        )
        head.append(tag)
        added.append(self_tag)
    # 2) other (si por algún caso no estaba)
    if other_tag not in existing:
        tag = soup.new_tag(
            "link", rel="alternate", hreflang=other_tag, href=pair_url
        )
        head.append(tag)
        added.append(other_tag)
    # 3) x-default → MX
    if "x-default" not in existing:
        tag = soup.new_tag(
            "link", rel="alternate", hreflang="x-default", href=mx_url
        )
        head.append(tag)
        added.append("x-default")

    if not added:
        return {"ok": True, "added": []}

    if not dry_run:
        path.write_text(str(soup), encoding="utf-8")

    return {"ok": True, "added": added}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    files: list[Path] = []
    for section in SECTIONS:
        d = ROOT / section
        if d.exists():
            files.extend(sorted(d.rglob("index.html")))

    print(f"fix_hreflang.py — analizando {len(files)} páginas\n")
    counts = {"updated": 0, "ok_already": 0, "skipped": 0, "tags_added": 0}
    by_tag: dict[str, int] = {}

    for f in files:
        rel = f.relative_to(ROOT)
        result = fix_file(f, dry_run=args.dry_run)
        if "skipped" in result:
            counts["skipped"] += 1
            continue
        if result.get("added"):
            counts["updated"] += 1
            counts["tags_added"] += len(result["added"])
            for tag in result["added"]:
                by_tag[tag] = by_tag.get(tag, 0) + 1
            print(f"  ✚ {rel}  → {','.join(result['added'])}")
        else:
            counts["ok_already"] += 1

    mode = "DRY-RUN" if args.dry_run else "APPLIED"
    print(f"\n[{mode}] páginas actualizadas: {counts['updated']}")
    print(f"          ya completas:        {counts['ok_already']}")
    print(f"          skipped (no par MX↔ES): {counts['skipped']}")
    print(f"          tags añadidos:       {counts['tags_added']}")
    if by_tag:
        print("          desglose por tag:")
        for tag, n in sorted(by_tag.items()):
            print(f"            {tag}: {n}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
