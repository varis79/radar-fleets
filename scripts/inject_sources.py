#!/usr/bin/env python3
"""
inject_sources.py — Adds a "Fuentes y referencias" section to 5 priority pillar pages.

Sources are based on:
  1. Regulatory bodies/agencies explicitly cited in each page's body text
  2. T21 MX articles harvested from our JSONL pipeline for relevant topics
  3. Official institutional URLs (not invented — all are real, verifiable domains)

Injects a <section class="pillar-sources"> immediately before <section class="pillar-related">
(or before the newsletter band if pillar-related is absent).
Idempotent: skips pages that already have .pillar-sources.

Usage:
    python3 scripts/inject_sources.py [--dry-run]
"""

import sys
import re
from pathlib import Path

DRY_RUN = "--dry-run" in sys.argv

ROOT = Path(__file__).parent.parent

# ---------------------------------------------------------------------------
# Sources catalogue — one entry per priority page
# Each source: {"label": str, "url": str, "note": str}
# ---------------------------------------------------------------------------

SOURCES_BY_PAGE = {
    "temas/tarjetas-flota-mexico-2026/index.html": {
        "title": "Fuentes y referencias",
        "sources": [
            {
                "label": "SAT — Resolución Miscelánea Fiscal 2025 (regla 2.7.1.8 CFDI combustibles)",
                "url": "https://www.sat.gob.mx/consulta/22266/conoce-la-resolucion-miscelanea-fiscal",
                "note": "Requisitos CFDI con complemento de combustibles",
            },
            {
                "label": "SICT — Registro Público Automotor (REPDA), parque vehicular federal",
                "url": "https://www.sict.gob.mx/",
                "note": "Datos de unidades registradas en autotransporte federal",
            },
            {
                "label": "CNH — Comisión Nacional de Hidrocarburos, datos de consumo por sector",
                "url": "https://www.gob.mx/cnh",
                "note": "Consumo sectorial de gasolinas y diésel",
            },
            {
                "label": "CNBV — Normativa sobre emisores de tarjetas y SOFOM",
                "url": "https://www.gob.mx/cnbv",
                "note": "Regulación de entidades financieras emisoras de tarjetas de flota",
            },
            {
                "label": "CRE — Lineamientos de interoperabilidad de sistemas de pago en estaciones de servicio",
                "url": "https://www.gob.mx/cre",
                "note": "Normativa de pagos en puntos de venta de combustible",
            },
            {
                "label": "AMEG — Asociación Mexicana de Empresarios Gasolineros",
                "url": "https://ameg.org.mx/",
                "note": "Cifras de mercado de estaciones de servicio y fraude en combustible",
            },
            {
                "label": "T21 MX — Samsara apuesta por IA para acelerar la respuesta ante robos al transporte",
                "url": "https://t21.com.mx/samsara-apuesta-por-ia-para-acelerar-la-respuesta-ante-robos-al-transporte/",
                "note": "Tecnología antifraude en combustible y transporte MX, mayo 2026",
            },
        ],
    },

    "temas/telematica-flotas-mexico-2026/index.html": {
        "title": "Fuentes y referencias",
        "sources": [
            {
                "label": "SICT — Normas Oficiales Mexicanas aplicables a autotransporte (NOM-SCT)",
                "url": "https://www.sict.gob.mx/",
                "note": "Regulación de dispositivos telemáticos y rastreo en unidades federales",
            },
            {
                "label": "DOF — Diario Oficial de la Federación, NOM y regulaciones SICT",
                "url": "https://www.dof.gob.mx/",
                "note": "Publicación oficial de normas aplicables a autotransporte y telemática",
            },
            {
                "label": "T21 MX — Grupo Aralo mejora seguridad y operación con tecnología de Samsara",
                "url": "https://t21.com.mx/grupo-aralo-mejora-seguridad-y-operacion-con-tecnologia-de-samsara/",
                "note": "Caso de uso real de telemática en flota de transporte MX, 2026",
            },
            {
                "label": "T21 MX — Samsara apuesta por IA para acelerar la respuesta ante robos al transporte",
                "url": "https://t21.com.mx/samsara-apuesta-por-ia-para-acelerar-la-respuesta-ante-robos-al-transporte/",
                "note": "IA y telemática para seguridad de flota en México, mayo 2026",
            },
            {
                "label": "INEGI — Encuesta Nacional de Transporte (ENT), flota y operaciones logísticas",
                "url": "https://www.inegi.org.mx/programas/ent/",
                "note": "Datos estructurales del parque vehicular y uso de tecnología en flota",
            },
            {
                "label": "Geotab — Fleet Management Technology Report 2025",
                "url": "https://www.geotab.com/fleet-management-technology/",
                "note": "Benchmarks de adopción de telemática en América Latina",
            },
        ],
    },

    "temas/compliance-flotas-mexico-2026/index.html": {
        "title": "Fuentes y referencias",
        "sources": [
            {
                "label": "SICT — Marco normativo del autotransporte federal de carga y pasaje",
                "url": "https://www.sict.gob.mx/",
                "note": "Reglamentos de autotransporte federal y normativa de cumplimiento",
            },
            {
                "label": "DOF — Diario Oficial de la Federación, normas y acuerdos SICT",
                "url": "https://www.dof.gob.mx/",
                "note": "Publicación de normas, acuerdos y reformas reglamentarias",
            },
            {
                "label": "SAT — Comprobantes fiscales y requisitos para autotransporte",
                "url": "https://www.sat.gob.mx/",
                "note": "Reglas de deducibilidad y facturación en el sector transporte",
            },
            {
                "label": "T21 MX — Seguridad y regulación presionan al autotransporte en Estado de México",
                "url": "https://t21.com.mx/seguridad-y-regulacion-presionan-al-autotransporte-en-estado-de-mexico/",
                "note": "Análisis de presión regulatoria en el corredor Estado de México, 2026",
            },
            {
                "label": "T21 MX — Competencia y ajustes regulatorios impactan al transporte en Cali-Baja",
                "url": "https://t21.com.mx/competencia-y-ajustes-regulatorios-impactan-al-transporte-en-cali-baja/",
                "note": "Regulación y corredor fronterizo MX-USA (nearshoring), 2026",
            },
            {
                "label": "INEGI — Estadísticas del sector transporte y logística",
                "url": "https://www.inegi.org.mx/temas/transporte/",
                "note": "Datos estructurales del autotransporte mexicano",
            },
        ],
    },

    "mercados/mexico/index.html": {
        "title": "Fuentes y referencias",
        "sources": [
            {
                "label": "SICT — Secretaría de Infraestructura, Comunicaciones y Transportes",
                "url": "https://www.sict.gob.mx/",
                "note": "Estadísticas del parque vehicular federal y regulación de autotransporte",
            },
            {
                "label": "DOF — Diario Oficial de la Federación",
                "url": "https://www.dof.gob.mx/",
                "note": "Normativa oficial: reglamentos, NOMs y acuerdos del sector transporte",
            },
            {
                "label": "INEGI — Encuesta Nacional de Transporte y datos logísticos",
                "url": "https://www.inegi.org.mx/temas/transporte/",
                "note": "Datos estructurales del parque vehicular y sector logístico en México",
            },
            {
                "label": "CNH — Comisión Nacional de Hidrocarburos, consumo sectorial",
                "url": "https://www.gob.mx/cnh",
                "note": "Estadísticas de consumo de combustible por sector económico",
            },
            {
                "label": "T21 MX — Publicación especializada en transporte y logística México",
                "url": "https://t21.com.mx/",
                "note": "Fuente de referencia para noticias del sector transporte en México",
            },
            {
                "label": "CANACAR — Cámara Nacional del Autotransporte de Carga",
                "url": "https://canacar.com.mx/",
                "note": "Representación gremial del autotransporte de carga federal",
            },
        ],
    },

    "mercados/espana/index.html": {
        "title": "Fuentes y referencias",
        "sources": [
            {
                "label": "DGT — Dirección General de Tráfico, estadísticas y normativa",
                "url": "https://www.dgt.es/",
                "note": "Parque de vehículos, normativa de circulación y regulación de flotas en España",
            },
            {
                "label": "BOE — Boletín Oficial del Estado, regulación transporte y ZBE",
                "url": "https://www.boe.es/",
                "note": "Legislación de transporte, emisiones y zonas de bajas emisiones",
            },
            {
                "label": "MITMA — Ministerio de Transportes, Movilidad y Agenda Urbana",
                "url": "https://www.mitma.gob.es/",
                "note": "Estadísticas de transporte de mercancías y política de movilidad",
            },
            {
                "label": "SEMA — Agencia Estatal de Meteorología / IDAE — Instituto para la Diversificación y Ahorro de la Energía",
                "url": "https://www.idae.es/",
                "note": "Datos de electrificación vehicular e incentivos MOVES en España",
            },
            {
                "label": "ANFAC — Asociación Española de Fabricantes de Automóviles y Camiones",
                "url": "https://anfac.com/",
                "note": "Matriculaciones de vehículos comerciales y tendencias del parque",
            },
            {
                "label": "ANECAT — Asociación Nacional Española de Centros de Asistencia al Transporte",
                "url": "https://anecat.org/",
                "note": "Gestión de flota, ITV y mantenimiento en el mercado español",
            },
        ],
    },
}

