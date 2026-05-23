"""
Render del HTML de edición semanal.

Decisiones de diseño:
- NO se rediseña ni se introduce un template engine nuevo. Se usa string.Template
  de stdlib con sustituciones explícitas. Respeta el sistema de diseño existente
  (assets/radar.css compartido + 4 vars de acento por edición).
- Se clona la estructura de la edición Nº 2 (magazines/2026-04-17-...html) que es
  la canónica tras las PRs de fix responsive y limpieza editorial.
- Toda la creatividad editorial (copy, headlines, resúmenes) viene del LLM en
  compose.py. Este módulo solo ensambla: recibe un dict y devuelve un HTML.

No maqueta a pelo secciones enteras — recibe los strings ya redactados y los
inserta en placeholders. Si una sección falta, se omite limpiamente (no aparece
en el render, sin dejar huecos ni divs vacíos).
"""
from __future__ import annotations
from pathlib import Path
from string import Template
from typing import Any
import csv
import datetime as dt

from .paths import ROOT


def _build_pillar_index() -> dict[tuple[str, str], tuple[str, str]]:
    """Builds (topic_code, market) → (short_label, url_path) from matrix.csv.
    Prefers intent=informational, then lowest tier. Only indexes pages that
    physically exist on disk (only links to published pillar pages)."""
    csv_path = ROOT / "content/pillar-matrix/matrix.csv"
    if not csv_path.exists():
        return {}
    index: dict[tuple[str, str], tuple[str, str]] = {}
    priority: dict[tuple[str, str], tuple[int, int]] = {}
    intent_rank = {"informational": 0, "guia-practica": 1, "comparativo": 2, "regulatorio": 3}
    with csv_path.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            tc = row.get("topic_code", "").strip()
            mkt = row.get("market", "").strip()
            url = row.get("url_path", "").strip()
            if not tc or not mkt or not url:
                continue
            # Only link to pages that physically exist
            page_dir = ROOT / url.strip("/")
            if not (page_dir / "index.html").exists():
                continue
            label = row.get("label", "").split(" · ")[0].replace(" 2026", "").strip()
            ir = intent_rank.get(row.get("intent", ""), 9)
            tr = int(row.get("tier", 9))
            key = (tc, mkt)
            if key not in priority or (ir, tr) < priority[key]:
                index[key] = (label, url)
                priority[key] = (ir, tr)
    return index


PILLAR_INDEX: dict[tuple[str, str], tuple[str, str]] = _build_pillar_index()


# Ruta de referencia para inspeccionar el sistema visual canónico.
REFERENCE_EDITION = ROOT / "magazines" / "2026-04-17-radar-fleet-by-pulpo.html"


HTML_HEAD = Template("""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
<meta name="msvalidate.01" content="F76AFEB4A9F8059A6B4046015931CB70">
<title>$title</title>
<meta name="description" content="$meta_description">
<meta name="author" content="Pulpo — getpulpo.com">
<meta name="keywords" content="$keywords">
<meta property="og:title" content="$og_title">
<meta property="og:description" content="$og_description">
<meta property="og:type" content="article">
<meta property="og:url" content="$canonical_url">
<meta property="og:site_name" content="The Fleet Radar · by Pulpo">
<meta property="og:locale" content="es_ES">
<meta property="og:image" content="https://thefleetradar.com/og-default.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="article:published_time" content="$iso_date">
<meta property="article:author" content="Pulpo">
<meta property="article:section" content="Fleet intelligence">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="$og_title">
<meta name="twitter:description" content="$og_description">
<meta name="twitter:image" content="https://thefleetradar.com/og-default.png">
<link rel="canonical" href="$canonical_url">
<link rel="icon" type="image/svg+xml" href="/assets/brand/favicon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/brand/favicon-32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/assets/brand/favicon-16.png">
<link rel="apple-touch-icon" sizes="180x180" href="/assets/brand/apple-touch-icon.png">
<link rel="alternate" type="application/rss+xml" title="The Fleet Radar · by Pulpo" href="/rss.xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,400;0,9..144,600;0,9..144,700;0,9..144,900;1,9..144,400;1,9..144,700&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/radar.css">
$schema_jsonld
<style>
  /* Acento semanal · Edición Nº $number · $human_date
     Única variación permitida por edición (4 vars). */
  :root{
    --accent:$accent;
    --accent-2:$accent_2;
    --cover-grad-a:$grad_a;
    --cover-grad-b:$grad_b;
  }
</style>
<script defer src="/_vercel/insights/script.js"></script>
<script defer src="/_vercel/speed-insights/script.js"></script>
</head>
""")


