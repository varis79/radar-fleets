"""
Deduplicación simple de items clasificados.

Estrategia:
 1. URL canónica idéntica -> mismo hecho (aunque el título varíe ligeramente).
 2. Si URLs distintas pero títulos normalizados muy similares
    (SequenceMatcher >= threshold) y comparten topic + market y el mismo day,
    se funden.

Conserva la primera aparición como primaria; las duplicadas se añaden como
`merged_from`. No se pierde información, solo se reduce ruido.

Lee  content/raw/YYYY-WW-classified.jsonl
Escribe content/raw/YYYY-WW-dedup.jsonl
"""
from __future__ import annotations
import argparse
import datetime as dt
import json
import re
import sys
from difflib import SequenceMatcher

from scripts.lib.config import config
from scripts.lib.paths import RAW_DIR, iso_week_key


def normalize_title(t: str, strip_fragments: list[str]) -> str:
    t = (t or "").lower()
    for frag in strip_fragments:
        t = t.replace(frag.lower(), "")
    # Quitar puntuación básica
    t = re.sub(r"[^\w\sáéíóúñü]", " ", t, flags=re.UNICODE)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def similarity(a: str, b: str) -> float:
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a, b).ratio()


def dedupe(today: dt.date | None = None) -> dict:
    cfg = config()
    dedupe_cfg = cfg.get("dedupe", {})
    threshold = float(dedupe_cfg.get("title_similarity_threshold", 0.82))
    strip_frags = dedupe_cfg.get("strip_from_title", [])

    week = iso_week_key(today)
    in_path = RAW_DIR / f"{week}-classified.jsonl"
    out_path = RAW_DIR / f"{week}-dedup.jsonl"
    if not in_path.exists():
        return {"error": "no-classified-file", "expected": str(in_path)}

    items = []
    with in_path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                items.append(json.loads(line))

    # Index por URL
    by_url: dict[str, dict] = {}
    for it in items:
        u = it.get("link", "").strip().lower()
        if not u:
            continue
        if u in by_url:
            # mismo link → fundir
            by_url[u].setdefault("merged_from", []).append(it["id"])
        else:
            by_url[u] = {**it, "merged_from": []}

    # Fase 2: fusión por similitud de título dentro del mismo topic+market
    items_list = list(by_url.values())
    for i, a in enumerate(items_list):
        if a.get("_merged"):
            continue
        ta = normalize_title(a.get("title", ""), strip_frags)
        for j in range(i + 1, len(items_list)):
            b = items_list[j]
            if b.get("_merged"):
                continue
            if a.get("topic") != b.get("topic"):
                continue
            if a.get("market") != b.get("market"):
                continue
            tb = normalize_title(b.get("title", ""), strip_frags)
            if similarity(ta, tb) >= threshold:
                # Fundir b en a
                a.setdefault("merged_from", []).append(b["id"])
                # Guardar hasta 3 fuentes alternativas para contexto editorial
                a.setdefault("alt_sources", [])
                if len(a["alt_sources"]) < 3:
                    a["alt_sources"].append({
                        "source": b.get("source_name"),
                        "link": b.get("link"),
                    })
                b["_merged"] = True

    unique = [it for it in items_list if not it.get("_merged")]

    with out_path.open("w", encoding="utf-8") as f:
        for it in unique:
            it.pop("_merged", None)
            f.write(json.dumps(it, ensure_ascii=False) + "\n")

    return {
        "week": week,
        "path": str(out_path),
        "in": len(items),
        "after_url_dedup": len(by_url),
        "after_title_dedup": len(unique),
    }


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--date", help="YYYY-MM-DD (default: hoy)")
    args = p.parse_args(argv)
    today = dt.date.fromisoformat(args.date) if args.date else None
    result = dedupe(today)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if "error" not in result else 1


if __name__ == "__main__":
    sys.exit(main())
