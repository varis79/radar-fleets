"""
Generador de hubs índices del sitio.

Crea/actualiza:
  /temas/index.html         ← listado de páginas pilar por topic + dimensión
  /casos-uso/index.html     ← listado de casos de uso × mercado
  /sectores/index.html      ← listado de verticales × mercado
  /ciudades/index.html      ← listado de ciudades agrupadas por mercado
  /mercados/<X>/index.html  ← un hub por mercado activo (ampliado para
                              cubrir todas las dimensiones)

Decisiones:
- Los hubs muestran SOLO páginas que existen como HTML publicado (no enlazan
  a URLs muertas). Las páginas planeadas en la matriz pero aún no generadas
  no aparecen al visitante — no exponemos al público la estrategia interna
  de SEO ("X planeadas, Y publicadas, Z en preparación"). Si no hay nada
  publicado para una sección, mostramos un empty-state neutro y editorial.
- Hub padre indexado (sin noindex). Las hijas heredan tier; ver pillar.py.
- Diseño hereda assets/radar.css + paleta navy/cream/accent global.
- Schema.org CollectionPage + ItemList para SEO.

Uso:
    python -m scripts.build_hubs           # genera todos los hubs
    python -m scripts.build_hubs --dry-run # muestra qué se haría sin escribir
"""
from __future__ import annotations
import argparse
import datetime as dt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.lib.paths import ROOT
from scripts.lib.pillar import (
    enumerate_pages, load_markets, load_topics, load_use_cases,
    load_verticals, load_subgeographies, pages_by_market,
    pages_by_dimension, PillarPage,
)

SITE_URL = "https://thefleetradar.com"
SITE_NAME = "The Fleet Radar · by Pulpo"
SITE_LOGO = f"{SITE_URL}/og-default.png"


# ─────────── Helpers ───────────

def page_exists(page: PillarPage) -> bool:
    """¿La página pilar ya tiene HTML publicado en el sitio?
    Convención: las pillar pages se publican en /temas/<slug>/index.html etc.
    El path varía por dimensión (ver page.url_path)."""
    rel = page.url_path().strip("/").rstrip("/")
    html_path = ROOT / rel / "index.html"
    return html_path.exists()


