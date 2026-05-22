"""
Detector de temas emergentes y huecos en la matriz.

Lee headlines de las últimas N semanas (de content/raw/*-dedup.jsonl)
y pide a Claude que detecte:
  - Tipo A: temas emergentes NO en la matriz (proponen nuevo topic)
  - Tipo B: ciudades emergentes NO en subgeographies.yml
  - Tipo C: huecos en combinaciones market × topic ya en la matriz

Output: JSON con propuestas. El workflow GitHub Actions abre un Issue
por cada propuesta para que Varis apruebe con /approve o /reject.

Uso:
    python -m scripts.detect_emerging_topics --weeks 12
    python -m scripts.detect_emerging_topics --weeks 8 --dry-run     # sin LLM
    python -m scripts.detect_emerging_topics --output proposals.json
"""
from __future__ import annotations
import argparse
import datetime as dt
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import yaml

from scripts.lib.paths import ROOT, RAW_DIR
from scripts.lib.config import config
from scripts.lib.pillar import (
    load_topics, load_subgeographies, load_markets,
)


PROMPT_PATH = ROOT / "prompts" / "emerging-topics-prompt.md"


def load_recent_headlines(weeks: int) -> list[dict]:
    """Lee las últimas N semanas de content/raw/*-dedup.jsonl y devuelve
    [{title, summary, topic, market, published_iso, source_name}, ...]."""
    if not RAW_DIR.exists():
        return []
    files = sorted(RAW_DIR.glob("*-dedup.jsonl"))
    # Filtrar las últimas N
    files = files[-weeks:] if len(files) > weeks else files

    headlines: list[dict] = []
    for f in files:
        with f.open(encoding="utf-8") as fh:
            for line in fh:
                if not line.strip():
                    continue
                try:
                    item = json.loads(line)
                except Exception:
                    continue
                # Si dedup.jsonl no tiene topic clasificado, leer del classified
                # (los archivos *-classified.jsonl están más arriba en el flow)
                headlines.append({
                    "title": item.get("title", "")[:200],
                    "summary": (item.get("summary", "") or "")[:300],
                    "topic": item.get("topic"),
                    "market": item.get("market"),
                    "source_name": item.get("source_name", ""),
                })
    return headlines


def load_classified_topics(weeks: int) -> list[dict]:
    """Fallback: si dedup no tiene topic, lee del classified.jsonl."""
    files = sorted(RAW_DIR.glob("*-classified.jsonl"))
    files = files[-weeks:] if len(files) > weeks else files
    headlines: list[dict] = []
    for f in files:
        with f.open(encoding="utf-8") as fh:
            for line in fh:
                if not line.strip():
                    continue
                try:
                    item = json.loads(line)
                except Exception:
                    continue
                headlines.append({
                    "title": item.get("title", "")[:200],
                    "summary": (item.get("summary", "") or "")[:300],
                    "topic": item.get("topic"),
                    "market": item.get("market"),
                    "source_name": item.get("source_name", ""),
                })
    return headlines


def existing_topic_codes() -> list[str]:
    return [t["code"] for t in load_topics()]


def existing_subgeos_flat() -> list[dict]:
    """Devuelve [{market_code, city_slug}, ...]."""
    out = []
    sg = load_subgeographies()
    for market_code, data in sg.items():
        for city in data.get("cities", []):
            out.append({"market_code": market_code, "city_slug": city["slug"]})
    return out


def active_market_codes() -> list[str]:
    return [m["code"] for m in load_markets() if m.get("active", True)]


def build_user_prompt(headlines: list[dict]) -> str:
    cfg = config()
    forbidden = cfg.get("selection", {}).get("competitor_blacklist", [])

    lines = []
    lines.append("## Existing matrix\n")
    lines.append(f"- existing_topics: {existing_topic_codes()}")
    lines.append(f"- existing_markets: {active_market_codes()}")
    lines.append(f"- existing_subgeos: {existing_subgeos_flat()}\n")
    lines.append(f"## Competidores prohibidos (NO usar como topic)\n")
    lines.append(f"{', '.join(forbidden)}\n")
    lines.append(f"## Headlines de las últimas semanas ({len(headlines)} items)\n")
    for i, h in enumerate(headlines[:500], 1):  # cap a 500 para no inflar tokens
        market = h.get("market") or "?"
        topic = h.get("topic") or "null"
        lines.append(f"{i}. [{market} / topic={topic}] {h['title']}")
    lines.append("\n## Tu output")
    lines.append("Responde SOLO con el JSON pedido en el system prompt. Sé conservador.")
    return "\n".join(lines)


