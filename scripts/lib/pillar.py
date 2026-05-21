"""
Long-tail pillar matrix · biblioteca base.

Lee `content/pillar-matrix/{markets,topics,intents}.yml`, cruza market × topic
× intent y devuelve la lista de páginas pilar que el sistema debe gestionar.

Decisiones:
- Las combinaciones se generan, NO se enumeran a mano. Esto evita inflar
  YAML con cientos de filas duplicadas.
- Cada combinación se etiqueta con su `tier` (1, 2, 3) calculado por
  `tier_for_page`. El tier determina el ciclo de vida: schedule de
  revisión, threshold de liberación noindex→index, prioridad de
  generación inicial.
- Año actual hardcoded como `2026` por ahora; cuando llegue 2027 se
  abrirá un PR para regenerar slugs (mantenemos 301 desde slugs viejos).
- NO hace llamadas LLM aquí. SEO-3.1 es solo estructura + enumeración.
  La generación de contenido viene en SEO-3.2.

Uso programático:
    from scripts.lib.pillar import enumerate_pages, summarize
    pages = enumerate_pages()
    print(summarize(pages))
"""
from __future__ import annotations
import datetime as dt
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from scripts.lib.paths import ROOT

PILLAR_DIR = ROOT / "content" / "pillar-matrix"
PAGES_DIR = ROOT / "content" / "pillar-matrix" / "pages"
DATA_OVERRIDES_DIR = ROOT / "content" / "pillar-matrix" / "data-overrides"

CURRENT_YEAR = 2026   # cuando cambie, abrir PR para regenerar slugs

REVIEW_DAYS_BY_TIER = {1: 30, 2: 60, 3: 90}


# ─────────── Carga YAML ───────────

def load_markets() -> list[dict]:
    with open(PILLAR_DIR / "markets.yml", encoding="utf-8") as f:
        return yaml.safe_load(f)["markets"]


def load_topics() -> list[dict]:
    with open(PILLAR_DIR / "topics.yml", encoding="utf-8") as f:
        return yaml.safe_load(f)["topics"]


def load_intents() -> dict[str, dict]:
    with open(PILLAR_DIR / "intents.yml", encoding="utf-8") as f:
        return yaml.safe_load(f)["intents"]


def load_use_cases() -> list[dict]:
    with open(PILLAR_DIR / "use-cases.yml", encoding="utf-8") as f:
        return yaml.safe_load(f)["use_cases"]


def load_verticals() -> list[dict]:
    with open(PILLAR_DIR / "verticals.yml", encoding="utf-8") as f:
        return yaml.safe_load(f)["verticals"]


def load_subgeographies() -> dict[str, dict]:
    with open(PILLAR_DIR / "subgeographies.yml", encoding="utf-8") as f:
        return yaml.safe_load(f)["subgeographies"]


# ─────────── Lógica de matriz ───────────

@dataclass
class PillarPage:
    """Una página pilar concreta (combinación de dimensiones)."""
    dimension: str                   # "topic" | "use-case" | "vertical" | "subgeo"
    market_code: str
    market_label: str
    market_slug: str
    topic_code: str                  # topic, use_case_code, vertical_code o subgeo
    intent_code: str
    slug: str                        # final URL slug
    label: str                       # título humano
    tier: int                        # 1, 2 ó 3
    schema_type: str                 # Article / HowTo / FAQPage
    review_days: int                 # cada cuánto revisar
    pulpopay_relevant: bool
    section_template: list[str] = field(default_factory=list)
    # Refs útiles para SEO-3.2 (sin uso aún en 3.1)
    metadata: dict = field(default_factory=dict)

    def url_path(self) -> str:
        """Devuelve el path relativo de la página en el sitio.
        Cada dimensión vive en su propio directorio para SEO y arquitectura clara."""
        prefix = {
            "topic":     "/temas/",
            "use-case":  "/casos-uso/",
            "vertical":  "/sectores/",
            "subgeo":    "/ciudades/",
        }.get(self.dimension, "/temas/")
        return f"{prefix}{self.slug}/"

    def file_path(self) -> Path:
        """Devuelve la ruta del .md que la representa en el repo."""
        return PAGES_DIR / f"{self.slug}.md"


def applies_to_market(topic: dict, market_code: str) -> bool:
    """¿Este topic aplica a este mercado según topics.yml?"""
    a = topic.get("applies_to_markets", "*")
    if a == "*":
        return True
    if isinstance(a, list):
        if a and isinstance(a[0], str) and a[0].startswith("exclude:"):
            excluded = {item.removeprefix("exclude:") for item in a}
            return market_code not in excluded
        return market_code in a
    return False


def tier_for_page(market: dict, topic: dict, intent_code: str) -> int:
    """Calcula el tier final de una página.
    Reglas:
      base = market.tier_default
      + topic.tier_modifier (positivo = degrada)
      capped a [1, 3]
    Excepciones:
      - Mercados Tier 1 (mexico, espana) con topic core → siempre T1.
      - Mercados Tier 1 con topic muy específico (tier_modifier > 1) → T2.
    """
    base = int(market.get("tier_default", 3))
    mod = int(topic.get("tier_modifier", 0))
    tier = base + mod

    # Excepción: market T1 con topic core (mod=0) siempre T1
    if base == 1 and mod == 0:
        tier = 1

    return max(1, min(3, tier))


