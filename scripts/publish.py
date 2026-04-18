"""
Publish. Actualiza los artefactos del sitio tras compose + qa exitosos.

Responsabilidades:
 - Copia la edición compuesta a index.html ajustando canonical a raíz y
   añadiendo <link rel="alternate"> al permalink.
 - Añade fila en archive.html (pill 'Última' en la nueva; quita 'Última'
   de la anterior).
 - Actualiza sitemap.xml (añade la nueva URL, priority 0.9).
 - Actualiza rss.xml (primer <item>, lastBuildDate, pubDate del channel).
 - Append a editorial-memory.md con el bloque canónico.

NO hace commit ni push. Eso lo gestiona el workflow.

En modo pause (qa no bloqueada, compose devolvió pause) no toca nada del
sitio; solo registra la pausa en editorial-memory.
"""
from __future__ import annotations
import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup

from scripts.lib.config import config
from scripts.lib.paths import (
    ROOT, INDEX_HTML, ARCHIVE_HTML, SITEMAP_XML, RSS_XML, EDITORIAL_MEMORY,
    DECISIONS_DIR, iso_week_key, magazine_paths
)
from scripts.lib.templating import human_date_es


def update_index_from_edition(edition_html: str, permalink: str) -> str:
    """Devuelve el contenido de index.html: copia de la edición con canonical a raíz."""
    soup = BeautifulSoup(edition_html, "html.parser")
    can = soup.find("link", rel="canonical")
    og = soup.find("meta", attrs={"property": "og:url"})
    if can:
        can["href"] = "https://thefleetradar.com/"
    if og:
        og["content"] = "https://thefleetradar.com/"
    # Añadir alternate al permalink justo después del canonical.
    # Title sacado del <title> de la propia edición (si existe) para que
    # el head-metadata del home incluya el título real del permalink.
    if can:
        t_tag = soup.find("title")
        alt_title = t_tag.get_text(strip=True) if t_tag else "Permalink"
        alt = soup.new_tag("link", rel="alternate", href=permalink, title=alt_title)
        can.insert_after(alt)
    return str(soup)


def update_archive(number: int, edition_date: dt.date, cover_headline: str, tags: list[str]) -> None:
    if not ARCHIVE_HTML.exists():
        return
    soup = BeautifulSoup(ARCHIVE_HTML.read_text(encoding="utf-8"), "html.parser")
    edition_list = soup.select_one(".edition-list")
    if not edition_list:
        return

    # Quitar 'Última' de la primera fila actual
    first_row = edition_list.find("a", class_="edition-row")
    if first_row:
        bad = first_row.select_one(".latest-badge")
        if bad:
            bad.decompose()

    # Construir la nueva fila
    tags_html = "".join(f'<span class="edition-tag">{t}</span>' for t in tags[:6])
    new_row_html = f"""
      <a href="/magazines/{edition_date.isoformat()}-radar-fleet-by-pulpo.html" class="edition-row">
        <div class="edition-num">{number:02d}</div>
        <div class="edition-meta">
          <div class="edition-date">{human_date_es(edition_date)} <span class="latest-badge">Última</span></div>
          <div class="edition-title">{cover_headline}</div>
          <div class="edition-tags">{tags_html}</div>
        </div>
        <div class="edition-arrow">→</div>
      </a>
"""
    new_soup = BeautifulSoup(new_row_html, "html.parser")
    edition_list.insert(0, new_soup)
    ARCHIVE_HTML.write_text(str(soup), encoding="utf-8")


def update_sitemap(edition_date: dt.date) -> None:
    if not SITEMAP_XML.exists():
        return
    text = SITEMAP_XML.read_text(encoding="utf-8")
    new_url = f"https://thefleetradar.com/magazines/{edition_date.isoformat()}-radar-fleet-by-pulpo.html"
    if new_url in text:
        return
    new_block = f"""  <url>
    <loc>{new_url}</loc>
    <lastmod>{edition_date.isoformat()}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.9</priority>
  </url>
"""
    text = text.replace("</urlset>", new_block + "</urlset>")
    # Refresca lastmod de home y archive al día de la edición
    text = re.sub(
        r"(<loc>https://thefleetradar\.com/</loc>\s*<lastmod>)[^<]+(</lastmod>)",
        rf"\g<1>{edition_date.isoformat()}\g<2>", text
    )
    text = re.sub(
        r"(<loc>https://thefleetradar\.com/archive\.html</loc>\s*<lastmod>)[^<]+(</lastmod>)",
        rf"\g<1>{edition_date.isoformat()}\g<2>", text
    )
    SITEMAP_XML.write_text(text, encoding="utf-8")


def rss_pubdate(d: dt.date, hour: str = "07:00:00 +0200") -> str:
    weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    return f"{weekdays[d.weekday()]}, {d.day:02d} {months[d.month - 1]} {d.year} {hour}"


