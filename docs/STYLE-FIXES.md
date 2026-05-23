# The Fleet Radar · Lista negra de clichés IA

Documento de trabajo para limpieza editorial (ítem A-6 de la auditoría 2026-05-22).

Origen: grep sobre 147 pillar pages + 7 ediciones. Frecuencias brutas.
Criterio de inclusión: términos que suenan genéricos, de consultoría o LLM-generated.

---

## 🔴 Prioridad máxima (aparecen en casi todas las páginas)

### `ecosistema` — 130 ocurrencias

**Problema:** La palabra más sobreutilizada de todo el site. "Ecosistema de Pulpo", "ecosistema de proveedores", "ecosistema de soluciones"... Todo es un ecosistema. Es la palabra que más delata el origen LLM.

**Ejemplos reales:**
- *"publicación editorial dentro del ecosistema de Pulpo"*
- *"El ecosistema de electrificación de flotas en España..."*

**Alternativas según contexto:**
| Contexto | En lugar de | Usa |
|---------|-------------|-----|
| Software/plataforma | ecosistema de herramientas | conjunto de herramientas, plataforma, suite |
| Proveedores | ecosistema de players | mercado de proveedores, oferta disponible |
| Sector | ecosistema de movilidad | sector del transporte, mercado de flotas |
| Pulpo | dentro del ecosistema de Pulpo | publicación de Pulpo |

---

### `cada vez más` — 39 ocurrencias

**Problema:** Vaguedad pura. Dice que algo aumenta sin decir cuánto, cuándo ni por qué. Siempre se puede sustituir por un dato o una afirmación más concreta.

**Ejemplos reales:**
- *"los fabricantes de vehículos comerciales integran cada vez más tecnología nativa"*
- *"los controles de gasto determinan cada vez más la elección"*

**Regla:** Eliminar o sustituir por el dato que lo respalde. Si no hay dato → reformular en pasado afirmativo (*"el gasto en telemática creció 18% en 2025"*).

---

### `es clave` / `es clave para` — 31 ocurrencias

**Problema:** Todo "es clave" no dice nada. Es la muletilla de los LLMs para rematar párrafos.

**Ejemplos reales:**
- *"Los actores clave en la adaptación ZBE"* ← aquí "clave" está bien (actores principales)
- *"los cambios tarifarios en corredores clave"* ← aceptable como adjetivo
- Problemático: *"La gestión del combustible es clave para la rentabilidad"*

**Regla:** Sustituir por el verbo de acción (*"determina", "define", "impacta directamente"*). Conservar solo cuando es adjetivo antes de sustantivo (*"actores clave"*, *"corredor clave"*).

---

### `transformación digital` — 29 ocurrencias

**Problema:** Buzzword corporativo de 2018 que ha perdido todo significado. En 2026 ya no es una "transformación": es el estado normal del sector.

**Ejemplos reales:**
- *"La transformación digital del sector se acelera ante las presiones..."*
- *"cobertura especializada sobre la transformación digital del transporte"*

**Alternativas:**
- *"digitalización operativa"*, *"adopción de telemática"*, *"gestión basada en datos"*
- O directamente: *"Las flotas que no usan datos en tiempo real..."* (sin nombrar la transformación)

---

## 🟡 Prioridad media

### `en un contexto de` — 11 ocurrencias

Fórmula de inicio de párrafo típica de LLM. *"En un contexto de presión regulatoria..."* → *"Con la regulación apretando..."* o *"Ante la presión regulatoria..."*.

### `es fundamental` — 9 ocurrencias

Igual que "es clave". *"Es fundamental entender..."* → *"Para entender... hay que..."* o simplemente cortar y decirlo directo.

### `sin precedentes` — 6 ocurrencias

Casi nunca es verdad. *"presiones sin precedentes"* → especificar qué presión y desde cuándo.

---

## 🟢 Prioridad baja (aparecen poco, pero son ruidosas)

| Término | Ocurrencias | Alternativa |
|---------|------------|-------------|
| `solución integral` | 4 | software de gestión de flotas, plataforma, suite |
| `valor añadido` | 4 | ventaja diferencial, beneficio concreto |
| `hoja de ruta` | 4 | plan, calendario, pasos a seguir |
| `permite optimizar` | 2 | mejora, reduce, recorta |
| `gestión eficiente` | 2 | gestión ágil / gestión con datos / [ser específico] |
| `mejora continua` | 1 | [eliminar o especificar qué mejora] |

---

## Términos aceptados (no eliminar)

Estos términos PARECEN clichés pero tienen uso editorial legítimo en este contexto:

- **`flota`** — es el término técnico correcto
- **`telemática`** — término de industria, no sustituir
- **`compliance`** — anglicismo aceptado en el sector (cumplimiento normativo es más largo y menos preciso)
- **`players`** — en el contexto de "players del mercado" es aceptable; evitar en otros contextos
- **`nearshoring`** — término económico establecido

---

## Cómo aplicar estas correcciones

1. **Nuevas pillar pages**: actualizar el system prompt del LLM en `prompts/radar-master-prompt.md` con esta lista negra.
2. **Páginas existentes**: corrección manual prioritizando las páginas de México y España (las que recibirán tráfico antes).
3. **Verificación**: tras cada corrección, re-grep para confirmar que el término desapareció de la página.

### Grep de verificación rápida:
```bash
grep -r "ecosistema\|cada vez más\|transformación digital\|es clave\|sin precedentes" \
  temas/ casos-uso/ sectores/ ciudades/ --include="*.html" | wc -l
```
Baseline actual: **~247 ocurrencias**. Objetivo: < 30 (solo usos justificados).
