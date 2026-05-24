#!/usr/bin/env python3
"""
rotate_facts.py — Inyecta caja "💡 Sabías qué" rotatoria con pool de 137+
facts, filtrada por mercado y categoría de cada página.

Cada página recibe el fact más relevante a su tema/mercado, rotando cada
semana basado en (isoweek + page_hash) para que el contenido cambie pero
sea consistente dentro de la misma semana.

Inputs:
  - content/sabias-que-pool.json (compilado desde sabias-que-pool.md
    por scripts/build_facts_json.py)

Cobertura:
  - Pillars (temas/, mercados/, casos-uso/, sectores/, ciudades/)
  - Home (index.html)
  - Archive (archive.html)
  - Magazines (magazines/*.html)
  - Páginas con `<aside class="did-you-know">` existente se actualizan;
    si no existe se inyecta tras la primera sección de contenido

Filtrado:
  - Detecta market de la página (mexico/espana/latam/etc) por path
  - Detecta categorías/topics relevantes por URL slug + h1
  - Prefiere facts cuyo market y categoría coinciden con la página
  - Fallback a facts globales o de cualquier categoría

Idempotente dentro de la misma semana.

Uso:
    python3 scripts/rotate_facts.py [--dry-run]
"""
import sys
import json
import re
import hashlib
import datetime as dt
from pathlib import Path
from bs4 import BeautifulSoup, Tag

DRY_RUN = "--dry-run" in sys.argv
ROOT = Path(__file__).parent.parent
POOL_JSON = ROOT / "content/sabias-que-pool.json"


# ── Categoría → keywords para detectar topic de página ──
CATEGORY_KEYWORDS = {
    "⛽ Combustible": ["combustible", "fuel", "tarjetas", "diesel", "gasoil", "gasolin",
                       "tarjetas-flota", "control-gasto"],
    "📡 Telemática": ["telemat", "gps", "rastreo", "tracking", "monitoreo", "fleet-management",
                       "gestion-flota"],
    "⚖️ Regulación España": ["dgt", "itv", "zbe", "tacografo", "v-16", "tacógrafo", "espana",
                              "compliance-espana", "compliance-flotas-espana"],
    "⚖️ Regulación México": ["sict", "cne", "t-mec", "tmec", "carta-porte", "nom-012",
                              "compliance-mexico", "compliance-flotas-mexico"],
    "⚡ Electrificación": ["electric", "ev", "bev", "phev", "carga", "olinia", "moves"],
    "🔧 Mantenimiento": ["mantenimiento", "neumatic", "lubric", "preventivo", "correctivo"],
    "🛡️ Compliance": ["compliance", "infraccion", "multa", "sancion", "tacografo"],
    "🚨 Seguridad": ["seguridad", "robo", "cargo-theft", "siniestralidad", "accidente",
                     "fatalidad", "fatal"],
    "📦 Última milla": ["ultima-milla", "reparto", "ecommerce", "delivery", "lastmile",
                        "distribucion-urban"],
    "🚛 Renting & Leasing": ["renting", "leasing", "arrendamiento"],
    "🏭 Sectores verticales": ["sector", "alimentacion", "farmaceutic", "retail",
                                "construccion", "ecommerce", "telecom", "utilities"],
    "🌎 Geopolítica": ["t-mec", "tmec", "nearshoring", "brexit", "comercio-exterior", "ets2"],
    "🚢 Logística": ["puerto", "ferrocarril", "peaje", "corredor"],
    "💼 Operadores": ["dhl", "fedex", "ups", "amazon", "3pl", "operador"],
    "🏢 Gestión de flotas": ["gestion-flota", "fleet-management", "control-gasto"],
}

MARKET_KEYWORDS = {
    "mexico": ["mexico", "-mx-", "cdmx", "guadalajara", "monterrey", "tijuana", "manzanillo",
               "cuautitlan", "veracruz", "altamira", "leon", "merida", "puebla", "queretaro",
               "lazaro-cardenas", "nuevo-laredo", "toluca", "sict", "cne", "t-mec"],
    "espana": ["espana", "spain", "europa", "madrid", "barcelona", "valencia", "sevilla",
               "bilbao", "zaragoza", "malaga", "vigo", "dgt", "baliza", "v16", "tacografo",
               "zbe", "itv"],
    "colombia": ["colombia", "bogota", "medellin", "cali", "barranquilla"],
    "chile": ["chile", "santiago", "valparaiso"],
    "argentina": ["argentina", "buenos-aires"],
    "peru": ["peru", "lima"],
    "usa": ["usa", "estados-unidos"],
    "uk": ["uk", "london", "reino-unido"],
    "europa": ["europa", "europe", "eu-", "moves"],
}


def load_pool() -> list[dict]:
    if not POOL_JSON.exists():
        print(f"❌ {POOL_JSON} no existe. Corre primero: python3 scripts/build_facts_json.py")
        return []
    data = json.loads(POOL_JSON.read_text(encoding="utf-8"))
    return data.get("facts", [])


def detect_market(path: Path) -> str | None:
    s = str(path).lower()
    for market, kws in MARKET_KEYWORDS.items():
        if any(kw in s for kw in kws):
            return market
    return None