HTML_HEADER_COVER = Template("""<body>

<header class="topbar">
  <a href="/" class="topbar-brand">The Fleet Radar <span>by Pulpo</span></a>
  <div class="topbar-meta">Nº $number · $human_date</div>
  <nav class="topbar-nav">
    <a href="/" class="nav-extra">Última</a>
    <a href="/archive.html">Archivo</a>
    <a href="/temas/">Temas</a>
    <a href="/mercados/">Mercados</a>
    <a href="https://www.getpulpo.com/" class="cta" target="_blank" rel="noopener">Pulpo ↗</a>
  </nav>
</header>

<section class="cover">
  <div class="cover-head">
    <div class="cover-logo">The Fleet Radar <span>by Pulpo</span></div>
    <div class="cover-num">Nº $number_padded · $short_date</div>
  </div>
  <div class="cover-overline">$overline</div>
  <h1 class="cover-issue">$cover_headline</h1>
  <p class="cover-deck">$cover_deck</p>
  <div class="cover-tags">
$cover_tags
  </div>
</section>
""")


HTML_EDITORS_NOTE = Template("""
<section class="editors-note">
  <div class="container">
    <div class="editors-note-inner">
      <div class="editors-byline">Nota del editor · Nº $number</div>
      <div class="editors-body">
$editors_body
      </div>
      <div class="editors-signature">
        Publicado cada lunes a las 7:00 (Europa/Madrid)
        <strong>The Fleet Radar · by Pulpo · Nº $number · $human_date</strong>
      </div>
    </div>
  </div>
</section>
""")


HTML_WHAT_MATTERED_WRAP = Template("""
<section class="section section-near-black">
  <div class="container-wide">
    <div class="section-header">
      <span class="section-label section-label-light">Esta semana</span>
      <h2 class="section-title section-title-light">Lo que importó</h2>
      <div class="section-divider"></div>
    </div>
    <div class="wm-grid">
$wm_cards
    </div>
  </div>
</section>
""")


HTML_WM_CARD = Template("""      <div class="wm-card $tone">
        <div class="wm-number">$num</div>
        <div class="wm-headline">$headline</div>
        <div class="wm-body">$body</div>
      </div>""")


HTML_MOVEMENTS_WRAP = Template("""
<section class="section section-sand">
  <div class="container">
    <div class="section-header">
      <span class="section-label">Movimientos</span>
      <h2 class="section-title">En el tablero esta semana</h2>
      <div class="section-divider"></div>
      <p class="movements-sub">Contrataciones, M&amp;A, rondas y expansiones en el sector flota.</p>
    </div>
    <ul class="movements-list">
$movements
    </ul>
  </div>
</section>
""")

HTML_MOVEMENT_ITEM = Template("""      <li class="movement-item">
        <span class="mv-type mv-type-$type">$type_label</span>
        <span class="mv-market">$flag</span>
        <div class="mv-content">
          <strong class="mv-headline">$headline</strong>
          <span class="mv-detail">$detail</span>
        </div>
      </li>""")

HTML_STORIES_WRAP = Template("""
<section class="section section-cream">
  <div class="container">
    <div class="section-header">
      <span class="section-label">Las historias de la semana</span>
      <h2 class="section-title">$stories_title</h2>
      <div class="section-divider"></div>
    </div>
$stories
  </div>
</section>
""")