def build_slug(topic: dict, market: dict, intent: dict) -> str:
    template = topic["slug_template"]
    base = template.format(
        market_slug=market["slug"],
        year=CURRENT_YEAR,
    )
    # Sufijo de intent (si no informational)
    suffix = intent.get("slug_suffix", "")
    if suffix:
        # Insertar ANTES del año
        # ej. "telematica-flotas-mexico-2026" + "-comparativa"
        # → "telematica-flotas-mexico-comparativa-2026"
        base = base.replace(f"-{CURRENT_YEAR}", f"{suffix}-{CURRENT_YEAR}")
    return base


def build_label(topic: dict, market: dict, intent: dict) -> str:
    base = topic["label_template"].format(
        market_label=market["label"],
        year=CURRENT_YEAR,
    )
    # Append intent label discreto al título (afecta SEO, ayuda CTR)
    intent_code = intent_key_of(intent)
    if intent_code == "comparativo":
        base = base + " · comparativa"
    elif intent_code == "regulatorio":
        base = base + " · regulación y obligaciones"
    elif intent_code == "guia-practica":
        base = base + " · guía"
    return base


def intent_key_of(intent: dict) -> str:
    """Helper para encontrar la key de un intent dict."""
    return intent.get("_key", "")


def _market_active(market: dict, only_active: bool) -> bool:
    return market.get("active", True) or not only_active


def enumerate_topic_pages(markets, topics, intents) -> list[PillarPage]:
    """Dimensión 1: market × topic × intent (la matriz original)."""
    pages = []
    for market in markets:
        for topic in topics:
            if not applies_to_market(topic, market["code"]):
                continue
            for intent_code in topic.get("intents", ["informational"]):
                intent = intents.get(intent_code)
                if not intent:
                    continue
                tier = tier_for_page(market, topic, intent_code)
                slug = build_slug(topic, market, intent)
                label = build_label(topic, market, intent)
                review_days = intent.get("review_days") or REVIEW_DAYS_BY_TIER[tier]
                pages.append(PillarPage(
                    dimension="topic",
                    market_code=market["code"], market_label=market["label"], market_slug=market["slug"],
                    topic_code=topic["code"], intent_code=intent_code,
                    slug=slug, label=label, tier=tier,
                    schema_type=intent["schema_type"], review_days=int(review_days),
                    pulpopay_relevant=bool(topic.get("pulpopay_relevant", False)),
                    section_template=intent.get("section_template", []),
                ))
    return pages


def enumerate_use_case_pages(markets, use_cases, intents) -> list[PillarPage]:
    """Dimensión 2: use_case × market × intent (informational + guía).
    Cada use case se aplica a TODOS los mercados activos (con tier modulado
    por mercado). PulpoPay relevance derivado de product_priority."""
    pages = []
    intents_for_use_case = ["informational", "guia-practica"]
    for uc in use_cases:
        pp_relevant = uc.get("product_priority") in ("pulpopay", "both")
        for market in markets:
            for intent_code in intents_for_use_case:
                intent = intents.get(intent_code)
                if not intent:
                    continue
                # Tier: base del mercado + tier_modifier del use case
                tier = max(1, min(3, int(market.get("tier_default", 3)) + int(uc.get("tier_modifier", 0))))
                base = f"flota-{uc['code']}-{market['slug']}-{CURRENT_YEAR}"
                suffix = intent.get("slug_suffix", "")
                if suffix:
                    base = base.replace(f"-{CURRENT_YEAR}", f"{suffix}-{CURRENT_YEAR}")
                label = f"{uc['label']} en {market['label']} {CURRENT_YEAR}"
                if intent_code == "guia-practica":
                    label += " · guía"
                review_days = intent.get("review_days") or REVIEW_DAYS_BY_TIER[tier]
                pages.append(PillarPage(
                    dimension="use-case",
                    market_code=market["code"], market_label=market["label"], market_slug=market["slug"],
                    topic_code=uc["code"], intent_code=intent_code,
                    slug=base, label=label, tier=tier,
                    schema_type=intent["schema_type"], review_days=int(review_days),
                    pulpopay_relevant=pp_relevant,
                    section_template=intent.get("section_template", []),
                    metadata={"product_priority": uc.get("product_priority", "")},
                ))
    return pages


