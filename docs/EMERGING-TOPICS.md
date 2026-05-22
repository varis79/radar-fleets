# Sistema vivo · Detección de temas emergentes

Mecanismo automático para que la matriz long-tail NO se quede estática.
Detecta clústeres de noticias sobre temas que no están en la matriz y
propone añadirlos vía GitHub Issue. Tú apruebas con `/approve` o
descartas con `/reject`. El sistema aplica los cambios solo.

## Flujo

```
[mes 1]                  [mes 2]                  [mes 3]
    │                        │                        │
    ▼                        ▼                        ▼
[cron mensual]          [cron mensual]          [cron mensual]
    │                        │                        │
    ▼                        ▼                        ▼
detect-emerging-topics.yml  (workflow GitHub Actions)
    │
    ├─ Lee últimas 12 semanas de content/raw/*-classified.jsonl
    ├─ Llama a Claude Opus con prompt "emerging-topics-prompt.md"
    └─ Recibe propuestas tipo new_topic / new_subgeo / gap
    │
    ▼
Por cada propuesta → abre GitHub Issue con label `topic-suggested`
    │
    ▼
Tú comentas /approve o /reject
    │
    ├─ /reject → cierra issue
    └─ /approve → approve-emerging-topic.yml workflow se dispara
                    │
                    ├─ Extrae JSON del body del issue
                    ├─ Corre scripts/expand_matrix.py
                    │   ├─ new_topic → añade a topics.yml
                    │   ├─ new_subgeo → añade a subgeographies.yml
                    │   └─ gap → no edita YAML (marca prioridad)
                    │
                    └─ Crea PR `claude/matrix-expand-{issue}`
                        ├─ Cierra automáticamente el issue al mergear
                        └─ La matriz se amplía. Las nuevas combinaciones
                           se pueden generar con generate-pillar-pages.yml.
```

## Tipos de propuestas

### A · Nuevo topic
Cluster de ≥4 headlines sin mapeo a topic existente.
Ejemplo: 6 historias sobre "hidrógeno verde fleet" → propone topic `hidrogeno-verde-flotas`.

### B · Nueva subgeografía
Ciudad mencionada en ≥3 headlines sin slot.
Ejemplo: "Querétaro" mencionado 4 veces sin estar en `subgeographies.yml` → propone añadir.

### C · Gap en combinación existente
Tema con ≥5 historias pero sin página pilar generada todavía.
Ejemplo: `compliance × espana` con 6 historias y la página `/temas/compliance-flotas-espana-2026/` aún sin LLM. → propone priorizar generación.

## Cron

- **Schedule**: primer martes del mes a las 09:00 UTC.
- **Manual**: workflow_dispatch desde Actions UI con input `weeks` (default 12).

## Coste

~$0.20-0.50/mes una llamada LLM mensual (Opus). Si no hay propuestas razonables, no abre ningún issue.

## Auth para /approve

Por defecto solo el owner del repo puede aprobar. Si querés ampliar a colaboradores, editar la lógica en `approve-emerging-topic.yml > steps > "Check author"`.

## Ejecutar manualmente para testear

```bash
# Local (dry-run, sin gastar tokens)
python -m scripts.detect_emerging_topics --weeks 12 --dry-run --output /tmp/p.json
python -m scripts.expand_matrix --proposal-file /tmp/p.json --dry-run

# En GitHub Actions
# 1. Actions → "Detect · Emerging topics" → Run workflow
# 2. Espera 1-2 min
# 3. Mira los Issues creados con label `topic-suggested`
# 4. Comenta `/approve` o `/reject` en uno
# 5. Verás un nuevo PR `claude/matrix-expand-N` con los cambios
```

## Cómo desactivarlo temporalmente

Para pausar:
- Si querés pausar TODO: borra el workflow yml o cambia el cron a `'0 0 1 1 *'` (1 enero, casi nunca).
- Si querés pausar solo el approval automático: deshabilita el workflow `approve-emerging-topic.yml` desde Actions UI.

## Archivos relevantes

- `prompts/emerging-topics-prompt.md` — prompt del detector.
- `scripts/detect_emerging_topics.py` — detector.
- `scripts/expand_matrix.py` — aplica una propuesta al YAML.
- `.github/workflows/detect-emerging-topics.yml` — cron mensual.
- `.github/workflows/approve-emerging-topic.yml` — handler de /approve.
