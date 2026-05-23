#!/usr/bin/env python3
"""
linkify_brands.py — Adds internal links to brand/player mentions in magazine story bodies.

Strategy:
  - Only linkifies the FIRST mention of each brand in each story body
  - Links to internal pillar pages (never external brand sites)
  - Only processes brands with a high-confidence topic-to-pillar mapping
  - Skips stories where the brand's pillar page is already in the story-related div
    (it's already linked there, no need to add in-body link too)
  - Idempotent: won't double-link

Usage:
    python3 scripts/linkify_brands.py [--dry-run] [--file magazines/YYYY-MM-DD-*.html]
"""

import sys
import re
import glob
from pathlib import Path

DRY_RUN = "--dry-run" in sys.argv

ROOT = Path(__file__).parent.parent

# Brand → internal pillar URL mapping (only brands with clear pillar page relevance)
# Using "informational" intent pages: market-agnostic when possible, MX-default otherwise
BRAND_TO_URL: dict[str, tuple[str, str]] = {
    "Samsara":  ("telemática",           "/temas/telematica-flotas-mexico-2026/"),
    "Geotab":   ("telemática",           "/temas/telematica-flotas-mexico-2026/"),
    "Motive":   ("telemática",           "/temas/telematica-flotas-mexico-2026/"),
    "Webfleet": ("telemática",           "/temas/telematica-flotas-espana-2026/"),
    "Fleetio":  ("gestión de flotas",    "/temas/gestion-flota-mexico-2026/"),
    "Lytx":     ("telemática",           "/temas/telematica-flotas-mexico-2026/"),
    "WEX":      ("tarjetas de combustible", "/temas/tarjetas-flota-mexico-2026/"),
}

# ES-market overrides: if story flag is 🇪🇸, use ES pillar instead
BRAND_ES_OVERRIDE: dict[str, tuple[str, str]] = {
    "Samsara":  ("telemática",    "/temas/telematica-flotas-espana-2026/"),
    "Geotab":   ("telemática",    "/temas/telematica-flotas-espana-2026/"),
    "Motive":   ("telemática",    "/temas/telematica-flotas-espana-2026/"),
    "Fleetio":  ("gestión",       "/temas/gestion-flota-espana-2026/"),
    "Lytx":     ("telemática",    "/temas/telematica-flotas-espana-2026/"),
}

FLAG_TO_MARKET = {
    "🇲🇽": "mexico", "🇪🇸": "espana", "🇺🇸": "usa",
    "🌎": "latam", "🌐": "global", "🌍": "global", "🇪🇺": "europa",
}

def get_market_from_story_html(story_html: str) -> str:
    """Detect market from flag emoji in story-meta."""
    for flag, market in FLAG_TO_MARKET.items():
        if flag in story_html:
            return market
    return "global"


def linkify_story(story_html: str) -> tuple[str, int]:
    """Add first-occurrence brand links to a story HTML block.
    Returns (modified_html, count_of_links_added)."""
    market = get_market_from_story_html(story_html)

    # Find the story-summary paragraph (main body text of story)
    body_match = re.search(
        r'(<p class="story-summary">)(.*?)(</p>)',
        story_html,
        re.DOTALL
    )
    if not body_match:
        return story_html, 0

    body_html = body_match.group(2)
    links_added = 0

    for brand, (label, url) in BRAND_TO_URL.items():
        # ES override if market is espana
        if market == "espana" and brand in BRAND_ES_OVERRIDE:
            label, url = BRAND_ES_OVERRIDE[brand]

        # Skip if: brand not in body, brand already linked, or pillar URL already in story-related
        if brand not in body_html:
            continue
        if f'href="' in body_html and brand in body_html:
            # Check if brand is already inside an anchor tag
            link_pattern = rf'<a[^>]*>[^<]*{re.escape(brand)}[^<]*</a>'
            if re.search(link_pattern, body_html):
                continue
        if url in story_html:
            # Already linked somewhere in this story (likely story-related div)
            continue

        # Build the replacement: link only the first occurrence, word-boundary aware
        pattern = rf'\b({re.escape(brand)})\b'
        replacement = rf'<a href="{url}" class="brand-link">\1</a>'
        new_body_html, count = re.subn(pattern, replacement, body_html, count=1)

        if count > 0:
            body_html = new_body_html
            links_added += count

    if links_added == 0:
        return story_html, 0

    # Reconstruct: replace the body content portion between the p tags
    new_story = (
        story_html[:body_match.start(2)]
        + body_html
        + story_html[body_match.end(2):]
    )
    return new_story, links_added


