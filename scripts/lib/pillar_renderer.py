"""
Renderiza una página pilar completa a HTML.

Recibe:
  - PillarPage (metadata estructural: slug, dimension, market, intent, etc.)
  - editorial (dict del LLM con title_seo, intro, sections, faq, pulpo_box...)
  - related (dict de related_pages() con grupos de relaciones)
  - all_pages (lista completa de PillarPage para resolver URLs vivas)

Devuelve un str HTML completo con:
  - <head> con meta tags, og, twitter
  - schema.org JSON-LD (Article / HowTo / FAQPage según intent)
  - <body> con hero + intro + sections + FAQ + pulpo_box + related links
  - reusa assets/radar.css
"""
from __future__ import annotations
import datetime as dt
import json
from typing import Any

SITE_URL = "https://thefleetradar.com"
SITE_NAME = "The Fleet Radar · by Pulpo"
SITE_LOGO = f"{SITE_URL}/og-default.png"


def _jsonld(obj: dict) -> str:
    return f'<script type="application/ld+json">{json.dumps(obj, ensure_ascii=False, separators=(",", ":"))}</script>'


def _schema_blocks(page, editorial: dict, canonical: str, today_iso: str) -> str:
    """Genera Schema.org blocks según el intent de la página.

    NewsMediaOrganization + WebSite reusan el helper central en seo.py
    (consistencia con hubs y páginas estáticas). Aquí añadimos los
    específicos del pillar: Article/HowTo + BreadcrumbList + FAQPage.
    """
    # Import perezoso para evitar ciclos (seo.py no debe importar pillar_renderer)
    from scripts.lib.seo import organization as _org_jsonld, website as _site_jsonld
    # Article o HowTo según intent
    main: dict = {
        "@context": "https://schema.org",
        "@type": page.schema_type,
        "headline": editorial.get("h1", page.label)[:110],
        "description": editorial.get("meta_description", ""),
        "url": canonical,
        "mainEntityOfPage": {"@type": "WebPage", "@id": canonical},
        "datePublished": today_iso,
        "dateModified": today_iso,
        "author": {"@type": "Organization", "name": SITE_NAME, "url": SITE_URL},
        "publisher": {"@id": f"{SITE_URL}/#organization"},
        "isPartOf": {"@id": f"{SITE_URL}/#website"},
        "inLanguage": "es-ES",
        "image": {"@type": "ImageObject", "url": SITE_LOGO, "width": 1200, "height": 630},
    }
    if editorial.get("keywords_seo"):
        main["keywords"] = ", ".join(editorial["keywords_seo"])

    if page.schema_type == "HowTo":
        # Para guías, las sections son steps
        main["step"] = [
            {"@type": "HowToStep", "position": i + 1,
             "name": s.get("h2", "")[:80], "text": s.get("body_html", "")[:500]}
            for i, s in enumerate(editorial.get("sections", []))
        ]

    # FAQPage como bloque separado (puede coexistir con Article)
    faq_block = None
    if editorial.get("faq"):
        faq_block = {
            "@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": f["q"],
                 "acceptedAnswer": {"@type": "Answer", "text": f["a"]}}
                for f in editorial["faq"]
            ],
        }

    # Breadcrumbs según dimensión
    crumbs = _breadcrumbs_for(page, canonical)
    breadcrumb_block = {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": u}
            for i, (n, u) in enumerate(crumbs)
        ],
    }

    # NewsMediaOrganization + WebSite van como strings ya serializados desde seo.py
    pre = _org_jsonld() + "\n" + _site_jsonld()
    blocks = [main, breadcrumb_block]
    if faq_block:
        blocks.append(faq_block)
    return pre + "\n" + "\n".join(_jsonld(b) for b in blocks)


def _breadcrumbs_for(page, canonical: str) -> list[tuple[str, str]]:
    dim_label = {"topic": "Temas", "use-case": "Casos de uso",
                 "vertical": "Sectores", "subgeo": "Ciudades"}.get(page.dimension, "Temas")
    dim_url = {"topic": "/temas/", "use-case": "/casos-uso/",
               "vertical": "/sectores/", "subgeo": "/ciudades/"}.get(page.dimension, "/temas/")
    return [
        (SITE_NAME, SITE_URL + "/"),
        (dim_label, SITE_URL + dim_url),
        (page.market_label, f"{SITE_URL}/mercados/{page.market_slug}/"),
        (page.label[:60], canonical),
    ]


