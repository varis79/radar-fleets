"""
Composición de la edición semanal.

Lee la selección (`content/decisions/YYYY-WW-selection.json`) y pide al LLM
(Anthropic Claude) que produzca el JSON editorial completo: cover headline,
deck, tags, editor's note, wm-cards, stories con redacción lista y CTA.

Luego renderiza el HTML con `scripts/lib/templating.py` y guarda el
`…summary.txt`.

Requisitos:
 - Variable de entorno ANTHROPIC_API_KEY.
 - Si falta, compose escribe un stub (solo estructura y titulares automáticos),
   lo etiqueta como modo stub y marca en el output. El pipeline sigue adelante
   pero QA marcará falta de contenido. Esto permite probar el workflow sin gastar
   API. En producción la API key es obligatoria.

Modos:
 - "normal" y "short": compone edición completa.
 - "pause": no compone; escribe una nota corta en decisions y sale con status
   pause. El publish script tratará este caso sin tocar el sitio.

Salida:
 - magazines/YYYY-MM-DD-radar-fleet-by-pulpo.html
 - magazines/YYYY-MM-DD-radar-fleet-by-pulpo-summary.txt
 - content/decisions/YYYY-WW-compose.json (metadatos de la llamada al LLM)
"""
from __future__ import annotations
import argparse
import datetime as dt
import json
import os
import sys
from pathlib import Path

from scripts.lib.config import config
from scripts.lib.paths import (
    ROOT, MAGAZINES_DIR, DECISIONS_DIR, ARCHIVE_HTML,
    MASTER_PROMPT, iso_week_key, magazine_paths, next_monday, ensure_dirs
)
from scripts.lib.templating import render_edition, render_summary_txt, human_date_es


# ──────────────── helpers ────────────────

def next_edition_number() -> int:
    """Cuenta <a class="edition-row"> en archive.html y devuelve N+1.
       Si archive.html no existe o no matchea, devuelve 3 como fallback seguro."""
    if not ARCHIVE_HTML.exists():
        return 3
    text = ARCHIVE_HTML.read_text(encoding="utf-8")
    count = text.count('class="edition-row"')
    return max(count, 0) + 1


def pick_accent_palette(week_key: str) -> dict:
    palettes = config()["compose"]["accent_palettes"]
    # Rotación determinística: hash corto → módulo len
    idx = sum(ord(c) for c in week_key) % len(palettes)
    return palettes[idx]


# ──────────────── prompting ────────────────