HTML_STORY = Template("""
    <article class="story">
      <div class="story-grid">
        <div class="story-left">
          <div class="story-number">$num</div>
          $story_tag_html
          <div class="story-meta"><span>$flag $market_label</span><span>$date_label</span></div>
        </div>
        <div>
          <h3 class="story-headline">$headline</h3>
          <p class="story-summary">$summary</p>
          <div class="why-box">
            <div class="why-item"><div class="why-label">Para quien opera</div><div class="why-text">$why_operator</div></div>
            <div class="why-item commercial"><div class="why-label">Para el negocio</div><div class="why-text">$why_business</div></div>
          </div>$related_links
        </div>
      </div>
    </article>
""")


# ─── Mapping topic/market/player → hub URL existente ─────────────────────
# PILLAR_INDEX (arriba) cubre todas las páginas pilar publicadas con lookup
# específico (topic_code, market). Las tablas siguientes son complementarias:
# HUB_LINKS_BY_MARKET → hub de mercado (siempre añadido si el mercado existe)
# LEGACY_TOPIC_HUBS → fallback genérico cuando PILLAR_INDEX no tiene match
# HUB_LINKS_BY_PLAYER → fichas de players mencionados en la historia
HUB_LINKS_BY_MARKET: dict[str, tuple[str, str]] = {
    "mexico":               ("Flotas en México",         "/mercados/mexico/"),
    "espana":               ("Flotas en España",         "/mercados/espana/"),
    "latam":                ("Flotas en LatAm",          "/mercados/latam/"),
    "argentina":            ("Flotas en Argentina",      "/mercados/argentina/"),
    "chile":                ("Flotas en Chile",          "/mercados/chile/"),
    "colombia":             ("Flotas en Colombia",       "/mercados/colombia/"),
    "ecuador":              ("Flotas en Ecuador",        "/mercados/ecuador/"),
    "peru":                 ("Flotas en Perú",           "/mercados/peru/"),
    "republica-dominicana": ("Flotas en R. Dominicana",  "/mercados/republica-dominicana/"),
    "uruguay":              ("Flotas en Uruguay",        "/mercados/uruguay/"),
}
LEGACY_TOPIC_HUBS: dict[str, tuple[str, str]] = {
    "fuel-cards":             ("Hub · Tarjetas de flota",          "/temas/fuel-cards/"),
    "electrificacion-flotas": ("Hub · Electrificación de flotas",  "/temas/electrificacion-flotas/"),
    "compliance":             ("Hub · Compliance",                 "/temas/compliance-espana/"),
}
HUB_LINKS_BY_PLAYER: dict[str, tuple[str, str]] = {
    "pulpo":    ("Ficha de Pulpo",               "/players/pulpo/"),
    "samsara":  ("Telemática de flotas",          "/temas/telematica-flotas-mexico-2026/"),
    "geotab":   ("Telemática de flotas",          "/temas/telematica-flotas-mexico-2026/"),
    "motive":   ("Telemática de flotas",          "/temas/telematica-flotas-mexico-2026/"),
    "webfleet": ("Telemática de flotas",          "/temas/telematica-flotas-espana-2026/"),
    "fleetio":  ("Telemática de flotas",          "/temas/telematica-flotas-mexico-2026/"),
    "lytx":     ("Telemática de flotas",          "/temas/telematica-flotas-mexico-2026/"),
    "wex":      ("Tarjetas de combustible",       "/temas/tarjetas-flota-mexico-2026/"),
    "coast":    ("Tarjetas de combustible",       "/temas/tarjetas-flota-mexico-2026/"),
    "ayvens":   ("Renting y leasing de flotas",  "/temas/gestion-flota-espana-2026/"),
    "tesla":    ("Electrificación de flotas",     "/temas/electrificacion-flotas-mexico-2026/"),
    "byd":      ("Electrificación de flotas",     "/temas/electrificacion-flotas-mexico-2026/"),
}


