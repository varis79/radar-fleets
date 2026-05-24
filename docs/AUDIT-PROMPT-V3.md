# Prompt maestro de auditoría interna · v3

Versión INTERNA. Para usar con Claude/cualquier LLM que tenga acceso al
filesystem del repo (Claude Code, Cursor, Cline, Aider, etc.).

A diferencia de v1/v2 (auditorías externas con web search), v3 audita
profundamente el repo en sí: integridad del código, consistencia editorial,
SEO técnico aplicado, navegación coherente.

**Cuándo usarlo**:
- Tras un sprint largo de cambios (≥10 commits)
- Antes de un push a producción importante
- Cuando sospechas que algo se regresionó
- Cada 2-4 semanas como check-up

---

## Prompt (copiar literal y pegar al LLM)

```
Eres un auditor senior de SEO técnico + editorial + UX para sitios estáticos
B2B. Vas a auditar a fondo el repo de "The Fleet Radar" — publicación
editorial semanal de Pulpo (getpulpo.com) sobre gestión de flotas en
México, España y LatAm.

═══════════════════════════════════════════════════════════════════════
CONTEXTO OBLIGATORIO — LEE ANTES DE EMPEZAR
═══════════════════════════════════════════════════════════════════════

1. Lee primero `docs/SEO-GUIDE.md` íntegro. Es el documento canónico de
   cómo debe construirse y mantenerse el sitio. Toda regla y patrón está
   ahí. NO inventes criterios distintos.

2. Lee `prompts/pillar-page-prompt.md` para entender la voz editorial,
   las reglas críticas sobre cifras (especialmente la sección "REGLA
   CRÍTICA — cifras atribuidas a empresas privadas") y la lista negra
   de expresiones.

3. El sitio tiene ~189 páginas: home, magazines (7-8), temas (58+),
   mercados (14), casos-uso (41), sectores (19), ciudades (33),
   evergreen (6+), legal (2), about. Stack: HTML estático + Vercel +
   Python build pipeline. Sin framework JS.

═══════════════════════════════════════════════════════════════════════
ÁMBITO DE AUDITORÍA
═══════════════════════════════════════════════════════════════════════

Cubre las 7 dimensiones siguientes. Para cada una, prepara una sección
de hallazgos con ✅ (OK), ⚠️ (warn) y 🔴 (crítico).

▸ DIMENSIÓN 1 — Integridad técnica
  Comprueba:
  - `python3 scripts/qa_pillars.py` — debe ser 0 FAIL
  - `python3 scripts/purge_dead_links.py --dry-run` — debe ser 0 links rotos
  - `python3 scripts/rebuild_sitemap.py --dry-run` — comparar URLs vs paginas en disco
  - HTML válido (BeautifulSoup parsea sin errores)
  - Todas las páginas tienen canonical, og:image, twitter:image, JSON-LD,
    title==og:title, BreadcrumbList (excepto home), topbar global, footer
    global
  - Cifras objetivo: 100% canonical, 100% og:image, 100% topbar, 99%+
    BreadcrumbList

▸ DIMENSIÓN 2 — SEO técnico
  Comprueba:
  - Sitemap.xml refleja todas las páginas publicadas (no orphans)
  - robots.txt permite GPTBot, ClaudeBot, PerplexityBot, Google-Extended
  - hreflang recíproco entre pares MX↔ES (en casos-uso/, sectores/, temas/)
  - JSON-LD esquemas correctos por tipo (ver tabla en SEO-GUIDE)
  - Ninguna pillar con `<meta robots="noindex">` no intencionada
  - Sin titles duplicados (excepto home=magazine actual, intencional)
  - Sin descriptions duplicadas o vacías

▸ DIMENSIÓN 3 — Editorial / cifras
  Lee `docs/SEO-GUIDE.md` sección 5 (reglas críticas). Audita:
  - Cifras de empresas privadas con fuente verificable o lenguaje
    cualitativo
  - Consistencia interna: la misma empresa NO puede tener cifras
    distintas en páginas distintas (Amazon Madrid: 850 vs 400 = error)
  - "Caso X con resultado Y%" debe tener fuente; si no, lenguaje cualitativo
  - Cifras de instituciones públicas (CFE, Pemex, ANFAC, INEGI, etc.) son OK
    SI tienen fuente nombrada
  - Run `qa_pillars.py --verbose` y reporta WARNS si hay alguno
  - Busca patrones tipo "[Brand] [N]%", "[Brand] [N.000] vehículos" y verifica

▸ DIMENSIÓN 4 — Navegación y UX
  Spot-check 8 páginas (1 de cada tipo): home, magazine, mercado, pillar
  tema, caso uso, sector, ciudad, evergreen, legal, 404.

  Para cada una verifica:
  - Topbar canónico con 8 links (Última · Archivo · Mercados · Temas ·
    Casos de uso · Sectores · Recursos · Pulpo↗)
  - topbar-meta correcto para su tipo (ver tabla SEO-GUIDE sección 4)
  - H1 único y descriptivo
  - Footer global presente con 5 columnas
  - Si es pillar: hero con `<time class="page-updated">` visible
  - Si es pillar: caja `<aside class="did-you-know">` rotatoria

▸ DIMENSIÓN 5 — Frescura
  Comprueba:
  - `<meta property="article:modified_time">` presente en pillars/casos
  - `<time class="page-updated" datetime="">` visible en hero
  - JSON-LD `dateModified` actualizado
  - Sitemap `<lastmod>` refleja mtime real
  - Workflow `weekly-freshness.yml` activo (si no, anota como pendiente)

▸ DIMENSIÓN 6 — Workflow y automatización
  Verifica scripts existentes y su consistencia:
  - Los 15+ scripts listados en `docs/SEO-GUIDE.md` sección 8 existen
  - Pre-commit hook `.git/hooks/pre-commit` instalado
  - `.github/workflows/` tiene weekly-edition, deploy-canary, (freshness
    si está activado)
  - `publish.py` tiene hooks post-publish a patch_home_magazine_seo +
    rebuild_sitemap + seo_polish

▸ DIMENSIÓN 7 — Deuda / pendientes
  Revisa `docs/SEO-GUIDE.md` sección 12 (Roadmap pendiente) y reporta:
  - Cuáles están hechos (✅)
  - Cuáles siguen pendientes (⚠️ o 🔴 si bloquean)
  - Cualquier nueva deuda observada que no esté en la lista

═══════════════════════════════════════════════════════════════════════
CÓMO EJECUTAR LA AUDITORÍA
═══════════════════════════════════════════════════════════════════════

Recomendado: lanza 3-4 sub-agentes en paralelo, cada uno cubriendo 2
dimensiones, para que el reporte sea exhaustivo sin saturar contexto.

Comandos útiles (no exhaustivo, complementa con grep / find / read):

  # Coverage SEO técnico
  python3 -c "..." (ver script de audit en SEO-GUIDE sección 4)

  # QA editorial
  python3 scripts/qa_pillars.py
  python3 scripts/qa_pillars.py --verbose 2>&1 | tail -30

  # Integridad de enlaces
  python3 scripts/purge_dead_links.py --dry-run

  # Sitemap
  python3 scripts/rebuild_sitemap.py --dry-run

  # Búsqueda de patrones sospechosos
  grep -rE "([A-Z][a-z]+).{0,80}\b[0-9]+%" temas/ casos-uso/ sectores/ ciudades/

═══════════════════════════════════════════════════════════════════════
FORMATO DE OUTPUT
═══════════════════════════════════════════════════════════════════════

Bajo 1.500 palabras totales. Estructura:

# Auditoría · {fecha}

## Resumen ejecutivo (1 párrafo)
Estado general del sitio en una línea. ¿Listo para tráfico serio?
¿Hay regresión vs último audit? ¿Algo crítico bloqueante?

## Hallazgos por dimensión

### 1. Integridad técnica  ✅/⚠️/🔴
- (bullet points específicos con file paths)

### 2. SEO técnico  ✅/⚠️/🔴
- ...

### 3. Editorial / cifras  ✅/⚠️/🔴
- ...

### 4. Navegación / UX  ✅/⚠️/🔴
- ...

### 5. Frescura  ✅/⚠️/🔴
- ...

### 6. Workflow / automatización  ✅/⚠️/🔴
- ...

### 7. Deuda pendiente  ✅/⚠️/🔴
- ...

## Métricas finales (tabla)
- Total páginas
- QA OK/WARN/FAIL
- Coverage SEO (canonical, og, jsonld, breadcrumb, title-match)
- Links rotos
- Sitemap URLs

## Top 5 acciones recomendadas (priorizadas)
1. [CRÍTICO] ...
2. [ALTO] ...
3. [MEDIO] ...
4. [MEDIO] ...
5. [BAJO] ...

═══════════════════════════════════════════════════════════════════════
REGLAS NO NEGOCIABLES
═══════════════════════════════════════════════════════════════════════

❌ NO edites archivos durante la auditoría (solo lee + reporta).
   La auditoría es DIAGNÓSTICO. Las correcciones vienen DESPUÉS, en una
   sesión separada con el plan en mano.

❌ NO inventes problemas. Si no encuentras issue, di que está OK.
   La tentación es "encontrar cosas" para parecer útil. Resiste.

❌ NO confíes en tu memoria de cómo "debería" ser el sitio. Lee
   `docs/SEO-GUIDE.md` como source of truth. Si tu memoria difiere
   del guide, gana el guide.

❌ NO uses scripts/select.py shadowea select del stdlib — al ejecutar
   cualquier script, asegúrate de hacer:
     import sys
     if sys.path and sys.path[0].endswith("/scripts"):
         sys.path.pop(0)

✅ SÍ usa file paths absolutos en el reporte
   (`/Users/varis/.../temas/foo/index.html`)

✅ SÍ cita el número de páginas afectadas para cada hallazgo

✅ SÍ usa el verbose mode de scripts cuando hay dudas

✅ SÍ propón scripts nuevos si encuentras un patrón sistemático que
   merezca automatización (pero NO los escribas, solo propónlos)

═══════════════════════════════════════════════════════════════════════
DESPUÉS DE LA AUDITORÍA
═══════════════════════════════════════════════════════════════════════

Si encuentras issues, pregúntame por dónde quiero empezar antes de
fixearlos. Buenas fases típicas:
- FASE 1: Bombazos (críticos que rompen SEO o navegación)
- FASE 2: Estructura (consistencia)
- FASE 3: Frescura (sistema vivo)
- FASE 4: Calidad editorial puntual
- FASE 5: Nuevas features / contenido

Cada fase debe terminar en commit + push + verificación.
```

