#!/usr/bin/env python3
"""
inject_magazine_tags.py — Convert ALL <span class="cover-tag"> and
<span class="story-tag"> in magazines into clickable <a> tags by looking
up the tag text in a comprehensive mapping.

Idempotent: tags already converted to <a> are left untouched.
Tags without a destination remain as <span> and are reported as GAPs.

Usage:
  python scripts/inject_magazine_tags.py [--dry-run] [--file <path>]
"""
from __future__ import annotations
import argparse
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).parent))
from lib.paths import ROOT, MAGAZINES_DIR


# ─── Tag text (normalized) → URL ────────────────────────────────────────
# None value means: known tag but no destination page yet → reported as GAP
TAG_MAPPING: dict[str, str | None] = {
    # ── Topics / Themes ─────────────────────────────────────────────
    # Cargo theft pillar creada 2026-05-24 — esta clave se updatea aunque ya sea <a>
    "seguridad": "/temas/cargo-theft-flotas-mexico-2026/",
    "seguridad vial": "/temas/dgt-flotas-comerciales-2026/",
    "cargo theft": "/temas/cargo-theft-flotas-mexico-2026/",
    "robo de carga": "/temas/cargo-theft-flotas-mexico-2026/",
    "robo al transporte": "/temas/cargo-theft-flotas-mexico-2026/",
    "fraude": "/temas/cargo-theft-flotas-mexico-2026/",

    "telematica": "/temas/telematica-flotas-mexico-2026/",
    "telemática": "/temas/telematica-flotas-mexico-2026/",

    "ev": "/temas/electrificacion-flotas-mexico-2026/",
    "electrificacion": "/temas/electrificacion-flotas-mexico-2026/",
    "electrificación": "/temas/electrificacion-flotas-mexico-2026/",
    "producto ev": "/temas/electrificacion-flotas-mexico-2026/",
    "carga ev": "/temas/electrificacion-flotas-mexico-2026/",
    "puntos de carga": "/temas/electrificacion-flotas-mexico-2026/",
    "paridad ev": "/temas/electrificacion-flotas-espana-2026/",
    "combustibles alternativos": "/temas/electrificacion-flotas-mexico-2026/",

    "regulacion": "/temas/regulacion-mexico/",
    "regulación": "/temas/regulacion-mexico/",
    "compliance": "/temas/compliance-flotas-mexico-2026/",
    "arbitraje fiscal": "/temas/compliance-flotas-mexico-2026/",

    "fuel cards": "/temas/tarjetas-flota-mexico-2026/",
    "combustible": "/temas/tarjetas-flota-mexico-2026/",
    "pagos": "/temas/tarjetas-flota-mexico-2026/",

    "mantenimiento": "/temas/mantenimiento-flota-mexico-2026/",
    "renting": "/temas/renting-leasing-flota-espana-2026/",
    "leasing": "/temas/renting-leasing-flota-espana-2026/",
    "renting municipal": "/temas/renting-leasing-flota-espana-2026/",

    "ultima milla": "/casos-uso/flota-reparto-ultima-milla-mexico-2026/",
    "última milla": "/casos-uso/flota-reparto-ultima-milla-mexico-2026/",
    "last mile": "/casos-uso/flota-reparto-ultima-milla-mexico-2026/",

    "zbe": "/temas/zbe-flotas-comerciales-espana-2026/",
    "v-16": "/temas/baliza-v16-flotas-2026/",
    "tacografo": "/temas/tacografo-flota-espana-2026/",
    "tacógrafo": "/temas/tacografo-flota-espana-2026/",
    "peajes eu": "/temas/peaje-europa-flota-camiones-2026/",
    "peaje eu": "/temas/peaje-europa-flota-camiones-2026/",

    "operaciones": "/temas/gestion-flota-mexico-2026/",
    "producto": "/temas/gestion-flota-mexico-2026/",
    "producto y operaciones": "/temas/gestion-flota-mexico-2026/",
    "tendencia operativa": "/temas/gestion-flota-mexico-2026/",
    "ia operativa": "/temas/gestion-flota-mexico-2026/",
    "ia": "/temas/gestion-flota-mexico-2026/",
    "conduccion autonoma": "/temas/gestion-flota-mexico-2026/",
    "conducción autónoma": "/temas/gestion-flota-mexico-2026/",

    "intermodal": "/temas/transporte-larga-distancia-mexico-2026/",
    "comercio exterior": "/temas/t-mec-autotransporte-mexico-2026/",
    "nearshoring": "/temas/t-mec-autotransporte-mexico-2026/",
    "norteamerica": "/temas/t-mec-autotransporte-mexico-2026/",
    "norteamérica": "/temas/t-mec-autotransporte-mexico-2026/",

    "señales de mercado": "/mercados/",
    "senales de mercado": "/mercados/",
    "datos de mercado": "/mercados/",
    "inteligencia de mercado": "/mercados/",
    "movimiento de mercado": "/mercados/",
    "mercado": "/mercados/",
    "m&a": "/mercados/",
    "partnership": "/mercados/",
    "sostenibilidad": "/temas/electrificacion-flotas-mexico-2026/",

    # ── Markets ─────────────────────────────────────────────────────
    "mexico": "/mercados/mexico/",
    "méxico": "/mercados/mexico/",
    "espana": "/mercados/espana/",
    "españa": "/mercados/espana/",
    "spain": "/mercados/espana/",
    "latam": "/mercados/latam/",
    "usa": "/mercados/usa/",
    "us": "/mercados/usa/",
    "estados unidos": "/mercados/usa/",
    "uk": "/mercados/uk/",
    "europa": "/mercados/europa/",
    "mexico 2030": "/mercados/mexico/",
    "méxico 2030": "/mercados/mexico/",
    "mexico · espana · usa": "/mercados/",
    "méxico · españa · usa": "/mercados/",
    "mexico · espana · usa · europa": "/mercados/",
    "méxico · españa · usa · europa": "/mercados/",
    "112m€ catalunya": "/mercados/espana/",

    # ── Sectors ─────────────────────────────────────────────────────
    "ecommerce": "/sectores/flotas-ecommerce-paqueteria-mexico-2026/",
    "logistica": "/sectores/flotas-logistica-3pl-mexico-2026/",
    "logística": "/sectores/flotas-logistica-3pl-mexico-2026/",

    # ── Players ─────────────────────────────────────────────────────
    "samsara": "/mercados/",   # no /players/samsara yet → fallback to /mercados/

    # ── GAPs (known tag, no page exists) ────────────────────────────
    "ferrocarril": "/corredores/t-mec-2026/",
    "intermodal": "/corredores/t-mec-2026/",
    "componentes": "/temas/fabricantes-camiones-mexico-2026/",
    "recambios": "/temas/fabricantes-camiones-mexico-2026/",
    "supply chain": "/temas/fabricantes-camiones-mexico-2026/",
    "componentes automotrices": "/temas/fabricantes-camiones-mexico-2026/",
    "china": None,
    "global": None,
    "licitaciones": None,
    "puertos": None,
    "aviacion cargo": None,
    "aviación cargo": None,
    "infraestructura": None,
}


