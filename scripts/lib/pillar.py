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


# ─────────── Lógica de matriz ───────────

@dataclass
class PillarPage:
    """Una página pilar concreta (combinación market × topic × intent)."""
    market_code: str
    market_label: str
    market_slug: str
    topic_code: str
    intent_code: str
    slug: str                        # final URL slug
    label: str                       # título humano
    tier: int                        # 1, 2 ó 3
    schema_type: str                 # Article / HowTo / FAQPage
    review_days: int                 # cada cuánto revisar
    pulpopay_relevant: bool
    section_template: list[str] = field(default_factory=list)

    def url_path(self) -> str:
        """Devuelve el path relativo de la página en el sitio."""
        return f"/temas/{self.slug}/"

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


def enumerate_pages(only_active_markets: bool = True) -> list[PillarPage]:
    """Genera todas las páginas pilar válidas según las reglas de la matriz."""
    markets = load_markets()
    topics = load_topics()
    intents = load_intents()

    # Marcar cada intent dict con su key (utilidad)
    for k, v in intents.items():
        v["_key"] = k

    pages: list[PillarPage] = []

    for market in markets:
        if only_active_markets and not market.get("active", True):
            continue

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

                review_days = intent.get("review_days")
                if review_days is None:
                    review_days = REVIEW_DAYS_BY_TIER[tier]

                pages.append(PillarPage(
                    market_code=market["code"],
                    market_label=market["label"],
                    market_slug=market["slug"],
                    topic_code=topic["code"],
                    intent_code=intent_code,
                    slug=slug,
                    label=label,
                    tier=tier,
                    schema_type=intent["schema_type"],
                    review_days=int(review_days),
                    pulpopay_relevant=bool(topic.get("pulpopay_relevant", False)),
                    section_template=intent.get("section_template", []),
                ))

    return pages


# ─────────── Resumen / reporting ───────────

def summarize(pages: list[PillarPage]) -> dict[str, Any]:
    """Estadísticas sobre la matriz construida."""
    by_tier: dict[int, int] = {1: 0, 2: 0, 3: 0}
    by_market: dict[str, int] = {}
    by_topic: dict[str, int] = {}
    by_intent: dict[str, int] = {}
    pulpopay_count = 0

    for p in pages:
        by_tier[p.tier] += 1
        by_market[p.market_label] = by_market.get(p.market_label, 0) + 1
        by_topic[p.topic_code] = by_topic.get(p.topic_code, 0) + 1
        by_intent[p.intent_code] = by_intent.get(p.intent_code, 0) + 1
        if p.pulpopay_relevant:
            pulpopay_count += 1

    return {
        "total_pages": len(pages),
        "by_tier": by_tier,
        "by_market": dict(sorted(by_market.items(), key=lambda kv: -kv[1])),
        "by_topic": dict(sorted(by_topic.items(), key=lambda kv: -kv[1])),
        "by_intent": by_intent,
        "pulpopay_relevant": pulpopay_count,
        "review_schedule_days": REVIEW_DAYS_BY_TIER,
    }
