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

    # ─── Filtro de competidores ───
    # Items que mencionan competidores se excluyen del pool. No damos
    # visibilidad gratuita al competidor en nuestra propia revista.
    competitor_blacklist = sel_cfg.get("competitor_blacklist", []) or []
    competitor_filtered: list[dict] = []
    if competitor_blacklist:
        competitor_patterns = [
            re.compile(rf"(?<![A-Za-zÁÉÍÓÚáéíóúÑñÜü0-9]){re.escape(c.lower())}(?![A-Za-zÁÉÍÓÚáéíóúÑñÜü0-9])")
            for c in competitor_blacklist
        ]
        kept_after_competitors: list[dict] = []
        for it in items:
            hay = f"{it.get('title','')} {it.get('summary','')}".lower()
            matched = False
            for pat in competitor_patterns:
                if pat.search(hay):
                    matched = True
                    break
            if matched:
                competitor_filtered.append({"id": it["id"], "title": it["title"][:120]})
            else:
                kept_after_competitors.append(it)
        items = kept_after_competitors

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

    # Scoring por editorial signal. Pesos en config para afinar sin tocar código.
    #
    # Histórico:
    #   2026-05-21 (v1): introducidos pesos por mercado para que USA no
    #     quedase invisible (era 0, pasó a 0.45). Resultado en simulación:
    #     5 USA / 10. Demasiado.
    #   2026-05-21 (v2): subido market_primary a 1.2 (foco editorial real es
    #     Pulpo MX+ES) y bajado secondary a 0.4. USA entra por cuota mínima,
    #     no por score puro. Y añadido topic_priority_boost para empujar
    #     temas editorialmente interesantes y desinflar freight forwarding
    #     USA-céntrico. Selección final por cuotas geo_quotas con min/max
    #     por bucket (primary MX+ES, secondary USA, china, other Europa+...).
    primary_markets = {"mexico", "espana"}
    scoring = sel_cfg.get("scoring", {})
    w_topic = float(scoring.get("topic_match", 1.0))
    w_mkt_primary = float(scoring.get("market_primary", 1.2))
    w_mkt_secondary = float(scoring.get("market_secondary", 0.4))
    w_mkt_china = float(scoring.get("market_china", 0.4))
    w_mkt_tertiary = float(scoring.get("market_tertiary", 0.3))
    w_mkt_other = float(scoring.get("market_other", 0.15))
    w_player_base = float(scoring.get("player_base", 0.5))
    w_player_each = float(scoring.get("player_extra_each", 0.1))
    w_fleet = float(scoring.get("fleet_type", 0.3))
    w_recency_max = float(scoring.get("recency_max", 2.0))
    w_recency_decay = float(scoring.get("recency_decay_per_day", 0.2))
    w_hint_fallback = float(scoring.get("source_topic_hint_fallback", 0.5))
    w_topic_boost = float(scoring.get("topic_priority_boost", 0.5))
    topic_priority_list = set(scoring.get("topic_priority_list", []))
    w_fleet_boost = float(scoring.get("fleet_type_priority_boost", 0.5))
    fleet_priority_list = set(scoring.get("fleet_type_priority_list", []))

    secondary_markets = {"usa"}
    china_markets = {"china"}
    tertiary_markets = {"europa", "canada"}

    def score(it: dict) -> float:
        s = 0.0
        if it.get("topic"):
            s += w_topic
            if it["topic"] in topic_priority_list:
                s += w_topic_boost
        elif it.get("source_topic_hint"):
            s += w_hint_fallback
            if it["source_topic_hint"] in topic_priority_list:
                s += w_topic_boost
        m = it.get("market")
        if m in primary_markets:
            s += w_mkt_primary
        elif m in secondary_markets:
            s += w_mkt_secondary
        elif m in china_markets:
            s += w_mkt_china
        elif m in tertiary_markets:
            s += w_mkt_tertiary
        else:
            s += w_mkt_other
        if it.get("players"):
            s += w_player_base + w_player_each * min(len(it["players"]), 3)
        if it.get("fleet_type"):
            s += w_fleet
            if it["fleet_type"] in fleet_priority_list:
                s += w_fleet_boost
        if it.get("published_iso"):
            try:
                age_days = (dt.datetime.now(dt.timezone.utc) - dt.datetime.fromisoformat(it["published_iso"])).total_seconds() / 86400
                s += max(0.0, w_recency_max - age_days * w_recency_decay)
            except Exception:
                pass
        return s

    kept_sorted = sorted(kept, key=lambda it: -score(it))

    target_normal = int(sel_cfg.get("target_stories_normal", 12))
    target_short = int(sel_cfg.get("target_stories_short", 9))
    min_pause = int(sel_cfg.get("min_stories_pause", 4))
    topic_min = int(sel_cfg.get("topic_min_diversity", 3))
    geo_min_ratio = float(sel_cfg.get("geo_min_primary_ratio", 0.55))

    # ─── Filtro por topic_quotas (máximos por topic) ───
    # Aplica ANTES del selector geográfico para que el ranking ya no incluya
    # items que excederían su cuota de topic. Si quota=0, el topic se excluye
    # totalmente (ej. rail-freight, freight-market no aplican a Pulpo).
    topic_quotas = sel_cfg.get("topic_quotas", {}) or {}
    if topic_quotas:
        filtered: list[dict] = []
        topic_count: dict[str, int] = {}
        for it in kept_sorted:
            t = it.get("topic")
            if t and t in topic_quotas:
                limit = int(topic_quotas[t])
                used = topic_count.get(t, 0)
                if used >= limit:
                    continue
                topic_count[t] = used + 1
            filtered.append(it)
        kept_sorted = filtered

    # ─── Selección por cuotas geográficas ───
    # Si geo_quotas está definido, agrupa items por bucket y respeta min/max
    # de cada uno. Si no, fallback simple top-N por score (sin cuotas).
    geo_quotas = sel_cfg.get("geo_quotas")

    def select_with_quotas(target: int) -> list[dict]:
        if not geo_quotas:
            return kept_sorted[:target]

        # Mapear market → bucket
        bucket_of_market: dict[str, str] = {}
        for bucket_name, bucket_cfg in geo_quotas.items():
            for mk in bucket_cfg.get("markets", []):
                bucket_of_market[mk] = bucket_name

        # Agrupar items por bucket (preservando orden de score)
        by_bucket: dict[str, list[dict]] = {b: [] for b in geo_quotas.keys()}
        unknown_bucket: list[dict] = []
        for it in kept_sorted:
            mk = it.get("market") or ""
            b = bucket_of_market.get(mk)
            if b:
                by_bucket[b].append(it)
            else:
                unknown_bucket.append(it)

        chosen: list[dict] = []

        # Fase 1: respetar mínimos por bucket
        for bucket_name, bucket_cfg in geo_quotas.items():
            min_n = int(bucket_cfg.get("min", 0))
            take = by_bucket[bucket_name][:min_n]
            chosen.extend(take)
            by_bucket[bucket_name] = by_bucket[bucket_name][len(take):]

        # Fase 2: llenar hasta el target respetando máximos
        # Construimos pool de candidatos restantes ordenados por score.
        already_used = {(it["id"]) for it in chosen}
        remaining_target = target - len(chosen)
        if remaining_target > 0:
            # Cuántos quedan en cada bucket (count actual de chosen por bucket)
            count_by_bucket: dict[str, int] = {b: sum(1 for c in chosen if bucket_of_market.get(c.get("market") or "") == b) for b in geo_quotas.keys()}
            # Pool: items restantes en orden de score
            pool: list[tuple[dict, str | None]] = []
            for b, items_b in by_bucket.items():
                for it in items_b:
                    pool.append((it, b))
            for it in unknown_bucket:
                pool.append((it, None))
            pool.sort(key=lambda p: -score(p[0]))

            for it, b in pool:
                if remaining_target <= 0:
                    break
                if it["id"] in already_used:
                    continue
                if b is not None:
                    cap = int(geo_quotas[b].get("max", 9999))
                    if count_by_bucket.get(b, 0) >= cap:
                        continue
                    count_by_bucket[b] = count_by_bucket.get(b, 0) + 1
                chosen.append(it)
                already_used.add(it["id"])
                remaining_target -= 1

        # Reordenar por score
        chosen.sort(key=lambda it: -score(it))
        return chosen[:target]

    chosen_normal = select_with_quotas(target_normal)
    chosen_short = select_with_quotas(target_short)

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
        "discarded_competitor": competitor_filtered[:50],
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