def _related_block(related: dict, all_pages_by_slug: dict) -> str:
    """Genera la sección 'Páginas relacionadas' al pie. Solo enlaza páginas
    que existen como PillarPage en la matriz (no URLs muertas; el filtro
    de "publicadas" lo aplica el caller si lo necesita)."""
    sections = [
        ("Mismo tema en otros mercados", related.get("sibling_same_topic_other_markets", [])),
        ("Casos de uso relacionados",    related.get("same_market_use_cases", [])),
        ("Sectores donde aplica",        related.get("same_market_verticals", [])),
        ("Ciudades relevantes",          related.get("same_market_subgeos", [])),
        ("Temas relacionados",           related.get("same_market_topics", [])),
    ]
    block_html = []
    for title, pages in sections:
        if not pages:
            continue
        links = "".join(f'<li><a href="{p.url_path()}">{p.label}</a></li>' for p in pages[:4])
        block_html.append(f'<div class="related-group"><h3 class="related-group-title">{title}</h3><ul class="related-list">{links}</ul></div>')
    if not block_html:
        return ""
    return f'<section class="pillar-related"><div class="container"><h2 class="pillar-related-title">Más sobre esto en The Fleet Radar</h2><div class="related-grid">{"".join(block_html)}</div></div></section>'


def _intent_eyebrow(page) -> str:
    return {
        "informational": "Análisis editorial",
        "comparativo":   "Comparativa",
        "regulatorio":   "Regulación y obligaciones",
        "guia-practica": "Guía práctica",
    }.get(page.intent_code, "Análisis editorial")


def _dimension_eyebrow_link(page) -> tuple[str, str]:
    """Devuelve (label_plural_correcto, url_hub). Plural correcto para
    breadcrumb sin tener que sufijar 's' (evita 'Caso de usos')."""
    return {
        "topic":    ("Temas",         "/temas/"),
        "use-case": ("Casos de uso",  "/casos-uso/"),
        "vertical": ("Sectores",      "/sectores/"),
        "subgeo":   ("Ciudades",      "/ciudades/"),
    }.get(page.dimension, ("Temas", "/temas/"))