def update_rss(number: int, edition_date: dt.date, cover_headline: str,
               cover_deck: str, permalink_full: str) -> None:
    if not RSS_XML.exists():
        return
    text = RSS_XML.read_text(encoding="utf-8")
    pub = rss_pubdate(edition_date)
    new_item = f"""
  <item>
    <title>Nº {number} · {cover_headline}</title>
    <link>{permalink_full}</link>
    <guid isPermaLink="true">{permalink_full}</guid>
    <pubDate>{pub}</pubDate>
    <dc:creator>The Fleet Radar · by Pulpo</dc:creator>
    <category>Fleet management</category>
    <description><![CDATA[
      {cover_deck}
    ]]></description>
  </item>
"""
    # Inserta justo después de la imagen del channel (antes del primer <item> existente).
    # Si no encuentra patrón, inserta antes de </channel>.
    anchor = text.find("<item>")
    if anchor == -1:
        text = text.replace("</channel>", new_item + "</channel>")
    else:
        text = text[:anchor] + new_item.strip() + "\n\n  " + text[anchor:]

    # Actualiza lastBuildDate y pubDate del channel
    text = re.sub(
        r"<lastBuildDate>[^<]+</lastBuildDate>",
        f"<lastBuildDate>{pub}</lastBuildDate>", text, count=1
    )
    text = re.sub(
        r"<pubDate>[^<]+</pubDate>",
        f"<pubDate>{pub}</pubDate>", text, count=1
    )
    RSS_XML.write_text(text, encoding="utf-8")


def append_editorial_memory(number: int, edition_date: dt.date, cover_headline: str,
                            stories: list[dict], mode: str, palette: dict) -> None:
    if not EDITORIAL_MEMORY.exists():
        return
    human = human_date_es(edition_date)
    block = [
        "",
        f"## Nº {number} · {edition_date.isoformat()} · \"{cover_headline}\"",
        f"Acento semanal: {palette.get('accent')}, {palette.get('accent_2')}",
        f"Permalink: /magazines/{edition_date.isoformat()}-radar-fleet-by-pulpo.html",
        f"Modo: {mode}",
        "",
        "### Historias cubiertas",
    ]
    for s in stories:
        topic = s.get("topic") or "?"
        market = s.get("market") or "?"
        head = s.get("headline", "")
        block.append(f"- [{topic}] {head} · {market}")
    block.append("")
    content = EDITORIAL_MEMORY.read_text(encoding="utf-8")
    if not content.endswith("\n"):
        content += "\n"
    content += "\n".join(block) + "\n"
    EDITORIAL_MEMORY.write_text(content, encoding="utf-8")


def publish(today: dt.date | None = None) -> dict:
    week = iso_week_key(today)
    compose_info_path = DECISIONS_DIR / f"{week}-compose.json"
    if not compose_info_path.exists():
        return {"error": "no-compose-info", "week": week}
    compose_info = json.loads(compose_info_path.read_text(encoding="utf-8"))

    if compose_info.get("status") == "pause":
        # Registrar pausa en memoria y salir
        pause_note = f"\n## Nº ? · {iso_week_key(today)} · pausa editorial\nRazón: material insuficiente.\n"
        if EDITORIAL_MEMORY.exists():
            EDITORIAL_MEMORY.write_text(
                EDITORIAL_MEMORY.read_text(encoding="utf-8") + pause_note,
                encoding="utf-8"
            )
        return {"status": "pause", "week": week}

    edition_date = dt.date.fromisoformat(compose_info["edition_date"])
    paths = magazine_paths(edition_date)
    html = paths["html"].read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")

    # Extraer datos de la propia edición
    cover_h1 = soup.select_one(".cover-issue")
    cover_headline = cover_h1.get_text(" ", strip=True) if cover_h1 else ""
    deck_el = soup.select_one(".cover-deck")
    cover_deck = deck_el.get_text(" ", strip=True) if deck_el else ""
    tag_els = soup.select(".cover-tag")
    tags = [t.get_text(strip=True) for t in tag_els[:6]]

    # index.html
    index_html = update_index_from_edition(html, paths["permalink"])
    INDEX_HTML.write_text(index_html, encoding="utf-8")

    # archive
    update_archive(compose_info["number"], edition_date, cover_headline, tags)

    # sitemap + rss
    permalink_full = f"https://thefleetradar.com{paths['permalink']}"
    update_sitemap(edition_date)
    update_rss(compose_info["number"], edition_date, cover_headline, cover_deck, permalink_full)

    # memoria editorial
    # Recuperamos los stories estructurados del HTML (topic del selection)
    sel_path = DECISIONS_DIR / f"{week}-selection.json"
    sel = json.loads(sel_path.read_text(encoding="utf-8")) if sel_path.exists() else {}
    stories = []
    for a, src in zip(soup.select("article.story"), sel.get("chosen", [])):
        head = a.select_one(".story-headline")
        stories.append({
            "headline": head.get_text(strip=True) if head else "",
            "topic": src.get("topic"),
            "market": src.get("market"),
        })

    # palette del compose info (está en data pero aquí inferimos por CSS inline)
    style = soup.find("style")
    accent = accent_2 = ""
    if style:
        m = re.search(r"--accent\s*:\s*([^;]+);", style.string or "")
        if m: accent = m.group(1).strip()
        m2 = re.search(r"--accent-2\s*:\s*([^;]+);", style.string or "")
        if m2: accent_2 = m2.group(1).strip()

    append_editorial_memory(
        compose_info["number"], edition_date, cover_headline, stories,
        compose_info.get("mode", "normal"), {"accent": accent, "accent_2": accent_2}
    )

    return {
        "status": "published",
        "week": week,
        "edition_date": edition_date.isoformat(),
        "number": compose_info["number"],
        "files_touched": [
            str(paths["html"].relative_to(ROOT)),
            str(paths["summary"].relative_to(ROOT)),
            "index.html", "archive.html", "sitemap.xml", "rss.xml",
            "content/editorial-memory.md",
        ],
    }


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--date", help="YYYY-MM-DD (default: hoy)")
    args = p.parse_args(argv)
    today = dt.date.fromisoformat(args.date) if args.date else None
    result = publish(today)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if "error" in result:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
