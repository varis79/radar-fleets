#!/usr/bin/env python3
"""
inject_story_links.py — Retroactive internal-link injection for existing magazine HTMLs.

Processes all (or a specific) magazine HTML file(s) and:
  1. Injects a <div class="story-related"> block after the .why-box of each story
     (if not already present — idempotent).
  2. Replaces <span class="story-tag ..."> with <a href="..." class="story-tag ...">
     when a relevant internal URL can be resolved.

Usage:
  python scripts/inject_story_links.py [--dry-run] [--file <path>]

Examples:
  python scripts/inject_story_links.py --dry-run
  python scripts/inject_story_links.py
  python scripts/inject_story_links.py --file magazines/2026-05-18-radar-fleet-by-pulpo.html
"""
from __future__ import annotations
import argparse
import sys
from pathlib import Path

from bs4 import BeautifulSoup, Tag

# Make lib importable from scripts/
sys.path.insert(0, str(Path(__file__).parent))
from lib.templating import (
    PILLAR_INDEX,
    HUB_LINKS_BY_MARKET,
    LEGACY_TOPIC_HUBS,
    HUB_LINKS_BY_PLAYER,
)
from lib.paths import ROOT, MAGAZINES_DIR


# ─── Tag class → topic code mapping (best-effort for retroactive parsing) ──
TAG_CLASS_TO_TOPIC: dict[str, str] = {
    "tag-ev":       "electrificacion-flotas",
    "tag-reg":      "compliance",
    "tag-tech":     "telematica",
    "tag-payments": "fuel-cards",
    "tag-ops":      "operacion-flotas",
    # tag-market, tag-mexico, tag-spain, tag-product → no specific topic
    # → will only get a market hub link
}

# ─── Flag emoji → market slug ───────────────────────────────────────────────
FLAG_TO_MARKET: dict[str, str] = {
    "🇲🇽": "mexico",
    "🇪🇸": "espana",
    "🇺🇸": "usa",
    "🌎": "latam",
    "🌍": "global",
    "🌐": "global",
    "🇪🇺": "europa",
    "🇬🇧": "global",
    "🇨🇴": "colombia",
    "🇨🇱": "chile",
    "🇦🇷": "argentina",
    "🇵🇪": "peru",
    "🇪🇨": "ecuador",
    "🇺🇾": "uruguay",
    "🇩🇴": "republica-dominicana",
}


def _parse_story_signals(article: Tag) -> dict[str, str]:
    """Extract tag_class and market from a story article/div element."""
    tag_class = ""
    market = ""

    # Find the story-tag element (span or a)
    tag_el = article.find(class_="story-tag")
    if tag_el:
        for cls in tag_el.get("class", []):
            if cls.startswith("tag-") and cls != "story-tag":
                tag_class = cls
                break

    # Find market from flag emoji in story-meta
    meta = article.find(class_="story-meta")
    if meta:
        spans = meta.find_all("span")
        if spans:
            text = spans[0].get_text(strip=True)
            for flag, mkt in FLAG_TO_MARKET.items():
                if flag in text:
                    market = mkt
                    break

    return {"tag_class": tag_class, "market": market}


def _resolve_links(tag_class: str, market: str) -> list[tuple[str, str]]:
    """Return up to 3 (label, url) pairs for a story's tag_class + market."""
    links: list[tuple[str, str]] = []
    seen: set[str] = set()

    def _add(label: str, url: str) -> None:
        if url not in seen:
            links.append((label, url))
            seen.add(url)

    topic = TAG_CLASS_TO_TOPIC.get(tag_class, "")

    # 1. Specific pillar (topic × market)
    if topic and market:
        hit = PILLAR_INDEX.get((topic, market))
        if hit:
            _add(*hit)

    # 2. Legacy generic hub fallback
    if not links and topic in LEGACY_TOPIC_HUBS:
        lbl, url = LEGACY_TOPIC_HUBS[topic]
        if topic == "compliance" and market == "mexico":
            lbl, url = "Regulación México", "/temas/regulacion-mexico/"
        _add(lbl, url)

    # 3. Market hub
    if market in HUB_LINKS_BY_MARKET:
        _add(*HUB_LINKS_BY_MARKET[market])

    return links[:3]


