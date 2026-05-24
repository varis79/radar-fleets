# The Fleet Radar · Roadmap

Documento vivo. Va por delante del repo: aquí van ideas antes de tener PR.
Cuando una idea llega a producción, se mueve a `docs/SYSTEM.md` y se marca aquí
como `[done]` con el commit/PR de aterrizaje.

Última revisión: **2026-05-24** (post-sprint linking + Sabías qué v2 con 6 LLMs).

---

## 🎯 TODO inmediato (priorizado)

### TIER 1 · Bloquea features ya construidas

| # | Tarea | Quién | ETA | Bloquea |
|---|---|---|---|---|
| T1-1 | **Push `weekly-freshness.yml`** — actualizar PAT con scope `workflow` o crear via GitHub UI | Varis | 5 min | Cron miércoles de freshness + rotación facts NO corre |
| T1-2 | **Activar Resend** — `RESEND_API_KEY` + `RESEND_AUDIENCE_ID` en Vercel env | Varis | 15 min | Newsletter form devuelve 500 |
| T1-3 | **Submitir sitemap a Search Console** — `https://thefleetradar.com/sitemap.xml` (211 URLs) | Varis | 10 min | Indexación más rápida |

### TIER 2 · Segundo batch de facts "Sabías qué" (categorías débiles)

Pool actual: **137 facts** producción-ready repartidos en 12 categorías. Las
8 categorías con cobertura baja necesitan otro batch dirigido a los 6 LLMs:

| Categoría | Facts actuales | Target | Ideas y ángulos |
|---|---|---|---|
| 🚛 Renting & Leasing | **0** | 15-20 | Cuotas ALD/Arval/Alphabet UE+ES, % residual, mercado secundario, evolución renting 2020-2025, alianzas BBVA/Santander fleet financing |
| 💼 Operadores 3PL | **0** | 15-20 | DHL/FedEx/UPS perfiles públicos, top 10 3PL Europa según T&L, top 10 LatAm, volumen TEUs Maersk/MSC, M&A logístico 2023-25 |
| 🌎 Geopolítica & Comercio | **0** | 15-20 | T-MEC datos comercio MX-USA, nearshoring impacto en flotas norte de México, Brexit logística UK-EU, ETS2 carbono pesados, Mobility Package EU |
| 🏭 Sectores verticales | **3** | 15-20 | Datos por sector: cemento (Cemex/Domicem), gas (Natural/Gas), retail (Walmart/Carrefour cifras públicas), tabaco/cerveza distribución, agro |
| 🏢 Gestión de flotas | **2** | 10-15 | Datos genéricos del software fleet (Berg Insight, Ptolemus, Gartner), mercado SaaS gestión flotas, índice digitalización |
| 🚢 Logística & Corredores | **2** | 15-20 | **Corredores con récords** (Suez Canal 12% comercio mundo, Panamá 40 buques/día, Hormuz 20% petróleo, top 10 puertos mundo), Felixstowe-Madrid, Houston-Veracruz |
| ⚡ Electrificación | **3** | 15-20 | Más datos MOVES III importes, Olinia avance, ANFAC matriculaciones EV mensuales, ChargePoint/Iberdrola/Enel X cuotas, Tesla Semi flotas pilotos públicos |
| 🔧 Mantenimiento | **1** | 10-15 | Vida útil componentes (frenos/neumáticos/embrague), MTBF camiones, costes correctivo vs preventivo por marca, programas Iveco/Volvo/Scania |

### TIER 2b · Ideas que pidió el usuario (nuevos ejes de facts)

**🏆 Corredores con números récord** — datos espectaculares y memorables:
- Suez Canal: 12% comercio global pasa por aquí
- Panamá Canal: 40 buques/día capacidad, restricciones por sequía 2024
- Strait of Hormuz: 20% petróleo mundial transita
- Estrecho de Malaca: 25% comercio marítimo global
- Eurotunnel: 4M camiones/año entre UK y FR
- Rotterdam: puerto #1 Europa, 470M toneladas/año
- Top 10 puertos mundo (Shanghai, Singapore, Ningbo, Shenzhen, etc.)
- Corredor T-MEC: 80% comercio terrestre Norteamérica
- Madrid-Barcelona AP-2: corredor logístico interior #1 España

**📜 Históricos y curiosidades del sector flotas** — facts memorables:
- 1956: Malcom McLean inventa el contenedor ISO — el cambio que redefinió la logística
- 1953: Volvo lanza el primer cinturón de seguridad de 3 puntos en vehículo comercial
- USPS: la flota más grande del mundo con ~220.000 vehículos
- 1985: el primer tacógrafo digital aparece en Europa
- Tesla Semi: primera entrega comercial PepsiCo, dic 2022, 100 unidades Modesto CA
- Mercedes Actros récord eficiencia: 19,4 L/100km en condiciones de prueba
- Récord histórico distancia un solo viaje cargo: container Shanghai→Hamburg 19.000 km
- 1907: primer camión de bomberos motorizado en USA (Knox Automobile)
- 1937: Diesel-electric truck (KW-Cummins) marca arquitectura moderna

