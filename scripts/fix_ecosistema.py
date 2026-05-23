#!/usr/bin/env python3
"""
fix_ecosistema.py — Bulk-replace "ecosistema" (and variants) in tier-1 pillar pages.

Targets: temas/ and mercados/ directories only.
Handles .html files recursively.

Usage:
    python3 scripts/fix_ecosistema.py --dry-run     # preview only
    python3 scripts/fix_ecosistema.py               # apply changes
"""

import argparse
import os
import re
import sys
from pathlib import Path
from collections import defaultdict

# ---------------------------------------------------------------------------
# Replacement rules — ordered from most specific to least specific.
# Each rule is (pattern, replacement, label).
# Patterns use re.IGNORECASE so we handle both Ecosistema and ecosistema.
# ---------------------------------------------------------------------------

RULES = [
    # --- Specific "ecosistema de X" phrases ---

    # ecosistema de proveedores / players / emisores / operadores
    # Require "de" to avoid matching "ecosistema diverso con players"
    (
        r"[Ee]cosistema\s+de\s+(?:[a-záéíóúüñ\s]+?)?(?:proveedores|players|emisores|operadores)\b",
        "mercado de proveedores",
        "proveedores/players",
    ),

    # ecosistema de herramientas / soluciones / productos / software / plataformas
    # Require "de" to avoid matching "ecosistema donde … plataformas"
    (
        r"[Ee]cosistema\s+de\s+(?:[a-záéíóúüñ\s]+?)?(?:herramientas|soluciones|productos|software|plataformas)\b",
        "conjunto de herramientas",
        "herramientas/soluciones",
    ),

    # ecosistema de movilidad / transporte / autotransporte / logística / hidrocarburo
    (
        r"[Ee]cosistema\s+de(?:\s+[a-záéíóúüñ]+)*\s+(?:movilidad|transporte|autotransporte|logística|logistica|hidrocarburos|hidrocarburo)\b",
        "sector del transporte",
        "movilidad/transporte",
    ),

    # ecosistema de Pulpo / editorial (branded)
    (
        r"[Ee]cosistema\s+de\s+(?:[a-záéíóúüñ\s]+?)?(?:Pulpo|editorial)\b",
        "plataforma de Pulpo",
        "Pulpo/editorial",
    ),

    # ecosistema de flotas (standalone)
    (
        r"[Ee]cosistema\s+de\s+flotas\b",
        "mercado de flotas",
        "flotas",
    ),

    # ecosistema de gestión (de flotas / mexicano / español / etc.)
    # When followed by "de flotas", just replace with "sector de gestión" to avoid duplication.
    (
        r"[Ee]cosistema\s+de\s+gestión\s+de\s+flotas",
        "sector de gestión de flotas",
        "gestión (ya lleva de flotas)",
    ),
    (
        r"[Ee]cosistema\s+de\s+gestión\b",
        "sector de gestión de flotas",
        "gestión",
    ),

    # ecosistema de electrificación
    (
        r"[Ee]cosistema\s+de\s+electrificación\b",
        "mercado de electrificación",
        "electrificación",
    ),

    # ecosistema de telemática
    (
        r"[Ee]cosistema\s+de\s+telemática\b",
        "mercado de telemática",
        "telemática",
    ),

    # ecosistema de control / gasto / compliance / mantenimiento / renting / tarjetas / cargadores
    (
        r"[Ee]cosistema\s+de\s+(?:control|gasto|compliance|mantenimiento|renting|tarjetas|cargadores)\b",
        "sector",
        "control/gasto/misc",
    ),

    # ecosistema (adjective-standalone in a heading like "ecosistema mexicano / español / ITV / DGT / V-16")
    # e.g. "ecosistema mexicano", "ecosistema español", "ecosistema ITV"
    (
        r"[Ee]cosistema\s+(?:mexicano|español|española|ITV|DGT|V-16)\b",
        "sector",
        "adjectival standalone",
    ),

    # --- Generic "ecosistema de X" catch-all (2-4 word noun after "de") ---
    (
        r"[Ee]cosistema\s+de\s+[a-záéíóúüñA-ZÁÉÍÓÚÜÑ][a-záéíóúüñA-ZÁÉÍÓÚÜÑ\s]{1,40}?(?=[\s,.<]|$)",
        "sector",
        "generic de X (catch-all)",
    ),

    # --- Bare "ecosistema" (no "de") — safe fallback ---
    (
        r"[Ee]cosistema\b",
        "sector",
        "bare standalone",
    ),
]

