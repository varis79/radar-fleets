#!/usr/bin/env python3
"""
discover_entities.py — Discovery semanal de entidades mencionadas en contenido.

Cada jueves recorre magazines + pillars recientes (últimos 14 días) y:
  1. Extrae entidades nombradas: ciudades, marcas/empresas, corredores
  2. Cruza con páginas existentes
  3. Para entidades mencionadas ≥2 veces que NO tienen página:
     - Si está en CITIES_KNOWN → crea stub automático (noindex, follow)
     - Si está en BRANDS_KNOWN → reporta como candidate (no crea, requiere
       page editorial real)
     - Si está en CORRIDORS_KNOWN → reporta como candidate
     - Si no encaja → log "unknown entity" para revisión manual
  4. Genera reporte en docs/discovery-log.md
  5. Re-corre linkify_master para que las nuevas pages se enlacen

Uso:
    python3 scripts/discover_entities.py [--dry-run] [--days 14]

Diseñado para correr en cron jueves 07:00 UTC (después del cron miércoles
de freshness, antes del lunes de magazine nueva).
"""
import os
import sys
if sys.path and sys.path[0].endswith("/scripts"):
    sys.path.pop(0)

import re
import datetime as dt
import argparse
from pathlib import Path
from collections import Counter
from bs4 import BeautifulSoup

ROOT = Path(__file__).parent.parent

# ─────────────── ENTITIES CONOCIDAS ───────────────
# Solo entidades EN ESTA LISTA pueden auto-crearse stubs (anti-spam,
# anti-falsos-positivos por errores OCR de la LLM).

CITIES_KNOWN = {
    # MX
    "Manzanillo": ("manzanillo-2026", "mexico", "Puerto Pacífico, mayor manejo de contenedores de México"),
    "Cuautitlán Izcalli": ("cuautitlan-izcalli-2026", "mexico", "Zona industrial-logística clave entre CDMX y Toluca"),
    "Cuautitlán": ("cuautitlan-2026", "mexico", "Hub logístico colindante a CDMX, sede de operaciones Bimbo/Coca-Cola FEMSA"),
    "Lázaro Cárdenas": ("lazaro-cardenas-2026", "mexico", "Puerto Pacífico, exportación automotriz y agrícola"),
    "Veracruz": ("veracruz-2026", "mexico", "Puerto histórico del Golfo, principal hub atlántico"),
    "Altamira": ("altamira-2026", "mexico", "Puerto del Golfo, química e industrial"),
    "Nuevo Laredo": ("nuevo-laredo-2026", "mexico", "Principal cruce fronterizo T-MEC con USA"),
    "Toluca": ("toluca-2026", "mexico", "Hub automotriz (Nissan, Chrysler) en Edomex"),
    "Tijuana": ("tijuana-2026", "mexico", "Frontera Pacífico, maquiladora y manufactura"),
    "Querétaro": ("queretaro-2026", "mexico", "Corredor industrial Bajío, aeroespacial y automotriz"),
    "Puebla": ("puebla-2026", "mexico", "Hub Volkswagen, automotriz Bajío sur"),
    "Mérida": ("merida-2026", "mexico", "Hub Sureste, turismo y logística regional"),
    "León": ("leon-2026", "mexico", "Bajío norte, calzado e industria"),
    # ES
    "Valencia": ("valencia-2026", "espana", "Puerto Mediterráneo, agroexportador y logístico"),
    "Sevilla": ("sevilla-2026", "espana", "Andalucía, agroindustrial y exportación"),
    "Bilbao": ("bilbao-2026", "espana", "Cantábrico, industria pesada y portuario"),
    "Zaragoza": ("zaragoza-2026", "espana", "PLAZA, hub logístico nacional ferroviario-carretero"),
    "Málaga": ("malaga-2026", "espana", "Costa, turismo y tech hub creciente"),
    "Vigo": ("vigo-2026", "espana", "Galicia, automotriz y pesca"),
    # LatAm
    "Bogotá": ("bogota-2026", "colombia", "Capital y eje del corredor logístico Buenaventura"),
    "Medellín": ("medellin-2026", "colombia", "Clúster transporte y logística, segunda ciudad"),
    "Cali": ("cali-2026", "colombia", "Pacífico colombiano, agroindustria"),
    "Santiago de Chile": ("santiago-2026", "chile", "Capital, mayor flota EV de buses fuera de China"),
    "Santiago": ("santiago-2026", "chile", "Capital, mayor flota EV de buses fuera de China"),
    "Buenos Aires": ("buenos-aires-2026", "argentina", "Capital, mayor hub logístico del Cono Sur"),
    "Lima": ("lima-2026", "peru", "Capital y eje portuario Callao"),
    "Quito": ("quito-2026", "ecuador", "Capital andina, mercado interno"),
    "Montevideo": ("montevideo-2026", "uruguay", "Capital, puerto y eje agroexportador"),
    "Santo Domingo": ("santo-domingo-2026", "republica-dominicana", "Capital, hub turístico y logístico Caribe"),
}

