# The Fleet Radar · MVP autónomo

Este documento describe el MVP del sistema editorial autónomo. Cubre qué hace el pipeline, cómo corre, qué archivos genera y qué hacer cuando falla. Está escrito para que alguien que llegue al repo dentro de 6 meses entienda el sistema sin leer código.

## Qué hace el MVP

Cada lunes a las 05:07 UTC (~07:07 Madrid CEST, ~06:07 CET) el sistema:

1. Ingesta noticias de una lista curada de fuentes RSS/Atom.
2. Clasifica cada item con la taxonomía interna (topic, market, fleet_type, players, micro-tags).
3. Deduplica por URL canónica y similitud de título.
4. Selecciona las historias que merecen entrar en la edición y decide modo (`normal` | `short` | `pause`).
5. Compone la edición completa en HTML (vía Claude con el master prompt).
6. Pasa la edición por QA bloqueante.
7. Actualiza `index.html`, `archive.html`, `sitemap.xml`, `rss.xml` y `editorial-memory.md`.
8. Abre un PR contra `main` con label según el resultado. **Sin auto-merge.**

## Cómo corre

**Automático:**

- Workflow: `.github/workflows/weekly-edition.yml`.
- Dispara con cron `'7 5 * * 1'`.
- Requisito: secret `ANTHROPIC_API_KEY` en el repo (Settings → Secrets → Actions).

**Manual (dry run y pruebas):**

- Desde GitHub UI → Actions → `Radar Fleet — Weekly edition` → Run workflow.
- Inputs opcionales: `edition_date` (forzar fecha), `allow_stub` (no usado aún).

**Local (desarrollo):**

```bash
pip install -r requirements.txt
python -m scripts.pipeline [--date YYYY-MM-DD]
```

Si no hay `ANTHROPIC_API_KEY`, compose produce un stub etiquetado que QA **siempre** bloquea. Útil para probar que el pipeline corre sin gastar API.

## Archivos tocados

**Pipeline (`scripts/`):**

| Archivo | Responsabilidad |
|---|---|
| `scripts/ingest.py` | Lee fuentes RSS de `pipeline-config.yml`, filtra por ventana temporal, genera `content/raw/YYYY-WW-raw.jsonl` |
| `scripts/classify.py` | Etiqueta cada item con topic/market/fleet_type/players/micro-tags (determinístico, keywords) |
| `scripts/dedupe.py` | Fusiona items por URL canónica y por similitud de título dentro del mismo topic+market |
| `scripts/select.py` | Decide modo y elige historias. Compara contra memoria editorial para evitar repetición |
| `scripts/compose.py` | Llama a Claude con el master prompt. Renderiza HTML + summary |
| `scripts/qa.py` | 9 checks bloqueantes + 2 avisos. Escribe informe en `content/qa/` |
| `scripts/publish.py` | Actualiza index, archive, sitemap, rss y memoria editorial |
| `scripts/pipeline.py` | Orquestador (un solo entrypoint) |
| `scripts/lib/config.py` | Carga `pipeline-config.yml` |
| `scripts/lib/paths.py` | Rutas canónicas del repo |
| `scripts/lib/forbidden.py` | Lista regex de framing interno prohibido |
| `scripts/lib/templating.py` | Render del HTML de edición |

**Config:**

- `pipeline-config.yml` — fuentes, umbrales, paletas, keywords. Único sitio con parámetros.
- `prompts/radar-master-prompt.md` — reglas editoriales que Claude recibe como system prompt.
- `prompts/qa-checklist.md` — documentación de los checks de QA.

**Artefactos de ejecución (no código, versionados):**

- `content/raw/YYYY-WW-raw.jsonl` — items ingestados.
- `content/raw/YYYY-WW-classified.jsonl` — items clasificados.
- `content/raw/YYYY-WW-dedup.jsonl` — items deduplicados.
- `content/decisions/YYYY-WW-selection.json` — selección editorial.
- `content/decisions/YYYY-WW-compose.json` — metadatos de la composición.
- `content/qa/YYYY-WW-report.md` — informe QA legible.

**Salidas publicadas:**

- `magazines/YYYY-MM-DD-radar-fleet-by-pulpo.html`
- `magazines/YYYY-MM-DD-radar-fleet-by-pulpo-summary.txt`
- `index.html`, `archive.html`, `sitemap.xml`, `rss.xml`, `content/editorial-memory.md` (todos actualizados).

## Qué checks bloquean la publicación

Ver `prompts/qa-checklist.md` para la lista completa. Resumen:

| Check | Qué mira | Bloquea |
|---|---|---|
| C1 framing | Expresiones prohibidas (competidor, Para Pulpo, argumento comercial, etc.) | Sí |
| C2 thin | Edición demasiado corta o stories con <120 palabras | Sí |
| C3 voice | Em dashes en prosa, "no es X, es Y" | Sí |
| C4 meta | title, description, canonical, og:url, article:published_time | Sí |
| C5 structure | H1 único, cover / editors-note / cta / closing presentes | Sí |
| C6 links | Enlaces internos rotos | Sí |
| C7 repetition | Headline cover muy similar a ediciones recientes | Sí |
| C8 claims | Afirmaciones absolutas sin fuente | Sí |
| C9 stub | Marker `[stub:` presente | Sí |
| A1 geo mix | Ratio MX+ES bajo | Aviso |
| A2 topics | Pocos topics distintos | Aviso |

## Qué queda fuera del MVP

- **Auto-merge**. Siempre PR revisado por humano.
- **Refresh mensual/trimestral de páginas**.
- **Newsletter**.
- **Versión en inglés** (y `hreflang`).
- **Comparativas y nuevas páginas públicas**. Ninguna página nueva se crea por el pipeline.
- **Clasificación por LLM**. Hoy es determinística por keywords.
- **Embeddings o vector search** para dedup.
- **Check de enlaces externos** (HEAD HTTP). No lo hacemos aún; sumar latencia a Actions sin gran valor.
- **Issues estratégicos automáticos** para decisiones editoriales. El sistema aún no te abre Issues cuando detecta un candidato a página nueva o un cambio de cobertura. Queda para Fase 2.

## Cómo se interpreta un fallo del pipeline

**PR con label `ready-to-review`**
QA pasó. Revisa preview de Vercel, revisa el PR body y mergea cuando te cuadre.

**PR con label `needs-editorial-fix`**
QA bloqueó. Abre `content/qa/YYYY-WW-report.md` en la rama: lista exacta de lo que falla. Opciones:
1. Corregir a mano el HTML en la propia rama y volver a pasar QA local.
2. Ajustar `pipeline-config.yml` si el problema es de umbrales (raro; hay que pensarlo).
3. Cerrar el PR y relanzar `workflow_dispatch` tras ajustar reglas si es un falso positivo.

**PR con label `editorial-pause`**
El pipeline detectó que no había material suficiente para publicar. No tocó el sitio. El PR lo único que trae son artefactos de trazabilidad en `content/raw/`, `content/decisions/` y una nota de pausa en `editorial-memory.md`. Mergear es opcional (solo sirve para preservar logs); cerrar también está bien.

**PR con label `pipeline-error`**
Hubo una excepción o status inesperado. Mira `pipeline-output.json` en la rama. Causas típicas: fuente RSS caída, API timeout, secret `ANTHROPIC_API_KEY` ausente. Es un fallo técnico, no editorial.

## Seguridad y límites

- **Datos**: todas las fuentes son públicas (RSS/Atom de medios). No hay PII, no hay scraping agresivo.
- **Secrets**: solo `ANTHROPIC_API_KEY`. Nunca aparece en logs ni en archivos versionados.
- **Coste**: una ejecución típica = ~1 llamada a Claude Opus con ~6-8k tokens de contexto y ~4-6k de output. Unos $0.15–0.30 por edición.
- **Runtime**: workflow ~4-8 minutos en GitHub Actions.
- **Idempotencia**: si se lanza dos veces la misma semana, la segunda ejecución sobrescribe los artefactos de la primera. El PR abre con otra rama (`claude/edition-<fecha>-<runid>`) distinta, así que no hay colisión.

## Siguiente paso recomendado tras mergear este MVP

1. Añadir el secret `ANTHROPIC_API_KEY` en GitHub (Settings → Secrets → Actions).
2. Correr manualmente el workflow con `workflow_dispatch` una primera vez para verificar end-to-end en la infra real.
3. Revisar el PR que abra. Si QA marca cosas razonables, ajustar reglas; si marca falsos positivos, añadir excepciones específicas.
4. Dejar correr una semana sin tocar. Si el lunes siguiente sale un PR con label `ready-to-review` sin intervención, el MVP está en producción.

## Limitaciones conocidas

- **Fuentes dependen de que los sites tengan RSS**. Añadir nuevas fuentes = editar `pipeline-config.yml` y re-commit.
- **Clasificación por keywords** tiene falsos positivos/negativos. Basta para MVP, pero hay que mantener la lista de keywords con cabeza.
- **Dedup fuzzy** puede dejar pasar items del mismo hecho si el título cambia mucho. Umbral ajustable en config.
- **Select no garantiza** 10 historias si ingest vino flojo. Ahí es cuando el modo `short` o `pause` actúan.
- **LLM redacta stories** a partir de la selección, pero su contexto es el summary del feed RSS. Si el RSS da poco, la redacción sufre. En esos casos QA C2 (thin) tiende a disparar. Es la intención.