def build_related_links(story: dict) -> str:
    """Devuelve un bloque HTML con 1-3 enlaces internos al pie de la story.
    Prioridad:
      1. Página pilar específica (topic_code × market) desde PILLAR_INDEX
      2. Hub genérico legacy (LEGACY_TOPIC_HUBS) si 1 no encontró nada
      3. Hub de mercado (siempre, si el mercado está en HUB_LINKS_BY_MARKET)
      4. Ficha de player mencionado
    Si no hay ningún enlace aplicable, devuelve cadena vacía."""
    links: list[tuple[str, str]] = []
    seen: set[str] = set()
    topic  = story.get("topic") or ""
    market = story.get("market") or ""

    def _add(label: str, url: str) -> None:
        if url not in seen:
            links.append((label, url))
            seen.add(url)

    # 1. Pillar específico (topic × market)
    if topic and market:
        hit = PILLAR_INDEX.get((topic, market))
        if hit:
            _add(*hit)

    # 2. Fallback hub genérico legacy
    if not links and topic in LEGACY_TOPIC_HUBS:
        lbl, url = LEGACY_TOPIC_HUBS[topic]
        if topic == "compliance" and market == "mexico":
            lbl, url = "Regulación México", "/temas/regulacion-mexico/"
        _add(lbl, url)

    # 3. Hub de mercado
    if market in HUB_LINKS_BY_MARKET:
        _add(*HUB_LINKS_BY_MARKET[market])

    # 4. Player pages
    for p in (story.get("players") or []):
        if p in HUB_LINKS_BY_PLAYER:
            _add(*HUB_LINKS_BY_PLAYER[p])

    if not links:
        return ""

    items = " · ".join(
        f'<a href="{u}" class="related-link">{l}</a>'
        for l, u in links[:3]
    )
    return f'\n          <div class="story-related">{items}</div>'


def build_tag_html(story: dict) -> str:
    """Devuelve el elemento tag de la story: <a> si hay URL interna aplicable,
    <span> en caso contrario. El <a> hereda todos los estilos del <span>
    gracias a la regla a.story-tag en radar.css."""
    tc  = story.get("tag_class", "tag-market")
    lbl = story.get("tag_label", "")
    topic  = story.get("topic") or ""
    market = story.get("market") or ""
    url: str | None = None
    # Primero: página pilar específica
    if topic and market:
        hit = PILLAR_INDEX.get((topic, market))
        if hit:
            url = hit[1]
    # Fallback: hub de mercado
    if url is None and market in HUB_LINKS_BY_MARKET:
        url = HUB_LINKS_BY_MARKET[market][1]
    if url:
        return f'<a href="{url}" class="story-tag {tc}">{lbl}</a>'
    return f'<span class="story-tag {tc}">{lbl}</span>'


HTML_OPINION = Template("""
<section class="opinion-section">
  <div class="container">
    <span class="section-label section-label-light" style="margin-bottom:40px;display:block;">Opinión editorial</span>
    <div class="opinion-quote">$opinion_quote</div>
    <div class="opinion-body">
$opinion_body
    </div>
    <div class="opinion-byline">The Fleet Radar · by Pulpo · Nº $number · $human_date</div>
  </div>
</section>
""")


HTML_CTA = Template("""
<section class="cta-band">
  <div class="cta-inner">
    <div class="cta-kicker">Pulpo · Gestión de flotas con IA</div>
    <div class="cta-headline">$cta_headline</div>
    <p class="cta-sub">Pulpo lleva desde 2018 ayudando a flotas en México, España y otros países a poner orden en sus gastos, combustible, mantenimiento, documentación y operación. +200.000 vehículos gestionados, de 10 unidades hasta clientes con más de 10.000 unidades de todos los sectores.</p>
    <a href="https://www.getpulpo.com/" target="_blank" rel="noopener" class="cta-button">Ver Pulpo en acción</a>
    <a href="https://www.getpulpo.com/" target="_blank" rel="noopener" class="cta-secondary">Hablar con el equipo →</a>
  </div>
</section>
""")


