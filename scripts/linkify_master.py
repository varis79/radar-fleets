#!/usr/bin/env python3
"""
linkify_master.py — Sistema unificado de auto-linking para The Fleet Radar.

Reemplaza/complementa los scripts especializados anteriores
(linkify_topics, linkify_brands, linkify_institutions) con un diccionario
unificado de entidades y políticas consistentes.

Cobertura:
  - Ciudades (Madrid, Manzanillo, Cuautitlán Izcalli, etc.)
  - Marcas/Empresas (Samsara, Geotab, Volkswagen, Tesla, BYD, etc.)
  - Corredores logísticos (T-MEC, California-Baja California, etc.)
  - Términos genéricos editoriales ("gestión de flotas", "control de gasto")
  - Topics (telemática, ZBE, ITV, ya cubiertos)

Reglas:
  - Una mención por entidad por página (primera ocurrencia)
  - Skip si ya está dentro de <a>
  - Skip si está en script/style/meta/head/nav/title
  - Skip si target URL es la página actual (self-link)
  - Skip si target page no existe en disco (filtrar a páginas publicadas)
  - Anchor diversificado por hash de URL origen (variantes 0-2)
  - CSS class por tipo: .city-link, .brand-link, .corridor-link, .topic-link

Uso:
    python3 scripts/linkify_master.py [--dry-run] [--dir temas]
    python3 scripts/linkify_master.py --file path/to/index.html
"""
import os
import sys
# Evitar conflicto con scripts/select.py al importar subprocess más tarde
if sys.path and sys.path[0].endswith("/scripts"):
    sys.path.pop(0)

import re
import hashlib
import csv
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString, Tag

DRY_RUN = "--dry-run" in sys.argv
ROOT = Path(__file__).parent.parent

TARGET_DIRS = ["temas", "mercados", "casos-uso", "sectores", "ciudades",
               "evergreen", "magazines"]
for i, arg in enumerate(sys.argv):
    if arg == "--dir" and i + 1 < len(sys.argv):
        TARGET_DIRS = [sys.argv[i + 1]]

SPECIFIC_FILE = None
for i, arg in enumerate(sys.argv):
    if arg == "--file" and i + 1 < len(sys.argv):
        SPECIFIC_FILE = Path(sys.argv[i + 1])


# ─────────────── ENTITY DICTIONARY ───────────────
#
# Cada entidad: tuple de variantes (todas se buscan, una se enlaza)
# Cada destino: dict con url, css_class, opcional partner_pulpo
#
# Order matters: entidades más específicas/largas PRIMERO para evitar
# que matches parciales tapen los completos (ej: "Mercedes-Benz" antes
# que "Mercedes").

CITIES_MX = {
    ("Cuautitlán Izcalli",): "/ciudades/cuautitlan-izcalli-2026/",
    ("Ciudad de México",): "/ciudades/cdmx-2026/",
    ("CDMX",): "/ciudades/cdmx-2026/",
    ("Guadalajara",): "/ciudades/guadalajara-2026/",
    ("Monterrey",): "/ciudades/monterrey-2026/",
    ("Querétaro",): "/ciudades/queretaro-2026/",
    ("Puebla",): "/ciudades/puebla-2026/",
    ("Manzanillo",): "/ciudades/manzanillo-2026/",
    ("Cuautitlán",): "/ciudades/cuautitlan-2026/",
    ("Toluca",): "/ciudades/toluca-2026/",
    ("Tijuana",): "/ciudades/tijuana-2026/",
    ("Lázaro Cárdenas",): "/ciudades/lazaro-cardenas-2026/",
    ("Veracruz",): "/ciudades/veracruz-2026/",
    ("Altamira",): "/ciudades/altamira-2026/",
    ("Nuevo Laredo",): "/ciudades/nuevo-laredo-2026/",
    ("Mérida",): "/ciudades/merida-2026/",
    ("León",): "/ciudades/leon-2026/",
}