**🌟 Récords mundiales operación de flota**:
- Walmart: ~12.000 tractocamiones propios (la flota privada más grande USA)
- Amazon Air: 100+ aviones, 50+ centros de procesamiento
- Maersk: 700+ buques, primera carrier en orderar metanol verde
- Ferrocarril norteamericano: BNSF + Union Pacific mueven ~30% del PIB USA en carga

**🔬 Curiosidades técnicas**:
- Volvo VNL Aero: -7% consumo vs versión estándar gracias a sólo cambios aerodinámicos
- Scania R Super: motor 13L de 560CV mantiene torque desde 850 RPM
- Mercedes eActros: 600 km autonomía con megacharging 1MW
- Cummins X15N: primer motor pesado natural gas con prestaciones de diésel

### TIER 3 · Mejoras de UI/UX

| # | Tarea | ETA |
|---|---|---|
| T3-1 | **Caja "Sabías qué" rediseñada** — degradado moderno, más visual | ✅ done 2026-05-24 |
| T3-2 | Mobile: revisar topbar con 8 links — confirmar scroll horizontal en móvil real | review |
| T3-3 | Lighthouse audit — score actual desconocido | 1h |
| T3-4 | Imagen OG por mercado (en lugar de la genérica) | 2h |
| T3-5 | Pulpo box rediseño visual (alinear con DYK v2) | 1h |

### TIER 4 · Distribución (no técnico)

| # | Tarea | Notas |
|---|---|---|
| T4-1 | LinkedIn — página corporativa "The Fleet Radar" + post auto tras edición | requiere LinkedIn API |
| T4-2 | Newsletter — broadcast semanal vía Resend (cron lunes tras edición) | post T1-2 |
| T4-3 | RSS submitted a Feedly + agregadores sectoriales | manual |

---

## 📋 Sprint 2026-05-24 · Linking masivo + Sabías qué v2

**Resumen ejecutivo**: 2 mega-sesiones consecutivas. Sitio pasó de 174 URLs
a 211 indexables, de 158 páginas con DYK a 230 (100% editorial), de 30
facts hardcoded a 137 dinámicos con filtrado por mercado+categoría.
6 LLMs aportaron facts vía megaprompt común.

### Sub-sprint A: Infraestructura de linking (commits `378300b` → `8d03876`)

| ID | Tarea | Commit |
|---|---|---|
| L-1 | `linkify_master.py` — sistema unificado entity dictionary | `378300b` |
| L-2 | `discover_entities.py` — cron jueves auto-detecta entidades nuevas | `378300b` |
| L-3 | `inject_magazine_tags.py` — 73 spans cover/story-tag → `<a>` | `378300b` |
| L-4 | `fix_hreflang.py` — completa hreflang reciprocity en 92 pages | `4987953` |
| L-5 | 19 stubs ciudades (8 MX + 6 LatAm + 5 ES) noindex/follow | `378300b` |
| L-6 | 5 corredores logísticos nueva dimensión `/corredores/` | `378300b` |
| L-7 | 10 brand pages telematics + fuel cards | `378300b` |
| L-8 | 10 OEM brand pages | `8d03876` |
| L-9 | 4 segment panorama pages | `8c1954f` |
| L-10 | Reorganización 6 hubs | `8d03876` |

### Sub-sprint B: Sistema "Sabías qué" v2 (commits `e127859` → `739f1c0`)

| ID | Tarea | Commit |
|---|---|---|
| F-1 | `content/sabias-que-pool.md` source of truth | `e127859`, `fceed3f` |
| F-2 | 6 LLMs procesados: Perplexity (12) + Grok (16) + Gemini (64) + DeepSeek (84) + ChatGPT (60) + Claude (85) = 321 crudos | `fceed3f` |
| F-3 | 137 facts producción-ready, 41 cross-validated (2+ LLMs coinciden), 7 conflictos resueltos | `fceed3f` |
| F-4 | `build_facts_json.py` compila MD → JSON parseable | `739f1c0` |
| F-5 | `rotate_facts.py` v2 con scoring inteligente por mercado+categoría+confidence+evergreen | `739f1c0` |
| F-6 | Caja DYK en 230 páginas (100% corpus editorial) | `739f1c0` |
| F-7 | Raw audit trail en `content/raw-facts-batches/` (6 LLMs JSON crudos preservados) | `e127859`, `fceed3f` |
| F-8 | Rediseño visual caja DYK con degradado moderno | (pendiente este commit) |

### Stats post-sprint