def head_block(
    *,
    title: str,
    description: str,
    canonical: str,
    schema_jsonld: str,
) -> str:
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="author" content="Pulpo — getpulpo.com">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="The Fleet Radar · by Pulpo">
<meta property="og:locale" content="es_ES">
<meta property="og:image" content="{SITE_LOGO}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="{SITE_LOGO}">
<link rel="canonical" href="{canonical}">
<link rel="alternate" type="application/rss+xml" title="{SITE_NAME}" href="/rss.xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,600;0,9..144,700;0,9..144,900;1,9..144,400&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/radar.css">
<style>:root{{ --accent:#c9a84c; --accent-2:#1e7fcb; }}</style>
{schema_jsonld}
</head>
<body>
<header class="topbar">
  <a href="/" class="topbar-brand">The Fleet Radar <span>by Pulpo</span></a>
  <div class="topbar-meta">Hub editorial</div>
  <nav class="topbar-nav">
    <a href="/" class="nav-extra">Última edición</a>
    <a href="/archive.html">Archivo</a>
    <a href="https://www.getpulpo.com/" class="cta" target="_blank" rel="noopener">Pulpo ↗</a>
  </nav>
</header>"""


CLOSING_BLOCK = """<section class="closing">
  <div class="closing-logo">The Fleet Radar <span>by Pulpo</span></div>
  <div class="closing-tagline">Inteligencia semanal para el sector de gestión de flotas</div>
  <div class="closing-divider"></div>
  <p style="font-size:13px;color:rgba(255,255,255,0.42);max-width:520px;margin:0 auto 32px;line-height:1.7;">Este hub forma parte de The Fleet Radar, publicación editorial dentro del ecosistema de Pulpo. Cada edición semanal añade nuevas referencias y enlaces a este índice.</p>
  <div class="closing-links" style="margin-top:24px;border-top:none;padding-top:0;">
    <a href="/">Última edición</a>
    <a href="/archive.html">Archivo</a>
    <a href="/temas/">Temas</a>
    <a href="/casos-uso/">Casos de uso</a>
    <a href="/sectores/">Sectores</a>
    <a href="/ciudades/">Ciudades</a>
    <a href="https://www.getpulpo.com/" target="_blank" rel="noopener">Pulpo</a>
  </div>
</section>
</body>
</html>
"""


def jsonld_collection(name: str, description: str, url: str,
                     items_count: int, breadcrumbs: list[tuple[str, str]]) -> str:
    import json
    blocks = []
    # Organization
    blocks.append({
        "@context": "https://schema.org",
        "@type": "Organization",
        "@id": f"{SITE_URL}/#organization",
        "name": SITE_NAME,
        "url": SITE_URL,
        "logo": SITE_LOGO,
        "parentOrganization": {"@type": "Organization", "name": "Pulpo", "url": "https://getpulpo.com"},
    })
    # WebSite
    blocks.append({
        "@context": "https://schema.org", "@type": "WebSite",
        "@id": f"{SITE_URL}/#website", "url": SITE_URL,
        "name": SITE_NAME, "inLanguage": "es-ES",
        "publisher": {"@id": f"{SITE_URL}/#organization"},
    })
    # CollectionPage + ItemList
    blocks.append({
        "@context": "https://schema.org", "@type": "CollectionPage",
        "name": name, "description": description, "url": url,
        "isPartOf": {"@id": f"{SITE_URL}/#website"},
        "publisher": {"@id": f"{SITE_URL}/#organization"},
        "inLanguage": "es-ES",
        "mainEntity": {"@type": "ItemList", "numberOfItems": items_count},
    })
    # Breadcrumbs
    if breadcrumbs:
        blocks.append({
            "@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": i + 1, "name": n, "item": u}
                for i, (n, u) in enumerate(breadcrumbs)
            ],
        })
    return "\n".join(f'<script type="application/ld+json">{json.dumps(b, ensure_ascii=False, separators=(",", ":"))}</script>' for b in blocks)


def hub_card_html(p: PillarPage) -> str:
    """Card individual clicable de una página publicada.
    Solo se llama para páginas que ya existen como HTML (no leak de
    estrategia SEO al visitante: las no publicadas simplemente no aparecen)."""
    return f"""
    <a class="hub-card" href="{p.url_path()}">
      <div class="hub-card-label">{p.label}</div>
      <div class="hub-card-meta"><span class="hub-card-market">{p.market_label}</span></div>
    </a>"""


# ─────────── Builders ───────────

def build_dimension_hub(dimension: str, all_pages: list[PillarPage], dry: bool) -> dict:
    """Genera /<dimension-prefix>/index.html con listado de páginas de esa dimensión."""
    dim_pages = pages_by_dimension(all_pages, dimension)
    dim_pages.sort(key=lambda p: (p.market_label, p.topic_code, p.intent_code))

    # Metadata por dimensión
    cfg = {
        "topic":    {"prefix": "temas",       "name": "Temas editoriales",            "desc": "Hub editorial de The Fleet Radar agrupando ediciones y análisis por tema de gestión de flotas: telemática, fuel cards, electrificación, mantenimiento, regulación, ciudades, sectores y más."},
        "use-case": {"prefix": "casos-uso",   "name": "Casos de uso de gestión de flota", "desc": "Casos de uso operativos para flotas: vehículos directivos, fuerza de ventas, reparto última milla, transporte pesado, perecederos, maquinaria pesada, taxis y más. Por mercado, con referencias de clientes reales."},
        "vertical": {"prefix": "sectores",    "name": "Sectores que usan flotas",     "desc": "Análisis por sector de industria: alimentación, e-commerce, telco, utilities, construcción, minería, farmacéutica, facility management, salud, gobierno y logística 3PL. Por mercado."},
        "subgeo":   {"prefix": "ciudades",    "name": "Flotas por ciudad",            "desc": "Análisis por ciudad: Madrid, Barcelona, CDMX, Guadalajara, Buenos Aires, Bogotá, Santiago, Lima y más, con foco en topics core (telemática, fuel cards, electrificación, mantenimiento, ZBE, robo de carga)."},
    }[dimension]

    out_path = ROOT / cfg["prefix"] / "index.html"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    published_count = sum(1 for p in dim_pages if page_exists(p))
    total = len(dim_pages)

    # Agrupar por mercado
    by_market: dict[str, list[PillarPage]] = {}
    for p in dim_pages:
        by_market.setdefault(p.market_label, []).append(p)

    # Solo páginas publicadas; las no-publicadas no se listan al visitante.
    cards_html_blocks = []
    for market_label, pages in sorted(by_market.items()):
        published_pages = [p for p in pages if page_exists(p)]
        if not published_pages:
            continue
        cards = "\n".join(hub_card_html(p) for p in published_pages)
        cards_html_blocks.append(f"""
  <section class="hub-section">
    <h2 class="hub-section-title">{market_label}</h2>
    <div class="hub-grid">
      {cards}
    </div>
  </section>""")

    # Si no hay nada publicado todavía, mostramos un estado neutro y editorial,
    # sin revelar conteos internos.
    if not cards_html_blocks:
        empty_state = f'<div class="hub-empty-state"><p>Estamos preparando la cobertura de esta sección. Mientras tanto, puedes consultar las <a href="/archive.html">ediciones publicadas</a> de The Fleet Radar o explorar otros <a href="/mercados/mexico/">mercados</a>.</p></div>'
        body_main = empty_state
    else:
        body_main = "".join(cards_html_blocks)

    canonical = f"{SITE_URL}/{cfg['prefix']}/"
    breadcrumbs = [("The Fleet Radar", SITE_URL + "/"), (cfg["name"], canonical)]
    schema = jsonld_collection(cfg["name"], cfg["desc"], canonical, published_count, breadcrumbs)

    html = head_block(
        title=f"{cfg['name']} · The Fleet Radar",
        description=cfg["desc"],
        canonical=canonical,
        schema_jsonld=schema,
    ) + f"""
<section class="hub-hero">
  <div class="container">
    <span class="hub-eyebrow">Hub editorial</span>
    <h1 class="hub-title">{cfg['name']}</h1>
    <p class="hub-intro">{cfg['desc']}</p>
  </div>
</section>
<main class="hub-main">
  <div class="container">
    {body_main}
  </div>
</main>
""" + CLOSING_BLOCK

    if not dry:
        out_path.write_text(html, encoding="utf-8")

    return {"path": str(out_path.relative_to(ROOT)), "total": total, "published": published_count}


def build_market_hub(market_code: str, all_pages: list[PillarPage], markets_dict: dict, dry: bool) -> dict:
    """Genera /mercados/<market_slug>/index.html con TODAS las páginas pilar
    de ese mercado, agrupadas por dimensión."""
    market = markets_dict.get(market_code)
    if not market:
        return {"path": None, "status": "market not found"}

    market_pages = pages_by_market(all_pages, market_code)
    market_pages.sort(key=lambda p: (p.dimension, p.topic_code))

    out_path = ROOT / "mercados" / market["slug"] / "index.html"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Si ya hay un index.html escrito a mano (mercados/mexico, mercados/espana,
    # mercados/latam), respetamos su contenido editorial y AÑADIMOS al final
    # una sección "Todas las páginas de este mercado" autogenerada con marker.
    # Si no existe, generamos uno desde cero con header genérico.
    MARKER_START = "<!-- AUTOGEN: pillar-pages-list START -->"
    MARKER_END   = "<!-- AUTOGEN: pillar-pages-list END -->"

    # Sección autogenerada (la misma siempre)
    by_dim = {}
    for p in market_pages:
        by_dim.setdefault(p.dimension, []).append(p)

    dim_labels = {
        "topic":    ("Temas",        "/temas/"),
        "use-case": ("Casos de uso", "/casos-uso/"),
        "vertical": ("Sectores",     "/sectores/"),
        "subgeo":   ("Ciudades",     "/ciudades/"),
    }
    # Solo dimensiones que tienen al menos 1 página publicada; sin estados
    # internos visibles al lector.
    dim_blocks = []
    for dim, (label, parent) in dim_labels.items():
        ps = by_dim.get(dim, [])
        if not ps:
            continue
        published = [p for p in ps if page_exists(p)]
        if not published:
            continue
        cards = "\n".join(hub_card_html(p) for p in published[:24])
        more_link = f'<a class="hub-section-link" href="{parent}">ver más →</a>' if len(published) > 24 else ""
        section = f"""
  <section class="hub-section">
    <h3 class="hub-section-title">{label} en {market['label']}  {more_link}</h3>
    <div class="hub-grid">{cards}</div>
  </section>"""
        dim_blocks.append(section)

    if not dim_blocks:
        # Aún sin nada publicado para este mercado: estado neutro, sin conteos.
        autogen_section = f"""{MARKER_START}
<section class="hub-autogen container">
  <p class="hub-empty-state">Estamos preparando la cobertura editorial sobre flotas en {market['label']}. Mientras tanto puedes explorar las <a href="/archive.html">ediciones publicadas</a> de The Fleet Radar.</p>
</section>
{MARKER_END}"""
    else:
        autogen_section = f"""{MARKER_START}
<section class="hub-autogen container">
  <h2 class="hub-section-supertitle">Más sobre flotas en {market['label']}</h2>
  {"".join(dim_blocks)}
</section>
{MARKER_END}"""

    if out_path.exists():
        # Existe (mercados/mexico, espana, latam). Insertar o reemplazar bloque autogen.
        original = out_path.read_text(encoding="utf-8")
        if MARKER_START in original and MARKER_END in original:
            # Reemplazar entre markers
            before = original.split(MARKER_START)[0]
            after = original.split(MARKER_END)[1]
            html = before + autogen_section + after
        else:
            # Insertar antes de </body>
            html = original.replace("</body>", f"\n{autogen_section}\n</body>", 1)
    else:
        # No existe, generar desde cero
        canonical = f"{SITE_URL}/mercados/{market['slug']}/"
        title = f"Flotas en {market['label']} · The Fleet Radar"
        desc = f"Análisis de gestión de flotas en {market['label']}: temas, casos de uso, sectores y ciudades cubiertos por The Fleet Radar."
        breadcrumbs = [("The Fleet Radar", SITE_URL + "/"), (market["label"], canonical)]
        schema = jsonld_collection(title, desc, canonical, len(market_pages), breadcrumbs)
        html = head_block(
            title=title, description=desc, canonical=canonical, schema_jsonld=schema,
        ) + f"""
<section class="hub-hero">
  <div class="container">
    <span class="hub-eyebrow">Mercado · {market.get('flag', '')}</span>
    <h1 class="hub-title">Flotas en {market['label']}</h1>
    <p class="hub-intro">{desc}</p>
  </div>
</section>
{autogen_section}
""" + CLOSING_BLOCK

    if not dry:
        out_path.write_text(html, encoding="utf-8")

    return {"path": str(out_path.relative_to(ROOT)), "pages_in_market": len(market_pages), "published": sum(1 for p in market_pages if page_exists(p))}


# ─────────── CSS extra para los hubs ───────────
# Lo inyectamos en assets/radar.css si no está, idempotente.
EXTRA_CSS_MARKER = "/* === HUB INDEX EXTRA STYLES (autogen by build_hubs.py) === */"
EXTRA_CSS = """
/* === HUB INDEX EXTRA STYLES (autogen by build_hubs.py) === */
.hub-hero{background:linear-gradient(135deg,var(--navy) 0%,var(--near-black) 100%);color:#fff;padding:96px 0 56px;border-bottom:2px solid var(--accent);}
.hub-eyebrow{font-size:11px;font-weight:600;letter-spacing:.22em;text-transform:uppercase;color:var(--accent);margin-bottom:18px;display:block;}
.hub-title{font-family:'Fraunces',serif;font-size:clamp(36px,5.5vw,64px);font-weight:800;line-height:1.05;margin-bottom:22px;}
.hub-intro{font-size:16px;line-height:1.75;color:rgba(255,255,255,.7);max-width:780px;margin-bottom:34px;}
.hub-stats{display:flex;gap:48px;flex-wrap:wrap;}
.hub-stat-num{font-family:'Fraunces',serif;font-size:36px;font-weight:700;color:var(--accent);}
.hub-stat-label{font-size:11px;color:rgba(255,255,255,.55);letter-spacing:.1em;text-transform:uppercase;}
.hub-main{padding:64px 0 96px;background:var(--off-white);}
.hub-section{margin-bottom:64px;}
.hub-section-supertitle{font-family:'Fraunces',serif;font-size:32px;font-weight:700;margin:48px 0 24px;}
.hub-section-title{font-family:'Fraunces',serif;font-size:22px;font-weight:600;margin-bottom:20px;color:var(--text-dark);border-bottom:1px solid var(--border-dark);padding-bottom:8px;display:flex;justify-content:space-between;align-items:baseline;}
.hub-section-link{font-family:'Inter',sans-serif;font-size:12px;font-weight:500;color:var(--accent-2);text-decoration:none;}
.hub-section-link:hover{color:var(--accent);}
.hub-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:14px;}
.hub-card{background:#fff;padding:16px 18px;border-radius:4px;border-left:3px solid var(--accent-2);text-decoration:none;color:var(--text-dark);transition:all .15s;display:flex;flex-direction:column;gap:8px;}
.hub-card:hover{transform:translateY(-2px);box-shadow:0 8px 24px rgba(0,0,0,.08);border-left-color:var(--accent);}
.hub-card-label{font-size:14px;font-weight:500;line-height:1.4;}
.hub-card-meta{font-size:11px;color:var(--text-light);display:flex;gap:10px;}
.hub-card-pending{background:rgba(0,0,0,.02);border-left-color:rgba(0,0,0,.1);color:var(--text-light);cursor:default;}
.hub-card-pending:hover{transform:none;box-shadow:none;}
.hub-card-state{color:var(--text-light);font-style:italic;}
.hub-empty{color:var(--text-light);font-size:13px;padding:20px;background:rgba(0,0,0,.02);border-radius:4px;}
.hub-pending-note{margin-top:14px;font-size:12px;color:var(--text-light);font-style:italic;}
.hub-disclaimer{margin-top:48px;padding:20px 24px;background:var(--cream);border-left:3px solid var(--accent);font-size:13px;color:var(--text-mid);line-height:1.7;border-radius:0 4px 4px 0;}
.hub-autogen{padding-top:32px;}
"""


def ensure_hub_css(dry: bool) -> bool:
    css_path = ROOT / "assets" / "radar.css"
    text = css_path.read_text(encoding="utf-8")
    if EXTRA_CSS_MARKER in text:
        return False
    if not dry:
        css_path.write_text(text + "\n" + EXTRA_CSS, encoding="utf-8")
    return True


# ─────────── Main ───────────

def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args(argv)

    print("Cargando matriz…")
    all_pages = enumerate_pages()
    print(f"  {len(all_pages)} páginas en matriz.")

    markets = {m["code"]: m for m in load_markets() if m.get("active", True)}

    # 1. CSS extra (idempotente)
    added = ensure_hub_css(args.dry_run)
    print(f"\nCSS hubs: {'añadido' if added else 'ya presente'}")

    # 2. Hubs de dimensión
    print("\nHubs de dimensión:")
    for dim in ["topic", "use-case", "vertical", "subgeo"]:
        result = build_dimension_hub(dim, all_pages, args.dry_run)
        print(f"  {result['path']:35s}  total={result['total']:>4}  publicadas={result['published']}")

    # 3. Hubs de mercado
    print("\nHubs de mercado:")
    for market_code in markets:
        result = build_market_hub(market_code, all_pages, markets, args.dry_run)
        if result.get("path"):
            # Logs internos sí muestran conteos (para nosotros); el HTML público no.
            print(f"  {result['path']:42s}  pages={result['pages_in_market']:>3}  publicadas={result['published']}")

    print("\n✅ Hubs " + ("simulados" if args.dry_run else "generados") + ".")
    return 0


if __name__ == "__main__":
    sys.exit(main())