def _resolve_tag_url(tag_class: str, market: str) -> str | None:
    """Return the best URL for making the story tag clickable, or None."""
    topic = TAG_CLASS_TO_TOPIC.get(tag_class, "")
    if topic and market:
        hit = PILLAR_INDEX.get((topic, market))
        if hit:
            return hit[1]
    if market in HUB_LINKS_BY_MARKET:
        return HUB_LINKS_BY_MARKET[market][1]
    return None


def _process_magazine(html_path: Path, dry_run: bool = False) -> dict[str, int]:
    """Process a single magazine HTML file. Returns stats dict."""
    content = html_path.read_text(encoding="utf-8")
    soup = BeautifulSoup(content, "html.parser")

    # Editions use either <article class="story"> or <div class="story">
    articles = soup.find_all("article", class_="story")
    if not articles:
        articles = soup.find_all("div", class_="story")

    links_injected = 0
    tags_made_clickable = 0

    for article in articles:
        signals = _parse_story_signals(article)
        tag_class = signals["tag_class"]
        market    = signals["market"]

        # ── 1. Inject story-related div ─────────────────────────────────
        already_has_related = bool(article.find(class_="story-related"))
        if not already_has_related:
            link_pairs = _resolve_links(tag_class, market)
            if link_pairs:
                items_html = " · ".join(
                    f'<a href="{u}" class="related-link">{l}</a>'
                    for l, u in link_pairs
                )
                related_html = f'<div class="story-related">{items_html}</div>'
                related_tag = BeautifulSoup(related_html, "html.parser").find()

                # Inject after .why-box (the last meaningful block in the story body)
                why_box = article.find(class_="why-box")
                if why_box and related_tag:
                    why_box.insert_after(related_tag)
                    links_injected += 1

        # ── 2. Make story tag clickable ──────────────────────────────────
        tag_el = article.find(class_="story-tag")
        if tag_el and tag_el.name == "span":
            tag_url = _resolve_tag_url(tag_class, market)
            if tag_url:
                classes = " ".join(tag_el.get("class", []))
                text    = tag_el.get_text()
                new_a   = BeautifulSoup(
                    f'<a href="{tag_url}" class="{classes}">{text}</a>',
                    "html.parser"
                ).find()
                if new_a:
                    tag_el.replace_with(new_a)
                    tags_made_clickable += 1

    stats = {
        "stories":             len(articles),
        "links_injected":      links_injected,
        "tags_made_clickable": tags_made_clickable,
    }

    if dry_run:
        print(f"  [DRY-RUN] {html_path.name}: "
              f"{len(articles)} stories · "
              f"{links_injected} link blocks to inject · "
              f"{tags_made_clickable} tags to make clickable")
    else:
        html_path.write_text(str(soup), encoding="utf-8")
        print(f"  ✓ {html_path.name}: "
              f"{len(articles)} stories · "
              f"{links_injected} link blocks injected · "
              f"{tags_made_clickable} tags made clickable")

    return stats


def main() -> None:
    parser = argparse.ArgumentParser(description="Inject internal links into magazine HTMLs.")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would change without writing files.")
    parser.add_argument("--file", type=Path, default=None,
                        help="Process a single file instead of all magazines.")
    args = parser.parse_args()

    if args.file:
        targets = [ROOT / args.file] if not args.file.is_absolute() else [args.file]
    else:
        targets = sorted(MAGAZINES_DIR.glob("*-radar-fleet-by-pulpo.html"))

    if not targets:
        print("No magazine HTML files found.")
        sys.exit(0)

    mode = "DRY-RUN" if args.dry_run else "LIVE"
    print(f"\ninject_story_links.py · {mode} · {len(targets)} file(s)\n"
          f"PILLAR_INDEX entries: {len(PILLAR_INDEX)}\n")

    total = {"stories": 0, "links_injected": 0, "tags_made_clickable": 0}
    for path in targets:
        stats = _process_magazine(path, dry_run=args.dry_run)
        for k in total:
            total[k] += stats[k]

    print(f"\nTotal: {total['stories']} stories · "
          f"{total['links_injected']} link blocks {'(would be) ' if args.dry_run else ''}injected · "
          f"{total['tags_made_clickable']} tags {'(would be) ' if args.dry_run else ''}made clickable")


if __name__ == "__main__":
    main()
