# QA checklist — The Fleet Radar

Checks aplicados por `scripts/qa.py` antes de publicar cualquier edición. Son la barrera entre el pipeline autónomo y el lector. Si algún bloqueante falla, la edición no sale.

## Bloqueantes

### C1 · Framing interno prohibido

La capa pública nunca muestra labels, pills, secciones, microcopy o cuerpos con framing interno o comercial de Pulpo.

Lista específica (regex en `scripts/lib/forbidden.py`):

- `competidor`, `competidor directo`, `competidor / referencia`, `competidor / señal`, `competidor PulpoPay`
- `competitor watch`, `vigilancia competitiva`, `señal competitiva`
- `oportunidad partner`, `oportunidad de partner`, `argumento comercial`, `argumento de mercado más contundente`
- `referencia de producto`, `inspiración de producto`
- `educación al cliente`
- `Para Pulpo`, `Pulpo debe`, `Pulpo necesita`, `PulpoPay necesita`, `implicación para Pulpo`
- `roadmap de Pulpo`, `tesis de producto de Pulpo`
- Pills/tags `<span>` con clasificación interna visible

### C2 · Thin content

- Edición entera: mínimo `qa.min_words_edition_short` palabras (ver `pipeline-config.yml`).
- Cada story: mínimo `qa.min_words_story` palabras en summary + why_operator + why_business.

### C3 · Voz editorial

- Em dashes en prosa (`—`) = 0.
- Estructuras "no es X, es Y" detectadas → bloqueo.

### C4 · Metadatos obligatorios

- `<title>` no vacío.
- `<meta name="description">`.
- `<link rel="canonical">` absoluto (https://).
- `<meta property="og:url">`.
- `<meta property="article:published_time">`.

### C5 · Estructura HTML

- Exactamente 1 `<h1>`.
- Secciones presentes: `.cover`, `.editors-note`, `.cta-band`, `.closing`.

### C6 · Enlaces internos

- Todos los `<a href="/...">` apuntan a fichero existente en el filesystem del repo.
- Excepciones toleradas: `/_vercel/*` (inyectado por Vercel en runtime).

### C7 · Repetición sin novedad

- Cover headline no puede tener ratio ≥ 0.85 con el headline de alguna de las últimas 8 ediciones en `content/editorial-memory.md`.

### C8 · Claims sensibles sin fuente

- "el mejor", "el peor", "el único", "el líder" sin fuente → bloqueo.
- "más barato que X", "más caro que X" sin fuente → bloqueo.
- "N% menos", "N% más" sin "según", "fuente" en el contexto inmediato → bloqueo.

### C9 · Stub marker

- Si el HTML contiene `[stub:` → bloqueo. El pipeline marca así las ediciones generadas sin LLM (modo de prueba del workflow).

## Avisos (no bloquean, quedan en el informe)

### A1 · Mix geográfico

- Ratio México+España < `selection.geo_min_primary_ratio` → aviso.

### A2 · Diversidad de topics

- Topics distintos en stories < `selection.topic_min_diversity` → aviso.

## Cómo se actúa según resultado

- **Todo OK**: publish corre, PR se abre con label `ready-to-review`.
- **Bloqueante**: publish no corre. PR queda con label `needs-editorial-fix` y el informe `content/qa/YYYY-WW-report.md` lista lo que falla.
- **Pausa**: si select devolvió modo pause, no se ejecuta compose ni publish. Se registra en editorial-memory.

## Añadir un check nuevo

1. Añadir la función en `scripts/qa.py`.
2. Documentar aquí como bloqueante o aviso.
3. Si el check implica texto prohibido, añadir regex en `scripts/lib/forbidden.py`.
4. Ejecutar `python -m scripts.qa` contra la última edición publicada para asegurar que no se dispara un falso positivo retroactivo.