BRANDS_KNOWN = {
    # Telematics
    "Samsara": ("samsara", "telematica", "Plataforma telemetría enterprise USA"),
    "Geotab": ("geotab", "telematica", "Líder canadiense, partner integraciones"),
    "Motive": ("motive", "telematica", "ex-KeepTruckin, foco transporte USA"),
    "Webfleet": ("webfleet", "telematica", "Bridgestone Mobility Solutions, partner"),
    "Lytx": ("lytx", "telematica", "Video-telemática y safety"),
    "Omnitracs": ("omnitracs", "telematica", "Carga pesada y long-haul"),
    "Verizon Connect": ("verizon-connect", "telematica", "Telco-backed fleet platform"),
    "Trimble": ("trimble", "telematica", "Heavy industry telematics"),
    "Microlise": ("microlise", "telematica", "UK fleet telematics"),
    # OEMs
    "Volkswagen": ("volkswagen", "oem", "Fabricante alemán, hub MX en Puebla"),
    "Tesla": ("tesla", "oem", "Pionero EV ligero, Tesla Semi en piloto"),
    "BYD": ("byd", "oem", "Líder global EV pesado, BYD T7/T8 en MX/Chile"),
    "Mercedes-Benz": ("mercedes-benz", "oem", "Grupo Daimler Truck + autos premium"),
    # Operators
    "DHL Express": ("dhl", "operador", "Logística internacional"),
    "FedEx": ("fedex", "operador", "Express delivery global"),
    "Amazon Logistics": ("amazon-logistics", "operador", "Última milla propia y DSP"),
    "Mercado Libre": ("mercado-libre", "operador", "MeLi Envíos en LatAm"),
    "99 Minutos": ("99-minutos", "operador", "Última milla nativa LatAm"),
    # Fuel cards
    "WEX": ("wex", "fuel-cards", "Líder global fuel cards"),
    "Edenred": ("edenred", "fuel-cards", "Ticket Restaurant, fuel cards"),
}

CORRIDORS_KNOWN = {
    "California-Baja California": ("california-baja-california-2026", "Cross-border Pacífico MX-USA"),
    "Cali-Baja": ("california-baja-california-2026", "Cross-border Pacífico MX-USA"),
    "Nuevo Laredo - Laredo": ("nuevo-laredo-laredo-2026", "Cruce fronterizo #1 Norteamérica"),
    "corredor T-MEC": ("t-mec-2026", "Tratado USMCA aplicado al autotransporte"),
    "Bogotá-Buenaventura": ("bogota-buenaventura-2026", "Eje logístico colombiano #1"),
    "México-Querétaro": ("mexico-queretaro-2026", "Eje industrial automotriz/aeroespacial"),
}


# ─────────────── EXTRACT ENTITIES ───────────────

def _body_text(soup: BeautifulSoup) -> str:
    """Devuelve texto editorial limpio."""
    for el in soup.find_all(["header","footer","nav","script","style"]):
        el.decompose()
    return soup.get_text(" ", strip=True)


def extract_entities(text: str) -> dict:
    """Count mentions of known entities in text."""
    counts = {"cities": Counter(), "brands": Counter(), "corridors": Counter()}
    for entity in CITIES_KNOWN:
        cnt = len(re.findall(rf'\b{re.escape(entity)}\b', text))
        if cnt > 0:
            counts["cities"][entity] += cnt
    for entity in BRANDS_KNOWN:
        cnt = len(re.findall(rf'\b{re.escape(entity)}\b', text))
        if cnt > 0:
            counts["brands"][entity] += cnt
    for entity in CORRIDORS_KNOWN:
        cnt = text.count(entity)
        if cnt > 0:
            counts["corridors"][entity] += cnt
    return counts


# ─────────────── STUB GENERATION (ciudades) ───────────────

