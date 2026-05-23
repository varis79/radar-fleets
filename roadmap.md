# The Fleet Radar · Roadmap

Documento vivo. Va por delante del repo: aquí van ideas antes de tener PR.
Cuando una idea llega a producción, se mueve a `docs/SYSTEM.md` y se marca aquí
como `[done]` con el commit/PR de aterrizaje.

Última revisión: 2026-05-22 (post-auditoría externa: Perplexity · DeepSeek · ChatGPT · Gemini).

---

## Post-auditoría 2026-05-22 · Señales fuertes (4/4 IAs)

Origen: `docs/audits/2026-05-22-summary.md`. Solo se listan aquí los ítems
que NO estaban ya en el backlog o que necesitan entrada nueva.

| ID | Tarea | Responsable | Estado |
|---|---|---|---|
| A-1 | Disclaimer PulpoPay en `/temas/fuel-cards/` y `/temas/electrificacion-flotas/` | Técnico (Claude) | ✅ `f5b6fc9` |
| A-2 | Hreflang `es-MX` / `es-ES` en pillar pages y hubs de mercado | Técnico (Claude) | ✅ `f5b6fc9` |
| A-3 | Schema.org `NewsArticle` en las 7 ediciones de `/magazines/` | Técnico (Claude) | ✅ `f5b6fc9` |
| A-4 | Check: ¿aparece el Pulpo box tras artículo operador asesinado (Nº8)? | Técnico (Claude) | ✅ OK — CTA band está tras la opinión editorial, no adyacente al artículo |
| A-5 | Fuentes/citations visibles al pie de 20 páginas prioritarias | Editorial (Varis) | ✅ 5 páginas prioritarias · `e3bd0b0` · expandir a 20 en backlog |
| A-6 | Eliminación de clichés IA-sounding: lista negra en `docs/STYLE-FIXES.md` | Editorial (Varis) | ✅ Doc creado + prompt actualizado · limpieza manual pendiente |
| A-7 | Lead magnets x3: checklist antifraude MX · plantilla coste/vehículo · matriz ZBE+ITV ES | Editorial (Varis) | 🟡 Checklist antifraude MX publicado · `e3bd0b0` · pendiente: plantilla coste/vehículo + matriz ZBE+ITV ES |
| A-8 | Enriquecer country briefs CO, CL, AR, PE con regulación local y players | Editorial (Varis) | Backlog |
| A-9 | **Fleet Fuel Index MX 2026** — reporte con datos anonimizados de los 200k vehículos | Editorial + Datos Pulpo | Exploración |
| A-10 | Rankings de proveedores telemática MX y ES (ventaja: The Fleet Radar no necesita anunciantes) | Editorial | Exploración |
| A-11 | Fleet Operating Benchmarks — publicación anual de benchmarks agregados (coste/vehículo, mantenimiento, combustible por sector) | Editorial + Datos Pulpo | Exploración estratégica |

---

## En curso

| ID | Idea | Estado | Notas |
|---|---|---|---|
| C-4 | PR-SEO-1 · Fundamentos técnicos | PR `claude/seo-1-foundations` | Schema.org, robots LLM bots, internal linking. |
| C-5 | PR-SEO-3.1 · Matriz long-tail (estructura) | PR `claude/seo-3-1-matrix` | **~900 páginas planeadas** en 4 dimensiones: 300 topic + 280 use-case + 184 subgeo + 140 vertical. 14 casos de uso Pulpo con clientes reales (Banorte, DHL, Iberdrola, Bofrost...). 14 sectores. Ciudades MX/ES/AR/CO/CL/PE. Todo arranca en noindex; liberación gradual con threshold. CSV en `content/pillar-matrix/matrix.csv`. |
| C-6 | PR-SEO-3.2 · Sistema interlinking + hubs índices | PR `claude/seo-3-1-matrix` (commit 3) | 4 hubs de dimensión (/temas/, /casos-uso/, /sectores/, /ciudades/) + 10 hubs de mercado dinámicos (México, España + 8 nuevos LatAm). Schema.org CollectionPage + ItemList por hub. Sitemap ampliado a 30 URLs. Diseño hereda radar.css. Helper `related_pages()` en pillar.py para cross-linking automático futuro. |
| C-7 | PR-SEO-3.3 · Generador pillar pages + workflow | PR `claude/seo-3-3-content-t1` | Prompt maestro pillar, renderer HTML con schema.org, script generate_pillar_page.py, workflow GitHub Actions con 3 modos (single/tier/filter), 3 piloto stub generadas. Pendiente: instalar workflow yml desde UI (PAT sin workflow scope) y ejecutar piloto LLM real. |

