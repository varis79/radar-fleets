"""
generate_newsletter_copy.py — Usa Claude para generar la versión newsletter (teasers).

Dado el contenido de una edición, Claude selecciona las 5 mejores historias y
para cada una escribe:
  - hook: dato o ángulo más impactante (1 frase, ≤65 chars)
  - question: pregunta que crea tensión y obliga al click (≤85 chars)

También genera:
  - intro: nota editorial de 2-3 frases, tono directo
  - subject_line: asunto alternativo para maximizar apertura

Requiere ANTHROPIC_API_KEY en el entorno.
Si no hay API key, devuelve fallback con resúmenes truncados.

Uso standalone:
  python -m scripts.generate_newsletter_copy --date 2026-05-18
"""
from __future__ import annotations
import argparse
import datetime as dt
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.generate_email import load_compose_info
from scripts.lib.templating import FLAGS, MARKET_LABELS


SYSTEM_PROMPT = """Eres el editor de The Fleet Radar, publicación semanal de inteligencia \
de mercado para gestores de flota en México, España y LatAm.

Tu trabajo es escribir la versión newsletter de cada edición: corta, directa, \
diseñada para generar clicks hacia la revista completa.

Responde SOLO con JSON válido, sin texto adicional, con esta estructura exacta:
{
  "intro": "2-3 frases de nota editorial. Tono: directo, profesional, sin fluff. \
Habla al gestor de flota que lee en 30 segundos camino a una reunión.",
  "subject_line": "Asunto del email, máx 60 chars, maximiza apertura sin ser clickbait",
  "stories": [
    {
      "index": 0,
      "headline": "titular original sin cambiar",
      "hook": "el dato o ángulo más concreto e impactante, máx 65 chars",
      "question": "pregunta que incomoda ligeramente y obliga al click, máx 85 chars",
      "market": "mexico|espana|usa|latam|europa|global",
      "flag": "emoji de bandera correspondiente"
    }
  ]
}

Reglas:
- Selecciona las 5 historias más relevantes para un gestor de flota (prioriza operación, \
costes, regulación y tecnología con impacto directo en el negocio)
- El hook es un dato concreto o afirmación directa — nunca "descubre cómo" ni genérico
- La question debe crear tensión real: que el lector piense "necesito saber esto ahora"
- Nunca uses: "te contamos", "en este artículo", "descubre", "conoce", "te presentamos"
- Todo en español salvo términos técnicos del sector (EV, telemática, compliance, ROI…)
- El intro menciona 1-2 temas de la semana, no enumera ni lista"""


def _build_user_message(compose_info: dict) -> str:
    number = compose_info.get("number", 1)
    edition_date = compose_info.get("edition_date", "")
    cover_headline = compose_info.get("cover_headline", "")
    cover_deck = compose_info.get("cover_deck", "")
    stories = compose_info.get("stories", [])

    lines = [
        f"EDICIÓN Nº {number:02d} · {edition_date}",
        f"PORTADA: {cover_headline}",
        f"DECK: {cover_deck}",
        "",
        "HISTORIAS DISPONIBLES:",
    ]
    for i, s in enumerate(stories):
        flag = FLAGS.get(s.get("market", "global"), "🌐")
        market = MARKET_LABELS.get(s.get("market", "global"), "Global")
        lines.append(f"\n[{i}] {flag} {market}")
        lines.append(f"Titular: {s.get('headline', '')}")
        lines.append(f"Resumen: {s.get('summary', '')[:300]}")

    return "\n".join(lines)


def _fallback_copy(compose_info: dict) -> dict:
    """Genera teasers básicos sin Claude (fallback si no hay API key)."""
    stories = compose_info.get("stories", [])
    top5 = stories[:5]
    teaser_stories = []
    for i, s in enumerate(top5):
        summary = s.get("summary", "")
        hook = summary[:65].rsplit(" ", 1)[0] + "…" if len(summary) > 65 else summary
        teaser_stories.append({
            "index": i,
            "headline": s.get("headline", ""),
            "hook": hook,
            "question": "¿Qué significa esto para tu flota esta semana?",
            "market": s.get("market", "global"),
            "flag": FLAGS.get(s.get("market", "global"), "🌐"),
        })

    cover = compose_info.get("cover_headline", "")
    return {
        "intro": f"Esta semana: {cover[:120]}. Lo más relevante para tu operación.",
        "subject_line": f"Nº {compose_info.get('number', 1):02d} · {cover[:45]}",
        "stories": teaser_stories,
        "_source": "fallback",
    }


def generate_copy(compose_info: dict, api_key: str | None = None) -> dict:
    """
    Llama a Claude para generar la copia del newsletter.
    Si no hay api_key, usa el fallback básico.
    """
    key = api_key or os.environ.get("ANTHROPIC_API_KEY", "")
    if not key:
        print("WARN: ANTHROPIC_API_KEY no disponible — usando fallback", file=sys.stderr)
        return _fallback_copy(compose_info)

    try:
        import anthropic  # ya en requirements.txt
    except ImportError:
        print("WARN: anthropic no instalado — usando fallback", file=sys.stderr)
        return _fallback_copy(compose_info)

    client = anthropic.Anthropic(api_key=key)
    user_msg = _build_user_message(compose_info)

    print("  Llamando a Claude para generar teasers newsletter…", file=sys.stderr)
    try:
        response = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=1200,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_msg}],
        )
        raw = response.content[0].text.strip()

        # Extraer JSON aunque venga con ```json ... ```
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        data = json.loads(raw)
        data["_source"] = "claude"
        print(f"  ✓ Teasers generados por Claude ({len(data.get('stories', []))} historias)",
              file=sys.stderr)
        return data

    except Exception as e:
        print(f"  WARN: Claude falló ({e}) — usando fallback", file=sys.stderr)
        return _fallback_copy(compose_info)


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--date", help="YYYY-MM-DD")
    p.add_argument("--output", help="Archivo JSON de salida (default: stdout)")
    args = p.parse_args(argv)

    date = dt.date.fromisoformat(args.date) if args.date else None
    info = load_compose_info(date)
    if not info:
        print(json.dumps({"error": "No se encontró compose-info"}))
        return 1

    result = generate_copy(info)

    out = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(out, encoding="utf-8")
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