CITY_STUB_TEMPLATE = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<meta content="noindex, follow" name="robots"/>
<title>Flotas en {city} — cobertura editorial · The Fleet Radar</title>
<meta name="description" content="Cobertura editorial de flotas comerciales en {city} en 2026. Página en construcción mientras agregamos análisis."/>
<meta name="author" content="Pulpo — getpulpo.com"/>
<meta property="og:title" content="Flotas en {city} — The Fleet Radar"/>
<meta property="og:description" content="Cobertura editorial de flotas en {city}."/>
<meta property="og:type" content="article"/>
<meta property="og:url" content="https://thefleetradar.com/ciudades/{slug}/"/>
<meta property="og:site_name" content="The Fleet Radar · by Pulpo"/>
<meta property="og:image" content="https://thefleetradar.com/og-default.png"/>
<meta name="twitter:card" content="summary_large_image"/>
<meta name="twitter:title" content="Flotas en {city} — The Fleet Radar"/>
<meta name="twitter:description" content="Cobertura editorial de flotas en {city}."/>
<meta name="twitter:image" content="https://thefleetradar.com/og-default.png"/>
<meta property="article:published_time" content="{today}"/>
<meta property="article:modified_time" content="{today}"/>
<link rel="canonical" href="https://thefleetradar.com/ciudades/{slug}/"/>
<link rel="icon" type="image/svg+xml" href="/assets/brand/favicon.svg"/>
<link rel="stylesheet" href="/assets/radar.css"/>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"Article","headline":"Flotas en {city}","datePublished":"{today}","dateModified":"{today}","author":{{"@type":"Organization","name":"The Fleet Radar · by Pulpo"}},"publisher":{{"@id":"https://thefleetradar.com/#organization"}},"inLanguage":"{lang}"}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"The Fleet Radar","item":"https://thefleetradar.com/"}},{{"@type":"ListItem","position":2,"name":"Ciudades","item":"https://thefleetradar.com/ciudades/"}},{{"@type":"ListItem","position":3,"name":"{city}","item":"https://thefleetradar.com/ciudades/{slug}/"}}]}}</script>
</head>
<body>
<header class="topbar">
  <a class="topbar-brand" href="/">The Fleet Radar <span>by Pulpo</span></a>
  <div class="topbar-meta">Ciudad · {city}</div>
  <nav class="topbar-nav">
    <a href="/">Última</a><a href="/archive.html">Archivo</a><a href="/mercados/">Mercados</a><a href="/temas/">Temas</a><a href="/casos-uso/">Casos de uso</a><a href="/sectores/">Sectores</a><a href="/evergreen/">Recursos</a><a class="cta" href="https://www.getpulpo.com/" rel="noopener" target="_blank">Pulpo ↗</a>
  </nav>
</header>

<main class="pillar-main" style="max-width:780px;margin:0 auto;padding:48px 24px">
  <header class="pillar-hero">
    <span class="pillar-eyebrow">Ciudad · {country_label}</span>
    <h1 class="pillar-h1">Flotas en {city}</h1>
    <p class="pillar-intro">{description}.</p>
    <time class="page-updated" datetime="{today}">Actualizado el {today_pretty}</time>
  </header>

  <section class="pillar-body">
    <h2>Por qué importa {city} para gestión de flotas</h2>
    <p>{city} es {description_long}. Este contexto define el tipo de flota
    dominante (carga pesada, distribución urbana, última milla) y los retos
    operativos específicos del territorio.</p>

    <h2>Cobertura editorial en The Fleet Radar</h2>
    <p>The Fleet Radar ha mencionado {city} en {n_mentions} edición(es) recientes.
    Esta página crece con cada nueva cobertura editorial. Si gestionas flota
    en {city} y quieres que cubramos un ángulo específico (regulación local,
    operadores, sectores), <a href="mailto:hola@getpulpo.com">escríbenos</a>.</p>

    <h2>Páginas relacionadas</h2>
    <ul>
      <li><a href="/mercados/{market}/">Panorama de flotas en {country_label}</a></li>
      <li><a href="/temas/gestion-flota-{market}-2026/">Gestión de flotas en {country_label} 2026</a></li>
      <li><a href="/archive.html">Archivo de ediciones</a></li>
    </ul>

    <p><em>Stub generado automáticamente por discover_entities.py el {today_pretty}.
    Pasará a página completa (índex) cuando alcance el umbral de cobertura editorial.</em></p>
  </section>
</main>

