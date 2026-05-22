"""
Generador de páginas pilar usando Claude Opus.

Uso:
    python -m scripts.generate_pillar_page --slug <slug>          # 1 página
    python -m scripts.generate_pillar_page --tier 1               # todas T1
    python -m scripts.generate_pillar_page --dimension use-case   # todas use-case
    python -m scripts.generate_pillar_page --tier 1 --dry-run     # simula sin LLM
    python -m scripts.generate_pillar_page --slug <slug> --indexed  # liberar (sin noindex)

Pipeline por página:
  1. Lee PillarPage de la matriz.
  2. Construye user_prompt con:
     - page_meta (de la matriz)
     - data_context (de data-overrides/<market>.yml)
     - use_case_context (si dimension=use-case)
     - editorial_context (top 5 historias de editorial-memory afines)
     - forbidden_competitors (de pipeline-config.yml)
  3. Llama a Claude Opus con system prompt = pillar-page-prompt.md.
  4. Parse JSON, valida estructura mínima.
  5. Renderiza HTML con scripts.lib.pillar_renderer.render_pillar_page().
  6. Calcula related_pages() y los incluye.
  7. Escribe HTML en page.url_path() (/temas/<slug>/index.html etc).
  8. Escribe .md tracking en content/pillar-matrix/pages/<slug>.md con
     frontmatter: status, last_generated, indexed, related_editions.

Modo dry-run: usa un stub fixture en vez de LLM real. Útil para validar
flujo + renderer sin gastar tokens.

Idempotente: re-ejecutar sobre un slug regenera (sobreescribe).
"""
from __future__ import annotations
import argparse
import datetime as dt
import json
import os
import sys
import re
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import yaml

from scripts.lib.paths import ROOT
from scripts.lib.config import config
from scripts.lib.pillar import (
    enumerate_pages, load_markets, load_use_cases, load_topics,
    related_pages, PillarPage, PAGES_DIR, DATA_OVERRIDES_DIR,
)
from scripts.lib.pillar_renderer import render_pillar_page


PROMPT_PATH = ROOT / "prompts" / "pillar-page-prompt.md"
EDITORIAL_MEMORY_PATH = ROOT / "content" / "editorial-memory.md"