CITIES_ES = {
    ("Madrid",): "/ciudades/madrid-2026/",
    ("Barcelona",): "/ciudades/barcelona-2026/",
    ("Valencia",): "/ciudades/valencia-2026/",
    ("Sevilla",): "/ciudades/sevilla-2026/",
    ("Bilbao",): "/ciudades/bilbao-2026/",
    ("Zaragoza",): "/ciudades/zaragoza-2026/",
    ("Málaga",): "/ciudades/malaga-2026/",
    ("Vigo",): "/ciudades/vigo-2026/",
}

CITIES_LATAM = {
    ("Bogotá",): "/ciudades/bogota-2026/",
    ("Medellín",): "/ciudades/medellin-2026/",
    ("Cali",): "/ciudades/cali-2026/",
    ("Santiago de Chile",): "/ciudades/santiago-2026/",
    ("Santiago",): "/ciudades/santiago-2026/",
    ("Buenos Aires",): "/ciudades/buenos-aires-2026/",
    ("Lima",): "/ciudades/lima-2026/",
    ("Quito",): "/ciudades/quito-2026/",
    ("Montevideo",): "/ciudades/montevideo-2026/",
    ("Santo Domingo",): "/ciudades/santo-domingo-2026/",
}

CITIES = {**CITIES_MX, **CITIES_ES, **CITIES_LATAM}

# ─────────────── PLATAFORMAS TELEMETRÍA ───────────────
# NO SON COMPETENCIA DE PULPO — son telemetría complementaria.
# Algunos son partners (Geotab, Webfleet integración).
# Pulpo es SaaS de gestión + tarjeta combustible.
PLATFORMS_TELEMETRY = {
    ("Samsara",): "/players/samsara/",
    ("Geotab",): "/players/geotab/",
    ("Webfleet",): "/players/webfleet/",
    ("Motive",): "/players/motive/",
    ("Lytx",): "/players/lytx/",
    ("Verizon Connect",): "/players/verizon-connect/",
    ("Omnitracs",): "/players/omnitracs/",
    ("Position Logic",): "/players/position-logic/",
    ("Trimble",): "/players/trimble/",
    ("Microlise",): "/players/microlise/",
}

# ─────────────── FUEL CARDS (algunos competencia parcial) ───────────────
FUEL_CARDS = {
    ("WEX",): "/players/wex/",
    ("Edenred",): "/players/edenred/",
    ("Solred",): "/players/solred/",
    ("Pluxee",): "/players/pluxee/",
}

# ─────────────── OEM CAMIONES Y VEHÍCULOS ───────────────
OEMS = {
    ("Mercedes-Benz",): "/players/mercedes-benz/",
    ("Volkswagen",): "/players/volkswagen/",
    ("Volvo Trucks",): "/players/volvo-trucks/",
    ("Volvo",): "/players/volvo-trucks/",
    ("Scania",): "/players/scania/",
    ("MAN",): "/players/man-trucks/",
    ("Iveco",): "/players/iveco/",
    ("DAF",): "/players/daf-trucks/",
    ("Renault Trucks",): "/players/renault-trucks/",
    ("Ford Trucks",): "/players/ford-trucks/",
    ("Kenworth",): "/players/kenworth/",
    ("Freightliner",): "/players/freightliner/",
    ("International",): "/players/international-trucks/",
    ("Hino",): "/players/hino/",
    ("Foton",): "/players/foton/",
    ("JAC",): "/players/jac-motors/",
    ("BYD",): "/players/byd/",
    ("Tesla",): "/players/tesla/",
    ("Mercedes",): "/players/mercedes-benz/",  # fallback corto
    ("MG",): "/players/mg-motors/",
    ("Stellantis",): "/players/stellantis/",
}

# ─────────────── OPERADORES LOGÍSTICOS ───────────────
LOGISTICS_OPERATORS = {
    ("DHL Express",): "/players/dhl/",
    ("DHL Supply Chain",): "/players/dhl/",
    ("DHL",): "/players/dhl/",
    ("FedEx",): "/players/fedex/",
    ("UPS",): "/players/ups/",
    ("Amazon Logistics",): "/players/amazon-logistics/",
    ("Mercado Libre",): "/players/mercado-libre/",
    ("MeLi",): "/players/mercado-libre/",
    ("99 Minutos",): "/players/99-minutos/",
    ("Estafeta",): "/players/estafeta/",
    ("Correos Express",): "/players/correos-express/",
    ("Correos",): "/players/correos/",
    ("SEUR",): "/players/seur/",
}

