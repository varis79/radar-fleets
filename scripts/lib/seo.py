"""
SEO helpers: generadores de bloques Schema.org JSON-LD.

Cada función devuelve un str listo para inyectar dentro de
<script type="application/ld+json">...</script> en el <head>.

Decisiones:
- Usamos JSON-LD (formato preferido por Google y LLMs vs microdata/RDFa).
- Schemas separados por tipo: NewsArticle (edición), Organization (Pulpo +
  The Fleet Radar), WebSite (con SearchAction), BreadcrumbList (rutas).
- Un mismo <head> puede tener varios bloques JSON-LD; Google los une.

Refs:
  https://schema.org/NewsArticle
  https://developers.google.com/search/docs/appearance/structured-data/article
"""
from __future__ import annotations
import datetime as dt
import json
from typing import Any

SITE_URL = "https://thefleetradar.com"
SITE_NAME = "The Fleet Radar · by Pulpo"
SITE_LOGO = f"{SITE_URL}/og-default.png"
PUBLISHER_PARENT = "Pulpo"
PUBLISHER_PARENT_URL = "https://getpulpo.com"


def _jsonld(obj: dict[str, Any]) -> str:
    """Serializa el dict a JSON-LD compacto dentro de <script>."""
    payload = json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
    return f'<script type="application/ld+json">{payload}</script>'


# ──────────────── Bloques globales ────────────────

def organization() -> str:
    """NewsMediaOrganization para The Fleet Radar.

    Por qué NewsMediaOrganization (no Organization genérico): es el tipo más
    fuerte para que Google News, ChatGPT Search, Perplexity y LLMs en general
    identifiquen el sitio como medio editorial. Estos modelos priorizan
    fuentes marcadas explícitamente como medios.

    Pulpo aparece como parent + en sameAs para asociación clara medio↔matriz.
    """
    return _jsonld({
        "@context": "https://schema.org",
        "@type": "NewsMediaOrganization",
        "@id": f"{SITE_URL}/#organization",
        "name": SITE_NAME,
        "alternateName": "The Fleet Radar",
        "url": SITE_URL,
        "description": (
            "Publicación editorial semanal de Pulpo sobre gestión de flotas, "
            "combustible, pagos, telemática, logística, IA, electrificación y "
            "regulación en México, España, Latinoamérica, Europa y Estados Unidos."
        ),
        "logo": {
            "@type": "ImageObject",
            "url": SITE_LOGO,
            "width": 1200,
            "height": 630,
        },
        "image": SITE_LOGO,
        "foundingDate": "2026-04-14",     # fecha primera edición publicada (Nº 1)
        "inLanguage": "es",
        "areaServed": ["MX", "ES", "CO", "CL", "AR", "PE", "EC", "UY", "DO", "US"],
        "parentOrganization": {
            "@type": "Organization",
            "name": PUBLISHER_PARENT,
            "url": PUBLISHER_PARENT_URL,
            "sameAs": ["https://www.linkedin.com/company/getpulpo"],
        },
        "publisher": {
            "@type": "Organization",
            "name": PUBLISHER_PARENT,
            "url": PUBLISHER_PARENT_URL,
        },
        "sameAs": [
            PUBLISHER_PARENT_URL,
            "https://www.linkedin.com/company/getpulpo",
        ],
    })


def website() -> str:
    """WebSite con SearchAction. Habilita Google Sitelinks search box."""
    return _jsonld({
        "@context": "https://schema.org",
        "@type": "WebSite",
        "@id": f"{SITE_URL}/#website",
        "url": SITE_URL,
        "name": SITE_NAME,
        "description": "Inteligencia semanal de mercado para el sector de gestión de flotas.",
        "publisher": {"@id": f"{SITE_URL}/#organization"},
        "inLanguage": "es-ES",
    })


# ──────────────── Bloques por página ────────────────

