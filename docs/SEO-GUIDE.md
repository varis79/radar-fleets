# SEO Guide · The Fleet Radar

Documento canónico de SEO técnico, editorial y arquitectura del sitio.
Fuente de verdad cuando hay duda sobre cómo se construye o mantiene una
página. Actualizado **2026-05-24**.

> Lee este doc antes de:
> - Generar una nueva página pillar/hub/caso de uso/sector/ciudad
> - Tocar el sistema de frescura (cron miércoles)
> - Modificar el pipeline de magazines
> - Hacer auditorías profundas (usa `docs/AUDIT-PROMPT-V3.md`)

---

## 1. Identidad del sitio

| | |
|---|---|
| **Nombre** | The Fleet Radar · by Pulpo |
| **URL** | https://thefleetradar.com |
| **Publisher** | Pulpo (https://getpulpo.com), gestor de flotas, fundada 2018, +200.000 vehículos gestionados |
| **Tipo** | Publicación editorial semanal, voz periodística, no marketing |
| **Audiencia** | Gerentes de flota, COO, CFO, directores de operaciones (B2B, MX/ES/LatAm) |
| **Idioma** | Español únicamente (en planificación English para USA/EU) |
| **Foco geográfico primario** | México 🇲🇽, España 🇪🇸 |
| **Foco secundario** | Colombia, Chile, Argentina, Perú, Ecuador, Uruguay, R. Dominicana, LatAm regional |
| **Cobertura selectiva** | USA, UK, Europa (impacto regulatorio/comercial) |
| **Frecuencia magazine** | Cada lunes 07:00 hora Madrid (UTC+2 verano) |
| **Día de freshness rotation** | Cada miércoles 06:00 UTC |

---

## 2. Stack técnico

- **Frontend**: HTML estático, CSS único (`assets/radar.css`), JS mínimo inline
- **Hosting**: Vercel (static + serverless functions en `/api/`)
- **Build**: Python 3.11+, BeautifulSoup4, PyYAML, csv, no framework JS
- **API serverless**: Vercel Edge Functions (Node) — `api/subscribe.js`
- **Newsletter**: Resend (Audiences API)
- **Analytics**: Vercel Web Analytics + Speed Insights (no cookies)
- **Fuentes externas**: ANFAC, SICT, DGT, INEGI, AMDA, IDAE, T21, etc.
- **LLM editorial**: Claude (vía Anthropic API) en `scripts/compose.py`

**No usamos**: React/Vue, Webpack, npm builds, CMS headless, comentarios,
publicidad programática, trackers de terceros.

---

## 3. Arquitectura del sitio

```
/                                          # Home (duplica magazine actual con canonical)
/archive.html                              # Listado de ediciones
/about/                                    # Quiénes somos, FAQ editorial
/404.html                                  # Custom 404 con nav global
/styleguide.html                           # Doc interno de marca
/sitemap.xml                               # 185+ URLs auto-generado
/robots.txt                                # Permite todos los LLMs
/rss.xml                                   # Feed de magazines

/magazines/YYYY-MM-DD-radar-fleet-by-pulpo.html   # Editions (lunes)
/magazines/YYYY-MM-DD-radar-fleet-by-pulpo-summary.txt   # Slack summary

/mercados/                                 # Hub principal
  /mexico/ /espana/ /latam/ /colombia/ /chile/ /argentina/
  /peru/ /ecuador/ /uruguay/ /republica-dominicana/
  /usa/ /uk/ /europa/

/temas/                                    # Páginas pillar editoriales (~58)
  index.html                               # Listado
  <topic>-flotas-<market>-2026/            # 56 topics × markets × intents
  <topic>-flotas-<market>-comparativa-2026/
  <topic>-flotas-<market>-guia-2026/
  <topic>-flotas-<market>-regulacion-2026/

/casos-uso/                                # Casos por aplicación (41)
  flota-<caso>-<market>-2026/
  flota-<caso>-<market>-guia-2026/

/sectores/                                 # Verticales industria (19)
  flotas-<sector>-<market>-2026/

/ciudades/                                 # Por ciudad (33)
  <tema>-flotas-<ciudad>-2026/

/evergreen/                                # Recursos atemporales
  /index.html                              # Listado
  /checklists/<slug>/                      # Plantillas operativas
  /guias/<slug>/                           # Guías largas

/legal/
  /privacidad/                             # Política privacidad
  /terminos/                               # Términos uso

/players/                                  # Stub - hub de marcas (no expuesto aún)
/assets/
  radar.css                                # CSS único
  brand/                                   # Logo, favicons
  downloads/                               # Plantillas descargables (CSV)
```

**Conteos a 2026-05-24**: 189 páginas indexables, 185 URLs en sitemap.

---

## 4. SEO técnico — checklist obligatorio por página

Toda página HTML del sitio (excepto 404.html y styleguide.html) DEBE tener:

### En `<head>`

```html
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<meta content="index, follow, max-snippet:-1, max-image-preview:large" name="robots"/>
<title>{específico, único, <70 chars, datos primero}</title>
<meta name="description" content="{único, <155 chars, accionable}"/>
<meta name="author" content="Pulpo — getpulpo.com"/>

<!-- Open Graph -->
<meta property="og:title" content="{= title}"/>
<meta property="og:description" content="{descripción atractiva}"/>
<meta property="og:type" content="{article|website}"/>
<meta property="og:url" content="https://thefleetradar.com/{ruta}/"/>
<meta property="og:site_name" content="The Fleet Radar · by Pulpo"/>
<meta property="og:image" content="https://thefleetradar.com/og-default.png"/>
<meta property="og:image:width" content="1200"/>
<meta property="og:image:height" content="630"/>

<!-- Twitter -->
<meta name="twitter:card" content="summary_large_image"/>
<meta name="twitter:title" content="{= title}"/>
<meta name="twitter:description" content="{= og:description}"/>
<meta name="twitter:image" content="https://thefleetradar.com/og-default.png"/>

<!-- Freshness -->
<meta property="article:published_time" content="YYYY-MM-DD"/>
<meta property="article:modified_time" content="YYYY-MM-DD"/>
<meta property="article:author" content="Pulpo"/>
<meta property="article:section" content="Fleet intelligence"/>

<!-- Canonical -->
<link rel="canonical" href="https://thefleetradar.com/{ruta}/"/>

<!-- hreflang (si tiene par MX↔ES) -->
<link rel="alternate" hreflang="es-MX" href="{url MX}"/>
<link rel="alternate" hreflang="es-ES" href="{url ES}"/>
<link rel="alternate" hreflang="x-default" href="https://thefleetradar.com/"/>

<!-- Favicons, fonts, CSS (standard) -->
<link rel="icon" type="image/svg+xml" href="/assets/brand/favicon.svg"/>
<link rel="stylesheet" href="/assets/radar.css"/>
<link rel="alternate" type="application/rss+xml" href="/rss.xml" title="The Fleet Radar · by Pulpo"/>
```

### En `<body>`

```html
<header class="topbar">
  <a class="topbar-brand" href="/">The Fleet Radar <span>by Pulpo</span></a>
  <div class="topbar-meta">{Tipo · Mercado}</div>
  <nav class="topbar-nav">
    <a href="/">Última</a>
    <a href="/archive.html">Archivo</a>
    <a href="/mercados/">Mercados</a>
    <a href="/temas/">Temas</a>
    <a href="/casos-uso/">Casos de uso</a>
    <a href="/sectores/">Sectores</a>
    <a href="/evergreen/">Recursos</a>
    <a class="cta" href="https://www.getpulpo.com/" rel="noopener" target="_blank">Pulpo ↗</a>
  </nav>
</header>

<main>
  <!-- contenido principal -->
  <!-- En pillars: hero con h1 + intro + <time class="page-updated"> -->
  <!-- En pillars: <aside class="did-you-know"> tras primera sección -->
</main>

<footer class="site-footer">
  <!-- 5 columnas: Brand · Secciones · Ediciones · Legal · Pulpo -->
</footer>
```

### JSON-LD obligatorio por tipo

| Tipo página | Schemas requeridos |
|---|---|
| Home (`index.html`) | `NewsMediaOrganization` + `WebSite` + `ItemList` (últimas 5 ediciones) |
| Magazine | `NewsArticle` + `BreadcrumbList` |
| Hub mercado | `CollectionPage` + `BreadcrumbList` + `NewsMediaOrganization` + `WebSite` |
| Pillar tema | `Article` + `FAQPage` + `BreadcrumbList` + `NewsMediaOrganization` + `WebSite` |
| Caso uso | `Article` + `FAQPage` + `HowTo` (si aplica) + `BreadcrumbList` |
| Sector | `Article` + `BreadcrumbList` |
| Ciudad | `Article` + `BreadcrumbList` |
| Evergreen checklist | `Article` + `HowTo` + `BreadcrumbList` |
| Legal | `WebPage` + `BreadcrumbList` |

Toda Organization ref usa `@id: https://thefleetradar.com/#organization`.
Toda WebSite ref usa `@id: https://thefleetradar.com/#website`.

### Topbar-meta por tipo

| Sección | Pattern topbar-meta |
|---|---|
| Home | `Nº {N} · {fecha}` |
| Magazine | `Nº {N} · {fecha}` |
| Mercado | `Mercado · {país} {bandera}` |
| Temas (pillar) | `Página pilar · {mercado}` |
| Casos de uso | `Caso de uso · {mercado}` |
| Sectores | `Sector · {mercado}` |
| Ciudades | `Ciudad · {nombre ciudad}` |
| Evergreen checklist | `Checklist · {mercado}` |
| Evergreen guía | `Guía · {mercado}` |
| Legal | `Legal · {tipo}` |
| 404 | `Error 404` |

---

## 5. SEO editorial — reglas críticas

### REGLA CRÍTICA #1: cifras atribuidas a empresas privadas

Audit 2026-05-24 detectó 30+ páginas con cifras inventadas tipo "DHL redujo
costes 18%", "Amazon expandió flota 40%", "MeLi 28% del volumen" sin fuente.
Esto es **riesgo editorial y legal** serio.

**Política**:

❌ **PROHIBIDO**:
- Cifras específicas atribuidas a empresas privadas sin fuente verificable
- "Caso X con resultado Y%" cuando Y% no está en una fuente citada
- "Líder con N% del mercado" sin link a Gartner/IDC/Forrester/etc.
- Cifras de operación de clientes propios sin permiso explícito
- Inventar consistencia (si una página dice "Amazon 850", otra "Amazon 400" → ambos son inventados, usar cualitativo)

✅ **PERMITIDO**:
- Cifras de empresas/instituciones PÚBLICAS (CFE, Pemex, SAT, DGT, IMSS, CANACAR, AMEG, ANFAC, INEGI, ANT, MTOP, AMIA, ANPACT) con link
- Cifras de mercado AGREGADAS con fuente nombrada
- Cifras del propio Pulpo verificables (+200k vehículos, fundación 2018)
- Datos PÚBLICOS de empresas (declaraciones de resultados, comunicados oficiales) con link al doc original
- Lenguaje cualitativo cuando no hay fuente:
  - "líderes del sector como X, Y, Z operan flotas de gran escala"
  - "operadores internacionales como DHL han desplegado iniciativas eléctricas"
  - "amplia red de estaciones"

**Patrón de reescritura conservadora** (aplicado en 50+ archivos):
- "DHL opera 1.200 vehículos" → "operadores como DHL operan flotas significativas"
- "Aralo redujo 31%" → "Aralo reportó mejoras operativas medibles"
- "Samsara, Geotab, Webfleet concentran 55%" → "Samsara, Geotab y Webfleet son players de referencia"

**Validación**: `scripts/qa_pillars.py` cuenta porcentajes y cifras absolutas
no atribuidas. Falla la build si una página tiene ≥5 % de empresa privada
o ≥6 absolutos sin source. Pre-commit hook (`.git/hooks/pre-commit`) corre
sobre staged HTMLs.

### REGLA CRÍTICA #2: consistencia interna

Si una cifra ya aparece en otra página del sitio (mismo player, mismo
mercado), DEBE coincidir. Si no tienes cifra única defendible, usa
cualitativo. Síntoma de invención = misma empresa con 3 cifras distintas
entre páginas.

### REGLA CRÍTICA #3: voz editorial

Definida en `prompts/pillar-page-prompt.md`. Resumen:
- Periodismo, no marketing (no vendes Pulpo; informas con criterio)
- Datos antes que adjetivos ("crece 23%" vs "crece rápidamente")
- Sobriedad: cero hype, vocabulario técnico cuando aporta
- Pulpo mencionado discretamente en `<aside class="pillar-pulpo-box">` al final
- **Lista negra** de expresiones (en el prompt): "competidor", "ecosistema",
  "transformación digital", "claramente", clichés cualquiera

### REGLA CRÍTICA #4: regenerar = puede pisar fixes manuales

Si regeneras una pillar con `generate_pillar_page.py`, vas a pisar:
- Cleanups manuales del cuerpo
- Disclaimers ad-hoc
- Cualquier fix posterior

**Siempre** correr después de regenerar:
1. `python3 scripts/linkify_institutions.py`
2. `python3 scripts/linkify_topics.py`
3. `python3 scripts/seo_polish.py`
4. `python3 scripts/rebuild_sitemap.py`
5. `python3 scripts/qa_pillars.py` (verificar OK)

---

## 6. Frescura — por qué importa para Google 2026

Google premia páginas que se actualizan con cambios reales. El sitio tiene
189 páginas estáticas, sin sistema de freshness se volverían todas "stale"
en 90 días.

### Sistema implementado (cron miércoles 06:00 UTC)

**`scripts/rotate_facts.py`** — caja "💡 Sabías qué" rotatoria:
- Pool de 30 facts editoriales sobre el sector
- Cada página recibe: `pool[(isoweek + sha1(page_url)) % 30]`
- 158 páginas con caja semanal-rotatoria
- Cycle: cada página recibe ~17 facts distintos al año

**`scripts/refresh_freshness.py`** — meta freshness:
- Inyecta `<meta property="article:modified_time">` y visible `<time>`
- Rotación: cada página recibe refresh cada ~6 semanas (controlado por hash)
- ~30 páginas seleccionadas por semana (anti-spam: NO todas a la vez)
- Actualiza `dateModified` en JSON-LD Article

**`scripts/rebuild_sitemap.py`** — sitemap completo:
- `lastmod = mtime real` de cada archivo
- Prioridad por sección (home 1.0, magazines 0.9, mercados 0.85, etc.)
- Auto-excluye páginas con `noindex`

**Workflow GitHub Actions**: `.github/workflows/weekly-freshness.yml`
(actualmente no commiteado por scope PAT, ver
`docs/WORKFLOW-FRESHNESS-SETUP.md` para activar).

---

## 7. Navegación

### Topbar global (idéntico en 189 páginas)

```
The Fleet Radar by Pulpo | {topbar-meta} | Última · Archivo · Mercados · Temas · Casos de uso · Sectores · Recursos · Pulpo ↗
```

Inyectado/mantenido por `scripts/unify_navigation.py` (idempotente).

**Responsive**:
- <900px: scroll horizontal sin barra
- <640px: solo Última, Archivo, Pulpo↗ en topbar; resto via footer

### Footer global (idéntico en 189 páginas)

5 columnas:
- **Brand** — logo + tagline
- **Secciones** — Mercados, Temas, Casos uso, Sectores, Ciudades, Recursos
- **Ediciones** — Última edición, Archivo, RSS
- **Legal** — Privacidad, Términos, Contacto (mailto)
- **Pulpo** — getpulpo.com ↗, LinkedIn ↗

Bottom: `© 2026 Pulpo · The Fleet Radar` + disclaimer "publicación editorial
independiente. Análisis no constituye asesoría."

### Navegación transversal

Cada página pillar tiene además:
- **Breadcrumb schema** (JSON-LD `BreadcrumbList`)
- **Pillar eyebrow** visible (`<span class="pillar-eyebrow">`)
- **Pillar-related section** al final con cross-links a:
  - Mismo tema en otros mercados
  - Casos de uso relacionados
  - Ciudades relevantes
  - Temas relacionados
- **Ediciones que cubrieron este tema** (inject_edition_backlinks.py)

---

## 8. Scripts — tabla de referencia completa

### Generación de contenido

| Script | Cuándo correr | Función |
|---|---|---|
| `compose.py` | Cron lunes | LLM compose de magazine semanal |
| `select.py` | Cron lunes | Selecciona stories de pool ingerido |
| `classify.py` | Cron lunes | Clasifica items por topic/market |
| `dedupe.py` | Cron lunes | Filtra duplicados vs ediciones previas |
| `qa.py` | Cron lunes | QA bloqueante magazine (forbidden, thin, voice) |
| `publish.py` | Cron lunes | Renderiza + actualiza index/archive/sitemap/rss |
| `generate_pillar_page.py` | Manual | Genera pillar individual via LLM |
| `generate_country_briefs.py` | Manual | Genera hubs LatAm desde data hardcoded |

### Enlazado y SEO

| Script | Cuándo correr | Función |
|---|---|---|
| `linkify_institutions.py` | Tras gen. pillar | 107+ ext-links a SAT/DGT/ANFAC/etc. |
| `linkify_topics.py` | Tras gen. pillar | Interlinking entre pillars (topic terms) |
| `linkify_brands.py` | Tras gen. pillar | Brand mentions a páginas pillar |
| `inject_story_links.py` | Manual | Magazine stories → pillars/hubs |
| `inject_edition_backlinks.py` | Manual | Pillars ← magazines que las cubren |
| `inject_schema_static.py` | Manual | Inyecta JSON-LD missing |
| `inject_sources.py` | Manual | Añade bloque fuentes al pie |
| `seo_polish.py` | Tras cualquier change | og:title sync, breadcrumbs, hreflang, ItemList |
| `patch_home_magazine_seo.py` | Tras nueva edition | og:image, JSON-LD Org+WebSite en home |
| `rebuild_sitemap.py` | Tras cualquier change | Sitemap completo con lastmod real |

### Quality & maintenance

| Script | Cuándo correr | Función |
|---|---|---|
| `qa_pillars.py` | Pre-commit + CI | Valida no cifras inventadas en pillars |
| `release_pillars.py` | Manual | Libera de noindex pillars que pasan threshold |
| `purge_dead_links.py` | Tras cualquier change | Elimina `<a>` rotos del DOM |
| `unify_navigation.py` | Tras cualquier change | Header + footer canónico global |
| `fix_nav_metas.py` | Tras cualquier change | topbar-meta correcto por tipo |

### Frescura (cron miércoles)

| Script | Cuándo | Función |
|---|---|---|
| `rotate_facts.py` | Miércoles 06:00 UTC | Rota caja "Sabías qué" en 158 pages |
| `refresh_freshness.py` | Miércoles 06:00 UTC | article:modified_time + sitemap lastmod |

### Misc

| Script | Función |
|---|---|
| `install_hooks.sh` | Instala pre-commit hook |
| `build_hubs.py` | (Legacy) construye hubs viejos |
| `generate_brand_assets.py` | OG image, favicons |

---

## 9. Workflow automatizado

### `.github/workflows/weekly-edition.yml` (lunes 05:07 UTC)

```
ingest → classify → dedupe → select → compose → qa → publish → commit → PR → auto-merge → Vercel deploy hook → smoke test
```

Tras `publish`, ahora también corre (vía hook en `publish.py`):
- `patch_home_magazine_seo` (og:image, JSON-LD Org+WebSite)
- `rebuild_sitemap`
- `seo_polish.process_magazine()`

### `.github/workflows/weekly-deploy-canary.yml` (martes 08:00 UTC)

Verifica HTTP 200 de la edición publicada el lunes.

### `.github/workflows/weekly-freshness.yml` (miércoles 06:00 UTC)

⚠️ **Actualmente no commiteado por scope PAT** — ver `docs/WORKFLOW-FRESHNESS-SETUP.md`.

```
rotate_facts.py → refresh_freshness.py → rebuild_sitemap.py → commit auto → push → Vercel deploy hook
```

### `.github/workflows/generate-pillar-pages.yml` (manual workflow_dispatch)

Para regenerar batch de pillars cuando hay cambio mayor de prompt.

---

## 10. Gotchas conocidos (workarounds)

### A. `scripts/select.py` shadowea stdlib `select`

Al ejecutar cualquier script en `scripts/` que importe `subprocess` o
`os.popen`, Python encuentra primero `scripts/select.py` en lugar del
módulo `select` del stdlib.

**Workaround** (al inicio del script):
```python
import sys
if sys.path and sys.path[0].endswith("/scripts"):
    sys.path.pop(0)
```

Aplicado en `qa_pillars.py`. Aplicar en cualquier script nuevo que necesite
subprocess.

### B. BeautifulSoup re-serializa HTML

`soup.write_text(str(soup))` puede:
- Reordenar attrs (`<meta name="x" content="y">` → `<meta content="y" name="x">`)
- Auto-cerrar tags (`<meta>` → `<meta/>`)
- Colapsar whitespace

Esto es por diseño, no problema. Pero significa que cualquier diff post-script
muestra muchos cambios cosméticos. Para regex sobre attrs, usa patrones que
soporten ambos órdenes.

### C. PAT scope `workflow`

El PAT actual en el keychain macOS no tiene scope `workflow`. No puedes
pushear archivos en `.github/workflows/`. Solución: actualizar PAT en
https://github.com/settings/tokens.

### D. Regenerar pillar pisa cleanup manual

`generate_pillar_page.py` no preserva fixes manuales. Si tienes que
regenerar, vuelve a correr:
1. `linkify_institutions.py`
2. `linkify_topics.py`
3. `seo_polish.py`
4. `rebuild_sitemap.py`
5. `qa_pillars.py`

### E. Magazine USA/UK/Europa sin destinos hasta 2026-05-24

La edición Nº 1 (2026-04-14) es USA-céntrica y sus stories no tenían
hubs internos. Resuelto creando `mercados/usa/`, `/uk/`, `/europa/`.

### F. `pillar_renderer.py` default `indexed=False`

Las pillars nuevas se generaban con `noindex` por defecto. Cambiado a
`indexed=True`. Para forzar stub, usar `--no-indexed`.

---

## 11. Configuración de Vercel

### Env vars necesarias

| Var | Para qué | Cómo obtener |
|---|---|---|
| `ANTHROPIC_API_KEY` | Generación LLM | https://console.anthropic.com/ |
| `RESEND_API_KEY` | Newsletter | https://resend.com Settings → API Keys |
| `RESEND_AUDIENCE_ID` | Newsletter | Resend → Audiences → tu lista |
| `VERCEL_DEPLOY_HOOK` | Trigger redeploy desde GitHub Actions | Vercel → tu proyecto → Settings → Git → Deploy Hooks |

### vercel.json

- `cleanUrls: true` (sin .html)
- `trailingSlash: false`
- Headers cache: HTML no-cache, RSS/sitemap 30 min, assets 1 año

---

## 12. Roadmap pendiente (no bloqueante)

### Inmediato (acción tuya, 5-15 min cada uno)

1. **Activar Resend** — añadir env vars en Vercel (15 min)
2. **Activar cron freshness** — update PAT scope o crear via GitHub UI (5 min)
3. **Submitir sitemap a Search Console** — manual (10 min)

### Próximas iteraciones (1-3 horas cada uno)

4. **Newsletter broadcast automation** — script `send_newsletter.py` que
   crea broadcast en Resend tras cada publish
5. **Fact-check de pillars LatAm** — ningún audit aún cubrió mercados/
   colombia/chile/argentina/peru/ecuador/uruguay/republica-dominicana
6. **Image SEO** — actualmente sin `<img>` reales (solo SVG inline). Si
   añadimos imágenes: alt obligatorio, lazy loading, WebP
7. **Performance/Lighthouse audit** — score actual desconocido
8. **A/B headlines** — sistema de variantes para magazines
9. **Comparativas head-to-head** — DECIDIDO NO HACER (specs caducan,
   riesgo de inventar)

### Tier-3 (estratégico)

10. **English version** para USA + EU (cuando Pulpo lance EN)
11. **Búsqueda interna** (declarada en JSON-LD `SearchAction` pero no
    funcional aún)
12. **Comments / community** — DECIDIDO NO HACER (no escala para B2B)

---

## 13. Métricas de éxito SEO

| Métrica | Objetivo Q3 2026 | Hoy |
|---|---|---|
| Páginas indexadas en Google | 180+ | A medir post-push |
| Sessions orgánicas/mes | 5.000 | A medir |
| Brand impressions | 50.000/mes | A medir |
| Top 10 keywords ranking | 30+ | A medir |
| Backlinks de DR>30 | 20+ | A medir |
| Newsletter subscribers | 500 | A activar setup |

---

## 14. Apéndice — convenciones de slugs

- Pillar topic: `<topic>-flotas-<market>-<year>` (ej: `telematica-flotas-mexico-2026`)
- Pillar variante: agregar sufijo `-comparativa-<year>`, `-guia-<year>`, `-regulacion-<year>`
- Caso uso: `flota-<caso>-<market>-<year>`
- Sector: `flotas-<sector>-<market>-<year>`
- Ciudad: `<topic>-flotas-<ciudad>-<year>`
- Evergreen: `<tipo>-<asunto>-<market>-<year>` (sin "flotas" en el medio)

Cambio de año (2026 → 2027): abrir PR que regenere slugs y mantenga 301
desde slugs viejos. NO se ha hecho aún (pasa diciembre 2026).