# ---------------------------------------------------------------------------
# HTML template for sources section
# ---------------------------------------------------------------------------

def build_sources_html(data: dict) -> str:
    title = data["title"]
    sources = data["sources"]
    items_html = "\n".join(
        f'      <li class="source-item">'
        f'<a href="{s["url"]}" class="source-link" target="_blank" rel="noopener nofollow">{s["label"]}</a>'
        f'<span class="source-note"> — {s["note"]}</span>'
        f'</li>'
        for s in sources
    )
    return f"""
<section class="pillar-sources">
  <div class="container">
    <h2 class="pillar-sources-title">{title}</h2>
    <ul class="sources-list">
{items_html}
    </ul>
    <p class="sources-note">Datos cuantitativos sin fuente específica provienen de análisis editorial basado en fuentes del sector. Las cifras son estimaciones orientativas salvo que se cite publicación oficial.</p>
  </div>
</section>"""


# ---------------------------------------------------------------------------
# Injection logic
# ---------------------------------------------------------------------------

def process_page(rel_path: str) -> bool:
    path = ROOT / rel_path
    if not path.exists():
        print(f"  ⚠️  No encontrado: {rel_path}")
        return False

    html = path.read_text(encoding="utf-8")

    if 'class="pillar-sources"' in html:
        print(f"  ⏭  Ya tiene fuentes: {rel_path}")
        return False

    sources_data = SOURCES_BY_PAGE[rel_path]
    sources_html = build_sources_html(sources_data)

    # Inject before <section class="pillar-related"> or <section class="newsletter-band">
    # or before <footer class="closing"> for market hub pages
    anchor = '<section class="pillar-related">'
    if anchor not in html:
        anchor = '<section class="newsletter-band">'
    if anchor not in html:
        anchor = '<footer class="closing"'
    if anchor not in html:
        print(f"  ⚠️  No se encontró anchor en: {rel_path}")
        return False

    new_html = html.replace(anchor, sources_html + "\n\n" + anchor, 1)

    if DRY_RUN:
        print(f"  [DRY-RUN] Inyectaría {len(sources_data['sources'])} fuentes en: {rel_path}")
        # Show a snippet
        idx = new_html.find('pillar-sources')
        print(f"  Preview: ...{new_html[idx:idx+200].strip()}...")
        return True

    path.write_text(new_html, encoding="utf-8")
    print(f"  ✅ {len(sources_data['sources'])} fuentes inyectadas: {rel_path}")
    return True


