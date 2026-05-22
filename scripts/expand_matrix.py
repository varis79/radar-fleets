"""
Aplica una propuesta aprobada del detector a los YAML de la matriz.

Lee una propuesta JSON (formato del detector emerging-topics) y edita
content/pillar-matrix/topics.yml o subgeographies.yml correspondiente.

Uso:
    python -m scripts.expand_matrix --proposal-file proposal.json
    python -m scripts.expand_matrix --proposal-json '{"type":"new_topic",...}'
    python -m scripts.expand_matrix --proposal-file p.json --dry-run

Tipos soportados:
  - new_topic    → añade entrada a topics.yml
  - new_subgeo   → añade ciudad a subgeographies.yml para un market
  - gap          → no aplica cambio a YAML; el workflow lo trata como
                   "prioridad de generación" (no requiere expand)

Idempotente: si la entrada ya existe, no la duplica.
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import yaml

from scripts.lib.paths import ROOT

TOPICS_YML = ROOT / "content" / "pillar-matrix" / "topics.yml"
SUBGEOS_YML = ROOT / "content" / "pillar-matrix" / "subgeographies.yml"


def _add_new_topic(proposal: dict, dry: bool) -> dict:
    """Añade un topic nuevo al final de topics.yml."""
    slug = proposal["proposed_slug"]
    label = proposal.get("proposed_label_es", slug.replace("-", " ").capitalize())
    applies = proposal.get("applies_to_markets", ["mexico", "espana"])
    intents = proposal.get("intents", ["informational"])
    tier_mod = int(proposal.get("tier_modifier", 1))

    # Leer el YAML actual como texto (mantenemos comentarios y formato)
    text = TOPICS_YML.read_text(encoding="utf-8")

    # Comprobar idempotencia: ¿el slug ya existe?
    if f"  - code: {slug}\n" in text or f"- code: {slug}\n" in text:
        return {"status": "no-change", "reason": f"topic {slug} ya existe"}

    # Construir el bloque YAML del nuevo topic
    applies_str = json.dumps(applies, ensure_ascii=False)  # ["mexico", "espana"]
    intents_str = json.dumps(intents, ensure_ascii=False)  # ["informational"]
    block = f"""
  - code: {slug}
    slug_template: "{slug}-{{market_slug}}-{{year}}"
    label_template: "{label} en {{market_label}} {{year}}"
    applies_to_markets: {applies_str}
    intents: {intents_str}
    tier_modifier: {tier_mod}
    pulpopay_relevant: false
    notes: "Auto-añadido por detect_emerging_topics. Razón: {proposal.get('rationale', '')[:160]}"
"""

    # Insertar al final del archivo (antes del último newline si existe)
    new_text = text.rstrip() + "\n" + block

    if not dry:
        TOPICS_YML.write_text(new_text, encoding="utf-8")
    return {
        "status": "added" if not dry else "would-add",
        "file": str(TOPICS_YML.relative_to(ROOT)),
        "slug": slug,
        "applies_to_markets": applies,
        "intents": intents,
    }


def _add_new_subgeo(proposal: dict, dry: bool) -> dict:
    """Añade una ciudad a subgeographies.yml para un market."""
    market_code = proposal["market_code"]
    city_slug = proposal["proposed_city_slug"]
    city_label = proposal.get("proposed_city_label", city_slug.title())

    data = yaml.safe_load(SUBGEOS_YML.read_text(encoding="utf-8"))
    subgeos = data.get("subgeographies", {})
    market_data = subgeos.get(market_code)
    if market_data is None:
        return {"status": "error", "reason": f"market {market_code} no existe en subgeographies"}

    # Idempotencia
    existing_slugs = {c["slug"] for c in market_data.get("cities", [])}
    if city_slug in existing_slugs:
        return {"status": "no-change", "reason": f"ciudad {city_slug} ya existe"}

    # Añadir la ciudad
    market_data.setdefault("cities", []).append({
        "slug": city_slug,
        "label": city_label,
        "relevance": "medium",
    })

    if not dry:
        SUBGEOS_YML.write_text(
            yaml.safe_dump(data, allow_unicode=True, sort_keys=False, default_flow_style=False),
            encoding="utf-8",
        )
    return {
        "status": "added" if not dry else "would-add",
        "file": str(SUBGEOS_YML.relative_to(ROOT)),
        "market": market_code,
        "city_slug": city_slug,
    }


def apply_proposal(proposal: dict, dry: bool = False) -> dict:
    ptype = proposal.get("type")
    if ptype == "new_topic":
        return _add_new_topic(proposal, dry)
    elif ptype == "new_subgeo":
        return _add_new_subgeo(proposal, dry)
    elif ptype == "gap":
        # gap no requiere editar YAML; el workflow puede invocar al generador
        # con --slug específico desde la metadata del gap.
        return {"status": "no-change", "reason": "gap proposal does not require YAML expansion"}
    else:
        return {"status": "error", "reason": f"tipo desconocido: {ptype}"}


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--proposal-file", help="JSON file con la propuesta")
    p.add_argument("--proposal-json", help="JSON inline con la propuesta")
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args(argv)

    if args.proposal_file:
        proposal = json.loads(Path(args.proposal_file).read_text(encoding="utf-8"))
    elif args.proposal_json:
        proposal = json.loads(args.proposal_json)
    else:
        print("Error: pasa --proposal-file o --proposal-json")
        return 1

    # Si es un detector output completo, iterar propuestas
    if "proposals" in proposal:
        results = []
        for prop in proposal["proposals"]:
            results.append({"proposal": prop, "result": apply_proposal(prop, args.dry_run)})
        print(json.dumps({"applied": results}, ensure_ascii=False, indent=2))
    else:
        # Es una propuesta individual
        result = apply_proposal(proposal, args.dry_run)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