def build_user_prompt(selection: dict, edition_date: dt.date, number: int, mode: str) -> str:
    """Prompt que se envía al LLM junto con el master prompt como system."""
    chosen = selection.get("chosen", [])
    target = len(chosen)
    lines = []
    lines.append(f"# Tarea · Edición Nº {number} · {human_date_es(edition_date)} · modo {mode}")
    lines.append("")
    lines.append("Tienes una selección editorial ya hecha por el pipeline. Tu trabajo es redactar la edición completa siguiendo las reglas del master prompt (que ya conoces como system).")
    lines.append("")
    lines.append("## Reglas duras")
    lines.append("")
    lines.append("- Cumple la checklist editorial del master prompt, especialmente la sección 'Framing editorial — qué NO aparece en la capa pública'.")
    lines.append("- Los headlines son claros y periodísticos. Nada de metáforas grandilocuentes tipo 'la semana que redefinió…'.")
    lines.append("- Nada de em dashes; usa comas, puntos o paréntesis.")
    lines.append("- Nada de 'no es X, es Y'. Nada de 'Para Pulpo' / 'Pulpo debe' / 'competidor'. Nada de 'argumento comercial'.")
    lines.append("")
    lines.append("### Longitudes objetivo (críticas; el QA bloquea si no se cumplen)")
    lines.append("")
    lines.append("Medidas en palabras, no caracteres. Escribe con densidad editorial real: datos, contexto operativo, cifras y consecuencias. Nada de relleno.")
    lines.append("")
    lines.append("- `cover_deck`: **70-110 palabras**. Panorámica con las señales más fuertes y al menos 3 datos concretos.")
    lines.append("- `editors_body`: **180-260 palabras** en 3-4 párrafos. Primer párrafo enmarca la semana. Segundo aterriza cifras. Tercero conecta con el lector operativo. `<strong>` y `<br><br>` permitidos para separar.")
    lines.append("- `wm_cards` (6 en normal, 4 en short). Cada tarjeta: `headline` 8-14 palabras, `body` **35-60 palabras** con un dato concreto.")
    lines.append("- `stories` (10 en normal, 7 en short). Cada historia **150-210 palabras** sumando summary + why_operator + why_business. Dentro:")
    lines.append("  - `summary`: **70-110 palabras**. Qué pasó con datos, fechas, cifras y actores. Contexto suficiente para entender sin clicar la fuente.")
    lines.append("  - `why_operator`: **35-55 palabras**. Qué significa para quien opera la flota. Concreto y accionable.")
    lines.append("  - `why_business`: **35-55 palabras**. Qué significa para el negocio, el presupuesto o la licitación.")
    lines.append("- `opinion_quote`: **15-28 palabras**. Una frase editorial que resume el ángulo de la semana. Sin em dashes ni grandilocuencia.")
    lines.append("- `opinion_body`: **140-220 palabras** en 2-3 párrafos. Argumenta con los datos ya citados en las stories, sin inventar nuevos. Cierra con una acción observable para el lector.")
    lines.append("- `cta_headline`: 10-15 palabras, editorial (no publicitario).")
    lines.append("")
    lines.append("Total acumulado esperado: 10 stories × ~175 palabras + wm_cards + editors + opinion + cover_deck supera holgadamente 2.200 palabras (umbral QA). Si una historia tiene poco material fuente, prefiere quitarla antes que inflarla.")
    lines.append("")
    lines.append("## Formato de respuesta obligatorio")
    lines.append("")
    lines.append("Responde SOLO con un JSON válido dentro de un bloque ```json ... ```. Sin texto adicional.")
    lines.append("")
    lines.append("Schema esperado:")
    lines.append("""```
{
  "cover_headline": "...",                // 3-10 palabras. Claro, periodístico.
  "cover_deck": "...",                    // 70-110 palabras (ver reglas arriba).
  "overline": "Edición semanal · …",      // opcional
  "cover_tags": ["...", "..."],           // 4-6 etiquetas cortas, neutras
  "meta_description": "...",              // 140-160 chars para <meta>
  "executive_summary": "...",             // 3-5 líneas para summary.txt
  "editors_body": "...",                  // 180-260 palabras, 3-4 párrafos. <strong> y <br> permitidos.
  "cta_headline": "...",                  // 10-15 palabras, editorial
  "opinion_quote": "...",                 // 15-28 palabras. Una sola frase con el ángulo de la semana.
  "opinion_body": "...",                  // 140-220 palabras, 2-3 párrafos. <br><br> permitidos.
  "wm_cards": [
    {"tone":"signal","headline":"...","body":"..."},
    ...
  ],
  "stories": [
    {
      "ref_id": "<id del item seleccionado>",  // obligatorio
      "tag_class": "tag-market|tag-reg|tag-tech|tag-payments|tag-ev|tag-ops|tag-mexico|tag-spain",
      "tag_label": "Movimiento de mercado|Regulación|IA|Pagos|Electrificación|Last mile|México|España",
      "market": "mexico|espana|usa|colombia|brasil|chile|peru|argentina|latam|europa|global",
      "date_label": "...",                 // etiqueta humana corta
      "headline": "...",
      "summary": "...",                    // 70-110 palabras
      "why_operator": "...",               // 35-55 palabras
      "why_business": "...",               // 35-55 palabras
      "topic": "...",                      // slug taxonómico
      "fleet_type": "...",                 // opcional
      "players": ["..."],
      "micro_tags": ["sigla:…", "regulacion:…"]
    }
  ]
}
```""")
    lines.append("")
    lines.append("## Selección editorial (items que debes cubrir)")
    lines.append("")
    for i, it in enumerate(chosen, 1):
        lines.append(f"### Item {i}  ·  id={it['id']}")
        lines.append(f"- Título original: {it.get('title','').strip()}")
        if it.get("summary"):
            lines.append(f"- Resumen fuente: {it['summary'][:400]}")
        lines.append(f"- URL: {it.get('link','')}")
        lines.append(f"- Fuente: {it.get('source_name','?')}  ·  Geo fuente: {it.get('source_geo','?')}")
        if it.get("published_iso"):
            lines.append(f"- Publicado: {it['published_iso']}")
        lines.append(f"- Clasificación pipeline: topic={it.get('topic')}, market={it.get('market')}, fleet_type={it.get('fleet_type')}, players={it.get('players')}, micro_tags={it.get('micro_tags')}")
        if it.get("alt_sources"):
            lines.append(f"- Fuentes adicionales: {', '.join(s.get('source','') for s in it['alt_sources'])}")
        lines.append("")
    lines.append("")
    lines.append("## Recordatorio")
    lines.append("- `stories` debe tener exactamente los items elegidos, en el orden que consideres editorialmente mejor.")
    lines.append("- Para cada story, ref_id debe coincidir con el id del item.")
    lines.append("- Si un dato del item no es verificable o confuso, prefiere no inventar. Mejor una story ligeramente más corta que una inventada.")
    return "\n".join(lines)


