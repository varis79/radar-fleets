# Prompt maestro de auditoría externa

Para usar con ChatGPT (con web search), Gemini Pro (con grounding) y
Perplexity (Pro Search ideal). Pega el bloque tal cual.

Sirve para que cada LLM crawlee el sitemap, analice URLs muestra y devuelva
un informe estructurado de 8 secciones.

---

## Prompt (copiar literal)

```
Actúa como consultor senior SEO + editorial + brand strategy. Vas a auditar
un medio editorial recién lanzado: The Fleet Radar (https://thefleetradar.com).

CONTEXTO:
- The Fleet Radar es una publicación semanal editorial publicada por Pulpo
  (https://getpulpo.com), empresa de gestión de flotas fundada en 2018 que
  gestiona +200.000 vehículos en MX/ES.
- Pulpo tiene dos productos: Pulpo SaaS (gestión documental, mantenimiento,
  control flotas) y PulpoPay (tarjetas de combustible + control de gasto B2B).
- El medio cubre: telemática, fuel cards, electrificación, mantenimiento,
  regulación, logística, IA aplicada a flotas. Foco MX/ES + cobertura
  LatAm/USA/Europa.
- Sale cada lunes. ~10 ediciones publicadas + ~140 páginas pilar SEO en
  4 dimensiones: /temas/, /casos-uso/, /sectores/, /ciudades/, /mercados/.
- Voz editorial: periodismo sobrio, datos sobre adjetivos, sin hype, sin
  lenguaje de marketing.

ACCIÓN: Lee el sitemap https://thefleetradar.com/sitemap.xml. Después
visita y analiza al menos:
- La home (/)
- La página /about/
- Una muestra de 3-5 magazines en /magazines/
- 5-8 páginas pilar de diferentes dimensiones (/temas/, /casos-uso/,
  /sectores/, /ciudades/)
- 2-3 hubs de mercado (/mercados/mexico/, /mercados/espana/, etc.)

ENTREGA un informe estructurado con estas 8 secciones, sé directo y
específico, cita URLs concretas:

1. PRIMERA IMPRESIÓN
   ¿Se entiende en 5 segundos qué es el medio y quién lo publica?
   ¿La relación medio↔Pulpo es clara y honesta?

2. VOZ Y CALIDAD EDITORIAL
   ¿Es periodismo o suena a marketing? Cita 3 fragmentos donde la voz
   funcione y 3 donde flojee. ¿Hay frases vacías, adverbios de relleno,
   estructuras "no es X, es Y", em-dashes en exceso?

3. CONTENIDO POR DIMENSIONES
   Para cada dimensión (/temas/, /casos-uso/, /sectores/, /ciudades/,
   /mercados/), ¿hay redundancia entre páginas? ¿Se siente cada una única
   o es contenido reciclado? ¿Cuáles brillan, cuáles flojean?

4. SEO TÉCNICO
   Schema.org, meta tags, hreflang, sitemap, robots.txt. ¿Qué falta?
   ¿Qué está mal? ¿Algo huele a doorway pages / contenido auto-generado
   penalizable por Google?

5. COBERTURA PULPO + PULPOPAY
   ¿Se posiciona Pulpo de forma elegante o invasiva? ¿PulpoPay aparece
   solo donde tiene sentido (fuel cards, control de gasto) o se cuela en
   sitios donde no encaja? ¿Hay sesgo comercial detectable que minaría
   credibilidad editorial?

6. GAPS Y OPORTUNIDADES
   ¿Qué temas IMPORTANTES para flotas MX/ES NO están cubiertos? Lista
   5-10 temas/keywords que deberían existir y no existen. ¿Qué tipos
   de página faltan (rankings, comparativas, reportes trimestrales,
   mapas de mercado)?

7. RIESGOS
   ¿Algo podría dañar la reputación del medio o de Pulpo? ¿Errores
   factuales evidentes? ¿Tono que pueda interpretarse como propaganda?
   ¿Algo que un competidor pudiera usar en contra?

8. RECOMENDACIONES PRIORIZADAS
   3 acciones de alto impacto que harías esta semana.
   3 acciones de medio plazo (1-3 meses).
   3 ideas para diferenciar el medio (rankings propios, datos propios,
   formato único).

9. CONOCIMIENTO PROFUNDO DE PULPO
   Investiga lo que sepas (o puedas encontrar) sobre Pulpo y sus productos
   más allá de lo que cuenta el sitio. Mantenimiento, pagos B2B, antifraude
   en combustible, control documental, telemetría integrada, casos de
   clientes públicos. ¿Hay capacidades de Pulpo / PulpoPay que NO están
   reflejadas en el medio y deberían (de forma editorial, no marketing)?
   ¿Hay cosas que SÍ menciona el medio pero NO son tan exactas como podrían?

10. PROPUESTA DE COPYS MEJORADOS
    Selecciona 5 fragmentos del sitio (intros, FAQs, slot Pulpo, descripciones
    de pillar pages) que suenen demasiado a IA o demasiado genéricos. Para
    cada uno:
    - Cita el original literal.
    - Reescríbelo con voz humana, sobria, profesional, sin clichés tipo "en
      el cambiante mundo de…", "la transformación digital…", "es fundamental
      entender…". Periodismo, no marketing.
    - Explica brevemente qué cambiaste y por qué.

Sé crítico. No me halagues. Si algo está mal o suena raro, dilo.
```

---

## Adaptaciones por LLM

### Perplexity
Usa **Pro Search** (o Deep Research si está disponible). Pega el prompt
tal cual. Perplexity siempre crawlea las URLs reales — es el más completo
para auditoría web.

### ChatGPT
Activa **Search the web** antes de pegar. Usa el mejor modelo disponible
(GPT-5 / o equivalente). Tiende a ser más editorial + brand.

### Gemini
Usa **Gemini 2.5 Pro** con grounding activado. Añade al final del prompt:

> *"Incluye también un análisis técnico SEO específico: estructura de URLs,
> jerarquía de headings, Core Web Vitals si los puedes inferir, y
> comparativa con cómo Google probablemente categorizará el sitio."*

Gemini es más detallista en SEO técnico (sesgo Google natural).

---

## Cómo procesar los outputs

1. Guardar cada output en su archivo:
   - `docs/audits/2026-05-XX-perplexity.md`
   - `docs/audits/2026-05-XX-chatgpt.md`
   - `docs/audits/2026-05-XX-gemini.md`
2. Comparar hallazgos entre los 3 (qué coinciden todos = señal fuerte).
3. Crear `docs/audits/2026-05-XX-summary.md` con las acciones consolidadas.
4. Abrir issues GitHub para cada acción priorizada.

## Cadencia recomendada

Lanzar este prompt **trimestralmente** (cada 3 meses) para detectar deriva
editorial y oportunidades nuevas. Cada auditoría debería tardar 10 min de
trabajo nuestro + lo que tarden las IAs.