<footer class="site-footer">
  <div class="footer-grid">
    <div class="footer-brand">
      <a class="footer-brand-link" href="/">The Fleet Radar <span>by Pulpo</span></a>
      <p class="footer-tagline">Inteligencia semanal de mercado para el sector de gestión de flotas en México, España y LatAm.</p>
    </div>
    <div class="footer-col">
      <h4>Secciones</h4>
      <ul><li><a href="/mercados/">Mercados</a></li><li><a href="/temas/">Temas</a></li><li><a href="/casos-uso/">Casos de uso</a></li><li><a href="/sectores/">Sectores</a></li><li><a href="/ciudades/">Ciudades</a></li><li><a href="/evergreen/">Recursos</a></li></ul>
    </div>
    <div class="footer-col">
      <h4>Ediciones</h4>
      <ul><li><a href="/">Última edición</a></li><li><a href="/archive.html">Archivo</a></li><li><a href="/rss.xml">RSS</a></li></ul>
    </div>
    <div class="footer-col">
      <h4>Legal</h4>
      <ul><li><a href="/legal/privacidad/">Privacidad</a></li><li><a href="/legal/terminos/">Términos</a></li><li><a href="mailto:hola@getpulpo.com">Contacto</a></li></ul>
    </div>
    <div class="footer-col">
      <h4>Pulpo</h4>
      <ul><li><a href="https://www.getpulpo.com/" rel="noopener" target="_blank">getpulpo.com ↗</a></li><li><a href="https://www.linkedin.com/company/getpulpo" rel="noopener" target="_blank">LinkedIn ↗</a></li></ul>
    </div>
  </div>
  <div class="footer-bottom">
    <span>© 2026 Pulpo · The Fleet Radar</span>
    <span class="footer-meta">Publicación editorial independiente. Análisis no constituye asesoría.</span>
  </div>
