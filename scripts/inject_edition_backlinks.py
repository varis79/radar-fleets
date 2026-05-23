#!/usr/bin/env python3
"""
inject_edition_backlinks.py

Injects backlinks from pillar pages to the magazine editions that covered that topic.
Adds a <div class="related-group related-editions"> block inside the existing
.related-grid section of each pillar page.

Usage:
    python3 scripts/inject_edition_backlinks.py [--dry-run]

Idempotent: skips pages that already have related-editions injected.
"""

import argparse
import csv
import os
import re
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ── Edition catalogue ──────────────────────────────────────────────────────────
# (edition_number, date_slug, display_label, url_path)
# Actual edition numbers extracted from the HTML files.
EDITIONS = [
    (1,  "2026-04-14", "Nº1 · 14 abril 2026",  "/magazines/2026-04-14-radar-fleet-by-pulpo.html"),
    (2,  "2026-04-17", "Nº2 · 17 abril 2026",  "/magazines/2026-04-17-radar-fleet-by-pulpo.html"),
    (4,  "2026-04-20", "Nº4 · 20 abril 2026",  "/magazines/2026-04-20-radar-fleet-by-pulpo.html"),
    (5,  "2026-04-27", "Nº5 · 27 abril 2026",  "/magazines/2026-04-27-radar-fleet-by-pulpo.html"),
    (6,  "2026-05-04", "Nº6 · 4 mayo 2026",    "/magazines/2026-05-04-radar-fleet-by-pulpo.html"),
    (7,  "2026-05-11", "Nº7 · 11 mayo 2026",   "/magazines/2026-05-11-radar-fleet-by-pulpo.html"),
    (8,  "2026-05-18", "Nº8 · 18 mayo 2026",   "/magazines/2026-05-18-radar-fleet-by-pulpo.html"),
]

# Build a lookup: date_slug → edition tuple
_EDITION_BY_SLUG = {e[1]: e for e in EDITIONS}

# ── Topic → edition mapping ────────────────────────────────────────────────────
# Values are date slugs of the magazine files that covered each topic.
# Task spec uses positional labels Nº1–Nº7 → files in date order.
# Actual date slugs in order: 04-14, 04-17, 04-20, 04-27, 05-04, 05-11, 05-18
_POS_TO_SLUG = [
    "2026-04-14",  # positional Nº1
    "2026-04-17",  # positional Nº2
    "2026-04-20",  # positional Nº3
    "2026-04-27",  # positional Nº4
    "2026-05-04",  # positional Nº5
    "2026-05-11",  # positional Nº6
    "2026-05-18",  # positional Nº7
]

def _slugs(positions):
    """Convert 1-based positional list to date slugs."""
    return [_POS_TO_SLUG[p - 1] for p in positions]

TOPIC_EDITIONS = {
    "telematica":           _slugs([1, 2, 3, 4, 5, 6, 7]),
    "electrificacion-flotas": _slugs([1, 2, 3, 4, 5, 6, 7]),
    "fuel-cards":           _slugs([4, 5, 6, 7]),
    "compliance":           _slugs([2, 3, 5, 6]),
    "mantenimiento-flota":  _slugs([3, 4, 6]),
    "operacion-flotas":     _slugs([1, 2, 4, 5, 6, 7]),
    "nearshoring":          _slugs([5, 6]),
    "itv-camiones":         _slugs([5]),
}

MAX_EDITIONS = 3  # show only the N most recent editions per topic

# ── Build url_path → topic_code from matrix.csv ───────────────────────────────

