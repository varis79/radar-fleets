# The Fleet Radar · Roadmap

Documento vivo. Va por delante del repo: aquí van ideas antes de tener PR.
Cuando una idea llega a producción, se mueve a `docs/SYSTEM.md` y se marca aquí
como `[done]` con el commit/PR de aterrizaje.

Última revisión: 2026-05-21 (post-N°8).

---

## En curso

| ID | Idea | Estado | Notas |
|---|---|---|---|
| C-1 | Reparto editorial MX/ES dominante + cuotas USA/China/EU | PR abierto `claude/curation-usa-and-sources` | Reparto 12: 7-8 MX/ES, 2 USA, 1 China, 1-2 EU. Boost editorial a topics operativos. Pendiente merge. |
| C-2 | Google News RSS por queries Pulpo-relevantes | PR abierto `claude/curation-usa-and-sources` (5º commit) | 10 queries MX/ES sobre telemática, fuel cards, electrificación, última milla, regulación, mantenimiento, vehículos. ~110-140 items extra/semana. Cero coste. |
| C-3 | Filtro de competidores | PR abierto `claude/curation-usa-and-sources` (5º commit) | 17 nombres en blacklist (Mendel, Edenred, Repsol, Pluxee, Minu, Solred, Ticket Car, GoPass, Efecticard, Efectivale, Gosmo, Uvicuo, etc.) se excluyen del pool antes del scoring. |

## Backlog ordenado (alta prioridad → baja)

### 1. Formulario abierto · GitHub Issue template
**Estado:** propuesto.
**Problema que resuelve:** escasez crónica de material MX/ES; queremos que tú (Varis) o cualquiera del equipo pegue noticias curadas (Perplexity, Gemini, lectura humana) y entren al pipeline con filtros.
**Diseño tentativo:**
- Issue template "Nueva noticia sugerida" en `.github/ISSUE_TEMPLATE/sugerir-noticia.md` con campos: URL, headline propuesto, geo, topic sugerido, fuente original, fecha aproximada, motivación editorial.
- Nuevo step `scripts/ingest_suggestions.py` que el lunes lee issues abiertos con label `noticia-sugerida`, los normaliza al formato JSONL del pipeline, descarta los que:
  - tienen URL ya presente en editorial-memory,
  - tienen headline con >85% similitud contra titulares pasados,
  - parecen basura (sin URL válida, < 60 chars de descripción).
- Tras el merge semanal, los issues procesados se cierran automáticamente con un comentario "Incluido en N°X · ok / Descartado · razón".
**Por qué crítica:** desbloquea cobertura Pulpo-céntrica (telco fleet, LCV, last-mile, mantenimiento) que las fuentes RSS actuales no entregan.

### 2. SEO masivo + interlinking (NEXT — arrancamos en próxima sesión)

**Estado:** plan confirmado 2026-05-21, pendiente ejecución.

**Objetivo:** que The Fleet Radar (a) posicione bien en Google MX/ES (b) sea fuente citable en LLMs (ChatGPT, Perplexity, Claude, Gemini) (c) genere tráfico orgánico recurrente para Pulpo.

**Plan en 3 sub-PRs:**

#### PR-SEO-1 · Fundamentos técnicos (sesión 1, ~3h)
- Auditoría meta tags página por página (title, description, OG, Twitter, canonical, hreflang).
- Schema.org markup:
  - `NewsArticle` por edición (autor, datePublished, dateModified, organización, sección, image).
  - `Organization` (Pulpo + The Fleet Radar).
  - `WebSite` con `SearchAction` (caja Google Sitelinks search box).
  - `BreadcrumbList` en hubs y páginas internas.
- robots.txt explícito permitiendo crawlers de IA: GPTBot, ClaudeBot, anthropic-ai, PerplexityBot, ChatGPT-User, Google-Extended, Cohere-AI, Bytespider.
- Sitemap con changefreq/priority calibrados.
- Internal linking automático en compose: cuando una historia menciona topic/market/player con hub, se enlaza al hub.

