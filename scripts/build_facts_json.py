#!/usr/bin/env python3
"""
build_facts_json.py — Compila content/sabias-que-pool.md → content/sabias-que-pool.json

El MD es source of truth editorial (humano). El JSON es artefacto compilado
que consume rotate_facts.py para inyectar facts en páginas.

Se regenera cada vez que cambia el MD (idempotente).

Formato JSON resultante:
{
  "meta": {"total": 137, "generated_at": "2026-05-24"},
  "facts": [
    {
      "id": "combustible-001",
      "title": "Peso del combustible en TCO transporte pesado ES",
      "fact": "En España, el combustible representa...",
      "source": "Mitma · Observatorio de Costes...",
      "markets": ["espana"],
      "topics": ["combustible", "coste-operativo"],
      "vehicle_type": ["pesados"],
      "categoria": "⛽ Combustible",
      "confidence": "high-cross",
      "evergreen_score": 4,
      "origin": "Perplexity + Grok + Gemini"
    },
    ...
  ]
}

Uso:
    python3 scripts/build_facts_json.py [--dry-run]
"""
import re
import sys
import json
import datetime as dt
from pathlib import Path

DRY_RUN = "--dry-run" in sys.argv
ROOT = Path(__file__).parent.parent
MD_PATH = ROOT / "content/sabias-que-pool.md"
JSON_PATH = ROOT / "content/sabias-que-pool.json"


def _parse_list(value: str) -> list[str]:
    """Convierte 'mexico, espana' o 'mexico, espana (note)' a lista limpia."""
    # Quita paréntesis (notas tipo "high-cross (Perplexity + Grok)")
    value = re.sub(r"\s*\([^)]*\)", "", value)
    parts = [p.strip() for p in value.split(",")]
    return [p for p in parts if p]


def parse_md(md_text: str) -> list[dict]:
    """Parsea el MD y devuelve lista de facts.

    Estrategia: dividir por '### ' (headings de fact) y parsear cada bloque.
    Más robusto que un regex monolítico.
    """
    facts = []

    # Split por heading nivel 3
    # Cada bloque comienza con "{id} · {title}\n..." (tras quitar "### ")
    blocks = re.split(r"^### ", md_text, flags=re.MULTILINE)

    for block in blocks[1:]:  # blocks[0] es el preámbulo
        lines = block.split("\n")
        if not lines:
            continue

        # Línea 1: "{id} · {title}"
        header = lines[0].strip()
        header_match = re.match(r"^([a-z][a-z0-9_-]+-\d{3})\s+·\s+(.+)$", header)
        if not header_match:
            continue  # no es un fact, podría ser otro tipo de heading
        fact_id = header_match.group(1).strip()
        title = header_match.group(2).strip()

        # Encontrar el cuerpo: línea(s) que empiezan con "**Fact**:"
        body_start = None
        for i, line in enumerate(lines):
            if line.strip().startswith("**Fact**:"):
                body_start = i
                break
        if body_start is None:
            continue

        # Cuerpo del fact: desde la línea Fact hasta la línea anterior al primer "- **xxx**:"
        body_lines = []
        meta_start = None
        for i in range(body_start, len(lines)):
            line = lines[i]
            if re.match(r"^- \*\*[a-z_]+\*\*:", line.strip()):
                meta_start = i
                break
            body_lines.append(line)
        if meta_start is None:
            # No hay metadata, skip
            continue

        # Limpiar fact text
        fact_text = "\n".join(body_lines).strip()
        fact_text = re.sub(r"^\*\*Fact\*\*:\s*", "", fact_text)
        fact_text = re.sub(r"\s+", " ", fact_text).strip()

        # Metadata block: hasta el siguiente heading o sección
        meta = {}
        for i in range(meta_start, len(lines)):
            line = lines[i].strip()
            if not line:
                continue
            if not line.startswith("- **"):
                break  # fin del bloque de metadata
            m = re.match(r"- \*\*([a-z_]+)\*\*:\s*(.+)$", line)
            if m:
                meta[m.group(1).strip()] = m.group(2).strip()

        fact_obj = {
            "id": fact_id,
            "title": title,
            "fact": fact_text,
            "source": meta.get("source", ""),
            "markets": _parse_list(meta.get("markets", "")),
            "topics": _parse_list(meta.get("topics", "")),
            "vehicle_type": _parse_list(meta.get("vehicle_type", "")),
            "categoria": meta.get("categoria", "").strip(),
            "confidence": re.sub(r"\s*\(.*\)", "", meta.get("confidence", "")).strip(),
            "evergreen_score": _safe_int(meta.get("evergreen_score", "3")),
            "origin": meta.get("origin", ""),
        }

        # Filter out pending/conflict (no production)
        if fact_obj["confidence"] in ("pending", "conflict", ""):
            continue
        if not fact_obj["fact"]:
            continue

        facts.append(fact_obj)

    return facts


def _safe_int(val: str) -> int:
    try:
        return int(re.search(r"\d+", val).group())
    except (AttributeError, ValueError):
        return 3


def main():
    mode = "[DRY-RUN]" if DRY_RUN else "[LIVE]"
    print(f"\nbuild_facts_json.py {mode}\n")

    if not MD_PATH.exists():
        print(f"❌ {MD_PATH} no existe")
        return 1

    md_text = MD_PATH.read_text(encoding="utf-8")
    facts = parse_md(md_text)

    print(f"  Facts parseados: {len(facts)}")

    # Cobertura por categoría
    from collections import Counter
    by_cat = Counter(f["categoria"] for f in facts)
    by_market = Counter()
    by_conf = Counter(f["confidence"] for f in facts)
    for f in facts:
        for m in f["markets"]:
            by_market[m] += 1

    print(f"\n  Por categoría:")
    for cat, n in by_cat.most_common():
        print(f"    {cat:40} {n}")

    print(f"\n  Por mercado:")
    for mk, n in by_market.most_common(10):
        print(f"    {mk:20} {n}")

    print(f"\n  Por confianza:")
    for c, n in by_conf.most_common():
        print(f"    {c:15} {n}")

    output = {
        "meta": {
            "total": len(facts),
            "generated_at": dt.date.today().isoformat(),
            "source": "content/sabias-que-pool.md",
        },
        "facts": facts,
    }

    if not DRY_RUN:
        JSON_PATH.write_text(
            json.dumps(output, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"\n  ✅ {JSON_PATH.relative_to(ROOT)} regenerado")

        # Versión PÚBLICA reducida para JS dinámico (home/archive/magazines)
        public_path = ROOT / "assets/sabias-que.json"
        public_facts = []
        for f in facts:
            cat = f.get("categoria", "💡 Fleet Radar")
            # Separar emoji del nombre
            parts = cat.split(" ", 1)
            emoji = parts[0] if parts and len(parts[0]) <= 4 else "💡"
            cat_name = parts[1] if len(parts) > 1 else "Fleet Radar"
            public_facts.append({
                "emoji": emoji,
                "category": cat_name,
                "text": f["fact"],
                "markets": f.get("markets", []),
            })
        public_path.write_text(
            json.dumps({"facts": public_facts}, ensure_ascii=False, separators=(",", ":")),
            encoding="utf-8",
        )
        print(f"  ✅ {public_path.relative_to(ROOT)} regenerado (versión pública JS)")
    else:
        print(f"\n  [DRY-RUN] No se escribió JSON")

    return 0


if __name__ == "__main__":
    sys.exit(main())