HTML_CLOSING = Template("""
<section class="closing">
  <div class="closing-logo">The Fleet Radar <span>by Pulpo</span></div>
  <div class="closing-tagline">Inteligencia semanal para el sector de gestión de flotas</div>
  <div class="closing-divider"></div>
  <p style="font-size:13px;color:rgba(255,255,255,0.42);max-width:520px;margin:0 auto 32px;line-height:1.7;">The Fleet Radar es una publicación editorial dentro del ecosistema de Pulpo. Sale cada lunes a las 7:00 Europa/Madrid con lo que creemos que mueve los números de una flota esa semana.</p>
  <div class="closing-meta">Nº $number · $human_date · Próxima edición: $next_human</div>
  <div class="closing-footer">
    <div class="closing-tags">
      <span>México</span><span>España</span><span>USA</span><span>Europa</span><span>Telemática</span><span>Pagos</span><span>Electrificación</span><span>Regulación</span>
    </div>
  <div class="closing-links" style="margin-top:24px;border-top:none;padding-top:0;">
    <a href="/">Última edición</a>
    <a href="/archive.html">Archivo</a>
    <a href="/mercados/mexico/">México</a>
    <a href="/mercados/espana/">España</a>
    <a href="/mercados/latam/">LatAm</a>
    <a href="/temas/fuel-cards/">Fuel cards</a>
    <a href="/temas/electrificacion-flotas/">Electrificación</a>
    <a href="/players/pulpo/">Pulpo</a>
    <a href="/rss.xml" class="gold">RSS</a>
    <span class="closing-pulpo">Editado por <a href="https://www.getpulpo.com" target="_blank" rel="noopener">Pulpo</a></span>
  </div>
  </div>
</section>

<script defer src="/_vercel/insights/script.js"></script>

</body>
</html>
""")


def human_date_es(d: dt.date) -> str:
    meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio",
             "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
    return f"{d.day} de {meses[d.month - 1]} de {d.year}"


def short_date_es(d: dt.date) -> str:
    meses_short = ["ene", "feb", "mar", "abr", "may", "jun",
                   "jul", "ago", "sep", "oct", "nov", "dic"]
    return f"{d.day:02d} {meses_short[d.month - 1]} {d.year}"


FLAGS = {
    "mexico": "🇲🇽", "espana": "🇪🇸", "usa": "🇺🇸",
    "colombia": "🇨🇴", "brasil": "🇧🇷", "chile": "🇨🇱",
    "peru": "🇵🇪", "argentina": "🇦🇷",
    "latam": "🌎", "europa": "🇪🇺", "global": "🌐"
}
MARKET_LABELS = {
    "mexico": "México", "espana": "España", "usa": "USA",
    "colombia": "Colombia", "brasil": "Brasil", "chile": "Chile",
    "peru": "Perú", "argentina": "Argentina",
    "latam": "LatAm", "europa": "Europa", "global": "Global"
}