| Métrica | Pre-sprint | Post-sprint |
|---|---|---|
| URLs indexables | 174 | **211** |
| Links rotos internos | 16 | **0** |
| Magazine tags clickables | 33/112 (29%) | **106/112 (95%)** |
| Auto-links añadidos | — | **700+ en cascada** |
| Ciudades cubiertas | 32 | **51** (32 full + 19 stubs auto) |
| Corredores cubiertos | 0 | **5** (nueva dimensión) |
| Players cubiertos | 1 | **21** (Pulpo + 10 telematics/fuel + 10 OEMs) |
| Pool DYK | 30 hardcoded | **137 dinámicos** filtrados |
| Páginas con DYK | 158 | **230** |
| LLMs aportando facts | 0 | **6** |
| qa_pillars | 175 OK | **194 OK · 0 WARN · 0 FAIL** |

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
| A-7 | Lead magnets x3: checklist antifraude MX · plantilla coste/vehículo · matriz ZBE+ITV ES | Editorial (Varis) | ✅ Los 3 publicados · antifraude `e3bd0b0` · plantilla TCO + matriz ZBE `feat/movimientos-a7` |
| A-8 | Enriquecer country briefs CO, CL, AR, PE con regulación local y players | Editorial (Varis) | ✅ `c41e308` |
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
| 2026-05-23 | A-8 country briefs CO, CL, AR, PE: regulación local, players, cifras, fuentes institucionales | commit `c41e308` |
| 2026-05-23 | Sección "Movimientos" en magazine: templates + render + CSS + prompt LLM | feat/movimientos-a7 |
| 2026-05-23 | A-7 lead magnets: plantilla TCO por vehículo MX + matriz ZBE+ITV España | feat/movimientos-a7 |
| 2026-05-23 | Outbound institution links (107 ext-links a SAT/DGT/CNBV/etc.) + disclaimer mailto en 139 pillars | `1ab6ad6` |
| 2026-05-23 | Interlinking interno entre pillar pages (157 int-links auto) | `43b8f5e` |
| 2026-05-24 | FASE 1 SEO: liberar 137 pillars de noindex + purgar 407 links rotos + sitemap completo 36→171 URLs + 3 hubs LatAm engordados | `a8eab69` |
| 2026-05-24 | FASE 2 nav: header global + footer canónico + páginas legales (privacidad, términos) + evergreen index | `c625d45` |
| 2026-05-24 | FASE 3 frescura: refresh_freshness.py + rotate_facts.py + cron weekly-freshness.yml (pendiente push por PAT scope) | `40db0d8` |
| 2026-05-24 | FASE 4 polish: og:image+JSON-LD home, reconciliación cifras telemática MX, typo TCO, deduplicación titles | `e12654a` |
| 2026-05-24 | Polish final: 41 disclaimers GitHub eliminados, 88 hreflang MX↔ES, 10 BreadcrumbList magazines/evergreens, ItemList home | `19fdb97` |
| 2026-05-24 | Topbar móvil con 8 links (scroll horizontal + filtrado <640px) | `95f3e01` |
| 2026-05-24 | FASE 4 calidad editorial: cleanup cifras inventadas 33 archivos (DHL/Amazon/Bimbo/MeLi → cualitativo, Aralo+Samsara neutralizado) | `e5a8079` |
| 2026-05-24 | docs/SEO-GUIDE.md (canon) + docs/AUDIT-PROMPT-V3.md (audit interno reusable) | `dd1a535` |
| 2026-05-24 | hreflang completo (self+x-default) + qa_pillars bug fixes (whitelist ANT word-boundary, regex europeo, source detection) + cleanup pass 4 (14 archivos) | `4987953` |
| 2026-05-24 | 4 brand pillars fabricantes (camiones MX/ES + EV MX + furgonetas EV ES) | `1be6587` |
| 2026-05-24 | docs SEO-GUIDE corredores + players | `78e74b8` |
| 2026-05-24 | **Sprint linking masivo**: linkify_master.py + discover_entities.py + 19 stubs ciudades + 5 corredores + 10 brand telematics/fuel + 73 magazine tags clickables | `378300b` |
| 2026-05-24 | FASES D+E: reorganización 6 hubs + 10 OEM brand pages | `8d03876` |
| 2026-05-24 | Pool "Sabías qué" v1 inicial Perplexity batch | `e127859` |
| 2026-05-24 | Pool "Sabías qué" v2: 6 LLMs procesados (Perplexity+Grok+Gemini+DeepSeek+ChatGPT+Claude), 137 facts producción-ready, 41 cross-validated, 7 conflictos resueltos | `fceed3f` |
| 2026-05-24 | Sistema "Sabías qué" v2 live: build_facts_json.py + rotate_facts.py v2 con scoring + DYK en 230 páginas (100% editorial) | `739f1c0` |