#### PR-SEO-2 · Hubs enriquecidos con LLM (sesión 2, ~4h)
- Cada hub (`/mercados/*`, `/temas/*`, `/players/*`, `/evergreen/*`) se enriquece:
  - Síntesis temática generada por LLM (cada publish actualiza solo los hubs afectados).
  - Listado autoactualizable de historias relacionadas con snippet + enlace.
  - Datos clave / hitos en formato citable (listas, tablas).
  - "Páginas relacionadas" hacia otros hubs cercanos.
- Coste extra LLM: ~$0.10/semana.

#### PR-SEO-3 · Sistema vivo de páginas pilar (sesión 3+, varios sprints)

**Filosofía:** trabajo manual cero por defecto. LLM hace todo el ciclo de vida.
Intervención humana solo como vía de override via GitHub Web.

**Templates de páginas a generar** (cluster de keywords MX/ES):
- Geo+Topic: "Telemática para flotas en México 2026", "Tarjetas de combustible España 2026", "Electrificación flotas en CDMX", "Última milla España", "ITV camiones 2026".
- Vehicle-type+Geo: "Furgonetas eléctricas flota España", "Pickups flota México", "Vans last mile España".
- Regulación específica: "DGT V-16 obligación 2026", "Tacógrafo G2V2 España", "SICT México telemática hidrocarburos", "ZBE Madrid flotas comerciales", "T-MEC autotransporte".
- Comparativa marca-mercado: "Geotab vs Samsara vs Webfleet México", "Marcas telemática España" (sin competidores Pulpo).
- Sectores verticales: "Flotas cementeras México", "Flotas mineras LatAm", "Flotas telco España", "Flotas utilities ibericas", "Flotas alimentación última milla".
- Evergreen guías: "Cómo evaluar telemática 2026", "Peajes Europa 2026", "Renting vs leasing flota empresa".

---

**Subsistema 1 · Generación inicial (one-shot al lanzar)**
Cada página pilar nace de un `.md` en `content/pillar-pages/<slug>.md` con metadata:
```yaml
slug: telematica-flotas-mexico-2026
title_es: "Telemática para flotas en México 2026"
keyword_principal: "telemática flotas méxico"
intent: informational
sub_topics: [definicion, regulacion-cne, mercado-mx, casos-uso, comparativa]
data_overrides: {}    # campos para forzar datos propios cuando quieras
paused: false         # true = no regenerar automáticamente
forced_index: false   # true = saltarse threshold y publicar ya
```
Claude Opus genera HTML completo (~800-1500 palabras) basado en:
- Historias relacionadas existentes en `editorial-memory.md`.
- Conocimiento general del LLM sobre el tema.
- Estructura definida (intro, sub-secciones, FAQ, data box, schema.org Article).

Coste: ~$3-5 una sola vez para las 80-100 páginas iniciales.

---

**Subsistema 2 · Updates automáticos en cada publish semanal**
En cada `publish.py`:
1. Para cada historia de la edición, identificar páginas pilar relacionadas vía mapping topic/market/player.
2. Para cada página pilar afectada (no paused):
   - LLM evalúa si la nueva historia cambia el análisis principal.
   - Si sí, regenera sólo las 1-2 secciones afectadas (eficiente).
   - Si no, sólo añade snippet en sección "Últimas relacionadas".

Coste: ~$0.20-0.50/semana.

---

**Subsistema 3 · Liberación automática noindex → index**
Job semanal (junto al pipeline o canary martes):
- Evalúa cada página en noindex.
- Criterios de liberación (≥1 cumplido):
  - **3+ historias** relacionadas en `editorial-memory.md`.
  - **Score LLM publicable**: verificador LLM puntúa la página ≥7/10 en {longitud, estructura, factualidad, valor lector, unicidad vs otras páginas}.
  - **`forced_index: true`** en el `.md` (override manual).