# ─────────────── CORREDORES LOGÍSTICOS ───────────────
CORRIDORS = {
    ("California-Baja California",): "/corredores/california-baja-california-2026/",
    ("Cali-Baja",): "/corredores/california-baja-california-2026/",
    ("Nuevo Laredo - Laredo",): "/corredores/nuevo-laredo-laredo-2026/",
    ("corredor T-MEC",): "/corredores/t-mec-2026/",
    ("Bogotá-Buenaventura",): "/corredores/bogota-buenaventura-2026/",
    ("México-Querétaro",): "/corredores/mexico-queretaro-2026/",
    ("Ruta 5",): "/corredores/ruta-5-chile-2026/",
}

# ─────────────── TÉRMINOS GENÉRICOS EDITORIALES ───────────────
# Resuelven a pillar del MISMO mercado de la página actual.
GENERIC_TERMS = {
    "gestión de flotas": "/temas/gestion-flota-{market}-2026/",
    "fleet management": "/temas/gestion-flota-{market}-2026/",
    "control de gasto": "/temas/control-gasto-flota-{market}-2026/",
    "compliance vehicular": "/temas/compliance-flotas-{market}-2026/",
    "electrificación de flotas": "/temas/electrificacion-flotas-{market}-2026/",
    "mantenimiento de flota": "/temas/mantenimiento-flota-{market}-2026/",
    "tarjetas de combustible": "/temas/tarjetas-flota-{market}-2026/",
    "renting de flota": "/temas/renting-leasing-flota-{market}-2026/",
}

# ─────────────── COMBINED REGISTRY ───────────────
# Orden importante: longest first → no canibalizamos matches parciales.
REGISTRY = []
for src in (CITIES, PLATFORMS_TELEMETRY, FUEL_CARDS, OEMS,
            LOGISTICS_OPERATORS, CORRIDORS):
    for variants, url in src.items():
        for v in variants:
            REGISTRY.append((v, url))
# Sort by phrase length desc
REGISTRY.sort(key=lambda x: -len(x[0]))


def _css_class_for(url: str) -> str:
    if url.startswith("/ciudades/"):
        return "city-link int-link"
    if url.startswith("/players/"):
        return "brand-link int-link"
    if url.startswith("/corredores/"):
        return "corridor-link int-link"
    return "int-link"


def _page_url(path: Path) -> str:
    rel = path.relative_to(ROOT)
    if rel.name == "index.html":
        parts = rel.parts[:-1]
        return "/" + "/".join(parts) + "/"
    return "/" + rel.as_posix()


def _detect_market(path: Path) -> str | None:
    s = str(path)
    if "mexico" in s or "-mx-" in s or "sict" in s or "t-mec" in s:
        return "mexico"
    if ("espana" in s or "spain" in s or "europa" in s
            or "dgt" in s or "baliza" in s or "-v16-" in s
            or "tacografo" in s or "tacógrafo" in s or "zbe" in s
            or "itv" in s):
        return "espana"
    if "colombia" in s:
        return "colombia"
    if "chile" in s:
        return "chile"
    return None


def _target_exists(url: str) -> bool:
    if url.startswith("http"):
        return True
    p = ROOT / url.lstrip("/")
    if url.endswith("/"):
        return (p / "index.html").exists()
    return p.exists()


def _is_in_anchor(node: NavigableString) -> bool:
    for parent in node.parents:
        if parent.name == "a":
            return True
        if parent.name in ("body", "[document]"):
            break
    return False


def _inject_link(node: NavigableString, pattern: re.Pattern, url: str,
                  css_class: str) -> bool:
    text = str(node)
    m = pattern.search(text)
    if not m:
        return False
    parent = node.parent
    idx = list(parent.children).index(node)
    before = text[:m.start()]
    label = text[m.start():m.end()]
    after = text[m.end():]
    node.replace_with(NavigableString(before))
    soup = BeautifulSoup("", "html.parser")
    a = soup.new_tag("a", href=url)
    a["class"] = css_class
    a.string = label
    parent.insert(idx + 1, a)
    parent.insert(idx + 2, NavigableString(after))
    return True


