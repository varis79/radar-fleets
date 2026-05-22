"""
Inyecta Schema.org JSON-LD en las páginas estáticas del sitio
(index.html, archive.html, 404.html, hubs de mercados/temas/players/evergreen).

Decisiones:
- Las magazines NO se tocan aquí: ya se regeneran con templating.py en cada
  publish. Lo que tocamos aquí es contenido estático escrito a mano.
- Si la página YA tiene un <script type="application/ld+json">, lo
  reemplazamos por el nuevo (idempotente).
- Si NO tiene, lo inyectamos antes de </head>.
- También añadimos meta robots/og:image/twitter:image si faltan.

Uso:
    python -m scripts.inject_schema_static [--dry-run]

Idempotente: ejecutarlo dos veces da el mismo resultado.
"""
from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from scripts.lib.seo import (
    organization, website, news_article, collection_page,
    breadcrumb_list, head_blocks_hub, _jsonld, SITE_URL, SITE_NAME, SITE_LOGO,
)


# ─── Configuración por página ───
# Para cada página estática, definimos qué bloques Schema.org necesita.
# Las hub pages reciben CollectionPage + breadcrumbs. La home recibe WebSite
# + Organization + ItemList de últimas ediciones (más simple: solo
# Organization + WebSite + breadcrumbs).
PAGES: list[dict] = [
    {
        "path": "archive.html",
        "url": f"{SITE_URL}/archive.html",
        "name": "Archivo · The Fleet Radar",
        "description": "Todas las ediciones de The Fleet Radar · by Pulpo. Inteligencia semanal de mercado para el sector de gestión de flotas.",
        "type": "hub",
        "breadcrumbs": [("The Fleet Radar", SITE_URL + "/"), ("Archivo", f"{SITE_URL}/archive.html")],
    },
    {
        "path": "404.html",
        "url": f"{SITE_URL}/404.html",
        "name": "Página no encontrada · The Fleet Radar",
        "description": "Esta página no existe. Vuelve a la portada de The Fleet Radar.",
        "type": "minimal",
        "breadcrumbs": None,
    },
    {
        "path": "mercados/mexico/index.html",
        "url": f"{SITE_URL}/mercados/mexico/",
        "name": "Flotas en México 2026 · The Fleet Radar",
        "description": "Panorama de flotas en México en 2026: regulación CNE, Programa 6.000 MDP, SICT, players activos de telemática y pagos, tipos de flota dominantes.",
        "type": "hub",
        "breadcrumbs": [
            ("The Fleet Radar", SITE_URL + "/"),
            ("Mercados", f"{SITE_URL}/archive.html"),
            ("México", f"{SITE_URL}/mercados/mexico/"),
        ],
    },
    {
        "path": "mercados/espana/index.html",
        "url": f"{SITE_URL}/mercados/espana/",
        "name": "Flotas en España 2026 · The Fleet Radar",
        "description": "Panorama de flotas en España en 2026: DGT, V-16, ZBE, tacógrafo G2V2, renting empresarial, electrificación. Players, regulación y cifras.",
        "type": "hub",
        "breadcrumbs": [
            ("The Fleet Radar", SITE_URL + "/"),
            ("Mercados", f"{SITE_URL}/archive.html"),
            ("España", f"{SITE_URL}/mercados/espana/"),
        ],
    },
    {
        "path": "mercados/latam/index.html",
        "url": f"{SITE_URL}/mercados/latam/",
        "name": "Flotas en LatAm 2026 · The Fleet Radar",
        "description": "Panorama de flotas en LatAm: Colombia, Brasil, Chile, Perú, Argentina. Mercados, regulación y players.",
        "type": "hub",
        "breadcrumbs": [
            ("The Fleet Radar", SITE_URL + "/"),
            ("Mercados", f"{SITE_URL}/archive.html"),
            ("LatAm", f"{SITE_URL}/mercados/latam/"),
        ],
    },
    {
        "path": "temas/fuel-cards/index.html",
        "url": f"{SITE_URL}/temas/fuel-cards/",
        "name": "Tarjetas de flota (fuel cards) en 2026 · The Fleet Radar",
        "description": "Cómo están cambiando las tarjetas de flota en 2026: absorción de redes EV, peajes, mantenimiento. Players activos, criterios y cifras.",
        "type": "hub",
        "breadcrumbs": [
            ("The Fleet Radar", SITE_URL + "/"),
            ("Temas", f"{SITE_URL}/archive.html"),
            ("Fuel cards", f"{SITE_URL}/temas/fuel-cards/"),
        ],
    },
    {
        "path": "temas/electrificacion-flotas/index.html",
        "url": f"{SITE_URL}/temas/electrificacion-flotas/",
        "name": "Electrificación de flotas en 2026 · The Fleet Radar",
        "description": "Estado de la electrificación de flotas comerciales en 2026: MCS, depósito de carga, hubs de carga, paridad EV, mercado MX/ES/USA.",
        "type": "hub",
        "breadcrumbs": [
            ("The Fleet Radar", SITE_URL + "/"),
            ("Temas", f"{SITE_URL}/archive.html"),
            ("Electrificación de flotas", f"{SITE_URL}/temas/electrificacion-flotas/"),
        ],
    },
    {
        "path": "temas/compliance-espana/index.html",
        "url": f"{SITE_URL}/temas/compliance-espana/",
        "name": "Compliance en flotas españolas 2026 · The Fleet Radar",
        "description": "Cumplimiento normativo para flotas en España: DGT, V-16, ZBE, tacógrafo G2V2, BOE, peajes. Plazos, obligaciones y players.",
        "type": "hub",
        "breadcrumbs": [
            ("The Fleet Radar", SITE_URL + "/"),
            ("Temas", f"{SITE_URL}/archive.html"),
            ("Compliance España", f"{SITE_URL}/temas/compliance-espana/"),
        ],
    },
    {
        "path": "temas/regulacion-mexico/index.html",
        "url": f"{SITE_URL}/temas/regulacion-mexico/",
        "name": "Regulación de flotas en México 2026 · The Fleet Radar",
        "description": "Normativa para flotas y autotransporte en México: SICT, CNE (telemática hidrocarburos), DOF, Programa 6.000 MDP, T-MEC.",
        "type": "hub",
        "breadcrumbs": [
            ("The Fleet Radar", SITE_URL + "/"),
            ("Temas", f"{SITE_URL}/archive.html"),
            ("Regulación México", f"{SITE_URL}/temas/regulacion-mexico/"),
        ],
    },
    {
        "path": "players/pulpo/index.html",
        "url": f"{SITE_URL}/players/pulpo/",
        "name": "Pulpo · ficha de player · The Fleet Radar",
        "description": "Pulpo (getpulpo.com): fundada en 2018, gestiona +200k vehículos en México, España y otros mercados. Telemática, fuel cards, control de gasto.",
        "type": "hub",
        "breadcrumbs": [
            ("The Fleet Radar", SITE_URL + "/"),
            ("Players", f"{SITE_URL}/archive.html"),
            ("Pulpo", f"{SITE_URL}/players/pulpo/"),
        ],
    },
    {
        "path": "evergreen/guias/peaje-europa-2026/index.html",
        "url": f"{SITE_URL}/evergreen/guias/peaje-europa-2026/",
        "name": "Peajes en Europa 2026 · guía evergreen · The Fleet Radar",
        "description": "Guía evergreen sobre peajes en Europa en 2026: kilómetros, ejes, CO2, ruido. Países, sistemas, obligaciones.",
        "type": "hub",
        "breadcrumbs": [
            ("The Fleet Radar", SITE_URL + "/"),
            ("Evergreen", SITE_URL + "/"),
            ("Guías", SITE_URL + "/"),
            ("Peaje Europa 2026", f"{SITE_URL}/evergreen/guias/peaje-europa-2026/"),
        ],
    },
    {
        "path": "evergreen/checklists/evaluar-telematica-2026/index.html",
        "url": f"{SITE_URL}/evergreen/checklists/evaluar-telematica-2026/",
        "name": "Cómo evaluar telemática para tu flota en 2026 · The Fleet Radar",
        "description": "Checklist editorial para evaluar plataformas de telemática para flotas en 2026: criterios técnicos, integración, datos.",
        "type": "hub",
        "breadcrumbs": [
            ("The Fleet Radar", SITE_URL + "/"),
            ("Evergreen", SITE_URL + "/"),
            ("Checklists", SITE_URL + "/"),
            ("Evaluar telemática 2026", f"{SITE_URL}/evergreen/checklists/evaluar-telematica-2026/"),
        ],
    },
]