def load_url_to_topic(matrix_path):
    mapping = {}
    with open(matrix_path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            url = row.get("url_path", "").strip()
            topic = row.get("topic_code", "").strip()
            if url and topic:
                mapping[url] = topic
    return mapping


# ── HTML helpers ──────────────────────────────────────────────────────────────

def build_editions_block(edition_slugs):
    """Build the related-group HTML for a list of edition date slugs (most recent first)."""
    # Reverse to get most-recent first, then cap
    ordered = list(reversed(edition_slugs))[:MAX_EDITIONS]
    items = []
    for slug in ordered:
        ed = _EDITION_BY_SLUG.get(slug)
        if ed:
            _, _, label, url = ed
            items.append(f'<li><a href="{url}">{label}</a></li>')
    if not items:
        return ""
    li_html = "".join(items)
    return (
        '<div class="related-group related-editions">'
        '<h3 class="related-group-title">Ediciones que cubren este tema</h3>'
        f'<ul class="related-list">{li_html}</ul>'
        "</div>"
    )


def inject_into_html(html, editions_block):
    """Insert editions_block at the end of .related-grid."""
    # Find the closing tag of the related-grid div
    # The related-grid contains several related-group divs; we insert before </div></div></section>
    # Pattern: </div></div></section> where the first </div> closes related-grid
    # Use a targeted insert: find last </div> before </div></section> in the related section
    pattern = re.compile(
        r'(<section class="pillar-related">.*?<div class="related-grid">)(.*?)(</div></div></section>)',
        re.DOTALL,
    )
    match = pattern.search(html)
    if not match:
        return None  # no related section found
    prefix = match.group(1)
    inner = match.group(2)
    suffix = match.group(3)
    new_html = html[:match.start()] + prefix + inner + editions_block + suffix + html[match.end():]
    return new_html


# ── Main ──────────────────────────────────────────────────────────────────────

def find_pillar_pages(base_dir):
    """Yield (abs_path, url_path) for every index.html under target dirs."""
    target_dirs = ["temas", "casos-uso", "sectores", "ciudades"]
    for section in target_dirs:
        section_abs = os.path.join(base_dir, section)
        if not os.path.isdir(section_abs):
            continue
        for entry in sorted(os.listdir(section_abs)):
            entry_abs = os.path.join(section_abs, entry)
            index_html = os.path.join(entry_abs, "index.html")
            if os.path.isfile(index_html):
                url_path = f"/{section}/{entry}/"
                yield index_html, url_path


def main():
    parser = argparse.ArgumentParser(description="Inject edition backlinks into pillar pages.")
    parser.add_argument("--dry-run", action="store_true", help="Show what would change without writing files.")
    args = parser.parse_args()

    matrix_path = os.path.join(BASE_DIR, "content", "pillar-matrix", "matrix.csv")
    url_to_topic = load_url_to_topic(matrix_path)

    injected = 0
    skipped_no_topic = 0
    skipped_no_editions = 0
    skipped_already_done = 0
    skipped_no_related_section = 0
    errors = []

    for abs_path, url_path in find_pillar_pages(BASE_DIR):
        topic_code = url_to_topic.get(url_path)
        if not topic_code:
            skipped_no_topic += 1
            continue

        edition_slugs = TOPIC_EDITIONS.get(topic_code)
        if not edition_slugs:
            skipped_no_editions += 1
            continue

        with open(abs_path, "r", encoding="utf-8") as fh:
            html = fh.read()

        # Idempotency check
        if 'related-editions' in html:
            skipped_already_done += 1
            continue

        editions_block = build_editions_block(edition_slugs)
        if not editions_block:
            skipped_no_editions += 1
            continue

        new_html = inject_into_html(html, editions_block)
        if new_html is None:
            skipped_no_related_section += 1
            errors.append(f"No related-grid found: {url_path}")
            continue

        if args.dry_run:
            print(f"[DRY-RUN] Would inject editions for topic={topic_code!r}: {url_path}")
        else:
            with open(abs_path, "w", encoding="utf-8") as fh:
                fh.write(new_html)
            print(f"Injected editions for topic={topic_code!r}: {url_path}")

        injected += 1

    print()
    print("=" * 60)
    print(f"  Pages injected           : {injected}")
    print(f"  Skipped (already done)   : {skipped_already_done}")
    print(f"  Skipped (no topic match) : {skipped_no_topic}")
    print(f"  Skipped (topic not in map): {skipped_no_editions}")
    print(f"  Skipped (no related sect): {skipped_no_related_section}")
    if errors:
        print()
        print("Errors:")
        for e in errors:
            print(f"  {e}")
    if args.dry_run:
        print()
        print("  *** DRY RUN — no files were modified ***")
    print("=" * 60)


if __name__ == "__main__":
    main()
