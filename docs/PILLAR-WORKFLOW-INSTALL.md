# Instalar workflow · Generate Pillar Pages

El workflow `.github/workflows/generate-pillar-pages.yml` no se puede subir
por PR (el PAT del bot no tiene scope `workflow`). Sigue estos pasos para
crearlo manualmente desde la UI de GitHub.

## Pasos

1. Ve a https://github.com/varis79/radar-fleets/tree/main/.github/workflows
2. Botón **Add file → Create new file**.
3. Nombre exacto: `generate-pillar-pages.yml`
4. Pega el contenido del archivo (lo tienes en local en `.github/workflows/generate-pillar-pages.yml`, o copia del bloque más abajo).
5. Baja al final → **Commit directly to the main branch** → **Commit new file**.

## Cómo usarlo

1. https://github.com/varis79/radar-fleets/actions
2. Menú izquierdo: **Generate · Pillar pages**
3. Botón **Run workflow** (arriba a la derecha)
4. Configura:
   - **mode**:
     - `single`: 1 página por slug (prueba puntual, ~$0.10)
     - `tier`: todas las páginas de un tier (T1 ≈ 139 páginas, ~$15, ~25 min)
     - `filter`: combinación tier+dimension+market
   - **slug** (solo si mode=single): ej. `telematica-flotas-mexico-comparativa-2026`
   - **tier**: 1, 2 o 3
   - **dimension**: topic, use-case, vertical, subgeo
   - **market**: mexico, espana, colombia, etc.
   - **limit**: opcional, máximo de páginas a generar (para tests)
   - **indexed**: `false` (default, noindex) o `true` (publicar sin noindex)
5. Pulsa **Run workflow**.
6. Espera (single: 15s; tier 1: ~25 min).
7. Cuando termine, abre el PR creado con label `pillar-pages-generated`.
8. Revisa el contenido y merge si está bien.

## Flujos típicos

### Prueba piloto antes de generar masivo

```
mode: single
slug: telematica-flotas-mexico-comparativa-2026
```

Genera 1 página con Claude Opus en ~15 segundos. Coste: ~$0.10. Revisa el PR
y la calidad. Si todo OK, lanza el bulk.

### Generación masiva T1 (~139 páginas)

```
mode: tier
tier: 1
```

Genera todas las T1. ~25 min, ~$15. Crea un PR con 139 archivos. Revisa por
muestreo (no hace falta leer las 139 enteras; con revisar 5-10 al azar es
suficiente). Si OK, merge.

### Solo casos de uso de México

```
mode: filter
tier: 1
dimension: use-case
market: mexico
```

Genera solo las pillar pages de tipo use-case en México y Tier 1. Útil para
iteración por subset.

## Después del merge

Las páginas mergeadas se publican en Vercel automáticamente (mismo flujo
que las ediciones semanales). Estarán accesibles en sus URLs (en noindex
si no pediste `indexed=true`).

Los hubs (`/temas/`, `/casos-uso/`, `/sectores/`, `/ciudades/`) detectarán
automáticamente las páginas publicadas en el próximo build (o al ejecutar
`python -m scripts.build_hubs` localmente).