def news_article(
    *,
    headline: str,
    description: str,
    url: str,
    image_url: str,
    date_published: str,         # ISO 8601 con offset (YYYY-MM-DD o YYYY-MM-DDTHH:MM:SS+02:00)
    date_modified: str | None = None,
    section: str = "Fleet management",
    keywords: list[str] | None = None,
    word_count: int | None = None,
    article_body_excerpt: str | None = None,
) -> str:
    """NewsArticle para una edición publicada. Compatible con Google News
    structured data: requiere headline, image, datePublished, publisher."""
    obj: dict[str, Any] = {
        "@context": "https://schema.org",
        "@type": "NewsArticle",
        "headline": headline[:110],  # Google recomienda ≤110 chars
        "description": description,
        "url": url,
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": url,
        },
        "image": {
            "@type": "ImageObject",
            "url": image_url,
            "width": 1200,
            "height": 630,
        },
        "datePublished": date_published,
        "dateModified": date_modified or date_published,
        "author": {
            "@type": "Organization",
            "name": SITE_NAME,
            "url": SITE_URL,
        },
        "publisher": {"@id": f"{SITE_URL}/#organization"},
        "isPartOf": {"@id": f"{SITE_URL}/#website"},
        "articleSection": section,
        "inLanguage": "es-ES",
    }
    if keywords:
        obj["keywords"] = ", ".join(keywords)
    if word_count:
        obj["wordCount"] = int(word_count)
    if article_body_excerpt:
        # Google recomienda incluir el cuerpo o un extracto. No es obligatorio.
        obj["articleBody"] = article_body_excerpt[:4000]
    return _jsonld(obj)


def breadcrumb_list(items: list[tuple[str, str]]) -> str:
    """BreadcrumbList. items = [(name, url), (name, url), ...] en orden de raíz
    a hoja. El último elemento normalmente no necesita url, pero Google acepta."""
    return _jsonld({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i + 1,
                "name": name,
                "item": url,
            }
            for i, (name, url) in enumerate(items)
        ],
    })


def collection_page(
    *,
    name: str,
    description: str,
    url: str,
    parts_count: int | None = None,
) -> str:
    """CollectionPage para hubs (mercados, temas, players, archive)."""
    obj: dict[str, Any] = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": name,
        "description": description,
        "url": url,
        "isPartOf": {"@id": f"{SITE_URL}/#website"},
        "publisher": {"@id": f"{SITE_URL}/#organization"},
        "inLanguage": "es-ES",
    }
    if parts_count:
        obj["mainEntity"] = {
            "@type": "ItemList",
            "numberOfItems": parts_count,
        }
    return obj and _jsonld(obj)


# ──────────────── Combinadores ────────────────

def head_blocks_edition(
    *,
    headline: str,
    description: str,
    url: str,
    date_published: str,
    image_url: str = SITE_LOGO,
    keywords: list[str] | None = None,
    word_count: int | None = None,
    breadcrumbs: list[tuple[str, str]] | None = None,
) -> str:
    """Combina los bloques JSON-LD esperados en una edición (magazine):
    Organization + WebSite + NewsArticle + BreadcrumbList opcional."""
    blocks = [
        organization(),
        website(),
        news_article(
            headline=headline,
            description=description,
            url=url,
            image_url=image_url,
            date_published=date_published,
            keywords=keywords,
            word_count=word_count,
        ),
    ]
    if breadcrumbs:
        blocks.append(breadcrumb_list(breadcrumbs))
    return "\n".join(blocks)


def head_blocks_hub(
    *,
    name: str,
    description: str,
    url: str,
    breadcrumbs: list[tuple[str, str]] | None = None,
    parts_count: int | None = None,
) -> str:
    """Combina los bloques JSON-LD para una hub page (mercado/tema/player)."""
    blocks = [
        organization(),
        website(),
        collection_page(name=name, description=description, url=url, parts_count=parts_count),
    ]
    if breadcrumbs:
        blocks.append(breadcrumb_list(breadcrumbs))
    return "\n".join(blocks)