</footer>
</body>
</html>
"""

MONTH_NAMES = ["enero","febrero","marzo","abril","mayo","junio","julio",
               "agosto","septiembre","octubre","noviembre","diciembre"]


def _country_label(market: str) -> str:
    return {"mexico":"México","espana":"España","colombia":"Colombia",
            "chile":"Chile","argentina":"Argentina","peru":"Perú",
            "ecuador":"Ecuador","uruguay":"Uruguay",
            "republica-dominicana":"R. Dominicana"}.get(market, market.title())


def _hreflang(market: str) -> str:
    return "es-MX" if market == "mexico" else "es-ES" if market == "espana" else "es-419"


def create_city_stub(city: str, n_mentions: int, dry_run: bool = False) -> Path | None:
    if city not in CITIES_KNOWN:
        return None
    slug, market, description = CITIES_KNOWN[city]
    out = ROOT / "ciudades" / slug / "index.html"
    if out.exists():
        return None  # ya existe
    today = dt.date.today()
    today_iso = today.isoformat()
    today_pretty = f"{today.day} de {MONTH_NAMES[today.month-1]} de {today.year}"
    html = CITY_STUB_TEMPLATE.format(
        city=city,
        slug=slug,
        market=market,
        country_label=_country_label(market),
        description=description,
        description_long=f"un hub logístico mexicano/español/latam relevante por {description.lower()}",
        n_mentions=n_mentions,
        today=today_iso,
        today_pretty=today_pretty,
        lang=_hreflang(market),
    )
    if not dry_run:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html, encoding="utf-8")
    return out


# ─────────────── DISCOVERY MAIN ───────────────

def discover(days_back: int, dry_run: bool = False) -> dict:
    """Recorre contenido reciente y reporta entidades sin página."""
    cutoff = dt.datetime.now() - dt.timedelta(days=days_back)
    scanned = 0
    all_counts = {"cities": Counter(), "brands": Counter(), "corridors": Counter()}

    # Escanear magazines + pillars modificados recientes
    targets = list((ROOT / "magazines").glob("*.html"))
    for section in ("temas", "mercados", "casos-uso", "sectores"):
        targets.extend((ROOT / section).rglob("index.html"))

    for p in targets:
        try:
            mtime = dt.datetime.fromtimestamp(p.stat().st_mtime)
        except OSError:
            continue
        if mtime < cutoff:
            continue
        try:
            soup = BeautifulSoup(p.read_text(encoding="utf-8"), "html.parser")
        except Exception:
            continue
        text = _body_text(soup)
        counts = extract_entities(text)
        for cat in counts:
            all_counts[cat] += counts[cat]
        scanned += 1

    # Decidir acciones
    created_stubs = []
    candidates_brand = []
    candidates_corridor = []

    for city, n in all_counts["cities"].most_common():
        if city not in CITIES_KNOWN:
            continue
        slug, _, _ = CITIES_KNOWN[city]
        if (ROOT / "ciudades" / slug / "index.html").exists():
            continue
        if n < 2:
            continue
        path = create_city_stub(city, n, dry_run)
        if path:
            created_stubs.append((city, n, path))

    for brand, n in all_counts["brands"].most_common():
        if brand not in BRANDS_KNOWN:
            continue
        slug, _, _ = BRANDS_KNOWN[brand]
        if (ROOT / "players" / slug / "index.html").exists():
            continue
        if n >= 3:
            candidates_brand.append((brand, n))

    for corr, n in all_counts["corridors"].most_common():
        if corr not in CORRIDORS_KNOWN:
            continue
        slug, _ = CORRIDORS_KNOWN[corr]
        if (ROOT / "corredores" / slug / "index.html").exists():
            continue
        if n >= 2:
            candidates_corridor.append((corr, n))

    return {
        "scanned": scanned,
        "all_counts": all_counts,
        "created_stubs": created_stubs,
        "candidates_brand": candidates_brand,
        "candidates_corridor": candidates_corridor,
    }


def write_discovery_log(result: dict) -> Path:
    log_path = ROOT / "docs" / "discovery-log.md"
    today = dt.date.today().isoformat()

    existing = log_path.read_text(encoding="utf-8") if log_path.exists() else (
        "# Discovery log\n\n"
        "Registro semanal de entidades detectadas por `discover_entities.py`.\n\n"
        "---\n\n"
    )

    entry = [f"## {today}\n"]
    entry.append(f"Escaneados: {result['scanned']} archivos\n")

    if result["created_stubs"]:
        entry.append(f"\n### ✅ Stubs creados auto ({len(result['created_stubs'])})\n")
        for city, n, path in result["created_stubs"]:
            entry.append(f"- {city} ({n}x) → `{path.relative_to(ROOT)}`")
    else:
        entry.append("\n### ✅ Stubs creados auto: ninguno\n")

    if result["candidates_brand"]:
        entry.append(f"\n### 🟡 Brand pages candidatas (mención ≥3, sin page)\n")
        for brand, n in result["candidates_brand"][:10]:
            entry.append(f"- {brand} ({n}x)")

    if result["candidates_corridor"]:
        entry.append(f"\n### 🟡 Corredor pages candidatos\n")
        for corr, n in result["candidates_corridor"]:
            entry.append(f"- {corr} ({n}x)")

    entry.append("\n---\n")
    new = existing.rstrip() + "\n\n" + "\n".join(entry) + "\n"
    log_path.write_text(new, encoding="utf-8")
    return log_path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--days", type=int, default=14)
    args = parser.parse_args()

    mode = "[DRY-RUN]" if args.dry_run else "[LIVE]"
    print(f"\ndiscover_entities.py {mode}  (días: {args.days})\n")

    result = discover(args.days, args.dry_run)

    print(f"Escaneados: {result['scanned']} archivos modificados últimos {args.days} días")
    print()

    print(f"Top entidades mencionadas:")
    print(f"  Ciudades ({sum(result['all_counts']['cities'].values())} menciones totales):")
    for city, n in result['all_counts']['cities'].most_common(10):
        marker = "✓ page" if (ROOT / "ciudades" / CITIES_KNOWN.get(city, ("",))[0] / "index.html").exists() else "✗ GAP"
        print(f"    {n:3}x  {city:30}  {marker}")

    print(f"\n  Marcas ({sum(result['all_counts']['brands'].values())} menciones totales):")
    for brand, n in result['all_counts']['brands'].most_common(10):
        marker = "✓ page" if (ROOT / "players" / BRANDS_KNOWN.get(brand, ("",))[0] / "index.html").exists() else "✗ GAP"
        print(f"    {n:3}x  {brand:30}  {marker}")

    print(f"\n  Corredores:")
    for corr, n in result['all_counts']['corridors'].most_common():
        print(f"    {n:3}x  {corr}")

    print()
    if result["created_stubs"]:
        print(f"✅ Stubs creados: {len(result['created_stubs'])}")
        for city, n, path in result["created_stubs"]:
            print(f"  + {path.relative_to(ROOT)} ({city}, {n}x)")
    else:
        print("✅ Sin stubs nuevos esta vuelta")

    if not args.dry_run:
        log = write_discovery_log(result)
        print(f"\n📝 Discovery log actualizado: {log.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