def enumerate_vertical_pages(markets, verticals, intents) -> list[PillarPage]:
    """Dimensión 3: vertical × market (informational solo).
    Sectores de industria que cubre Pulpo."""
    pages = []
    intent_code = "informational"
    intent = intents.get(intent_code, {})
    for v in verticals:
        for market in markets:
            tier = max(1, min(3, int(market.get("tier_default", 3)) + int(v.get("tier_modifier", 0))))
            slug = f"flotas-{v['code']}-{market['slug']}-{CURRENT_YEAR}"
            label = f"Flotas en {v['label']} en {market['label']} {CURRENT_YEAR}"
            review_days = REVIEW_DAYS_BY_TIER[tier]
            pages.append(PillarPage(
                dimension="vertical",
                market_code=market["code"], market_label=market["label"], market_slug=market["slug"],
                topic_code=v["code"], intent_code=intent_code,
                slug=slug, label=label, tier=tier,
                schema_type=intent.get("schema_type", "Article"), review_days=int(review_days),
                pulpopay_relevant=False,
                section_template=intent.get("section_template", []),
                metadata={"typical_use_cases": v.get("typical_use_cases", [])},
            ))
    return pages


def enumerate_subgeo_pages(markets, topics, subgeos, intents) -> list[PillarPage]:
    """Dimensión 4: ciudad × topic (informational solo, mercado heredado).
    Solo para mercados grandes con subgeografía definida."""
    pages = []
    intent_code = "informational"
    intent = intents.get(intent_code, {})
    markets_by_code = {m["code"]: m for m in markets}
    topics_by_code = {t["code"]: t for t in topics}

    for market_code, sg_data in subgeos.items():
        market = markets_by_code.get(market_code)
        if not market:
            continue
        applicable_topics = sg_data.get("topics_applicable", [])
        for city in sg_data.get("cities", []):
            for topic_code in applicable_topics:
                topic = topics_by_code.get(topic_code)
                if not topic:
                    continue
                # Tier para ciudad: base + 1 (porque es más nicho) + relevance modifier
                rel_modifier = {"high": 0, "medium": 1, "low": 2}.get(city.get("relevance", "medium"), 1)
                tier = max(1, min(3, int(market.get("tier_default", 3)) + rel_modifier))
                # Evitamos duplicar "flotas-flotas" si el topic_code ya termina así.
                base = topic_code if topic_code.endswith("-flotas") else f"{topic_code}-flotas"
                slug = f"{base}-{city['slug']}-{CURRENT_YEAR}"
                label = f"{topic['label_template'].split(' en ')[0].split('para flotas')[0].strip()} para flotas en {city['label']} ({market['label']}) {CURRENT_YEAR}"
                review_days = REVIEW_DAYS_BY_TIER[tier]
                pages.append(PillarPage(
                    dimension="subgeo",
                    market_code=market["code"], market_label=market["label"], market_slug=market["slug"],
                    topic_code=topic_code, intent_code=intent_code,
                    slug=slug, label=label, tier=tier,
                    schema_type="Article", review_days=int(review_days),
                    pulpopay_relevant=bool(topic.get("pulpopay_relevant", False)),
                    section_template=intent.get("section_template", []),
                    metadata={"city_slug": city["slug"], "city_label": city["label"]},
                ))
    return pages


def enumerate_pages(only_active_markets: bool = True) -> list[PillarPage]:
    """Genera todas las páginas pilar válidas cruzando 4 dimensiones:
    - topic × market × intent (la matriz original)
    - use_case × market × intent
    - vertical × market
    - subgeography × topic
    """
    markets_all = load_markets()
    markets = [m for m in markets_all if _market_active(m, only_active_markets)]
    topics = load_topics()
    intents = load_intents()
    use_cases = load_use_cases()
    verticals = load_verticals()
    subgeos = load_subgeographies()

    # Marcar cada intent con su key
    for k, v in intents.items():
        v["_key"] = k

    pages: list[PillarPage] = []
    pages.extend(enumerate_topic_pages(markets, topics, intents))
    pages.extend(enumerate_use_case_pages(markets, use_cases, intents))
    pages.extend(enumerate_vertical_pages(markets, verticals, intents))
    pages.extend(enumerate_subgeo_pages(markets, topics, subgeos, intents))
    return pages


# ─────────── Resumen / reporting ───────────

def summarize(pages: list[PillarPage]) -> dict[str, Any]:
    """Estadísticas sobre la matriz construida."""
    by_tier: dict[int, int] = {1: 0, 2: 0, 3: 0}
    by_market: dict[str, int] = {}
    by_topic: dict[str, int] = {}
    by_intent: dict[str, int] = {}
    by_dimension: dict[str, int] = {}
    pulpopay_count = 0

    for p in pages:
        by_tier[p.tier] += 1
        by_market[p.market_label] = by_market.get(p.market_label, 0) + 1
        by_topic[p.topic_code] = by_topic.get(p.topic_code, 0) + 1
        by_intent[p.intent_code] = by_intent.get(p.intent_code, 0) + 1
        by_dimension[p.dimension] = by_dimension.get(p.dimension, 0) + 1
        if p.pulpopay_relevant:
            pulpopay_count += 1

    return {
        "total_pages": len(pages),
        "by_dimension": by_dimension,
        "by_tier": by_tier,
        "by_market": dict(sorted(by_market.items(), key=lambda kv: -kv[1])),
        "by_topic": dict(sorted(by_topic.items(), key=lambda kv: -kv[1])),
        "by_intent": by_intent,
        "pulpopay_relevant": pulpopay_count,
        "review_schedule_days": REVIEW_DAYS_BY_TIER,
    }
