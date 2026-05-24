# Raw facts batches (input crudo de los LLMs)

Aquí se guardan los outputs originales de cada LLM consultado vía megaprompt,
antes de normalización + dedupe.

**No editar directamente** estos archivos. Son la fuente de auditoría para
saber de qué LLM vino qué fact.

## Pipeline

1. Usuario pega output de cada LLM → guardo crudo aquí
2. Agente especialista normaliza al tono editorial y dedupea entre fuentes
3. Resultado consolidado se guarda en `content/sabias-que-pool.md`
4. Cuando estén todos los batches → integración a `scripts/rotate_facts.py`

## Batches recibidos

| LLM | Archivo | Facts entregados | Estado |
|---|---|---|---|
| Perplexity | batch-01-perplexity.json | 12 | ✅ normalizado (v1) |
| Grok | batch-02-grok.json | 16 | ✅ normalizado (v2) |
| Gemini | batch-03-gemini.json | ~40 | ⏳ pendiente normalizar |
| DeepSeek | batch-04-deepseek.json | ~84 | ⏳ pendiente normalizar |
| ChatGPT | batch-05-chatgpt.json | ~60 | ⏳ pendiente normalizar |
| Claude | — | — | ⏳ pendiente recibir |

**Target total**: ~200-300 facts únicos (después de dedupe).
