# Propuesta — páginas temáticas, de players, mercados y evergreen

Arquitectura acumulativa del sitio para SEO, navegación y captación. Alineada con la taxonomía formal de `content/taxonomy/`.

**Regla dura:** no se crean páginas automáticas. Solo páginas indexables con valor evergreen, material suficiente, intro útil redactable y aporte a navegación + SEO + captación. Ver los cinco criterios en `content/taxonomy/README.md`.

## Estructura pública

```
/temas/{slug}/               → topics (hoy 2; llegarán a 4-6 en Q2, 10+ en Q3)
/players/{slug}/             → players (uno inicial: pulpo)
/mercados/{slug}/            → markets (primary + aggregate)
/evergreen/{tipo}/{slug}/    → piezas evergreen (guías, checklists, explicadores, etc.)
```

Hubs padres (`/temas/`, `/players/`, `/mercados/`, `/evergreen/`) no se crean hasta acumular 5+ hijos. Hasta entonces, navegación por footer y bloques "Explora por tema" dentro del contenido.

## Ya creado (producción)

- `/temas/compliance-espana/` — V-16, tacógrafo G2V2, ADAS, ZBE.
- `/temas/regulacion-mexico/` — CNE hidrocarburos, Programa 6.000 MDP, SICT.

## Tanda 1 — crear después del PR de taxonomía

Esta es la prioridad final consensuada. Son cuatro páginas que cumplen los cinco criterios y cubren huecos reales:

| # | URL | Tipo | Por qué ahora |
|---|---|---|---|
| 1 | `/mercados/mexico/` | market primary | Landing geográfica MX, prioridad editorial máxima. Agrupa regulación, players activos y ediciones. |
| 2 | `/mercados/espana/` | market primary | Landing geográfica ES, prioridad editorial máxima. Complemento natural a compliance-espana. |
| 3 | `/players/pulpo/` | player (casa) | Página editorial de la casa. Extracto de `pulpo-facts.md`. Mueve leads por SEO directo. |
| 4 | `/temas/fuel-cards/` | topic | Tres ediciones con material denso. Búsqueda alta. Sin competencia editorial seria en español. |

## Tanda 2 — siguiente, no en este PR

| # | URL | Tipo | Por qué no ahora |
|---|---|---|---|
| 5 | `/mercados/latam/` | market aggregate | Requiere masa crítica de material por país antes de agregar. |
| 6 | `/temas/electrificacion-flotas/` | topic | Material abundante pero mejor después de tener fuel-cards publicada para cruzar enlaces. |
| 7 | `/evergreen/guias/peaje-europa-2026/` | evergreen guía | Primera guía evergreen. Mejor tras consolidar `/mercados/espana/` para apuntarla. |
| 8 | `/evergreen/checklists/evaluar-telematica-2026/` | evergreen checklist | Alta intención comercial. Se crea con un esqueleto de arquitectura ya estable. |

## Tanda 3 — Q3 2026

Topics:

- `/temas/telematica-flotas/`
- `/temas/video-telematica/`
- `/temas/mantenimiento/`
- `/temas/compliance-mexico/` (separación de `regulacion-mexico` si crece mucho)
- `/temas/compliance-usa/`
- `/temas/control-gasto/`

Players (cuando cada uno tenga 3+ menciones sustanciales + ángulo propio):

- `/players/samsara/`
- `/players/motive/`
- `/players/geotab/`
- `/players/fleetio/`
- `/players/corpay/`

Markets:

- `/mercados/europa/`

Evergreen (orden de `content/evergreen-plan.md`):

- `/evergreen/explicadores/mcs-charging/`
- `/evergreen/guias/criterios-evaluar-fuel-card/`
- `/evergreen/comparativas/samsara-motive-geotab-es-latam/`
- `/evergreen/faqs/ice-a-ev-flota-mixta/`
- `/evergreen/errores/implementacion-telematica-primera-vez/`
- `/evergreen/checklists/revision-mensual-flota/`

## Qué NO crear (al menos de momento)

- Páginas por micro-tag. Nunca.
- Páginas por país fuera del top-2 primary + LatAm + Europa aggregate.
- Hubs padres vacíos (`/temas/` solo, etc.).
- Páginas por autor/editor.
- Página "Sobre The Fleet Radar" — si se pide, vive como `about` discreto en footer, sin URL propia destacada.
- Newsletter subscribe — RSS y archivo cubren. Si se integra email, será embed de Buttondown o Beehiiv, no página propia.
- Páginas por fleet-type a granel. Solo si el vertical tiene búsqueda real y material (evaluar con los cinco criterios).

## Requisitos técnicos de cada página pública

1. **Estructura**:
   - `<h1>` claro, ≤10 palabras.
   - Intro editorial de 300–500 palabras.
   - Sección "Ediciones que hablan de esto" con 3–N enlaces a `/magazines/...`.
   - Sección "Cifras de referencia" (3–5 datos de `market-watch.md`).
   - CTA suave a Pulpo con el copy acordado (ver `pulpo-facts.md`).
2. **Metadatos**:
   - `<title>` y `<meta description>` según patrones de `slug-rules.md`.
   - Open Graph + Twitter card completos.
   - `<link rel="canonical">` a la URL propia.
   - Entrada en `sitemap.xml`.
3. **CSS**: carga `/assets/radar.css`. Puede declarar acento propio en `:root` si conviene al tema.
4. **Geografía**: si la página tiene geografía clara, lleva `.geo-tag.{country}` en header y en metadatos OG.
5. **Cadencia de actualización**: revisión mínima trimestral. Fecha "actualizado" visible al pie.
