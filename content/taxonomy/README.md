# Taxonomía editorial — The Fleet Radar · by Pulpo

Sistema de clasificación que sostiene la publicación semanal y el contenido acumulativo (temas, players, mercados, tipos de flota y micro-tags).

Este directorio es la fuente única de verdad para:

- cómo clasificar cada historia semanal,
- cómo alimentar memoria editorial,
- cómo decidir qué merece página pública,
- cómo descubrir nuevos actores sin duplicarlos,
- cómo etiquetar para SEO + AI search + navegación interna.

## Dos niveles, nunca mezclar

### Nivel interno (siempre rico)

Todo se etiqueta. Toda entidad nueva entra en el registro. No hay límite de granularidad. Incluye:

- `topics.md` — ejes editoriales.
- `players.md` — fichas de actores por categoría.
- `markets.md` — geografías con tiers y banderas.
- `fleet-types.md` — tipos de flota, verticales y casos de uso.
- `micro-tags.md` — vocabulario controlado granular (dispositivos, regulaciones, normas, siglas, productos, integraciones…).

Estos archivos son los que consulta el flujo semanal antes de escribir. Son los que se actualizan al cerrar la edición.

### Nivel público (selectivo y editorial)

Solo hay página pública cuando se cumplen los cinco criterios:

1. **Valor evergreen** — no caduca con una noticia.
2. **Material suficiente** — 2+ ediciones o 3+ menciones sustanciales.
3. **Introducción útil redactable** — no se rellena con aire.
4. **Aporta a navegación, SEO y captación** — hueco real en la búsqueda en español.
5. **No crea thin content** — si no da para 400+ palabras con datos, se espera.

Si falla alguno, no hay página.

## Las cinco capas

| Capa | Archivo | ¿Puede ser pública? |
|---|---|---|
| Topics | `topics.md` | Sí, cuando cumple los 5 criterios |
| Players | `players.md` | Sí, 3+ menciones + ángulo propio |
| Markets | `markets.md` | Sí, tier primary o aggregate top |
| Fleet types | `fleet-types.md` | Sí, solo si acumula material y búsqueda real |
| Micro-tags | `micro-tags.md` | **Nunca** |

## Convenciones de slug y URL

Ver `slug-rules.md`. Regla corta: español sin tildes, kebab-case, sin año en slug salvo ediciones.

## Flujo semanal con taxonomía

1. Antes de curar: leer `topics.md`, `players.md`, `markets.md`, `fleet-types.md`, `micro-tags.md` + `editorial-memory.md` + `market-watch.md` + `pulpo-update.md`.
2. Cada historia de la edición lleva etiquetas internas: 1 topic, 1 fleet-type (cuando aplique), 1-3 players, 1 market, N micro-tags.
3. Al cerrar: pass de descubrimiento (ver `discovery-playbook.md`) → actualizar `players.md` si aparecen nuevos actores.
4. Las etiquetas se guardan en el resumen de la edición (summary.txt) y en la memoria editorial (editorial-memory.md).
5. Nunca se crea página pública automáticamente.

## Qué no hace este sistema

- No clasifica en Inglés. Todo en español.
- No crea páginas por cada tag. Eso es thin content.
- No genera páginas de "autor", "newsletter" o "acerca de" por defecto.
- No mezcla capas dentro del mismo slug (un market no vive en `/temas/`).