def _normalize(s: str) -> str:
    """Lowercase + strip + collapse whitespace. Keep accents (mapping has both)."""
    s = s.strip().lower()
    s = re.sub(r"\s+", " ", s)
    return s


def _resolve(text: str) -> tuple[str | None, bool]:
    """
    Return (url, is_known). is_known=True if tag appears in mapping (even if value is None).
    """
    norm = _normalize(text)
    if norm in TAG_MAPPING:
        return TAG_MAPPING[norm], True
    # try accent-stripped lookup
    nfkd = unicodedata.normalize("NFKD", norm)
    no_accent = "".join(c for c in nfkd if not unicodedata.combining(c))
    if no_accent in TAG_MAPPING:
        return TAG_MAPPING[no_accent], True
    return None, False


def _process_magazine(html_path: Path, dry_run: bool, gap_counter: Counter,
                      unknown_counter: Counter, missing_pages: set[str]) -> dict[str, int]:
    content = html_path.read_text(encoding="utf-8")
    soup = BeautifulSoup(content, "html.parser")

    converted = 0
    skipped_gap = 0
    skipped_unknown = 0
    already_anchor = 0

    for cls_name in ("cover-tag", "story-tag"):
        for el in list(soup.find_all(class_=cls_name)):
            if el.name == "a":
                already_anchor += 1
                continue
            if el.name != "span":
                continue

            text = el.get_text()
            url, is_known = _resolve(text)

            if url is None:
                if is_known:
                    gap_counter[_normalize(text)] += 1
                    skipped_gap += 1
                else:
                    unknown_counter[_normalize(text)] += 1
                    skipped_unknown += 1
                continue

            # Build anchor preserving classes
            classes = " ".join(el.get("class", []))
            new_html = f'<a href="{url}" class="{classes}">{text}</a>'
            new_a = BeautifulSoup(new_html, "html.parser").find()
            if new_a:
                el.replace_with(new_a)
                converted += 1
                # Track if local page exists
                page_path = ROOT / url.strip("/")
                if not (page_path / "index.html").exists() and not page_path.with_suffix(".html").exists():
                    # /mercados/ etc. — check the directory itself
                    if not page_path.exists():
                        missing_pages.add(url)

    stats = {
        "converted": converted,
        "skipped_gap": skipped_gap,
        "skipped_unknown": skipped_unknown,
        "already_anchor": already_anchor,
    }

    label = "[DRY-RUN]" if dry_run else "✓"
    print(f"  {label} {html_path.name}: "
          f"converted={converted} · gap={skipped_gap} · unknown={skipped_unknown} · "
          f"already_anchor={already_anchor}")

    if not dry_run:
        html_path.write_text(str(soup), encoding="utf-8")

    return stats