def call_llm(system_prompt: str, user_prompt: str) -> dict:
    try:
        import anthropic
    except ImportError:
        raise RuntimeError("anthropic SDK no instalado")

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY no configurada")

    client = anthropic.Anthropic(api_key=api_key)
    cfg = config()
    model = cfg.get("compose", {}).get("model_primary", "claude-opus-4-1-20250805")

    resp = client.messages.create(
        model=model,
        max_tokens=3000,
        temperature=0.3,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    )
    text = resp.content[0].text

    m = re.search(r"```json\s*(\{.+?\})\s*```", text, flags=re.DOTALL)
    if not m:
        text = text.strip()
        if text.startswith("{"):
            return json.loads(text)
        raise ValueError(f"No JSON en respuesta:\n{text[:500]}")
    return json.loads(m.group(1))


def stub_proposals() -> dict:
    """Stub para dry-run."""
    return {
        "analysis_summary": "STUB. En modo --dry-run no se llama al LLM. Output de ejemplo.",
        "proposals": [
            {
                "type": "new_topic",
                "proposed_slug": "hidrogeno-verde-flotas",
                "proposed_label_es": "Hidrógeno verde para flotas",
                "applies_to_markets": ["mexico", "espana", "usa", "latam"],
                "intents": ["informational", "guia-practica"],
                "tier_modifier": 1,
                "rationale": "STUB: 6 headlines sobre H2 verde, fuel cells, FCEV en MX/ES/USA. Tema emergente sin slot.",
                "example_headlines": [
                    "STUB headline 1",
                    "STUB headline 2",
                    "STUB headline 3",
                ],
            },
        ],
    }


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--weeks", type=int, default=12,
                   help="Cuántas semanas hacia atrás analizar (default 12).")
    p.add_argument("--dry-run", action="store_true",
                   help="Usa stub. No llama al LLM.")
    p.add_argument("--output", help="Path para guardar el JSON de propuestas")
    args = p.parse_args(argv)

    print(f"Cargando headlines de las últimas {args.weeks} semanas…")
    # Preferimos classified.jsonl porque tiene topic asignado
    headlines = load_classified_topics(args.weeks)
    if not headlines:
        # Fallback: dedup
        headlines = load_recent_headlines(args.weeks)
    print(f"  {len(headlines)} headlines recolectados.")

    if not headlines:
        print("⚠️ Sin headlines. ¿Hay ediciones publicadas?")
        return 1

    if args.dry_run or not os.environ.get("ANTHROPIC_API_KEY"):
        print("(dry-run o sin ANTHROPIC_API_KEY: usando stub)")
        result = stub_proposals()
    else:
        system_prompt = PROMPT_PATH.read_text(encoding="utf-8")
        user_prompt = build_user_prompt(headlines)
        print(f"Llamando a LLM…")
        result = call_llm(system_prompt, user_prompt)

    n_proposals = len(result.get("proposals", []))
    print(f"\n📊 Análisis: {result.get('analysis_summary', '(sin summary)')}")
    print(f"📋 Propuestas: {n_proposals}")
    for prop in result.get("proposals", []):
        ptype = prop.get("type", "?")
        if ptype == "new_topic":
            print(f"   · [new_topic] {prop.get('proposed_slug')} — {prop.get('proposed_label_es')}")
        elif ptype == "new_subgeo":
            print(f"   · [new_subgeo] {prop.get('market_code')} / {prop.get('proposed_city_slug')}")
        elif ptype == "gap":
            print(f"   · [gap] {prop.get('market_code')} × {prop.get('topic_code')}")

    out_payload = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(out_payload, encoding="utf-8")
        print(f"\nGuardado en {args.output}")
    else:
        print(f"\n--- JSON ---\n{out_payload}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
