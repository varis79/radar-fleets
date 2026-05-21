# Long-tail pillar matrix

Sistema de páginas pilar autoescalable para SEO masivo + citación en LLMs.

## Filosofía

**No "generamos N páginas estáticas". Definimos la matriz y un sistema vivo
que gestiona el ciclo de vida**: generación inicial, updates mensuales,
liberación automática `noindex → index`, detección de huecos.

## Arquitectura

```
content/pillar-matrix/
├── README.md              ← este archivo
├── markets.yml            ← 13 mercados con tier_default + active flag
├── topics.yml             ← 28 topics con slug_template + intents + tier_modifier
├── use-cases.yml          ← 14 casos de uso Pulpo con referencias de clientes
│                            reales por mercado (MX/ES)
├── verticals.yml          ← 14 sectores verticales con use cases típicos
├── subgeographies.yml     ← ciudades grandes por mercado para topics core
├── intents.yml            ← 4 intents con schema_type + section_template
├── data-overrides/
│   ├── _template.yml      ← plantilla para cada mercado
│   ├── mexico.yml
│   ├── espana.yml
│   └── ... (uno por mercado activo)
├── matrix.csv             ← export del estado actual
└── pages/                 ← .md por página, generados en SEO-3.2
```

## 4 dimensiones de páginas

El sistema genera páginas cruzando estas dimensiones. Cada combinación
válida produce una URL única en un directorio diferente:

| Dimensión | URL pattern | Lo que es |
|---|---|---|
| `topic` | `/temas/<slug>/` | market × topic × intent. Páginas temáticas. |
| `use-case` | `/casos-uso/<slug>/` | caso de uso Pulpo × market × intent. Páginas operativas con referencias de clientes Pulpo reales. |
| `vertical` | `/sectores/<slug>/` | vertical (industria del cliente final) × market. |
| `subgeo` | `/ciudades/<slug>/` | ciudad grande × topic core. Long-tail local. |

Volumen actual: ~900 páginas planeadas.

## Cómo se calcula cada página

1. **Iteración**: por cada `market` activo × por cada `topic` aplicable a ese
   market × por cada `intent` definido en el topic.
2. **Slug**: `topic.slug_template` con `{market_slug}` y `{year}` sustituidos,
   más sufijo de `intent` cuando no es informational.
3. **Tier**: `market.tier_default + topic.tier_modifier`, con excepción de
   que markets T1 con topics core (modifier=0) son siempre T1.
4. **Schedule de revisión**: heredado del tier (T1=30d, T2=60d, T3=90d) o
   override por intent (ej. regulatorio=30d siempre).

## Comandos útiles

```bash
# Ver el estado de la matriz
python -m scripts.inspect_matrix

# Solo Tier 1 (las que se generan primero)
python -m scripts.inspect_matrix --tier 1

# Solo un mercado
python -m scripts.inspect_matrix --market colombia

# Exportar a CSV
python -m scripts.inspect_matrix --csv > matrix.csv
```

## Reglas anti-penalización (críticas)

1. **Tier 2/3 arrancan en `noindex`**: no entran a sitemap hasta cumplir threshold.
2. **Contenido único ≥ 30%** por página: validado por LLM verificador antes de liberar.
3. **Schema.org consistente** por intent (Article / HowTo / FAQPage).
4. **Updates con material editorial real**, no solo cambio de fecha.
5. **URLs únicas y canonical claro**: una URL por (market, topic, intent).

## Próximos pasos (roadmap dentro de PR-SEO-3)

- **SEO-3.1** (este PR): estructura YAML + script de inspección. Sin contenido aún.
- **SEO-3.2**: generador LLM de skeletons + slots Pulpo/PulpoPay.
- **SEO-3.3**: sistema de updates mensuales por schedule.
- **SEO-3.4**: threshold automático noindex → index + verificador LLM.
- **SEO-3.5**: auto-detección de huecos → GitHub Issue propuesta.