# ─── Regex (agnósticos al orden de atributos) ───
JSONLD_RE = re.compile(r'<script\s+type="application/ld\+json"[^>]*>.*?</script>', re.DOTALL | re.IGNORECASE)
HEAD_CLOSE_RE = re.compile(r'</head>', re.IGNORECASE)
META_ROBOTS_RE = re.compile(r'<meta[^>]*name="robots"[^>]*>', re.IGNORECASE)
OG_IMAGE_RE = re.compile(r'<meta[^>]*property="og:image"[^>]*>', re.IGNORECASE)
TWITTER_IMAGE_RE = re.compile(r'<meta[^>]*name="twitter:image"[^>]*>', re.IGNORECASE)
VIEWPORT_RE = re.compile(r'(<meta[^>]*name="viewport"[^>]*/?>)', re.IGNORECASE)
BING_VERIFY_RE = re.compile(r'<meta[^>]*name="msvalidate\.01"[^>]*>', re.IGNORECASE)


def inject_meta_robots(html: str) -> tuple[str, bool]:
    if META_ROBOTS_RE.search(html):
        return html, False
    tag = '<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">'
    return VIEWPORT_RE.sub(r'\1\n' + tag, html, count=1), True


def inject_bing_verify(html: str) -> tuple[str, bool]:
    """Bing Webmaster Tools verification. Bing busca este meta en cualquier
    URL del sitio, así que lo metemos en todas las páginas para máxima
    cobertura. Idempotente."""
    if BING_VERIFY_RE.search(html):
        return html, False
    tag = '<meta name="msvalidate.01" content="F76AFEB4A9F8059A6B4046015931CB70">'
    return VIEWPORT_RE.sub(r'\1\n' + tag, html, count=1), True


