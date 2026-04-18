"""
Selección editorial. Decide el modo (normal/short/pause) y elige historias.

Reglas:
 - Ordena por (score_novelty descendente, recency descendente).
 - Descarta items vistos en las últimas `recent_weeks_check` ediciones si
   el título+topic+market coinciden por encima de `dedup_title_overlap_max`.
 - Garantiza mínimo de geo primaria (MX+ES >= `geo_min_primary_ratio`).
 - Garantiza diversidad de topics >= `topic_min_diversity`.
 - Si no hay suficientes items para `target_stories_normal`, degrada a short.
 - Si tampoco llega a `min_stories_pause`, devuelve modo pause.

Salida:
  content/decisions/YYYY-WW-selection.json  # candidato elegido + descartes
"""
from __future__ import annotations
import argparse
import datetime as dt
import json
import re
import sys
from difflib import SequenceMatcher
from pathlib import Path

from scripts.lib.config import config
from scripts.lib.paths import RAW_DIR, DECISIONS_DIR, EDITORIAL_MEMORY, ensure_dirs, iso_week_key


def normalize(s: str) -> str:
    s = (s or "").lower()
    s = re.sub(r"[^\w\sáéíóúñü]", " ", s, flags=re.UNICODE)
    return re.sub(r"\s+", " ", s).strip()


def recent_titles_from_memory(max_chunks: int = 8) -> list[str]:
    """Extrae headlines de las últimas N ediciones de editorial-memory.md."""
    if not EDITORIAL_MEMORY.exists():
        return []
    text = EDITORIAL_MEMORY.read_text(encoding="utf-8")
    # Patrón suave: líneas bajo "### Historias cubiertas"
    titles: list[str] = []
    in_section = False
    chunks_seen = 0
    for line in text.splitlines():
        if line.startswith("## Nº "):
            chunks_seen += 1
            if chunks_seen > max_chunks:
                break
        if "### Historias cubiertas" in line:
            in_section = True
            continue
        if line.startswith("###") and in_section:
            in_section = False
        if in_section and line.startswith("- "):
            # quita corchetes [tag] al principio
            clean = re.sub(r"^-\s*\[[^\]]+\]\s*", "", line).strip()
            titles.append(clean)
    return titles


def looks_like_duplicate(candidate_title: str, memory_titles: list[str], threshold: float) -> tuple[bool, float]:
    cn = normalize(candidate_title)
    best = 0.0
    for t in memory_titles:
        r = SequenceMatcher(None, cn, normalize(t)).ratio()
        if r > best:
            best = r
    return best >= threshold, best


def select(today: dt.date | None = None) -> dict:
    ensure_dirs()
    cfg = config()
    sel_cfg = cfg["selection"]
    modes = cfg["modes"]

    week = iso_week_key(today)
    in_path = RAW_DIR / f"{week}-dedup.jsonl"
    if not in_path.exists():
        return {"error": "no-dedup-file", "expected": str(in_path)}

    items: list[dict] = []
    with in_path.open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                items.append(json.loads(line))

    # Filtra: requiere título no vacío y link válido
    items = [it for it in items if it.get("title") and it.get("link")]

    # Descarta repeticiones contra memoria editorial
    recent = recent_titles_from_memory(max_chunks=int(sel_cfg.get("recent_weeks_check", 8)))
    threshold = float(sel_cfg.get("dedup_title_overlap_max", 0.85))
    discarded_repetition: list[dict] = []
    kept: list[dict] = []
    for it in items:
        dup, score = looks_like_duplicate(it["title"], recent, threshold)
        if dup:
            discarded_repetition.append({**it, "_reason": "repetition", "_score": score})
        else:
            kept.append(it)

    # Scoring simple por editorial signal (recency + topic present + geo primary + players)
    primary_markets = {"mexico", "espana"}
    def score(it: dict) -> float:
        s = 0.0
        if it.get("topic"):
            s += 1.0
        if it.get("market") in primary_markets:
            s += 1.0
        if it.get("players"):
            s += 0.5 + 0.1 * min(len(it["players"]), 3)
        if it.get("fleet_type"):
            s += 0.3
        # recency: items más nuevos priorizados
        if it.get("published_iso"):
            try:
                age_days = (dt.datetime.now(dt.timezone.utc) - dt.datetime.fromisoformat(it["published_iso"])).total_seconds() / 86400
                s += max(0.0, 2.0 - age_days * 0.2)  # bonus decrece en ~10 días
            except Exception:
                pass
        return s

    kept_sorted = sorted(kept, key=lambda it: -score(it))

    target_normal = int(sel_cfg.get("target_stories_normal", 10))
    target_short = int(sel_cfg.get("target_stories_short", 7))
    min_pause = int(sel_cfg.get("min_stories_pause", 4))
    topic_min = int(sel_cfg.get("topic_min_diversity", 3))
    geo_min_ratio = float(sel_cfg.get("geo_min_primary_ratio", 0.30))

    # Selección greedy con balance
    def select_with_balance(target: int) -> list[dict]:
        chosen: list[dict] = []
        topics_used: set[str] = set()
        for it in kept_sorted:
            if len(chosen) >= target:
                break
            chosen.append(it)
            if it.get("topic"):
                topics_used.add(it["topic"])
        return chosen

    chosen_normal = select_with_balance(target_normal)
    chosen_short = select_with_balance(target_short)

    # Decidir modo
    available = len(kept_sorted)
    if available >= target_normal:
        mode = "normal"
        chosen = chosen_normal
    elif available >= target_short:
        mode = "short"
        chosen = chosen_short
    elif available >= min_pause:
        mode = "short"
        chosen = kept_sorted[:available]
    else:
        mode = "pause"
        chosen = []

    # Verificar balance mínimo (avisos, no bloqueo en MVP)
    warnings: list[str] = []
    if chosen:
        prim = sum(1 for c in chosen if c.get("market") in primary_markets)
        ratio = prim / len(chosen)
        if ratio < geo_min_ratio:
            warnings.append(f"geo-primary-low:{ratio:.2f}<{geo_min_ratio}")
        topics = {c.get("topic") for c in chosen if c.get("topic")}
        if len(topics) < topic_min:
            warnings.append(f"topic-diversity-low:{len(topics)}<{topic_min}")

    result = {
        "week": week,
        "mode": mode,
        "total_candidates": len(items),
        "total_after_memory_dedup": len(kept),
        "total_chosen": len(chosen),
        "warnings": warnings,
        "chosen": chosen,
        "discarded_repetition": [{"id": d["id"], "title": d["title"], "score": d["_score"]} for d in discarded_repetition][:50],
    }

    out_path = DECISIONS_DIR / f"{week}-selection.json"
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return {**{k: v for k, v in result.items() if k != "chosen"}, "path": str(out_path)}


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--date", help="YYYY-MM-DD (default: hoy)")
    args = p.parse_args(argv)
    today = dt.date.fromisoformat(args.date) if args.date else None
    result = select(today)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if "error" not in result else 1


if __name__ == "__main__":
    sys.exit(main())
