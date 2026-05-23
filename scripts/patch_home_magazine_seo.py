#!/usr/bin/env python3
"""
patch_home_magazine_seo.py — Patch puntual para home + magazines:
  - Añade <meta property="og:image"> y <meta name="twitter:image"> si faltan
  - Añade JSON-LD Organization + WebSite a home (si no existen)

Idempotente. Bajo perfil; tocar solo si falta el tag.

Uso:
    python3 scripts/patch_home_magazine_seo.py [--dry-run]
"""
import sys
from pathlib import Path
from bs4 import BeautifulSoup, Tag

DRY_RUN = "--dry-run" in sys.argv
ROOT = Path(__file__).parent.parent
SITE = "https://thefleetradar.com"
OG_IMAGE = f"{SITE}/og-default.png"

ORG_JSONLD = (
    '{"@context":"https://schema.org","@type":"NewsMediaOrganization",'
    '"@id":"https://thefleetradar.com/#organization",'
    '"name":"The Fleet Radar · by Pulpo","alternateName":"The Fleet Radar",'
    '"url":"https://thefleetradar.com",'
    '"description":"Publicación editorial semanal de Pulpo sobre gestión de flotas, '
    'combustible, pagos, telemática, logística, IA, electrificación y regulación en '
    'México, España, Latinoamérica, Europa y Estados Unidos.",'
    '"logo":{"@type":"ImageObject","url":"https://thefleetradar.com/og-default.png",'
    '"width":1200,"height":630},'
    '"image":"https://thefleetradar.com/og-default.png",'
    '"foundingDate":"2026-04-14","inLanguage":"es",'
    '"areaServed":["MX","ES","CO","CL","AR","PE","EC","UY","DO","US"],'
    '"parentOrganization":{"@type":"Organization","name":"Pulpo","url":"https://getpulpo.com",'
    '"sameAs":["https://www.linkedin.com/company/getpulpo"]},'
    '"publisher":{"@type":"Organization","name":"Pulpo","url":"https://getpulpo.com"},'
    '"sameAs":["https://getpulpo.com","https://www.linkedin.com/company/getpulpo"]}'
)

WEBSITE_JSONLD = (
    '{"@context":"https://schema.org","@type":"WebSite",'
    '"@id":"https://thefleetradar.com/#website",'
    '"url":"https://thefleetradar.com",'
    '"name":"The Fleet Radar · by Pulpo",'
    '"description":"Inteligencia semanal de mercado para el sector de gestión de flotas.",'
    '"publisher":{"@id":"https://thefleetradar.com/#organization"},'
    '"inLanguage":"es-ES",'
    '"potentialAction":{"@type":"SearchAction",'
    '"target":"https://thefleetradar.com/archive.html?q={search_term_string}",'
    '"query-input":"required name=search_term_string"}}'
)


def patch_file(path: Path, is_home: bool) -> dict:
    text = path.read_text(encoding="utf-8")
    soup = BeautifulSoup(text, "html.parser")
    head = soup.find("head")
    if head is None:
        return {}

    changes = {"og_image": False, "twitter_image": False, "org": False, "website": False}

    # og:image
    if not soup.find("meta", attrs={"property": "og:image"}):
        tag = soup.new_tag("meta", attrs={"property": "og:image", "content": OG_IMAGE})
        head.append(tag)
        changes["og_image"] = True
        # Also add og:image:width/height for richness
        head.append(soup.new_tag("meta", attrs={"property": "og:image:width", "content": "1200"}))
        head.append(soup.new_tag("meta", attrs={"property": "og:image:height", "content": "630"}))

    # twitter:image
    if not soup.find("meta", attrs={"name": "twitter:image"}):
        tag = soup.new_tag("meta", attrs={"name": "twitter:image", "content": OG_IMAGE})
        head.append(tag)
        changes["twitter_image"] = True

    # Organization + WebSite — solo home
    if is_home:
        existing_types = set()
        for sc in soup.find_all("script", type="application/ld+json"):
            txt = sc.string or ""
            if '"NewsMediaOrganization"' in txt:
                existing_types.add("org")
            if '"WebSite"' in txt:
                existing_types.add("website")

        if "org" not in existing_types:
            sc = soup.new_tag("script", type="application/ld+json")
            sc.string = ORG_JSONLD
            head.append(sc)
            changes["org"] = True
        if "website" not in existing_types:
            sc = soup.new_tag("script", type="application/ld+json")
            sc.string = WEBSITE_JSONLD
            head.append(sc)
            changes["website"] = True

    if any(changes.values()) and not DRY_RUN:
        path.write_text(str(soup), encoding="utf-8")
    return changes


def main():
    mode = "[DRY-RUN]" if DRY_RUN else "[LIVE]"
    print(f"\npatch_home_magazine_seo.py {mode}\n")

    files = [(ROOT / "index.html", True)]
    for p in sorted((ROOT / "magazines").glob("*.html")):
        files.append((p, False))

    for path, is_home in files:
        if not path.exists():
            continue
        ch = patch_file(path, is_home)
        if any(ch.values()):
            tags = [k for k, v in ch.items() if v]
            marker = "[DRY]" if DRY_RUN else "  ✅"
            print(f"  {marker} {path.relative_to(ROOT)}: +{', '.join(tags)}")
        else:
            print(f"  ·    {path.relative_to(ROOT)}: ya tiene todo")


if __name__ == "__main__":
    main()