def render_edition(data: dict) -> str:
    """
    Ensambla el HTML de una edición semanal.

    `data` es un dict con:
      number:int
      edition_date:date
      next_date:date
      accent, accent_2, grad_a, grad_b : str (4 vars semanales)
      cover_headline, cover_deck, overline: str
      cover_tags: list[str]
      editors_body: str (HTML inline permitido: <strong>, <br>)
      wm_cards: list[{num,tone,headline,body}]
      stories_title: str
      stories: list[{num,tag_class,tag_label,market,date_label,headline,summary,why_operator,why_business}]
      cta_headline: str
    """
    d = data["edition_date"]
    canonical_url = f"https://thefleetradar.com/magazines/{d.isoformat()}-radar-fleet-by-pulpo.html"
    headline_full = f"The Fleet Radar · by Pulpo · Nº {data['number']} · {data['cover_headline']} · {human_date_es(d)}"
    # Schema.org JSON-LD: NewsArticle + Organization + WebSite + Breadcrumbs.
    # Permite que Google News y LLMs (ChatGPT/Perplexity/Claude) citen la edición
    # como fuente estructurada con autor, fecha, sección, organización.
    from .seo import head_blocks_edition
    schema_jsonld = head_blocks_edition(
        headline=f"Nº {data['number']} · {data['cover_headline']}",
        description=data["meta_description"],
        url=canonical_url,
        date_published=d.isoformat(),
        keywords=[k.strip() for k in data.get("keywords", "").split(",") if k.strip()],
        breadcrumbs=[
            ("The Fleet Radar", "https://thefleetradar.com/"),
            ("Ediciones", "https://thefleetradar.com/archive.html"),
            (f"Nº {data['number']}", canonical_url),
        ],
    )
    parts = [
        HTML_HEAD.substitute(
            title=headline_full,
            meta_description=data["meta_description"],
            keywords=data.get("keywords", "gestión de flotas, fleet management, telemática"),
            og_title=f"The Fleet Radar · by Pulpo · Nº {data['number']}",
            og_description=data["meta_description"],
            canonical_url=canonical_url,
            iso_date=d.isoformat(),
            number=data["number"],
            human_date=human_date_es(d),
            accent=data["accent"], accent_2=data["accent_2"],
            grad_a=data["grad_a"], grad_b=data["grad_b"],
            schema_jsonld=schema_jsonld,
        ),
        HTML_HEADER_COVER.substitute(
            number=data["number"],
            number_padded=f"{data['number']:02d}",
            short_date=short_date_es(d),
            human_date=human_date_es(d),
            overline=data.get("overline", "Edición semanal · Flotas, combustible, telemática y regulación"),
            cover_headline=data["cover_headline"],
            cover_deck=data["cover_deck"],
            cover_tags="\n".join([f'    <span class="cover-tag">{t}</span>' for t in data.get("cover_tags", [])]),
        ),
        HTML_EDITORS_NOTE.substitute(
            number=data["number"],
            human_date=human_date_es(d),
            editors_body=data["editors_body"],
        ),
    ]

    if data.get("wm_cards"):
        cards_html = "\n".join([
            HTML_WM_CARD.substitute(
                tone=c.get("tone", "signal"),
                num=f"{i + 1:02d}",
                headline=c["headline"],
                body=c["body"],
            )
            for i, c in enumerate(data["wm_cards"])
        ])
        parts.append(HTML_WHAT_MATTERED_WRAP.substitute(wm_cards=cards_html))

    if data.get("stories"):
        stories_html = "\n".join([
            HTML_STORY.substitute(
                num=f"{i + 1:02d}",
                story_tag_html=build_tag_html(s),
                flag=FLAGS.get(s.get("market", "global"), "🌐"),
                market_label=MARKET_LABELS.get(s.get("market", "global"), "Global"),
                date_label=s.get("date_label", ""),
                headline=s["headline"],
                summary=s["summary"],
                why_operator=s.get("why_operator", ""),
                why_business=s.get("why_business", ""),
                related_links=build_related_links(s),
            )
            for i, s in enumerate(data["stories"])
        ])
        parts.append(HTML_STORIES_WRAP.substitute(
            stories_title=data.get("stories_title", f"{len(data['stories'])} historias clave"),
            stories=stories_html,
        ))

    # Sección de movimientos (M&A, rondas, contrataciones, nombramientos).
    # Opcional: se omite si el campo está vacío o ausente.
    _MV_TYPE_LABELS = {
        "ma":            "M&amp;A",
        "ronda":         "Ronda",
        "contratacion":  "Contratación",
        "expansion":     "Expansión",
        "nombramiento":  "Nombramiento",
    }
    movimientos = data.get("movimientos") or []
    if movimientos:
        mv_items = []
        for m in movimientos:
            mv_type = m.get("type", "expansion")
            mv_items.append(HTML_MOVEMENT_ITEM.substitute(
                type=mv_type,
                type_label=_MV_TYPE_LABELS.get(mv_type, mv_type.capitalize()),
                flag=FLAGS.get(m.get("market", "global"), "🌐"),
                headline=m["headline"],
                detail=m.get("detail", ""),
            ))
        parts.append(HTML_MOVEMENTS_WRAP.substitute(movements="\n".join(mv_items)))

    # Sección de opinión editorial. Se renderiza solo si el compose produce
    # quote + body con contenido real. Si alguno falta o está vacío, se omite
    # limpiamente (no deja sección vacía). El CSS de radar.css ya soporta las
    # clases .opinion-section / .opinion-quote / .opinion-body / .opinion-byline.
    op_quote = (data.get("opinion_quote") or "").strip()
    op_body = (data.get("opinion_body") or "").strip()
    if op_quote and op_body:
        # opinion_body puede venir con párrafos separados por \n\n o con <br><br>.
        # Lo envolvemos en <p> si no trae marcado HTML explícito.
        if "<p" not in op_body and "<br" not in op_body:
            # Split por doble salto de línea y mete <p>
            paragraphs = [p.strip() for p in op_body.split("\n\n") if p.strip()]
            op_body_html = "\n".join(f"      <p>{p}</p>" for p in paragraphs)
        else:
            op_body_html = op_body
        parts.append(HTML_OPINION.substitute(
            opinion_quote=op_quote,
            opinion_body=op_body_html,
            number=data["number"],
            human_date=human_date_es(d),
        ))

    parts.append(HTML_CTA.substitute(
        cta_headline=data.get("cta_headline", "Si algo de esta edición te toca el P&amp;L, hablemos sin compromiso"),
    ))
    parts.append(HTML_CLOSING.substitute(
        number=data["number"],
        human_date=human_date_es(d),
        next_human=human_date_es(data["next_date"]),
    ))

    return "".join(parts)


