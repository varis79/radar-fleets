# The Fleet Radar · Sistema actual

Qué hace el sistema hoy. Si está aquí, está funcionando en producción.
Las ideas que no están aquí viven en `/roadmap.md`.

Última revisión: 2026-05-21.

---

## Visión de 30 segundos

The Fleet Radar es un semanal editorial autónomo sobre gestión de flotas.
Se publica cada lunes a las 07:07 hora Madrid. El pipeline corre solo en
GitHub Actions, sin intervención humana en el flujo principal: ingesta
14 fuentes RSS, clasifica, dedupe, selecciona, compone con Claude, valida
QA, publica HTML en `thefleetradar.com` (Vercel) y notifica a Slack si
hay webhook configurado.

---

## Stack

| Capa | Tecnología |
|---|---|
| Hosting | Vercel (static export) |
| Dominio | thefleetradar.com |
| CI/CD | GitHub Actions |
| Pipeline | Python 3.11 |
| LLM compose | Anthropic Claude Opus 4.1 (fallback Sonnet 4.5) |
| Datos | JSONL + Markdown en repo (sin DB) |
| Editorial | HTML estático generado por templates |

---

## Pipeline semanal

Orquestado por `scripts/pipeline.py`. Cron `'7 5 * * 1'` UTC.

### 1. Ingest · `scripts/ingest.py`
- Lee 14 fuentes RSS de `pipeline-config.yml > sources`.
- Ventana: últimos 8 días.
- Máximo 30 items por fuente.
- Output: `content/raw/YYYY-WW-raw.jsonl`.
- Limpia utm_* y fragmentos de URLs.
- User-Agent identificable como `TheFleetRadarBot/1.0`.

Fuentes actuales (mayo 2026):
- **USA**: FleetOwner, FreightWaves, Transport Topics, Trucking Dive, Supply Chain Dive, Smart Cities Dive, Electrek.
- **Europa**: Transport & Energy.
- **España**: Fleet People ES, AECOC.
- **México**: T21 MX, Mundo Logístico MX.
- **Global EV**: Inside EVs, CleanTechnica · Clean Transport.
- **Google News (queries activas)**: 10 búsquedas Pulpo-relevantes MX/ES sobre telemática, fuel cards, electrificación, última milla, regulación, mantenimiento, ITV, V-16, ZBE, renting, vehículos comerciales.

### 2. Classify · `scripts/classify.py`
- Determinístico: keyword match con word-boundary Unicode (evita falsos positivos como 'epa' en 'preparación').
- Asigna por item: `topic`, `market`, `fleet_type`, `players`, `micro_tags`.
- Market scoring: matches en título cuentan ×2, en summary ×1. Gana el más puntuado.
- Players cargados desde `content/taxonomy/players.md`.
- 22 topics actuales (telematica, fuel-cards, mantenimiento, electrificacion-flotas, compliance, autonomous-trucking, tariffs-trade, rail-freight, freight-market, labor-shortage, cargo-theft, truck-oem, movilidad-urbana, logistica-distribucion, insurance, etc.).
- 9 fleet_types (transporte-pesado, vehiculos-comerciales-ligeros, pickups-utilitarios, reparto-ultima-milla, field-service, ambulancias-emergencias, construccion, mineria, flotas-corporativas).
- 13 mercados (mexico, espana, usa, china, europa, canada, latam, colombia, brasil, chile, peru, argentina, global).

### 3. Dedupe · `scripts/dedupe.py`
- URL canónica (sin utm_*).
- Fuzzy title con SequenceMatcher (umbral 0.82).
- Output: `content/raw/YYYY-WW-dedup.jsonl`.

### 4. Select · `scripts/select.py`
- **Filtra competidores** (`competitor_blacklist`): cualquier item que mencione un competidor (Mendel, Edenred, Repsol, Pluxee, Minu, Solred, Ticket Car, GoPass, Efecticard, Efectivale, Gosmo, Uvicuo, etc.) se excluye antes del scoring. Word-boundary case-insensitive.
- Filtra contra `editorial-memory.md` (8 ediciones recientes, umbral 0.85).
- Scoring por item (pesos configurables en `selection.scoring`):
  - Topic match + boost si está en `topic_priority_list`.
  - Market: primary (MX/ES) 1.2, USA/China 0.4, Europa/Canada 0.3, otros 0.15.
  - Players: base 0.5 + 0.1 por cada jugador extra.
  - Fleet_type: 0.3 + boost si está en `fleet_type_priority_list`.
  - Recency: bonus máx 2.0 que decae 0.2/día.
- Aplica `topic_quotas` (máximos por topic; tariffs-trade=1, rail-freight=0, etc.).
- Aplica `geo_quotas` (buckets primary 7-10, secondary USA 1-2, china 1, other 0-2).
- Modo `normal` (12 historias) / `short` (9) / `pause` (sin material suficiente).
- Output: `content/decisions/YYYY-WW-selection.json` (incluye `discarded_competitor` + `discarded_repetition` para auditoría).

### 5. Compose · `scripts/compose.py`
- Una sola llamada al LLM con system prompt `prompts/radar-master-prompt.md` (la "constitución editorial").
- User prompt construido desde la selección + plantillas de longitud (palabras por sección).
- Modelo primario: `claude-opus-4-1-20250805`. Fallback: `claude-sonnet-4-5-20250929`.
- Devuelve JSON con: `cover_headline`, `cover_deck`, `editors_body`, `wm_cards[]`, `stories[]`, `opinion_quote`, `opinion_body`, `cta_headline`, `slack_summary`, etc.
- Aplica paleta de acento semanal (rotación de 6).
- Renderiza HTML completo con `scripts/lib/templating.py`.
- Output: `magazines/YYYY-MM-DD-radar-fleet-by-pulpo.html` + summary.txt.
- Fallback `stub` sin API key: genera placeholder. QA lo detectaría y `pause`.