## Próxima ola SEO-3 (todavía sin implementar)

### PR-SEO-3.4 · Cross-dimension filtrado con typical_use_cases

Combinaciones que cruzan dimensiones (use_case × vertical, fleet_type × market)
generadas solo cuando tiene sentido editorial. Filtro automático: solo se
crean si el use_case está listado en `typical_use_cases` del vertical
(ya definido en verticals.yml).

Ejemplos:
- ✅ `flota-reparto-ultima-milla-en-ecommerce-paqueteria-mexico-2026/` (e-commerce típicamente hace last-mile)
- ✅ `flota-maquinaria-pesada-en-construccion-obra-mexico-2026/` (construcción típicamente usa maquinaria)
- ❌ `flota-maquinaria-pesada-en-ecommerce-...` (ecommerce no usa maquinaria; no se genera)
- ❌ `flota-vehiculos-directivos-en-construccion-...` (no es típico; no se genera)

Volumen estimado: ~180-220 páginas extra (≠ 840 sin filtro).

### PR-SEO-3.5 · Sistema vivo de matriz (auto-detección y expansión)

**La matriz no es estática.** Cada N semanas, un job mensual:

**A) Detecta clusters de historias sin página pilar**
Analiza `editorial-memory.md` y `content/raw/*.jsonl` recientes (12 semanas).
Si encuentra ≥3 historias sobre el mismo tema sin página, abre GitHub Issue:

> Detectados 4 historias sobre ZBE Sevilla en últimas 6 ediciones. Propuesta:
> - slug: `zbe-sevilla-flotas-comerciales`
> - sub-topics propuestos: [...]
> Responde con `/approve` para generar.

**B) Detecta NUEVOS TOPICS emergentes (no en la matriz)**
LLM agrupa headlines por similitud semántica. Si detecta un cluster que NO
mapea a ningún topic existente en `topics.yml`, propone añadirlo:

> Detectado cluster sobre "hidrógeno verde transporte" con 7 historias en
> MX/ES/USA. No existe topic `hidrogeno-verde` en la matriz. Propuesta:
> - Nuevo topic: `hidrogeno-verde`
> - applies_to_markets: [mexico, espana, latam, usa]
> - intents: [informational, guia-practica]
> - tier_modifier: 1 (emergente, sin tracción mainstream aún)
> - 4 nuevas páginas planeadas en T2
> Responde `/approve` para añadir a topics.yml + matrix.csv.

Al aprobar:
- Edita `topics.yml` (commit + PR).
- Las nuevas combinaciones aparecen en `matrix.csv`.
- Disponibles para generación con `generate-pillar-pages.yml`.

**C) Promoción de tier**
Si un topic en T2 acumula ≥10 historias en un mercado → propone T2→T1.

**D) Propuesta de subgeo / ciudad**
Si un cluster menciona repetidamente una ciudad sin slot, propone añadirla
a `subgeographies.yml`.

**E) Propuesta de cross-border / regional**
Detecta historias que cruzan mercados (USMCA, Mercosur, cross-border) y
propone topic regional.

**Ejemplos reales de temas que podrían emerger y necesitar página:**
- Hidrógeno verde transporte
- Baterías de segunda vida
- Carga ultra-rápida MCS
- Vehículos definidos por software (SDV)
- Trazabilidad supply chain con blockchain
- Carbon credits para flotas
- Tarifas dinámicas de electricidad para depots
- Robo de baterías (emergente en LatAm)
- Insurance telematics (UBI)
- Driver wellness / fatigue management

Coste estimado: ~$0.20-0.50/mes (1 análisis LLM + clustering mensual).

### PR-SEO-3.6 · Updates mensuales + threshold automático

Cada N días, el sistema:
- Refresca contenido de páginas pilar (LLM evalúa si cambió algo significativo).
- Mueve páginas de noindex → index cuando cumplen threshold (3+ historias
  relacionadas + score LLM publicable + no `paused: true` en .md).
- Decrementa tier si una página deja de tener tracción.

---

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

### 2. SEO masivo + interlinking
**Estado:** propuesto.
**Problema:** editorial sin tráfico = activo sin ROI.
**Pendiente cuando arranquemos:**
- Auditar keywords actuales por página interna (`/mercados/`, `/temas/`, `/players/`).
- Crear ~30 páginas pilar más sobre temas long-tail con volumen MX/ES/EN (peajes, ITV, fuel cards comparativa, telemática para flotas medianas, etc.).
- Interlinking automático desde cada edición: si una historia menciona un topic/player, enlazar al hub correspondiente.
- Schema.org `NewsArticle` por edición + breadcrumbs.
- Ajustar `sitemap.xml` con cambios de frecuencia adecuados.