---

## Cómo usar este prompt

### Caso 1: con Claude (esta CLI / sesión nueva)

1. Abre una sesión nueva de Claude en este repo
2. Pega el prompt entero como primer mensaje
3. Claude hará la auditoría y devolverá el reporte estructurado
4. Después decides qué fixear

### Caso 2: con otro LLM (Cursor, Cline, Aider, etc.)

1. Asegúrate de que el LLM tiene acceso al filesystem del repo
2. Pega el prompt en tu interfaz
3. El LLM debería leer `docs/SEO-GUIDE.md` primero y luego auditar

### Caso 3: como spec para un agente custom

Convierte cada dimensión en una función:
```python
def audit_dimension_1_technical_integrity():
    # check qa_pillars, purge_dead_links, rebuild_sitemap dry-run
    ...
def audit_dimension_2_seo_technical():
    ...
```

Y compón un report runner que las ejecute en paralelo y agrupe outputs.

---

## Versiones anteriores

- **v1** (`docs/AUDIT-PROMPT.md`): auditoría externa SEO básica con web search
- **v2** (`docs/AUDIT-PROMPT-V2.md`): auditoría externa SEO + crecimiento + monetización
- **v3** (este): auditoría INTERNA con acceso al repo, basada en SEO-GUIDE.md