def call_llm(user_prompt: str, system_prompt: str) -> dict:
    """Llamada al LLM. Devuelve dict con el JSON parseado o levanta excepción."""
    import anthropic
    cfg = config()["compose"]
    client = anthropic.Anthropic()  # lee ANTHROPIC_API_KEY del entorno
    model = cfg["model_primary"]
    try:
        msg = client.messages.create(
            model=model,
            max_tokens=int(cfg.get("max_tokens_per_call", 8000)),
            temperature=float(cfg.get("temperature", 0.4)),
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )
    except anthropic.APIError as e:
        # Fallback a sonnet si opus falla por cualquier cuestión transitoria
        model = cfg["model_fallback"]
        msg = client.messages.create(
            model=model,
            max_tokens=int(cfg.get("max_tokens_per_call", 8000)),
            temperature=float(cfg.get("temperature", 0.4)),
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )
    text = "".join(
        block.text for block in msg.content if getattr(block, "type", "") == "text"
    )
    # Extraer JSON del bloque ```json
    start = text.find("```json")
    if start >= 0:
        start = text.find("\n", start) + 1
        end = text.find("```", start)
        text = text[start:end].strip()
    else:
        # permitir que el modelo devuelva JSON pelado
        text = text.strip()
        if text.startswith("```"):
            text = text.strip("`")
    return json.loads(text)


def compose_stub(selection: dict, edition_date: dt.date, number: int) -> dict:
    """Fallback sin LLM. Genera estructura mínima a partir de la selección.
       Marca claramente que es un stub, no un texto editorial final."""
    chosen = selection.get("chosen", [])[:10]
    stub_stories = []
    for it in chosen:
        stub_stories.append({
            "ref_id": it["id"],
            "tag_class": "tag-market",
            "tag_label": "Movimiento de mercado",
            "market": it.get("market", "global"),
            "date_label": (it.get("published_iso") or "")[:10],
            "headline": (it.get("title") or "Sin titular")[:100],
            "summary": (it.get("summary") or "")[:320] or "[stub: redacción pendiente]",
            "why_operator": "[stub: pendiente de redacción editorial]",
            "why_business": "[stub: pendiente de redacción editorial]",
            "topic": it.get("topic"),
            "fleet_type": it.get("fleet_type"),
            "players": it.get("players") or [],
            "micro_tags": it.get("micro_tags") or [],
        })
    return {
        "cover_headline": f"Edición stub del {human_date_es(edition_date)}",
        "cover_deck": "Esta edición ha sido generada sin clave API, en modo stub. Los textos son placeholders y deben ser sustituidos antes de publicar.",
        "overline": "Edición semanal · Stub sin LLM",
        "cover_tags": ["Stub", "Pendiente redacción"],
        "meta_description": "Edición stub sin redacción editorial final; no publicar.",
        "executive_summary": "Stub. No publicar sin composición editorial completa.",
        "editors_body": "<strong>Stub.</strong><br><br>Esta edición se generó sin API key de LLM. QA la marcará como thin content y bloqueará publicación.",
        "cta_headline": "Edición stub pendiente de redacción",
        "opinion_quote": "[stub: opinión editorial pendiente]",
        "opinion_body": "[stub: cuerpo de opinión pendiente]",
        "wm_cards": [
            {"tone": "signal", "headline": f"Item {i + 1}: {c['title'][:70]}", "body": (c.get("summary") or "")[:200]}
            for i, c in enumerate(chosen[:6])
        ],
        "stories": stub_stories,
        "_stub": True,
    }


