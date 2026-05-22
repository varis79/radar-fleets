# Prompt maestro de auditoría externa · v2

Versión estratégica. Combina auditoría SEO/editorial con consultoría de
crecimiento, captación, conversión, monetización y diferenciación.

Para ChatGPT (con Search), Gemini Pro (con grounding) y Perplexity
(Pro Search). Pega el bloque tal cual.

---

## Prompt (copiar literal)

```
Actúa como consultor senior de medios editoriales B2B + crecimiento + SEO.
Tienes 15 años de experiencia construyendo publicaciones digitales para
startups SaaS (Stripe Press, Lenny's Newsletter, The Pragmatic Engineer,
The Generalist, The Information). Vas a auditar un medio recién lanzado
y proponer mejoras concretas con criterio comercial y editorial.

═══════════════════════════════════════════════════════════════════════
CONTEXTO COMERCIAL (importante, define el targeting)
═══════════════════════════════════════════════════════════════════════

El medio se llama **The Fleet Radar** (https://thefleetradar.com) y es
publicado por **Pulpo** (https://getpulpo.com), empresa de tecnología
de gestión de flotas comerciales.

Pulpo tiene DOS productos con geografía distinta:

1. **Pulpo (SaaS de gestión de flotas)**:
   - Opera en MÉXICO y ESPAÑA.
   - Próxima expansión: Colombia, Chile, Argentina, Perú (LatAm).
   - Va a lanzar versión en inglés para mercado USA / internacional en 2026.
   - Gestiona +200.000 vehículos. Fundada en 2018.
   - Módulos: gestión documental, mantenimiento, control de operadores,
     KPI de coste por vehículo, integración telemetría, control de
     conductores y turnos.

2. **PulpoPay (tarjetas de combustible B2B + control de gasto)**:
   - Opera SOLO en MÉXICO por ahora.
   - NO sugerir que está disponible en otros mercados.
   - Cobertura amplia en gasolineras MX, antifraude avanzado, límites por
     vehículo/horario/zona, captura de evidencias fotográficas, validación
     por ubicación, separación clara de gasto personal/profesional.
   - Producto core: tarjeta para flotas que reemplaza tarjeta de crédito
     genérica + dashboard de control.

CLIENTES PULPO públicos por mercado (relevantes para tono editorial):
- 🇲🇽 MX: Banorte, Sherwin Williams, Seguros Atlas, Tip, APYMSA, DHL
  Express, DHL LMD, 99 Minutos, Envialo, Zoom, Segmail, Lyncott, Grupo
  SAR, Carnes Selectas El Ingrato, La Rancherita, Arabela, Byal Logistics,
  Dliver, Bonnysa, Hielo Fiesta, Lácteos La Quinta, Hycsa, Epiroc, Tracsa,
  Grupo SDG, Energéticos Fusión, BHP, Traffic Light, Vorsevi, Rentokil,
  Enerclima, Green Protection, Grupo Vysisa, Element Fleet, AZ Leasing,
  Franlux, STN, Sherwin Williams, Ravago, Farmacias Similares, Transportes
  Monroy Schiavon, Transportes STN, AGR Transportes, El Shaddai (taxis AIFA).
- 🇪🇸 ES: Chubb, Isdin, Laboratorios Salvat, Calidad Pascual, Iberdrola,
  Avatel, Tradivel, OHLA, Magtel, Mondial Relay, CityLogin, Bofrost,
  Transgourmet, Rentokil, Serveo, Securitas, Fain, Orona, Grupo Nabeiro,
  Grupo Unide.

COMPETIDORES PULPO (no usar como inspiración ni mencionar como ejemplo):
Mendel, Uvicuo, Pluxee, Minu, Edenred, Repsol Solred, Ticket Car,
GoPass, Efecticard, Efectivale, Gosmo.

═══════════════════════════════════════════════════════════════════════
CONTEXTO EDITORIAL DEL MEDIO
═══════════════════════════════════════════════════════════════════════

- Publicación semanal · cada lunes 07:00 hora Madrid.
- 10 ediciones publicadas + 139 páginas pilar SEO en 4 dimensiones:
  /temas/, /casos-uso/, /sectores/, /ciudades/.
- Página /about/ explica el medio y la relación con Pulpo.
- /styleguide.html documenta el sistema de marca y voz.
- Voz: periodismo sobrio, datos antes que adjetivos, sin hype.
- Cobertura: foco MX + ES; secundaria LatAm; selectiva USA + Europa.

═══════════════════════════════════════════════════════════════════════
ACCIÓN
═══════════════════════════════════════════════════════════════════════

1. Lee el sitemap https://thefleetradar.com/sitemap.xml y entiende la
   arquitectura.
2. Visita y analiza:
   - Home (/)
   - /about/
   - /styleguide.html
   - 3-5 magazines en /magazines/
   - 8-10 páginas pilar de diferentes dimensiones
   - 3 hubs de mercado (/mercados/mexico/, /mercados/espana/, otro)
3. Visita brevemente https://getpulpo.com para captar la voz comercial
   de la empresa matriz.
4. Aplica TODO lo que sepas (de tu conocimiento general + búsqueda web)
   sobre Pulpo, PulpoPay, el sector de fleet management en MX/ES/LatAm,
   y publicaciones editoriales B2B exitosas.

═══════════════════════════════════════════════════════════════════════
ENTREGA EL INFORME (14 secciones, sé directo y específico)
═══════════════════════════════════════════════════════════════════════

1. PRIMERA IMPRESIÓN
   ¿Se entiende en 5 segundos qué es el medio y quién lo publica?
   ¿La relación medio↔Pulpo es clara y honesta o se nota forzada?

2. VOZ Y CALIDAD EDITORIAL
   ¿Es periodismo o suena a marketing? Cita 3 fragmentos donde funcione
   y 3 donde flojee. Detecta: frases hechas de IA, adverbios vacíos,
   "no es X, es Y", em-dashes en prosa, hype.

3. CONTENIDO POR DIMENSIONES
   /temas/, /casos-uso/, /sectores/, /ciudades/, /mercados/. ¿Hay
   redundancia? ¿Cada página se siente única o reciclada? ¿Cuáles
   brillan, cuáles flojean? Cita URLs concretas.

4. SEO TÉCNICO + LLM CITABILITY
   Schema.org, meta tags, sitemap, robots.txt, hreflang, Open Graph.
   ¿Qué falta para que ChatGPT Search / Perplexity / Gemini citen el
   medio como fuente? ¿Algo huele a doorway pages o auto-generated?

5. COBERTURA PULPO + PULPOPAY (con matices de geo)
   Recuerda: Pulpo opera MX + ES; PulpoPay solo MX. ¿El medio respeta
   esta segmentación o sugiere implícitamente que PulpoPay está en ES?
   ¿Pulpo aparece de forma elegante o invasiva? ¿Sesgo comercial
   detectable que mine credibilidad editorial?

6. CAPTACIÓN POR MERCADO
   ¿Cómo está captando lectores este medio en cada mercado clave?
   - MX (Pulpo + PulpoPay): ¿el contenido conecta con gerentes de flota
     mexicanos? ¿Cubre los dolores reales?
   - ES (solo Pulpo): ¿el contenido es relevante para flotas españolas
     o sufre de sesgo MX?
   - LatAm secundario (CO, CL, AR, PE): ¿hay cobertura suficiente o
     superficial? ¿Cómo entrar mejor en esos mercados editorialmente?
   - Versión EN futura para USA: ¿qué deberíamos hacer YA para
     prepararla? ¿Estructura, hreflang, contenido seed?

7. CONTENIDO RECURRENTE PARA HOME / EDICIÓN SEMANAL
   ¿Qué bloques recurrentes deberíamos incluir cada semana para subir
   engagement, recurrencia y diferenciación? Evalúa estas ideas y
   propón otras:
   - Caja "Sabías qué" con dato histórico curioso de flotas/transporte.
   - Caja "Pulpo destaca" con una feature distinta cada semana (rotación).
   - Banner de partner pagado (monetización futura) que quede como link
     permanente en esa edición.
   - Sección "Carta abierta" o "Tribuna": cliente o experto del sector
     escribe 1 artículo, featurizado en alguna edición.
   - "Movimientos": contrataciones senior, rondas, M&A en el sector.
   - "Cifra de la semana": un dato con contexto.
   - Newsletter por email con resumen de la edición + 1 dato exclusivo.

8. CONVERSIÓN EDITORIAL → COMERCIAL (Pulpo + PulpoPay)
   El medio NO es canal de venta directo. Pero genera tráfico cualificado.
   ¿Cómo está convirtiendo ese tráfico hoy? ¿CTAs ubicados con criterio?
   ¿Pulpo box discreto pero efectivo? ¿Qué embudo deberíamos diseñar
   desde una página pilar pillar hasta un demo de Pulpo / alta PulpoPay?
   Propón 3 mejoras concretas que NO comprometan credibilidad editorial.

9. MONETIZACIÓN FUTURA (sin canibalizar lo editorial)
   ¿Qué formatos de monetización son razonables para un medio así?
   - Sponsored content (artículo etiquetado como tal).
   - Partner banner con link permanente en ediciones.
   - Reportes trimestrales pagados ("Fleet Fuel Index MX 2026").
   - Job board del sector.
   - Eventos / webinars patrocinados.
   - Lead magnets (checklists descargables con email gate).
   ¿Cuál implementar primero? ¿Cuál NUNCA?

10. DIFERENCIACIÓN vs MEDIOS DEL SECTOR
    ¿Qué medios cubren hoy gestión de flotas en MX/ES/LatAm? Lista 5-8.
    ¿Qué hacen ELLOS bien que The Fleet Radar no? ¿Qué hace The Fleet
    Radar bien que ellos no? ¿Qué ángulo único deberíamos doblar
    (rankings, mapas de mercado, datos propios, formato, idioma)?

11. CONOCIMIENTO PROFUNDO DE PULPO + PULPOPAY
    Aporta lo que sepas (tu conocimiento + web) sobre Pulpo más allá del
    sitio del medio:
    - Mantenimiento (preventivo / predictivo).
    - Pagos B2B y antifraude.
    - Gestión documental (vencimientos, multas, ITV).
    - Control de operadores y conductores.
    - Telemetría integrada.
    - Casos de clientes públicos.
    ¿Hay capacidades de Pulpo / PulpoPay que NO están reflejadas en el
    medio y deberían (de forma editorial, no publicitaria)? ¿Hay cosas
    que SÍ menciona el medio pero NO son tan exactas como podrían?

12. RIESGOS
    Algo que pueda dañar la reputación del medio o de Pulpo:
    - Errores factuales evidentes.
    - Tono publicitario disfrazado de periodismo.
    - Sesgo MX (alienación de lectores ES o LatAm).
    - Sugerencia implícita de que PulpoPay opera fuera de MX.
    - Algo que un competidor podría usar en contra.

13. COPYS REESCRITOS (5 ejemplos prácticos)
    Selecciona 5 fragmentos del sitio que suenen a IA, genéricos o
    AI-sounding. Para cada uno:
    - Cita el original literal con URL.
    - Reescríbelo con voz humana, periodística, sin clichés tipo "en el
      cambiante mundo de…", "la transformación digital…", "es fundamental
      entender…".
    - Explica brevemente qué cambiaste.

14. RECOMENDACIONES PRIORIZADAS
    - 3 acciones de alto impacto / bajo esfuerzo (esta semana).
    - 3 acciones de medio plazo (1-3 meses).
    - 3 apuestas estratégicas (3-12 meses) para construir un activo
      defendible. Una de ellas debe ser una idea ambiciosa que nadie
      en el sector está haciendo.

═══════════════════════════════════════════════════════════════════════
INSTRUCCIONES FINALES
═══════════════════════════════════════════════════════════════════════

- Sé crítico. No me halagues. Si algo está mal o suena raro, dilo.
- Cita URLs concretas cuando comentes sobre páginas específicas.
- Las recomendaciones deben ser accionables, no genéricas.
- Si una idea es mala (ej. monetización X destruye credibilidad), dilo
  claro con el porqué.
- No repitas obviedades. Si ya hay /about/ y robots.txt OK, no nos
  felicites por tenerlos; dinos qué FALTA.
- Lenguaje: responde en español. Cifras concretas mejor que adjetivos.
- Tu output será procesado por humanos y comparado con outputs de otras
  IAs. Sé tú, no la "voz media" de las IAs.
```