- Si cumple, cambio automático a `index, follow` + add al sitemap + commit dispatch + Vercel deploy.

Coste: ~$0.10/semana.

---

**Subsistema 4 · Detección automática de huecos**
Job semanal: analiza historias publicadas sin página pilar asociada.
Si encuentra clusters (3+ historias sobre el mismo tema sin página existente), abre un **GitHub Issue** con label `pillar-page-suggested`:

> Detectados 4 historias sobre ZBE Sevilla en últimas 6 ediciones. Propuesta de nueva página pilar:
> - slug: `zbe-sevilla-flotas-comerciales`
> - keyword: "ZBE Sevilla flotas"
> - sub-topics propuestos: [...]
>
> Responde con `/approve` para generar, `/reject` para descartar.

Usuario comenta `/approve` → workflow lee el comentario, crea el `.md`, dispara la generación inicial vía subsistema 1.

Coste: ~$0.05/semana.

---

**Subsistema 5 · Verificador LLM interno (paz mental)**
Antes de cualquier publicación o liberación, LLM separado revisa el contenido:
- Detecta claims sospechosos sin fuente.
- Detecta estadísticas exactas no respaldadas.
- Detecta posibles errores factuales conocidos.

Si detecta problemas, marca la página con label `needs-review` y NO se libera. Issue creado para revisión humana.

Coste: ~$0.20/sem (incluido en otros costes).

---

**Subsistema 6 · Disclaimer transparente**
Footer discreto en páginas autogeneradas:

> Esta página recopila y sintetiza información pública sobre [tema] usando las ediciones semanales de The Fleet Radar y fuentes citadas. ¿Detectas un dato incorrecto? [Repórtalo en GitHub](link).

Aporta transparencia, permite feedback de lectores. No afecta SEO.

---

**Panel admin = GitHub Web**
- Cada página pilar es un `.md` editable en `content/pillar-pages/<slug>.md`.
- Editar en github.dev (web) o github.com directamente.
- Campos del `.md`:
  - `paused: true` → pausa regeneración automática.
  - `forced_index: true` → fuerza liberación inmediata.
  - `data_overrides: {key: value}` → datos propios que el LLM debe usar (estadísticas Pulpo, fuentes confidenciales, etc.).
  - `manual_intro: |` → texto introductorio escrito por humano (sobrescribe el del LLM).
- Sin auth nueva, sin infra nueva.

---

**Trabajo manual REAL en este modelo**

| Tarea | Frecuencia |
|---|---|
| Comentar `/approve` en issues de nuevas páginas sugeridas | 1-2/semana al principio, menos después |
| Revisar issues con label `needs-review` (verificador detectó algo) | Cuando ocurra |
| Editar `.md` para forzar liberación o añadir dato propio | Opcional |
| **Todo lo demás** | **Automático** |

**Coste total mensual estimado:** ~$3-5/mes recurrente + $3-5 one-shot al lanzar.

---

**Decisión multi-idioma confirmada:**
- ES primero (todo el plan).
- EN después, replicando estructura.
- URLs separadas: `thefleetradar.com/...` (ES default) y `thefleetradar.com/en/...` (EN).
- `hreflang` x-default + es + en por página.
- Selector visual en header.
- Sugerencia (no redirect forzado) por IP en primera visita; cookie de preferencia.

**Outcome esperado:**
- Mes 1-2: indexación inicial + 10-20 páginas liberadas.
- Mes 3-4: ~40-60 páginas indexadas + primeras señales SEO.
- Mes 6+: tráfico orgánico recurrente + citaciones en LLMs.