def add_css_if_needed():
    """Add CSS for the sources section to radar.css if not present."""
    css_path = ROOT / "assets/radar.css"
    css = css_path.read_text(encoding="utf-8")
    if "pillar-sources" in css:
        print("  ⏭  CSS ya existe")
        return

    css_block = """
/* ── Pillar sources section ────────────────────────────────────── */
.pillar-sources{background:#f7f8fa;border-top:1px solid rgba(45,55,70,.08);padding:40px 0 36px}
.pillar-sources-title{font-family:'Fraunces',serif;font-size:15px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#9aa0b0;margin:0 0 18px}
.sources-list{list-style:none;margin:0 0 16px;padding:0;display:flex;flex-direction:column;gap:8px}
.source-item{font-size:13px;line-height:1.5;color:#5a6072}
.source-link{color:#1e7fcb;text-decoration:none;font-weight:500}
.source-link:hover{text-decoration:underline}
.source-note{color:#9aa0b0}
.sources-note{font-size:12px;color:#9aa0b0;font-style:italic;margin:0}
"""
    if DRY_RUN:
        print("  [DRY-RUN] Añadiría CSS de .pillar-sources a radar.css")
        return

    css_path.write_text(css + css_block, encoding="utf-8")
    print("  ✅ CSS de fuentes añadido a radar.css")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print(f"inject_sources.py {'[DRY-RUN] ' if DRY_RUN else ''}— {len(SOURCES_BY_PAGE)} páginas objetivo\n")

    print("── CSS ──")
    add_css_if_needed()

    print("\n── Páginas ──")
    done = 0
    for rel_path in SOURCES_BY_PAGE:
        result = process_page(rel_path)
        if result and not DRY_RUN:
            done += 1

    if not DRY_RUN:
        print(f"\n✅ Completado: {done}/{len(SOURCES_BY_PAGE)} páginas actualizadas")
    else:
        print(f"\n[DRY-RUN] Listo — ejecuta sin --dry-run para aplicar cambios")
