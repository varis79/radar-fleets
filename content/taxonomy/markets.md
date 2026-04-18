# Markets — geografías

Sistema de clasificación geográfica del contenido. Sirve al mismo tiempo como:

- etiqueta interna en cada historia, señal, player y regulación,
- sistema visual de presentación (banderas, colores, kickers),
- base para páginas públicas de mercado cuando lleguen.

**Prioridad editorial:** México y España. El resto se cubre cuando hay señal real.

## Tiers

| Slug | Flag | Tier | Página pública | Uso |
|---|---|---|---|---|
| `mexico` | 🇲🇽 | Primary | **Sí** (PR #6) | Prioridad editorial alta |
| `espana` | 🇪🇸 | Primary | **Sí** (PR #6) | Prioridad editorial alta |
| `usa` | 🇺🇸 | Secondary | No por ahora | Cobertura constante |
| `colombia` | 🇨🇴 | Secondary | No | Cobertura cuando haya señal |
| `brasil` | 🇧🇷 | Secondary | No | Cobertura cuando haya señal |
| `chile` | 🇨🇱 | Secondary | No | Cobertura cuando haya señal |
| `peru` | 🇵🇪 | Secondary | No | Cobertura cuando haya señal |
| `argentina` | 🇦🇷 | Secondary | No | Cobertura cuando haya señal |
| `latam` | 🌎 | Aggregate | **Sí** (PR siguiente al #6) | Visión regional |
| `europa` | 🇪🇺 | Aggregate | Q3 | Cuando haya 3+ ediciones con material |
| `global` | 🌐 | Aggregate residual | No, es etiqueta | Señales globales sin geo única |

## Reglas de etiquetado

- **Una historia = una geografía primaria.** Si afecta a dos, se etiqueta con ambas y se explica en el texto.
- **Regulación de un país no se mezcla con mercado de otro sin contexto.** Si Austria cambia peajes y eso afecta al operador español, se redacta diciendo exactamente eso.
- **Banderas con criterio**, no decoración. Cada historia lleva flag en el meta y el kicker regional de la sección.
- **LatAm como agregador** no sustituye a México, Colombia, Brasil. Si la señal es específica de un país, va a ese país primero.
- **Global** se usa poco. Solo para jugadores/datos verdaderamente transversales (p.ej. mercado mundial de fleet management $32B).

## Jerarquía editorial

- Sección México y sección España siempre aparecen en la edición, aunque sea con 2-3 señales.
- Sección Internacional agrupa USA + Europa + LatAm cuando el volumen no justifica secciones propias.
- Si hay material abundante de un tercer país (p.ej. Colombia con 5+ señales en una semana), puede tener su propio radar regional esa edición.

## Banderas y colores (clases CSS)

Ver `assets/radar.css` (`.geo-tag.mx`, `.geo-tag.es`, `.geo-tag.usa`, etc.). Un emoji de bandera dentro del tag, plus color característico asociado al país o región.

## Descubrimiento

Cuando una edición toca un país que todavía no está clasificado (p.ej. `republica-dominicana`), se añade aquí como secondary en estado "observación" con primera aparición fechada.