### 6. QA · `scripts/qa.py`
- 9 chequeos: framing interno, contenido fino, voz editorial, meta, estructura, links internos, repetición, claims, stub marker.
- **Informativo, nunca bloquea publicación** (decisión 2026-04-27). Genera informe en `content/qa/YYYY-WW-report.md`.
- Status `ok-qa-warn` si hay avisos; `ok` si limpio.

### 7. Publish · `scripts/publish.py`
- Actualiza `index.html` (copia de la edición más reciente).
- Actualiza `archive.html` añadiendo fila.
- Actualiza `sitemap.xml` y `rss.xml`.
- Append en `content/editorial-memory.md` (historias cubiertas).

### 8. Notify · `scripts/notify.py`
- Postea a `SLACK_WEBHOOK_URL` el resumen Slack generado por compose.
- Si secret no existe, salta silenciosamente.

---

## Workflow de GitHub Actions

### `weekly-edition.yml`
Cron lunes 05:07 UTC. Pasos:
1. Checkout main.
2. Setup Python + cache pip + install deps.
3. Calcula fecha edición (próximo lunes).
4. Crea branch `claude/edition-YYYY-MM-DD-{runid}`.
5. Corre `python -m scripts.pipeline`.
6. Commit + push branch.
7. Crea PR con label según status (ready-to-review, needs-editorial-fix, editorial-pause, pipeline-error).
8. Auto-merge si status ∈ {ok, ok-qa-warn}.
9. **Trigger Vercel deploy hook** (post-merge).
10. **Smoke test live edition**: reintenta 8×20s curl a la URL final. Falla si 404.

### `weekly-deploy-canary.yml`
Cron martes 08:00 UTC. Verifica que la URL de la edición de la semana ISO responde HTTP 200. Si no, abre Issue con label `deploy-down` (y opcionalmente notifica a `SLACK_WEBHOOK_ALERTS_URL`).

---

## Identidad editorial

### Diseño
- CSS único en `assets/radar.css`. Variación semanal vía 4 vars de color (`--accent`, `--accent-2`, `--cover-grad-a`, `--cover-grad-b`).
- Tipografía: Fraunces (cabeceras) + Inter (body).
- Paleta base: navy + graphite + cream + warm-sand.
- 11 componentes visuales fijos: cover, editors-note, wm-card, story-grid, signal-card, radar-item, trend-card, data-card, opinion-quote, cta-band, closing.

### Voz
- Reglas en `prompts/radar-master-prompt.md` (la constitución editorial). Inmutable salvo cambio deliberado.
- Prohibidos absolutos (lista en `scripts/lib/forbidden.py`): "competidor", "Para Pulpo", "argumento comercial", em-dashes en prosa (máx 1 por edición), construcciones "no es X, es Y".

---

## Estructura del sitio

```
/                           ← index.html (copia de la última edición)
/archive.html               ← listado de ediciones
/magazines/YYYY-MM-DD-…html ← una por edición
/mercados/{mexico,espana,latam}/
/temas/{fuel-cards,electrificacion-flotas,compliance-espana,regulacion-mexico}/
/players/pulpo/
/evergreen/guias/peaje-europa-2026/
/evergreen/checklists/evaluar-telematica-2026/
/404.html
/rss.xml
/sitemap.xml
```

---

## Taxonomía

En `content/taxonomy/`:
- `topics.md` — 13 temas editoriales originales (más los nuevos del classifier).
- `players.md` — ~80 fichas (Pulpo, WEX, Geotab, Samsara, Motive, etc.).
- `markets.md` — 11 geografías.
- `fleet-types.md` — 9 clusters operativos.
- `micro-tags.md` — vocabulario controlado con prefijos.
- `slug-rules.md` — convenciones de URL.

---

## Secrets esperados en GitHub Actions

Ver `docs/SECRETS.md`:
- `ANTHROPIC_API_KEY` (obligatorio).
- `VERCEL_DEPLOY_HOOK` (resiliencia).
- `SLACK_WEBHOOK_URL` (notificación publicación, opcional).
- `SLACK_WEBHOOK_ALERTS_URL` (alertas canary, opcional).

---

## Datos persistentes en el repo

- `content/raw/` — items ingestados, clasificados, deduplicados (JSONL por semana).
- `content/decisions/` — selección final + slack summary + compose info.
- `content/qa/` — informes QA por semana.
- `content/editorial-memory.md` — append-only de qué se cubrió cuando.
- `content/market-watch.md` — watchlist de temas a vigilar (manual).
- `content/pulpo-update.md` — input para sección Desde Pulpo (manual).
- `content/pulpo-facts.md` — facts durables Pulpo (manual).

---

## Lo que NO está automatizado (todavía)

Ver `/roadmap.md`. Resumen:
- Formulario abierto para sugerir noticias (ahora todo viene de RSS).
- SEO masivo + interlinking dinámico.
- Versión EN.
- Cajas "Sabías qué" y "Pulpo destaca".
- Integración LinkedIn / redes sociales.
- Newsletter por email.
- Curación pre-select con LLM.
- Fuentes activas no-RSS (Google News, scraping).
