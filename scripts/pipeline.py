"""
Orquestador del pipeline semanal.

Corre los steps en orden y es el entrypoint del GitHub Actions workflow.

Pasos:
  1. ingest      (red externa)
  2. classify    (local)
  3. dedupe      (local)
  4. select      (local)
  5. compose     (LLM si hay ANTHROPIC_API_KEY, stub si no)
  6. qa          (local, bloqueante)
  7. publish     (local, actualiza sitio)

Devuelve exit code:
  0  → edición lista (o pausa registrada); el workflow abre PR.
  1  → error irrecuperable o QA bloqueante. El workflow abre PR con label fix.

Todos los artefactos del pipeline quedan en content/raw/, content/qa/,
content/decisions/ para trazabilidad.
"""
from __future__ import annotations
import argparse
import datetime as dt
import json
import sys
from pathlib import Path

from scripts import ingest, classify, dedupe, select, compose, qa, publish
from scripts.lib.paths import ensure_dirs, iso_week_key


def run(today: dt.date | None = None, skip_publish_on_fail: bool = True) -> dict:
    ensure_dirs()
    week = iso_week_key(today)
    log: dict = {"week": week, "steps": []}

    def step(name, fn):
        try:
            res = fn(today)
        except Exception as e:
            res = {"error": f"{type(e).__name__}: {e}"}
        log["steps"].append({"name": name, "result": res})
        return res

    ingest_res = step("ingest", ingest.ingest)
    if ingest_res.get("total_items", 0) == 0:
        log["status"] = "fail"
        log["reason"] = "ingest-empty"
        return log

    classify_res = step("classify", classify.classify)
    if "error" in classify_res:
        log["status"] = "fail"
        log["reason"] = classify_res["error"]
        return log

    dedupe_res = step("dedupe", dedupe.dedupe)
    if "error" in dedupe_res:
        log["status"] = "fail"
        log["reason"] = dedupe_res["error"]
        return log

    select_res = step("select", select.select)
    if "error" in select_res:
        log["status"] = "fail"
        log["reason"] = select_res["error"]
        return log

    if select_res.get("mode") == "pause":
        compose_res = step("compose", compose.compose)   # registra pausa
        log["status"] = "pause"
        return log

    compose_res = step("compose", compose.compose)
    if "error" in compose_res:
        log["status"] = "fail"
        log["reason"] = compose_res["error"]
        return log

    qa_res = step("qa", qa.run_qa)
    if qa_res.get("status") == "fail":
        log["status"] = "qa-fail"
        if skip_publish_on_fail:
            return log
        # si skip_publish_on_fail=False (para testing), sigue

    publish_res = step("publish", publish.publish)
    if "error" in publish_res:
        log["status"] = "publish-fail"
        return log

    log["status"] = "ok"
    return log


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--date", help="YYYY-MM-DD (default: hoy)")
    p.add_argument("--allow-publish-on-qa-fail", action="store_true",
                   help="Avanza a publish aunque QA falle. Solo para debugging local.")
    args = p.parse_args(argv)
    today = dt.date.fromisoformat(args.date) if args.date else None
    result = run(today, skip_publish_on_fail=not args.allow_publish_on_qa_fail)
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    if result.get("status") in ("ok", "pause"):
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