# ──────────────── main ────────────────

def compose(today: dt.date | None = None) -> dict:
    ensure_dirs()
    MAGAZINES_DIR.mkdir(exist_ok=True)

    week = iso_week_key(today)
    sel_path = DECISIONS_DIR / f"{week}-selection.json"
    if not sel_path.exists():
        return {"error": "no-selection-file", "expected": str(sel_path)}
    selection = json.loads(sel_path.read_text(encoding="utf-8"))

    mode = selection.get("mode", "normal")
    edition_date = next_monday(today)
    next_date = edition_date + dt.timedelta(days=7)
    number = next_edition_number()

    if mode == "pause":
        pause_info = {
            "status": "pause",
            "week": week,
            "reason": "insufficient-material",
            "number_would_have_been": number,
            "edition_date_skipped": edition_date.isoformat(),
        }
        (DECISIONS_DIR / f"{week}-compose.json").write_text(
            json.dumps(pause_info, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        return pause_info

    # Decidir: LLM real o stub
    use_stub = not os.environ.get("ANTHROPIC_API_KEY")
    system_prompt = MASTER_PROMPT.read_text(encoding="utf-8")
    user_prompt = build_user_prompt(selection, edition_date, number, mode)

    if use_stub:
        editorial = compose_stub(selection, edition_date, number)
        llm_meta = {"mode": "stub", "reason": "no ANTHROPIC_API_KEY in env"}
    else:
        editorial = call_llm(user_prompt, system_prompt)
        llm_meta = {"mode": "llm", "model": config()["compose"]["model_primary"]}

    # Acento semanal
    palette = pick_accent_palette(week)

    data = {
        "number": number,
        "edition_date": edition_date,
        "next_date": next_date,
        "accent": palette["accent"],
        "accent_2": palette["accent_2"],
        "grad_a": palette["grad_a"],
        "grad_b": palette["grad_b"],
        **editorial,
    }

    html = render_edition(data)
    txt = render_summary_txt(data)

    paths = magazine_paths(edition_date)
    paths["html"].write_text(html, encoding="utf-8")
    paths["summary"].write_text(txt, encoding="utf-8")

    compose_info = {
        "status": "composed",
        "week": week,
        "mode": mode,
        "number": number,
        "edition_date": edition_date.isoformat(),
        "html_path": str(paths["html"].relative_to(ROOT)),
        "summary_path": str(paths["summary"].relative_to(ROOT)),
        "llm": llm_meta,
        "is_stub": bool(editorial.get("_stub")),
        "stories_count": len(editorial.get("stories", [])),
        "wm_cards_count": len(editorial.get("wm_cards", [])),
    }
    (DECISIONS_DIR / f"{week}-compose.json").write_text(
        json.dumps(compose_info, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return compose_info


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--date", help="YYYY-MM-DD (default: hoy)")
    args = p.parse_args(argv)
    today = dt.date.fromisoformat(args.date) if args.date else None
    result = compose(today)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if "error" in result:
        return 1
    if result.get("status") == "pause":
        # No es error; el workflow lo trata distinto
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