def linkify_soup(soup: BeautifulSoup, market: str | None,
                  self_url: str) -> int:
    """Aplica linking sobre body. Devuelve nº de links añadidos."""
    body = soup.find("body")
    if not body:
        return 0
    added = 0
    linked_urls: set[str] = set()

    # 1. Entidades nombradas (REGISTRY)
    for phrase, url in REGISTRY:
        # Resolver URL final (puede ser stub si no existe)
        if not _target_exists(url):
            continue  # solo enlazamos a páginas existentes
        # Skip self
        if url.rstrip("/") == self_url.rstrip("/"):
            continue
        # Idempotencia: skip si ya hay link a esta URL
        if url in linked_urls or body.find("a", href=url):
            linked_urls.add(url)
            continue

        css = _css_class_for(url)
        pattern = re.compile(rf'(?<!\w){re.escape(phrase)}(?!\w)',
                              re.IGNORECASE | re.UNICODE)
        text_nodes = body.find_all(string=pattern)
        for node in text_nodes:
            if not isinstance(node, NavigableString):
                continue
            if _is_in_anchor(node):
                continue
            parents = {p.name for p in node.parents if isinstance(p, Tag)}
            if parents & {"script", "style", "meta", "head", "nav", "title"}:
                continue
            if _inject_link(node, pattern, url, css):
                linked_urls.add(url)
                added += 1
                break

    # 2. Términos genéricos (resuelven con market)
    if market:
        for phrase, url_pattern in GENERIC_TERMS.items():
            url = url_pattern.format(market=market)
            if not _target_exists(url):
                continue
            if url.rstrip("/") == self_url.rstrip("/"):
                continue
            if url in linked_urls or body.find("a", href=url):
                linked_urls.add(url)
                continue
            css = "topic-link int-link"
            pattern = re.compile(rf'(?<!\w){re.escape(phrase)}(?!\w)',
                                  re.IGNORECASE | re.UNICODE)
            text_nodes = body.find_all(string=pattern)
            for node in text_nodes:
                if not isinstance(node, NavigableString):
                    continue
                if _is_in_anchor(node):
                    continue
                parents = {p.name for p in node.parents if isinstance(p, Tag)}
                if parents & {"script", "style", "meta", "head", "nav", "title"}:
                    continue
                if _inject_link(node, pattern, url, css):
                    linked_urls.add(url)
                    added += 1
                    break

    return added


def process_file(path: Path) -> int:
    market = _detect_market(path)
    self_url = _page_url(path)
    text = path.read_text(encoding="utf-8")
    soup = BeautifulSoup(text, "html.parser")
    n = linkify_soup(soup, market, self_url)
    if n > 0 and not DRY_RUN:
        path.write_text(str(soup), encoding="utf-8")
    return n


def main():
    mode = "[DRY-RUN]" if DRY_RUN else "[LIVE]"
    print(f"\nlinkify_master.py {mode}\n")
    print(f"  Registry: {len(REGISTRY)} entity phrases")
    print(f"  Generic terms: {len(GENERIC_TERMS)}")
    print()

    files = []
    if SPECIFIC_FILE:
        files = [SPECIFIC_FILE]
    else:
        for d in TARGET_DIRS:
            if d == "magazines":
                files.extend((ROOT / d).glob("*.html"))
            else:
                target = ROOT / d
                if target.exists():
                    files.extend(target.rglob("index.html"))

    total = total_files = 0
    for path in sorted(files):
        if not path.exists():
            continue
        n = process_file(path)
        if n > 0:
            total += n
            total_files += 1
            marker = "[DRY]" if DRY_RUN else "  ✅"
            print(f"  {marker} {path.relative_to(ROOT)}: +{n}")

    print(f"\n  Total: {total} links en {total_files} archivos")


if __name__ == "__main__":
    main()