# Pre-compile
COMPILED_RULES = [
    (re.compile(pattern), replacement, label)
    for pattern, replacement, label in RULES
]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent
TARGET_DIRS = ["temas", "mercados"]


def find_html_files():
    files = []
    for dirname in TARGET_DIRS:
        d = REPO_ROOT / dirname
        if not d.is_dir():
            print(f"[WARN] Directory not found, skipping: {d}", file=sys.stderr)
            continue
        for f in sorted(d.rglob("*.html")):
            files.append(f)
    return files


def apply_rules(text):
    """
    Apply rules in order. Return (new_text, list_of_matches).
    Each match is a dict: {rule_label, original, replacement, position}.
    """
    matches = []
    result = text

    for pattern, replacement, label in COMPILED_RULES:
        new_result, n = pattern.subn(replacement, result)
        if n > 0:
            # Re-find all matches in the *original* result before substitution
            for m in pattern.finditer(result):
                matches.append({
                    "label": label,
                    "original": m.group(0),
                    "replacement": replacement,
                })
        result = new_result

    return result, matches


def process_file(path: Path, dry_run: bool):
    """Process a single file. Returns (changed: bool, matches: list)."""
    original = path.read_text(encoding="utf-8")
    modified, matches = apply_rules(original)

    if not matches:
        return False, []

    if not dry_run:
        path.write_text(modified, encoding="utf-8")

    return True, matches


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Fix 'ecosistema' clichés in tier-1 pillar pages.")
    parser.add_argument("--dry-run", action="store_true", help="Preview replacements without writing files.")
    args = parser.parse_args()

    mode = "DRY RUN" if args.dry_run else "LIVE"
    print(f"\n{'='*60}")
    print(f"  fix_ecosistema.py — {mode}")
    print(f"  Targets: {', '.join(TARGET_DIRS)}")
    print(f"{'='*60}\n")

    html_files = find_html_files()
    print(f"Found {len(html_files)} HTML files to scan.\n")

    total_replacements = 0
    files_modified = 0
    rule_counts = defaultdict(int)
    file_report = []

    for path in html_files:
        changed, matches = process_file(path, dry_run=args.dry_run)
        if changed:
            files_modified += 1
            total_replacements += len(matches)
            for m in matches:
                rule_counts[m["label"]] += 1
            rel = path.relative_to(REPO_ROOT)
            file_report.append((rel, matches))

    # --- Per-file report ---
    print("Files with replacements:")
    print("-" * 60)
    for rel, matches in file_report:
        print(f"\n  {rel}  ({len(matches)} replacement{'s' if len(matches) != 1 else ''})")
        for m in matches:
            orig_preview = m["original"][:70].replace("\n", " ")
            print(f"    [{m['label']}]  '{orig_preview}'  →  '{m['replacement']}'")

    # --- Summary ---
    print("\n" + "=" * 60)
    print(f"  SUMMARY ({mode})")
    print("=" * 60)
    print(f"  Files scanned   : {len(html_files)}")
    print(f"  Files modified  : {files_modified}")
    print(f"  Total replacements: {total_replacements}")
    print()
    print("  Replacements by rule:")
    for label, count in sorted(rule_counts.items(), key=lambda x: -x[1]):
        print(f"    {label:<35} {count}")

    if args.dry_run:
        print("\n  [DRY RUN — no files were modified]")
    else:
        print("\n  [Changes written to disk]")

    print()


if __name__ == "__main__":
    main()