def load_data_override(market_code: str) -> dict:
    p = DATA_OVERRIDES_DIR / f"{market_code}.yml"
    if not p.exists():
        return {}
    with p.open(encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def find_use_case(use_case_code: str) -> dict | None:
    for uc in load_use_cases():
        if uc["code"] == use_case_code:
            return uc
    return None


def editorial_context_for(page: PillarPage, max_items: int = 6) -> list[str]:
    """Extrae headlines relacionados de editorial-memory.md que matcheen
    market/topic/use_case de esta página."""
    if not EDITORIAL_MEMORY_PATH.exists():
        return []
    text = EDITORIAL_MEMORY_PATH.read_text(encoding="utf-8")
    # Cada línea con "- [tag] Title" es una historia
    headlines = re.findall(r"^- \[([^\]]+)\]\s*(.+)$", text, flags=re.MULTILINE)
    keys_to_match = {page.market_code, page.topic_code}
    matched = []
    for tag, title in headlines:
        tag_low = tag.lower()
        if any(k in tag_low for k in keys_to_match if k):
            matched.append(f"[{tag}] {title}")
    return matched[:max_items]


def build_user_prompt(page: PillarPage) -> str:
    """Construye el user prompt para el LLM."""
    cfg = config()
    forbidden = cfg.get("selection", {}).get("competitor_blacklist", [])
    data_override = load_data_override(page.market_code)
    editorial = editorial_context_for(page)
    use_case_ctx = find_use_case(page.topic_code) if page.dimension == "use-case" else None

    lines = []
    lines.append("## Page metadata")
    lines.append(f"- slug: `{page.slug}`")
    lines.append(f"- dimension: `{page.dimension}`")
    lines.append(f"- market: {page.market_label} ({page.market_code})")
    lines.append(f"- topic_code: `{page.topic_code}`")
    lines.append(f"- intent: `{page.intent_code}`")
    lines.append(f"- schema_type: {page.schema_type}")
    lines.append(f"- label propuesto: \"{page.label}\"")
    lines.append(f"- url: {page.url_path()}")
    lines.append(f"- pulpopay_relevant: {page.pulpopay_relevant}")

    lines.append("\n## Secciones requeridas (en este orden, h2 cada una)")
    for sec_key in page.section_template:
        # Construir hint editorial por sección estándar
        hint = SECTION_HINTS.get(sec_key, "Desarrolla esta sección con criterio editorial.")
        lines.append(f"- key: `{sec_key}` · hint: {hint}")

    lines.append("\n## Data context (datos del mercado disponibles)")
    if data_override:
        # Solo incluimos campos no-vacíos
        def _has(v): return v not in (None, "", [], {})
        for k, v in data_override.items():
            if k.startswith("_") or not _has(v):
                continue
            lines.append(f"- {k}: {json.dumps(v, ensure_ascii=False)}")
    else:
        lines.append("- (sin overrides locales; usa tu conocimiento general del mercado, con prudencia)")

    if use_case_ctx:
        lines.append("\n## Use case context (caso de uso Pulpo)")
        lines.append(f"- label: {use_case_ctx['label']}")
        lines.append(f"- sectores típicos: {', '.join(use_case_ctx.get('sectors', []))}")
        lines.append(f"- cómo operan: {use_case_ctx.get('how_they_operate', '')}")
        lines.append(f"- dolores: {', '.join(use_case_ctx.get('pain_points', []))}")
        lines.append(f"- producto prioritario: {use_case_ctx.get('product_priority', 'pulpo')}")
        lines.append(f"- demo focus: {use_case_ctx.get('demo_focus', '')}")
        if page.market_code == "mexico":
            refs = use_case_ctx.get("client_references_mx", [])
        elif page.market_code == "espana":
            refs = use_case_ctx.get("client_references_es", [])
        else:
            refs = []
        if refs:
            lines.append(f"- clientes Pulpo reales en este mercado: {', '.join(refs)}")
            lines.append("  Puedes mencionarlos en las secciones de manera editorial (no listado plano).")

    lines.append("\n## Editorial context (historias recientes que puedes citar)")
    if editorial:
        for h in editorial:
            lines.append(f"- {h}")
        lines.append("Si citas alguna, hazlo con tono editorial (\"según cubrió The Fleet Radar en mayo de 2026\"...).")
    else:
        lines.append("- (sin historias recientes específicas; redacta con tu conocimiento del sector)")

    lines.append("\n## Competidores prohibidos (no mencionar bajo ningún concepto)")
    lines.append(f"{', '.join(forbidden)}")

    lines.append("\n## Recordatorio final")
    lines.append("- Responde SOLO con el JSON pedido en el system prompt.")
    lines.append("- Datos antes que adjetivos. Voz sobria. Cero hype.")
    lines.append("- 900-1500 palabras combinadas total.")
    lines.append("- Una FAQ debe mencionar Pulpo de forma editorial (no anuncio).")

    return "\n".join(lines)


SECTION_HINTS = {
    "introduccion-tema-mercado": "Contexto del tema en este mercado específico. Dato fuerte de apertura.",
    "estado-actual-mercado": "Foto del mercado en 2026. Cifras, tendencias visibles, hitos del último año.",
    "players-activos-mercado": "Jugadores activos. Si hay clientes Pulpo en el mercado, menciónalos. Excluye competidores prohibidos.",
    "regulacion-aplicable": "Normativa relevante. Organismo competente. Plazos clave.",
    "cifras-clave": "5-8 datos cuantificados. Si no tienes fuente cierta, di \"según fuentes públicas / cifras del sector\".",
    "historias-relacionadas": "Síntesis de 2-3 historias que The Fleet Radar ha cubierto sobre este tema. Si no las hay, di que se irá actualizando.",
    "faq": "(esta sección la maneja el campo `faq`, no la incluyas en `sections`)",
    "como-encaja-pulpo": "(esta sección la maneja `pulpo_box`, no la incluyas en `sections`)",
    "introduccion-comparativa": "Por qué comparar opciones en este mercado. Qué buscar el lector.",
    "tabla-comparativa": "Tabla de criterios × opciones. Usa <table><thead><tr><th>...etc. Sin nombrar competidores prohibidos.",
    "criterios-eleccion": "5-7 criterios técnicos para decidir.",
    "players-detalle": "Players permitidos con breve descripción editorial neutral.",
    "recomendaciones-por-tamano-flota": "Recomendación por bucket: pequeña (<50), mediana (50-500), grande (>500).",
    "introduccion-norma": "Qué es la norma. Origen y motivación.",
    "alcance-quien-aplica": "A quién aplica exactamente. Excepciones si las hay.",
    "obligaciones-clave": "Lista de obligaciones operativas concretas.",
    "plazos-y-fechas-importantes": "Fechas clave 2026-2027.",
    "sanciones": "Tipo y rango de sanciones.",
    "como-cumplir": "Pasos operativos para una flota.",
    "introduccion-objetivo": "Qué consigue el lector si sigue esta guía.",
    "paso-1-evaluar-necesidades": "Preguntas que debe hacerse el gerente.",
    "paso-2-criterios-de-eleccion": "Criterios y trade-offs.",
    "paso-3-evaluar-players": "Cómo evaluar players concretos.",
    "paso-4-implementacion": "Pasos de implementación operativa.",
    "errores-comunes": "Top 5 errores a evitar.",
}


def call_llm(system_prompt: str, user_prompt: str) -> dict:
    """Llama a Claude Opus. Devuelve el JSON parsed del editorial."""
    try:
        import anthropic
    except ImportError:
        raise RuntimeError("anthropic SDK no instalado. pip install anthropic.")

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY no configurada en env.")

    client = anthropic.Anthropic(api_key=api_key)
    cfg = config()
    model = cfg.get("compose", {}).get("model_primary", "claude-opus-4-1-20250805")

    resp = client.messages.create(
        model=model,
        max_tokens=4000,
        temperature=0.4,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    )
    text = resp.content[0].text

    # Extraer JSON del bloque markdown
    m = re.search(r"```json\s*(\{.+?\})\s*```", text, flags=re.DOTALL)
    if not m:
        # Tal vez el modelo devolvió JSON pelado
        text = text.strip()
        if text.startswith("{"):
            return json.loads(text)
        raise ValueError(f"No se encontró bloque JSON en la respuesta:\n{text[:500]}")
    return json.loads(m.group(1))


def stub_editorial(page: PillarPage) -> dict:
    """Stub fixture para dry-run (sin LLM real)."""
    return {
        "title_seo": f"{page.label}",
        "meta_description": f"Análisis editorial sobre {page.label.lower()}. Stub generado por dry-run.",
        "h1": page.label,
        "intro": f"<strong>STUB.</strong> Esta es una página generada en modo dry-run, sin LLM real. Cuando se ejecute en modo producción, aquí irá una introducción editorial sobre {page.label.lower()}, con datos del mercado {page.market_label} y voz de The Fleet Radar.",
        "sections": [
            {"key": s, "h2": f"Sección · {s}",
             "body_html": f"<p><em>Placeholder</em> para la sección <code>{s}</code>. En generación real, aquí irán 150-400 palabras editoriales con datos específicos de {page.market_label}.</p>"}
            for s in page.section_template if s not in ("faq", "como-encaja-pulpo")
        ],
        "faq": [
            {"q": "¿Esto es contenido real?", "a": "No. Es un stub generado en modo dry-run para validar el renderer."},
            {"q": "¿Cuándo será real?", "a": "Cuando se ejecute con ANTHROPIC_API_KEY y sin --dry-run."},
            {"q": "¿Cómo me ayuda Pulpo aquí?", "a": "Pulpo soporta gestión documental, control de gasto y telemática. En esta página real verás casos de uso concretos."},
            {"q": "¿Esta página está indexada?", "a": "No. Las páginas en stub arrancan en noindex hasta cumplir threshold."},
        ],
        "pulpo_box": {
            "heading": "Cómo encaja Pulpo aquí",
            "body_html": '<p><strong>STUB.</strong> En generación real, este bloque conecta el tema de la página con Pulpo de manera editorial. Más en <a href="https://www.getpulpo.com/">getpulpo.com</a>.</p>',
        },
        "keywords_seo": [page.topic_code, page.market_code, "flotas", "gestión flota", "fleet management"],
    }


def write_tracking_md(page: PillarPage, indexed: bool, llm_meta: dict) -> Path:
    """Escribe content/pillar-matrix/pages/<slug>.md con frontmatter."""
    PAGES_DIR.mkdir(parents=True, exist_ok=True)
    md_path = PAGES_DIR / f"{page.slug}.md"
    today = dt.date.today().isoformat()
    frontmatter = {
        "slug": page.slug,
        "dimension": page.dimension,
        "market": page.market_code,
        "topic_code": page.topic_code,
        "intent": page.intent_code,
        "tier": page.tier,
        "schema_type": page.schema_type,
        "pulpopay_relevant": page.pulpopay_relevant,
        "indexed": indexed,
        "last_generated": today,
        "generation_mode": llm_meta.get("mode", "stub"),
        "model": llm_meta.get("model", ""),
        "review_days": page.review_days,
        "paused": False,
        "forced_index": False,
    }
    content = "---\n" + yaml.safe_dump(frontmatter, allow_unicode=True, sort_keys=False) + "---\n"
    content += f"\n# {page.label}\n\nMetadata de tracking. El HTML vive en `{page.url_path()}`.\n"
    md_path.write_text(content, encoding="utf-8")
    return md_path


def generate_one(page: PillarPage, dry_run: bool = False, indexed: bool = False) -> dict:
    """Genera UNA pillar page. Devuelve resumen."""
    system_prompt = PROMPT_PATH.read_text(encoding="utf-8")
    user_prompt = build_user_prompt(page)

    if dry_run or not os.environ.get("ANTHROPIC_API_KEY"):
        editorial = stub_editorial(page)
        llm_meta = {"mode": "stub", "model": ""}
    else:
        try:
            editorial = call_llm(system_prompt, user_prompt)
            cfg = config()
            llm_meta = {"mode": "llm", "model": cfg.get("compose", {}).get("model_primary", "")}
        except Exception as e:
            return {"slug": page.slug, "status": "error", "error": str(e)}

    # Resolver related links contra todas las páginas
    all_pages = enumerate_pages()
    related = related_pages(page, all_pages, limit_per_group=4)

    # Render HTML
    html = render_pillar_page(page, editorial, related, indexed=indexed)

    # Escribir HTML
    rel_path = page.url_path().strip("/").rstrip("/")
    html_path = ROOT / rel_path / "index.html"
    html_path.parent.mkdir(parents=True, exist_ok=True)
    html_path.write_text(html, encoding="utf-8")

    # Tracking .md
    md_path = write_tracking_md(page, indexed, llm_meta)

    return {
        "slug": page.slug,
        "status": "ok",
        "mode": llm_meta["mode"],
        "indexed": indexed,
        "html": str(html_path.relative_to(ROOT)),
        "md": str(md_path.relative_to(ROOT)),
        "words": _estimate_words(editorial),
    }


def _estimate_words(editorial: dict) -> int:
    total = 0
    for txt in [editorial.get("intro", ""), editorial.get("h1", "")]:
        total += len(txt.split())
    for s in editorial.get("sections", []):
        total += len(s.get("body_html", "").split())
    for f in editorial.get("faq", []):
        total += len(f.get("a", "").split())
    return total


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--slug", help="Generar solo este slug")
    p.add_argument("--tier", type=int, choices=[1, 2, 3])
    p.add_argument("--dimension", choices=["topic", "use-case", "vertical", "subgeo"])
    p.add_argument("--market")
    p.add_argument("--dry-run", action="store_true", help="Usa stub fixture, sin LLM real")
    p.add_argument("--indexed", action="store_true", help="Publica sin noindex (default: noindex)")
    p.add_argument("--limit", type=int, help="Límite de páginas a generar (para tests)")
    args = p.parse_args(argv)

    all_pages = enumerate_pages()
    pages = all_pages

    if args.slug:
        pages = [p for p in pages if p.slug == args.slug]
        if not pages:
            print(f"❌ slug '{args.slug}' no encontrado")
            return 1
    else:
        if args.tier:
            pages = [p for p in pages if p.tier == args.tier]
        if args.dimension:
            pages = [p for p in pages if p.dimension == args.dimension]
        if args.market:
            pages = [p for p in pages if p.market_code == args.market]

    if args.limit:
        pages = pages[:args.limit]

    print(f"Páginas a generar: {len(pages)}")
    if not pages:
        return 0

    results = []
    for i, p in enumerate(pages, 1):
        print(f"  [{i:>3}/{len(pages)}] {p.slug} ({p.dimension} · {p.market_label}) …", end=" ", flush=True)
        r = generate_one(p, dry_run=args.dry_run, indexed=args.indexed)
        if r["status"] == "ok":
            print(f"✅ {r['mode']} · {r.get('words', 0)}w")
        else:
            print(f"❌ {r.get('error', 'error')}")
        results.append(r)

    ok = sum(1 for r in results if r["status"] == "ok")
    err = len(results) - ok
    print(f"\nTotal: {ok} ok, {err} errores.")
    return 0 if err == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