def inject_og_image(html: str) -> tuple[str, bool]:
    if OG_IMAGE_RE.search(html):
        return html, False
    block = (
        f'<meta property="og:image" content="{SITE_LOGO}">\n'
        f'<meta property="og:image:width" content="1200">\n'
        f'<meta property="og:image:height" content="630">'
    )
    # Insertar después de og:site_name si existe; si no, antes de </head>
    pat = re.compile(r'(<meta[^>]*property="og:site_name"[^>]*>)', re.IGNORECASE)
    if pat.search(html):
        return pat.sub(r'\1\n' + block, html, count=1), True
    return HEAD_CLOSE_RE.sub(block + '\n</head>', html, count=1), True


def inject_twitter_image(html: str) -> tuple[str, bool]:
    if TWITTER_IMAGE_RE.search(html):
        return html, False
    tag = f'<meta name="twitter:image" content="{SITE_LOGO}">'
    pat = re.compile(r'(<meta[^>]*name="twitter:description"[^>]*>)', re.IGNORECASE)
    if pat.search(html):
        return pat.sub(r'\1\n' + tag, html, count=1), True
    return HEAD_CLOSE_RE.sub(tag + '\n</head>', html, count=1), True


def inject_schema(html: str, schema_block: str) -> tuple[str, str]:
    """Reemplaza el bloque JSON-LD existente o inserta uno nuevo antes de </head>.
    Devuelve (html_modificado, accion)."""
    existing = JSONLD_RE.findall(html)
    if existing:
        # Reemplazamos TODOS los bloques existentes por el nuestro consolidado.
        html_new = JSONLD_RE.sub("", html, count=len(existing))
        action = f"replace {len(existing)} bloques"
        return HEAD_CLOSE_RE.sub(schema_block + '\n</head>', html_new, count=1), action
    return HEAD_CLOSE_RE.sub(schema_block + '\n</head>', html, count=1), "insert nuevo"


def schema_for_page(page: dict) -> str:
    if page["type"] == "minimal":
        # 404 sin breadcrumbs: solo Organization + WebSite
        return organization() + "\n" + website()
    return head_blocks_hub(
        name=page["name"],
        description=page["description"],
        url=page["url"],
        breadcrumbs=page["breadcrumbs"],
    )


def process(page: dict, dry: bool) -> dict:
    path = ROOT / page["path"]
    if not path.exists():
        return {"path": page["path"], "status": "missing"}
    original = path.read_text(encoding="utf-8")
    html = original

    # 1. meta robots
    html, changed_robots = inject_meta_robots(html)
    # 2. og:image
    html, changed_og = inject_og_image(html)
    # 3. twitter:image
    html, changed_tw = inject_twitter_image(html)
    # 4. Bing Webmaster verification
    html, changed_bing = inject_bing_verify(html)
    # 5. schema.org JSON-LD
    schema_block = schema_for_page(page)
    html, schema_action = inject_schema(html, schema_block)

    actions = []
    if changed_robots: actions.append("+robots")
    if changed_og:     actions.append("+og:image")
    if changed_tw:     actions.append("+twitter:image")
    if changed_bing:   actions.append("+bing-verify")
    actions.append(f"schema: {schema_action}")

    if html != original and not dry:
        path.write_text(html, encoding="utf-8")
        status = "modified"
    elif html != original and dry:
        status = "would-modify"
    else:
        status = "no-change"

    return {"path": page["path"], "status": status, "actions": actions}


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args(argv)

    for page in PAGES:
        result = process(page, args.dry_run)
        print(f"  {result['status']:15s} {result['path']:55s} {' '.join(result.get('actions', []))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