### 3. Versión en inglés (EN) para mercado US/Int
**Estado:** propuesto, vendrá DESPUÉS del SEO-3 inicial.
**Contexto:** Pulpo va a lanzar en inglés. The Fleet Radar EN da tráfico simultáneo.
**Decisión arquitectónica (alineada con SEO multi-idioma):**
- Estructura URL: `thefleetradar.com/en/...` para EN; `thefleetradar.com/...` para ES (default).
- Cada edición se compone también en EN como `magazines/YYYY-MM-DD-the-fleet-radar.html` (slug EN).
- Un solo `compose` LLM con prompt que devuelve `{es: {...}, en: {...}}`. O dos calls separadas para mejor calidad por idioma; a decidir cuando arranquemos.
- `hreflang` x-default + es + en por página.
- Selector visual de idioma en topbar.
- Sugerencia (no redirect) por IP en primera visita + cookie de preferencia.

### 4. Caja "Sabías qué" · facts históricos
**Estado:** propuesto.
**Diseño:**
- `content/facts-history.md` con array de facts curados por ti (1 por entrada, 1-2 frases).
- Cada edición elige uno por rotación (no aleatorio para que no se repita).
- Render en componente nuevo `HTML_FACT_BOX` con icono 📜.

### 5. Caja "Pulpo destaca" · feature/funcionalidad
**Estado:** propuesto.
**Diseño:**
- `content/pulpo-features.md` con array de features de Pulpo (1 por entrada, con título + 2-3 frases + URL "saber más" a getpulpo.com).
- Cada edición rota una feature distinta. Si hay menos features que ediciones, repetir manteniendo distancia.
- Render `HTML_PULPO_BOX` con tono editorial discreto (no banner publicitario).

### 6. Integración LinkedIn (canal propio + cuenta Pulpo)
**Estado:** propuesto.
**Problema:** ahora la edición se publica en thefleetradar.com y nadie se entera.
**Decisión arquitectónica pendiente:**
- Opción A: canal LinkedIn dedicado `The Fleet Radar` (página de empresa). Independiente de Pulpo, marca propia.
- Opción B: solo desde cuenta corporativa Pulpo, sin marca separada.
- Opción C (mi recomendación): **híbrido**. Página propia LinkedIn de The Fleet Radar (ES + EN cuando exista versión EN), Y al mismo tiempo el canal Pulpo amplifica cada edición vía repost manual o automático.
**Implementación tentativa:** webhook LinkedIn API → post automático tras merge de cada edición con el `slack_summary` adaptado a 1300 chars.
**Por qué importante:** sin canal de distribución activo, el editorial es un activo SEO pasivo. LinkedIn da tracción B2B inmediata al mundo Pulpo.

### 7. Newsletter por email
**Estado:** propuesto.
**Pendiente:**
- Proveedor: Resend (técnico, barato), Buttondown (simple), ConvertKit (marketing). Decidir cuando arranquemos.
- Caja opt-in en footer + en cada edición.
- Cron domingo o lunes envía la edición a la lista.
- Versión también en EN cuando exista.

---

## Ideas en exploración (sin compromiso aún)

- Pre-select con LLM (curación con Claude sobre los 50-100 items antes del scoring determinístico). Filtra ruido editorial sin codear keywords.
- Búsquedas activas Google News con queries específicas (autoamplía cobertura MX/ES sin depender de RSS).
- Scraping ligero de 2-3 sitios sin RSS (Transport Topics, Heavy Duty Trucking, Trans.info).
- API pública `/api/latest.json` para que terceros consuman.
- Sección "Movimientos" semanal: contrataciones senior, inversiones, M&A en el sector.

---

## Hecho

| Fecha | Cambio | Commit/PR |
|---|---|---|
| 2026-05-21 | Sistema autónomo MVP completo (ingest + classify + dedupe + select + compose + qa + publish) | PR #13 |
| 2026-05-21 | Notificación Slack (deshabilitada hasta crear secret) | 642bf1e |
| 2026-05-21 | QA no-bloqueante; siempre publica con avisos | 24be10c |
| 2026-05-21 | Blindaje deploy: Vercel Deploy Hook + smoke test + canary martes | PR `claude/deploy-resilience` |
| 2026-05-21 | Curación USA + fuentes RSS + reparto editorial MX/ES dominante | PR `claude/curation-usa-and-sources` (en curso) |
