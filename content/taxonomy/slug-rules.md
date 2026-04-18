# Reglas de slug y URL

Convenciones para que todas las URLs de The Fleet Radar sean coherentes y no haya que adivinar.

## Reglas generales

1. **Español sin tildes ni signos.** Todo slug se escribe sin acentos, sin ñ (se convierte en `n`), sin signos. `españa` → `espana`. `México` → `mexico`. `mantenimiento predictivo` → `mantenimiento-predictivo`.
2. **Kebab-case.** Palabras separadas por guion medio. Nunca underscore, nunca camelCase.
3. **Minúsculas siempre.**
4. **Sin año en slug, salvo ediciones.** `/temas/fuel-cards/`, no `/temas/fuel-cards-2026/`. Las ediciones sí llevan fecha: `2026-04-17-radar-fleet-by-pulpo.html`.
5. **Sin abreviaturas ambiguas.** `vehiculos-comerciales-ligeros`, no `lcv` ni `vcl`. Excepción: siglas reconocidas dentro de la comunidad (`adas`, `ev`, `hdv`) cuando el contexto lo clarifica.
6. **Singular siempre que pueda.** `tema` → `topic`, `player`, `mercado`, `guia`, `checklist`. En URL el contenedor va en plural (`/temas/`, `/players/`, `/mercados/`) pero el slug interno no se repluraliza.

## Estructura de URLs

```
/                                            → home (copia de la última edición)
/archive.html                                → listado de ediciones
/magazines/YYYY-MM-DD-radar-fleet-by-pulpo.html
                                             → permalink de edición
/temas/{topic-slug}/                         → página de tema
/players/{player-slug}/                      → ficha de player
/mercados/{market-slug}/                     → página de mercado (geo primary + aggregate)
/evergreen/{tipo}/{slug}/                    → pieza evergreen
```

Tipos válidos dentro de `/evergreen/`:

- `guias/` — guías largas.
- `checklists/` — listas accionables.
- `comparativas/` — comparativas de producto.
- `explicadores/` — piezas cortas de tecnología/concepto.
- `faqs/` — preguntas frecuentes.
- `errores/` — "errores comunes al...".

## Hubs padres

No crear `/temas/`, `/players/`, `/mercados/` como páginas autónomas hasta que cada contenedor tenga **5+ hijos** y un texto editorial curado.

Hasta entonces:

- La navegación entre páginas de un mismo tipo se hace por footer y por bloques "Explora por tema" / "Temas relacionados" dentro del propio contenido.
- Un hub vacío o con 1-2 hijos es thin content. No se publica.

## Convenciones de metadatos

### Title

Patrón según tipo:

- Tema: `{Tema}: {subtítulo accionable} — The Fleet Radar · by Pulpo`
- Player: `{Player} · ficha de mercado — The Fleet Radar · by Pulpo`
- Market: `Flotas en {Market} 2026 · regulación, players y mercado — The Fleet Radar · by Pulpo`
- Evergreen guía: `Guía: {Asunto específico} — The Fleet Radar · by Pulpo`
- Evergreen checklist: `Checklist: {Asunto específico} — The Fleet Radar · by Pulpo`
- Evergreen explicador: `{Sigla o nombre} explicado para flotas — The Fleet Radar · by Pulpo`
- Evergreen comparativa: `{A} vs {B} vs {C} para flotas {geografía} — The Fleet Radar · by Pulpo`
- Evergreen FAQ: `FAQ: {Asunto} — The Fleet Radar · by Pulpo`
- Evergreen errores: `{N} errores al {verbo} — The Fleet Radar · by Pulpo`
- Edición: `The Fleet Radar · by Pulpo · Nº {N} · {titular} · {fecha}`

### Meta description

- Entre 140 y 160 caracteres.
- Frase periodística con dato o fecha concreta.
- Sin clickbait, sin "descubre", sin "todo lo que necesitas saber".

### Open Graph

- `og:title` = mismo patrón que `<title>` pero sin la parte de marca.
- `og:description` = primera frase editorial fuerte del contenido.
- `og:url` = URL canónica.
- `og:type` = `article` para ediciones y evergreen, `website` para topic/player/market hubs, archivo, 404.

## Canonical

- Ediciones: canonical apunta a su permalink `/magazines/...`.
- `index.html`: canonical a `https://thefleetradar.com/` + `alternate` al permalink de la edición copiada.
- Topic, player, market, evergreen: canonical a su propia URL.
- 404: canonical a home.

## Redirecciones

En `vercel.json` se mantienen cortas y útiles:

- `/archivo` → `/archive.html`
- `/feed`, `/feed.xml` → `/rss.xml`
- `/last`, `/latest` → `/`

Cuando un slug cambie (excepción, no regla), añadir redirect 301 en `vercel.json` y notificar en `editorial-memory.md`.

## Prohibido

- URLs con mayúsculas.
- URLs con parámetros para variantes editoriales (`?tag=...`).
- URLs duplicadas con y sin barra final (forzar con barra final en directorios `/temas/foo/`, sin barra en archivos `foo.html`).
- Generar páginas para cualquier micro-tag.
- Hubs padres vacíos.
