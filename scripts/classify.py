"""
Clasificación determinística de items.

Lee `content/raw/YYYY-WW-raw.jsonl`, etiqueta cada item con
{topic, market, fleet_type, micro_tags, players} usando los mapas
de `pipeline-config.yml`. No llama a LLM. Es trazable y barato.

Escribe `content/raw/YYYY-WW-classified.jsonl`.

Convenciones:
- Un item puede quedar sin topic explícito (topic=null). La selección
  posterior descartará items sin topic salvo que tengan player fuerte.
- Si un item matchea varios topics, el primero en orden de config gana,
  pero se conservan los alternativos en `topic_alt`.
- market se deriva por: (1) keywords del texto, (2) source_geo como fallback.
- fleet_type es opcional; muchos items no lo tendrán y está bien.
- players se detecta por coincidencia de nombre exacto en title+summary.
"""
from __future__ import annotations
import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

from scripts.lib.config import config
from scripts.lib.paths import RAW_DIR, iso_week_key


# Cargamos players desde taxonomy/players.md para detección simple.
# El formato esperado es: líneas que contengan "### <slug>" y luego "- Nombre: <Nombre>"
# como las secciones del archivo. Si algún player no matchea, simplemente no se detecta.
def load_players(players_md: Path) -> list[tuple[str, str, re.Pattern]]:
    """Devuelve [(slug, display_name, regex_compiled), ...]"""
    if not players_md.exists():
        return []
    text = players_md.read_text(encoding="utf-8")
    out = []
    current_slug = None
    for line in text.splitlines():
        if line.startswith("### "):
            current_slug = line[4:].strip()
            # Evitar títulos de secciones genéricas
            if " " in current_slug:
                current_slug = None
        elif current_slug and line.startswith("- Nombre:"):
            name = line.split(":", 1)[1].strip()
            # Quitar sufijos paréntesis tipo "Ayvens (ex LeasePlan + ALD)"
            base = re.sub(r"\s*\(.*?\)", "", name).strip()
            if not base:
                continue
            # Regex: palabra completa, case-insensitive
            rx = re.compile(rf"\b{re.escape(base)}\b", re.IGNORECASE)
            out.append((current_slug, base, rx))
            current_slug = None
    return out


def classify_one(item: dict, cfg: dict, players_db) -> dict:
    hay = f"{item.get('title', '')} {item.get('summary', '')}".lower()

    # topic
    topic_match: str | None = None
    topic_alt: list[str] = []
    for topic_slug, keywords in cfg["classification"]["topics"].items():
        for kw in keywords:
            if kw.lower() in hay:
                if topic_match is None:
                    topic_match = topic_slug
                elif topic_slug != topic_match and topic_slug not in topic_alt:
                    topic_alt.append(topic_slug)
                break
    # Si la fuente dio un hint explícito, úsalo como tiebreak si no hay match
    if topic_match is None and item.get("source_topic_hint"):
        topic_match = item["source_topic_hint"]

    # market: explícito por keywords, fallback source_geo
    market_match: str = item.get("source_geo", "global")
    for market_slug, keywords in cfg["classification"]["markets"].items():
        for kw in keywords:
            if kw.lower() in hay:
                market_match = market_slug
                break

    # fleet_type (opcional)
    fleet_type_match: str | None = None
    for ft_slug, keywords in cfg["classification"]["fleet_types"].items():
        for kw in keywords:
            if kw.lower() in hay:
                fleet_type_match = ft_slug
                break
        if fleet_type_match:
            break

    # players
    players: list[str] = []
    for slug, name, rx in players_db:
        if rx.search(hay):
            players.append(slug)

    # micro-tags simples: organismo, sigla
    micro_tags: list[str] = []
    sigla_map = [
        ("ELD", r"\beld\b"), ("FMCSA", r"\bfmcsa\b"), ("DGT", r"\bdgt\b"),
        ("BOE", r"\bboe\b"), ("DOF", r"\bdof\b"), ("CNE", r"\bcne\b"),
        ("SICT", r"\bsict\b"), ("ZBE", r"\bzbe\b"), ("ADAS", r"\badas\b"),
        ("MCS", r"\bmcs\b"), ("CCS", r"\bccs\b"),
    ]
    for sigla, rx in sigla_map:
        if re.search(rx, hay, re.IGNORECASE):
            micro_tags.append(f"sigla:{sigla}")

    return {
        **item,
        "topic": topic_match,
        "topic_alt": topic_alt,
        "market": market_match,
        "fleet_type": fleet_type_match,
        "players": players,
        "micro_tags": micro_tags,
    }


def classify(today: dt.date | None = None) -> dict:
    cfg = config()
    week = iso_week_key(today)
    in_path = RAW_DIR / f"{week}-raw.jsonl"
    out_path = RAW_DIR / f"{week}-classified.jsonl"
    if not in_path.exists():
        return {"error": f"no-raw-file", "expected": str(in_path)}

    from scripts.lib.paths import TAXONOMY_DIR
    players_db = load_players(TAXONOMY_DIR / "players.md")

    stats = {"total": 0, "with_topic": 0, "with_fleet_type": 0, "with_players": 0, "by_market": {}}
    with in_path.open(encoding="utf-8") as src, out_path.open("w", encoding="utf-8") as dst:
        for line in src:
            line = line.strip()
            if not line:
                continue
            item = json.loads(line)
            c = classify_one(item, cfg, players_db)
            dst.write(json.dumps(c, ensure_ascii=False) + "\n")
            stats["total"] += 1
            if c.get("topic"): stats["with_topic"] += 1
            if c.get("fleet_type"): stats["with_fleet_type"] += 1
            if c.get("players"): stats["with_players"] += 1
            m = c.get("market", "global")
            stats["by_market"][m] = stats["by_market"].get(m, 0) + 1

    return {"week": week, "path": str(out_path), **stats}


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--date", help="YYYY-MM-DD (default: hoy)")
    args = p.parse_args(argv)
    today = dt.date.fromisoformat(args.date) if args.date else None
    result = classify(today)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if "error" not in result else 1


if __name__ == "__main__":
    sys.exit(main())