def render_summary_txt(data: dict) -> str:
    """Genera el `…summary.txt` con etiquetas al final."""
    d = data["edition_date"]
    lines = []
    bar = "═" * 64
    lines.append(f"THE FLEET RADAR · BY PULPO — EDICIÓN Nº {data['number']}")
    lines.append(f"{human_date_es(d)}")
    lines.append(f'"{data["cover_headline"]}"')
    lines.append(bar)
    lines.append("")
    lines.append("RESUMEN EJECUTIVO")
    lines.append("─" * 17)
    lines.append(data.get("executive_summary", data["cover_deck"]))
    lines.append("")
    lines.append(bar)
    lines.append("")
    lines.append("HISTORIAS")
    lines.append("─" * 9)
    for i, s in enumerate(data.get("stories", []), 1):
        flag = FLAGS.get(s.get("market", "global"), "🌐")
        lines.append(f"{i}. {flag} {s['headline']}")
        if s.get("summary"):
            wrap = s["summary"][:320].replace("\n", " ")
            lines.append(f"   {wrap}")
        lines.append("")
    lines.append(bar)
    lines.append("")
    lines.append("ETIQUETAS POR HISTORIA")
    lines.append("─" * 22)
    for i, s in enumerate(data.get("stories", []), 1):
        tags = []
        if s.get("topic"): tags.append(f"topic:{s['topic']}")
        if s.get("market"): tags.append(f"market:{s['market']}")
        if s.get("fleet_type"): tags.append(f"fleet-type:{s['fleet_type']}")
        for p in s.get("players", []):
            tags.append(f"player:{p}")
        for mt in s.get("micro_tags", []):
            tags.append(mt)
        lines.append(f"{i}. {', '.join(tags) if tags else '(sin etiquetas)'}")
    lines.append("")
    lines.append(bar)
    lines.append(f"The Fleet Radar · by Pulpo · Nº {data['number']} · {human_date_es(d)}")
    lines.append(f"Próxima edición: {human_date_es(data['next_date'])} (lunes) — cadencia semanal")
    lines.append(bar)
    return "\n".join(lines) + "\n"