def find_stories(html: str):
    """Find all story article/div elements (support both tag types)."""
    # Try article first
    pattern = re.compile(r'(<article class="story"[^>]*>)(.*?)(</article>)', re.DOTALL)
    matches = list(pattern.finditer(html))
    if matches:
        return matches, "article"
    # Fallback: div (edition 1 used divs)
    pattern = re.compile(r'(<div class="story"[^>]*>)(.*?)(</div>(?:\s*<div class="story"|\s*</(?:main|section)))', re.DOTALL)
    return list(pattern.finditer(html)), "div"


def process_magazine(html_path: Path) -> dict:
    """Process one magazine file. Returns stats dict."""
    html = html_path.read_text(encoding="utf-8")

    matches, story_type = find_stories(html)

    if not matches:
        return {"file": html_path.name, "stories": 0, "links": 0}

    total_links = 0
    new_html = html

    # Process stories in reverse order to preserve string positions
    for match in reversed(matches):
        # group(0) is the full match; for article pattern that's the whole story
        original = match.group(0)
        modified, count = linkify_story(original)
        if count > 0:
            new_html = new_html[:match.start()] + modified + new_html[match.end():]
            total_links += count

    stats = {"file": html_path.name, "stories": len(matches), "links": total_links}

    if total_links > 0:
        if DRY_RUN:
            stats["action"] = "would write"
        else:
            html_path.write_text(new_html, encoding="utf-8")
            stats["action"] = "written"
    else:
        stats["action"] = "no changes"

    return stats


# ── CSS addition ────────────────────────────────────────────────────────────

def add_css_if_needed():
    css_path = ROOT / "assets/radar.css"
    css = css_path.read_text(encoding="utf-8")
    if "brand-link" in css:
        return
    css_block = """
/* ── Brand links (in-body player mentions) ──────────────────────────── */
.brand-link{color:inherit;text-decoration:underline;text-underline-offset:2px;text-decoration-thickness:1px;text-decoration-color:rgba(45,55,70,.28)}
.brand-link:hover{text-decoration-color:var(--accent)}
"""
    if DRY_RUN:
        print("  [DRY-RUN] añadiría CSS brand-link a radar.css")
        return
    css_path.write_text(css + css_block, encoding="utf-8")
    print("  ✅ CSS brand-link añadido")


# ── Main ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Determine target files
    custom_file = None
    for i, arg in enumerate(sys.argv):
        if arg == "--file" and i + 1 < len(sys.argv):
            custom_file = sys.argv[i + 1]

    if custom_file:
        paths = sorted(ROOT.glob(custom_file))
    else:
        paths = sorted((ROOT / "magazines").glob("*.html"))

    print(f"linkify_brands.py {'[DRY-RUN] ' if DRY_RUN else ''}— {len(paths)} archivos\n")

    add_css_if_needed()
    print()

    total_links = 0
    for path in paths:
        stats = process_magazine(path)
        action_sym = "✅" if stats["links"] > 0 else "⏭"
        print(f"  {action_sym}  {stats['file']:45s} {stats['links']:2d} enlaces  ({stats['action']})")
        total_links += stats["links"]

    print(f"\nTotal: {total_links} enlaces de marca añadidos en {len(paths)} archivos")