### 3. Versión en inglés (EN) para mercado US/Int
**Estado:** propuesto.
**Contexto:** Pulpo va a lanzar en inglés. El editorial debe generar tráfico EN simultáneo.
**Idea:**
- Cada edición se compone también en EN como `magazines/YYYY-MM-DD-the-fleet-radar.html`.
- Un solo `compose` LLM con prompt que devuelve `{es: {...}, en: {...}}`.
- `hreflang` x-default + es + en. Canónicos cruzados.
- Subdirectorio `/en/` o subdominio `en.thefleetradar.com` (decidir cuando llegue).

### 3b. Sección "Movimientos" semanal
**Estado:** propuesto. Señal fuerte de auditoría (ChatGPT + Gemini).
**Diseño:**
- Bloque fijo en cada edición: contrataciones senior, M&A, rondas de financiación en el sector fleet MX/ES/LatAm.
- Fuentes: press releases, LinkedIn, T21, Fleet News, AEGFA.
- Formato: 3-4 bullets cortos con nombre + empresa + movimiento + fecha.
- Integración: campo nuevo `movimientos` en el compose JSON → renderizado en el template.

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
- ~~Sección "Movimientos" semanal~~ → movido a backlog como ítem 3b.

---

## Hecho

| Fecha | Cambio | Commit/PR |
|---|---|---|
| 2026-05-21 | Sistema autónomo MVP completo (ingest + classify + dedupe + select + compose + qa + publish) | PR #13 |
| 2026-05-21 | Notificación Slack (deshabilitada hasta crear secret) | 642bf1e |
| 2026-05-21 | QA no-bloqueante; siempre publica con avisos | 24be10c |
| 2026-05-21 | Blindaje deploy: Vercel Deploy Hook + smoke test + canary martes | PR `claude/deploy-resilience` |
| 2026-05-21 | Curación: 24 fuentes (14 RSS + 10 Google News) + classifier USA + reparto MX/ES + blacklist competidores | PR #26 `claude/curation-usa-and-sources` |
| 2026-05-22 | PR-SEO-1: schema.org + robots.txt LLM bots + meta tags + internal linking | PR `claude/seo-1-foundations` |
| 2026-05-22 | Auditorías externas: Perplexity, DeepSeek, ChatGPT, Gemini → `docs/audits/` | commit `50a61ce` |
| 2026-05-22 | Fix geo LatAm: eliminado "Pulpo operativo desde sede en Bogotá" + CTA box corregido | commit `50a61ce` |
| 2026-05-22 | A-1 PulpoPay disclaimers · A-2 hreflang todos los hubs y pillar pages · A-3 NewsArticle JSON-LD en 7 ediciones | commit `f5b6fc9` |
| 2026-05-22 | A-4 verificado: CTA Pulpo en Nº8 está tras sección opinión, no adyacente al artículo sobre operador asesinado | verificación manual |
| 2026-05-22 | Internal linking: PILLAR_INDEX (65 páginas) + build_tag_html + story tags clickables + inject retroactivo en 7 ediciones (45 bloques, 33 tags) | commit `a9f91cc` |
| 2026-05-22 | Newsletter signup en 153 páginas (pillar pages, hubs, index, about) | commit `8b4761e` |
| 2026-05-22 | Topbar global: Temas + Mercados en 108 ficheros + nueva /mercados/index.html | commit `16fdb37` |
| 2026-05-22 | Sitemap: añadida /mercados/ (33 URLs) · STYLE-FIXES.md con análisis de clichés · lista negra en pillar-page-prompt.md | commit `fd38aec` |
| 2026-05-23 | Fuentes al pie (A-5): 5 páginas prioritarias con sección "Fuentes y referencias" (SAT, SICT, DGT, etc.) | commit `e3bd0b0` |
| 2026-05-23 | Backlinks pillar → ediciones: 37 páginas con grupo "Ediciones que cubren este tema" (3 más recientes por topic) | commit `e3bd0b0` |
| 2026-05-23 | Fix ecosistema (A-6 limpieza): 42 reemplazos en 35 páginas de temas/ y mercados/ | commit `e3bd0b0` |
| 2026-05-23 | Lead magnet checklist antifraude combustible MX (A-7 parcial): 12 controles · /evergreen/checklists/antifraude-combustible-mx-2026/ | commit `e3bd0b0` |
| 2026-05-23 | Brand links: HUB_LINKS_BY_PLAYER expandido (Samsara, Geotab, WEX, Tesla…) + linkify_brands.py para magazines existentes | commit `e3bd0b0` |
