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
import datetime as dt

from .paths import ROOT


# Ruta de referencia para inspeccionar el sistema visual canónico.
REFERENCE_EDITION = ROOT / "magazines" / "2026-04-17-radar-fleet-by-pulpo.html"


HTML_HEAD = Template("""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>$title</title>
<meta name="description" content="$meta_description">
<meta name="author" content="Pulpo — getpulpo.com">
<meta name="keywords" content="$keywords">
<meta property="og:title" content="$og_title">
<meta property="og:description" content="$og_description">
<meta property="og:type" content="article">
<meta property="og:url" content="$canonical_url">
<meta property="og:site_name" content="The Fleet Radar · by Pulpo">
<meta property="article:published_time" content="$iso_date">
<meta property="article:author" content="Pulpo">
<meta property="article:section" content="Fleet intelligence">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="$og_title">
<meta name="twitter:description" content="$og_description">
<link rel="canonical" href="$canonical_url">
<link rel="alternate" type="application/rss+xml" title="The Fleet Radar · by Pulpo" href="/rss.xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,400;0,9..144,600;0,9..144,700;0,9..144,900;1,9..144,400;1,9..144,700&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/radar.css">
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
</head>
""")


HTML_HEADER_COVER = Template("""<body>

<header class="topbar">
  <a href="/" class="topbar-brand">The Fleet Radar <span>by Pulpo</span></a>
  <div class="topbar-meta">Nº $number · $human_date</div>
  <nav class="topbar-nav">
    <a href="/" class="nav-extra">Última</a>
    <a href="/archive.html">Archivo</a>
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
          <span class="story-tag $tag_class">$tag_label</span>
          <div class="story-meta"><span>$flag $market_label</span><span>$date_label</span></div>
        </div>
        <div>
          <h3 class="story-headline">$headline</h3>
          <p class="story-summary">$summary</p>
          <div class="why-box">
            <div class="why-item"><div class="why-label">Para quien opera</div><div class="why-text">$why_operator</div></div>
            <div class="why-item commercial"><div class="why-label">Para el negocio</div><div class="why-text">$why_business</div></div>
          </div>
        </div>
      </div>
    </article>
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
    parts = [
        HTML_HEAD.substitute(
            title=f"The Fleet Radar · by Pulpo · Nº {data['number']} · {data['cover_headline']} · {human_date_es(d)}",
            meta_description=data["meta_description"],
            keywords=data.get("keywords", "gestión de flotas, fleet management, telemática"),
            og_title=f"The Fleet Radar · by Pulpo · Nº {data['number']}",
            og_description=data["meta_description"],
            canonical_url=f"https://thefleetradar.com/magazines/{d.isoformat()}-radar-fleet-by-pulpo.html",
            iso_date=d.isoformat(),
            number=data["number"],
            human_date=human_date_es(d),
            accent=data["accent"], accent_2=data["accent_2"],
            grad_a=data["grad_a"], grad_b=data["grad_b"],
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
                tag_class=s.get("tag_class", "tag-market"),
                tag_label=s.get("tag_label", "Movimiento de mercado"),
                flag=FLAGS.get(s.get("market", "global"), "🌐"),
                market_label=MARKET_LABELS.get(s.get("market", "global"), "Global"),
                date_label=s.get("date_label", ""),
                headline=s["headline"],
                summary=s["summary"],
                why_operator=s.get("why_operator", ""),
                why_business=s.get("why_business", ""),
            )
            for i, s in enumerate(data["stories"])
        ])
        parts.append(HTML_STORIES_WRAP.substitute(
            stories_title=data.get("stories_title", f"{len(data['stories'])} historias clave"),
            stories=stories_html,
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