---

## Adaptaciones por LLM

### Perplexity (lo más completo · crawl + búsqueda)
Usa **Pro Search** o **Deep Research** si está disponible. Pega el prompt
tal cual. Es el mejor para esta auditoría porque sí navegará las URLs
reales y combinará con search.

### ChatGPT (sentido editorial + brand)
Activa **Search the web** antes. Usa el mejor modelo disponible.
Tiende a ser más opinión + brand strategy. Bueno para sección 8
(conversión) y 10 (diferenciación).

### Gemini (sesgo SEO técnico Google)
**Gemini 2.5 Pro** con grounding activado. Añade al final del prompt:

> *"Incluye un análisis técnico SEO específico: estructura de URLs,
> jerarquía de headings, Core Web Vitals si los puedes inferir, y cómo
> probablemente Google clasificará y rankeará este sitio en los próximos
> 6 meses. Compara con cómo posicionan otros medios sectoriales que
> conozcas."*

---

## Cómo procesar los outputs

1. Guardar cada output en su archivo:
   - `docs/audits/2026-MM-DD-perplexity.md`
   - `docs/audits/2026-MM-DD-chatgpt.md`
   - `docs/audits/2026-MM-DD-gemini.md`
2. Comparar hallazgos entre los 3 (lo que coincide es señal fuerte).
3. Crear `docs/audits/2026-MM-DD-summary.md` con acciones consolidadas
   priorizadas + responsables + estimación de esfuerzo.
4. Abrir Issues GitHub para cada acción priorizada con label `audit`.

## Cadencia recomendada

Lanzar este prompt **cada trimestre** para detectar deriva editorial y
oportunidades nuevas. Cada auditoría toma 10 min nuestros + lo que tarden
las IAs.

## Diferencias clave vs v1

| v1 (técnico SEO) | v2 (estratégico crecimiento) |
|---|---|
| 8 secciones | 14 secciones |
| Auditoría reactiva | Consultoría propositiva |
| Solo voz + estructura | + captación + conversión + monetización |
| Pulpo en general | Pulpo MX+ES vs PulpoPay solo MX (matiz crítico) |
| No incluye competencia editorial | Sección dedicada diferenciación |
| No habla de monetización | Roadmap monetización |
| No pide propuestas de contenido recurrente | Bloques semanales + tribuna invitados + banners |