def render_pillar_page(page, editorial: dict, related: dict, indexed: bool = False) -> str:
    """Renderiza HTML completo de una página pilar."""
    today = dt.date.today().isoformat()
    canonical = SITE_URL + page.url_path()
    title = editorial.get("title_seo") or page.label
    desc = editorial.get("meta_description") or ""
    h1 = editorial.get("h1") or page.label
    keywords = ", ".join(editorial.get("keywords_seo", []))

    # Robots: noindex hasta liberación
    robots = "index, follow, max-snippet:-1, max-image-preview:large" if indexed else "noindex, follow"

    schema_jsonld = _schema_blocks(page, editorial, canonical, today)
    eyebrow_dim_label, eyebrow_dim_link = _dimension_eyebrow_link(page)
    intent_eyebrow = _intent_eyebrow(page)

    # Render sections
    sections_html = []
    for sec in editorial.get("sections", []):
        h2 = sec.get("h2", "").strip()
        body = sec.get("body_html", "").strip()
        if not body:
            continue
        sections_html.append(f'<section class="pillar-section"><h2 class="pillar-h2">{h2}</h2><div class="pillar-body">{body}</div></section>')
    sections_block = "\n".join(sections_html)

    # FAQ
    faq_html = ""
    if editorial.get("faq"):
        items = "".join(
            f'<details class="pillar-faq-item"><summary>{f["q"]}</summary><div class="pillar-faq-a">{f["a"]}</div></details>'
            for f in editorial["faq"]
        )
        faq_html = f'<section class="pillar-faq"><h2 class="pillar-h2">Preguntas frecuentes</h2><div class="pillar-faq-list">{items}</div></section>'

    # Pulpo box
    pulpo_html = ""
    if editorial.get("pulpo_box"):
        pb = editorial["pulpo_box"]
        pulpo_html = f'<aside class="pillar-pulpo-box"><div class="pillar-pulpo-icon">🐙</div><div class="pillar-pulpo-content"><h3>{pb.get("heading", "Pulpo en este contexto")}</h3><div>{pb.get("body_html", "")}</div></div></aside>'

    # Related
    related_html = _related_block(related, {})

    # Disclaimer transparente
    disclaimer = '<div class="pillar-disclaimer"><strong>Página viva.</strong> Esta página recopila y sintetiza información pública sobre el tema, junto con cobertura editorial de The Fleet Radar. Se actualiza con cada edición semanal. ¿Detectas un dato incorrecto? <a href="https://github.com/varis79/radar-fleets/issues/new">Repórtalo en GitHub</a>.</div>'

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="{robots}">
<meta name="msvalidate.01" content="F76AFEB4A9F8059A6B4046015931CB70">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="author" content="Pulpo — getpulpo.com">
<meta name="keywords" content="{keywords}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="article">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="The Fleet Radar · by Pulpo">
<meta property="og:locale" content="es_ES">
<meta property="og:image" content="{SITE_LOGO}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="article:published_time" content="{today}">
<meta property="article:author" content="Pulpo">
<meta property="article:section" content="Fleet intelligence">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{SITE_LOGO}">
<link rel="canonical" href="{canonical}">
<link rel="icon" type="image/svg+xml" href="/assets/brand/favicon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/brand/favicon-32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/assets/brand/favicon-16.png">
<link rel="apple-touch-icon" sizes="180x180" href="/assets/brand/apple-touch-icon.png">
<link rel="alternate" type="application/rss+xml" title="{SITE_NAME}" href="/rss.xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,600;0,9..144,700;0,9..144,900;1,9..144,400&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/radar.css">
<style>:root{{ --accent:#c9a84c; --accent-2:#1e7fcb; }}</style>
{schema_jsonld}
<script defer src="/_vercel/insights/script.js"></script>
<script defer src="/_vercel/speed-insights/script.js"></script>
</head>
<body>
<header class="topbar">
  <a href="/" class="topbar-brand">The Fleet Radar <span>by Pulpo</span></a>
  <div class="topbar-meta">Página pilar · {page.market_label}</div>
  <nav class="topbar-nav">
    <a href="/">Última edición</a>
    <a href="/archive.html">Archivo</a>
    <a href="https://www.getpulpo.com/" class="cta" target="_blank" rel="noopener">Pulpo ↗</a>
  </nav>
</header>

<section class="pillar-hero">
  <div class="container">
    <div class="pillar-breadcrumbs">
      <a href="/">Home</a> · <a href="{eyebrow_dim_link}">{eyebrow_dim_label}</a> · <a href="/mercados/{page.market_slug}/">{page.market_label}</a>
    </div>
    <span class="pillar-eyebrow">{intent_eyebrow} · {page.market_label}</span>
    <h1 class="pillar-h1">{h1}</h1>
    <p class="pillar-intro">{editorial.get('intro', '')}</p>
  </div>
</section>

<main class="pillar-main">
  <div class="container">
    {sections_block}
    {pulpo_html}
    {faq_html}
    {disclaimer}
  </div>
</main>

{related_html}

<section class="closing">
  <div class="closing-logo">The Fleet Radar <span>by Pulpo</span></div>
  <div class="closing-tagline">Inteligencia semanal para el sector de gestión de flotas</div>
  <div class="closing-divider"></div>
  <div class="closing-links" style="margin-top:24px;border-top:none;padding-top:0;">
    <a href="/">Última edición</a>
    <a href="/archive.html">Archivo</a>
    <a href="{eyebrow_dim_link}">{eyebrow_dim_label}</a>
    <a href="/mercados/{page.market_slug}/">{page.market_label}</a>
    <a href="https://www.getpulpo.com/" target="_blank" rel="noopener">Pulpo</a>
  </div>
</section>
</body>
</html>
"""
    return html