def detect_categories(path: Path, soup: BeautifulSoup) -> list[str]:
    """Devuelve categorías candidatas ordenadas por relevancia."""
    s = str(path).lower()
    h1 = soup.find("h1")
    h1_text = h1.get_text(" ", strip=True).lower() if h1 else ""
    title = soup.find("title")
    title_text = title.get_text(" ", strip=True).lower() if title else ""
    haystack = f"{s} {h1_text} {title_text}"

    matched = []
    for cat, kws in CATEGORY_KEYWORDS.items():
        for kw in kws:
            if kw in haystack:
                matched.append(cat)
                break  # 1 match por categoría es suficiente
    return matched


def filter_candidates(facts: list[dict], market: str | None,
                       categories: list[str]) -> list[dict]:
    """Devuelve facts relevantes para la página, ordenados por score."""
    scored = []
    for f in facts:
        score = 0
        # Match de categoría: +3 por cada match
        if f["categoria"] in categories:
            score += 3
        elif categories and not f["categoria"]:
            score += 0
        # Market match: +2 si la página tiene un market y el fact lo cubre
        f_markets = [m.lower() for m in f.get("markets", [])]
        if market and market in f_markets:
            score += 2
        elif "global" in f_markets or not f_markets:
            score += 1
        # Confidence bonus
        if f["confidence"] == "high-cross":
            score += 1
        # Evergreen bonus
        score += int(f.get("evergreen_score", 3)) * 0.1
        if score > 0:
            scored.append((score, f))

    scored.sort(key=lambda x: -x[0])
    return [f for _, f in scored]


def pick_fact(facts: list[dict], page_url: str, today: dt.date) -> dict | None:
    """Selecciona el fact final con rotación semanal por hash."""
    if not facts:
        return None
    iso_year, iso_week, _ = today.isocalendar()
    page_hash = int(hashlib.sha1(page_url.encode()).hexdigest(), 16)
    idx = (iso_week + page_hash) % len(facts)
    return facts[idx]


def format_box(fact: dict) -> str:
    cat = fact.get("categoria", "💡 Fleet Radar")
    text = fact["fact"]
    # Encode entities mínimas para HTML
    text_safe = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return (
        f'<aside class="did-you-know">'
        f'<span class="dyk-eyebrow">💡 Sabías qué · {cat}</span>'
        f'<p class="dyk-body">{text_safe}</p>'
        f'</aside>'
    )


def process_file(path: Path, facts: list[dict], today: dt.date) -> bool:
    text = path.read_text(encoding="utf-8")
    soup = BeautifulSoup(text, "html.parser")

    market = detect_market(path)
    categories = detect_categories(path, soup)
    candidates = filter_candidates(facts, market, categories)
    # Si no hay candidatos relevantes, usa todo el pool
    if not candidates:
        candidates = facts

    page_url = "/" + str(path.relative_to(ROOT)).replace("/index.html", "/")
    fact = pick_fact(candidates, page_url, today)
    if fact is None:
        return False

    new_html = format_box(fact)
    new_soup = BeautifulSoup(new_html, "html.parser")
    new_box = new_soup.find("aside")

    existing = soup.find("aside", class_="did-you-know")
    if existing:
        if existing.get_text(" ", strip=True) == new_box.get_text(" ", strip=True):
            return False  # mismo fact, no tocar
        existing.replace_with(new_box)
    else:
        # Inyectar tras .pillar-body o equivalente
        anchor = (soup.find(class_="pillar-body") or soup.find(class_="mkt-main")
                  or soup.find(class_="pillar-section") or soup.find(class_="e-body")
                  or soup.find("section") or soup.find("main"))
        if anchor is None:
            return False
        anchor.insert_after(new_box)

    if not DRY_RUN:
        path.write_text(str(soup), encoding="utf-8")
    return True


def main():
    today = dt.date.today()
    iso_year, iso_week, _ = today.isocalendar()
    mode = "[DRY-RUN]" if DRY_RUN else "[LIVE]"
    print(f"\nrotate_facts.py {mode}  today={today.isoformat()} (W{iso_week})\n")

    facts = load_pool()
    print(f"  Pool de facts: {len(facts)}")

    files = []
    # Pillars y hubs editoriales — caja ESTÁTICA semanal (señal SEO de freshness)
    for section in ("temas", "mercados", "casos-uso", "sectores", "ciudades",
                    "corredores", "players", "evergreen"):
        d = ROOT / section
        if d.exists():
            files.extend(sorted(d.rglob("index.html")))
    # about también recibe caja estática
    p = ROOT / "about/index.html"
    if p.exists() and p not in files:
        files.append(p)
    # NOTA: home, archive, magazines NO entran aquí. Reciben 2 cajas
    # DINÁMICAS (cargan facts random en cada recarga vía JS desde
    # /assets/sabias-que.json). Ver scripts/inject_dynamic_dyk.py.

    touched = 0
    by_cat = {}
    by_market = {}
    for path in files:
        if process_file(path, facts, today):
            touched += 1
            # tracking de cobertura
            soup = BeautifulSoup(path.read_text(), "html.parser")
            box = soup.find("aside", class_="did-you-know")
            if box:
                eyebrow = box.find(class_="dyk-eyebrow")
                if eyebrow:
                    cat = eyebrow.get_text(strip=True)
                    by_cat[cat] = by_cat.get(cat, 0) + 1
            mkt = detect_market(path)
            if mkt:
                by_market[mkt] = by_market.get(mkt, 0) + 1

    print(f"\n  Total cajas actualizadas: {touched} / {len(files)}")
    print(f"\n  Por mercado (páginas tocadas):")
    for m, n in sorted(by_market.items(), key=lambda x: -x[1]):
        print(f"    {m:15} {n}")


if __name__ == "__main__":
    main()