def _count_state(targets: list[Path]) -> tuple[int, int]:
    """Return (anchors, spans) totals across all magazines for both tag classes."""
    a = s = 0
    for path in targets:
        soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
        for cls_name in ("cover-tag", "story-tag"):
            for el in soup.find_all(class_=cls_name):
                if el.name == "a":
                    a += 1
                elif el.name == "span":
                    s += 1
    return a, s


def main() -> None:
    parser = argparse.ArgumentParser(description="Inject clickable anchors into magazine cover/story tags.")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--file", type=Path, default=None)
    args = parser.parse_args()

    if args.file:
        targets = [ROOT / args.file] if not args.file.is_absolute() else [args.file]
    else:
        targets = sorted(MAGAZINES_DIR.glob("*-radar-fleet-by-pulpo.html"))

    if not targets:
        print("No magazine HTML files found.")
        sys.exit(0)

    mode = "DRY-RUN" if args.dry_run else "LIVE"
    print(f"\ninject_magazine_tags.py · {mode} · {len(targets)} file(s)\n")

    before_a, before_s = _count_state(targets)
    print(f"BEFORE: <a> tags = {before_a} · <span> tags = {before_s}\n")

    total = {"converted": 0, "skipped_gap": 0, "skipped_unknown": 0, "already_anchor": 0}
    gap_counter: Counter = Counter()
    unknown_counter: Counter = Counter()
    missing_pages: set[str] = set()

    for path in targets:
        stats = _process_magazine(path, args.dry_run, gap_counter, unknown_counter, missing_pages)
        for k in total:
            total[k] += stats[k]

    after_a, after_s = _count_state(targets)
    print(f"\nAFTER: <a> tags = {after_a} · <span> tags = {after_s}")
    print(f"Totals: converted={total['converted']} · "
          f"gap={total['skipped_gap']} · unknown={total['skipped_unknown']} · "
          f"already_anchor={total['already_anchor']}")

    if gap_counter:
        print(f"\n── GAP tags (known but no destination page) — candidates for new pages ──")
        for t, n in gap_counter.most_common():
            print(f"  {n}x  {t!r}")

    if unknown_counter:
        print(f"\n── UNKNOWN tags (not in mapping) — extend TAG_MAPPING ──")
        for t, n in unknown_counter.most_common():
            print(f"  {n}x  {t!r}")

    if missing_pages:
        print(f"\n── URLs pointing to non-existent pages on disk ──")
        for url in sorted(missing_pages):
            print(f"  {url}")


if __name__ == "__main__":
    main()
