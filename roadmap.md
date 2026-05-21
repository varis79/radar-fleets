# The Fleet Radar · Roadmap

Documento vivo. Va por delante del repo: aquí van ideas antes de tener PR.
Cuando una idea llega a producción, se mueve a `docs/SYSTEM.md` y se marca aquí
como `[done]` con el commit/PR de aterrizaje.

Última revisión: 2026-05-21 (post-N°8).

---

## En curso

| ID | Idea | Estado | Notas |
|---|---|---|---|
| C-4 | PR-SEO-1 · Fundamentos técnicos | PR abierto `claude/seo-1-foundations` | Schema.org JSON-LD en magazines + hubs + 404. robots.txt con whitelist LLM bots. Meta tags ampliados. Internal linking automático en cada story. |

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
| 2026-05-21 | Curación: 24 fuentes (14 RSS + 10 Google News) + classifier USA + reparto MX/ES + blacklist competidores | PR #26 `claude/curation-usa-and-sources` |
| 2026-05-22 | PR-SEO-1: schema.org + robots.txt LLM bots + meta tags + internal linking | PR `claude/seo-1-foundations` |
