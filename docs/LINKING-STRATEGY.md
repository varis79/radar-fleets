# Linking Strategy · The Fleet Radar

Documento estratégico de arquitectura de enlaces internos y entity coverage.
**Estado**: borrador para discusión, NO ejecutado. Pendiente de aprobación.

> Fecha: 2026-05-24
> Origen: feedback de usuario tras revisar Magazine Nº 8 — "Manzanillo y
> Cuautitlán Izcalli no tienen página, tags no enlazan, Volkswagen no
> tiene página, ciudades hub está roto".

---

## 1. Diagnóstico — qué está realmente pasando

### 1.1 Tags de magazine no son links

Los 6 cover-tags de cada magazine son `<span>`, no `<a>`. Total: **79 tags
no clickables** distribuidos:

| Magazine | tags `<a>` | tags `<span>` |
|---|---|---|
| Nº 1 (2026-04-14) | 0 | 16 |
| Nº 2 (2026-04-17) | 4 | 12 |
| Nº 4 (2026-04-20) | 5 | 11 |
| Nº 5 (2026-04-27) | 7 | 9 |
| Nº 6 (2026-05-04) | 5 | 11 |
| Nº 7 (2026-05-11) | 5 | 11 |
| Nº 8 (2026-05-18) | 7 | 9 |
| **TOTAL** | **33** | **79** |

Cada tag debería disparar enlace a su pillar/hub correspondiente.

### 1.2 Entidades mencionadas SIN página destino (Magazine Nº 8)

**Ciudades mencionadas (5+ veces en magazines):**

| Ciudad | Apariciones | Página existe |
|---|---|---|
| Cali (Colombia) | 22 | ✗ no |
| Madrid | 13 | ✓ sí (5 topics) |
| Chicago | 7 | ✗ no (USA fuera de scope?) |
| Manzanillo | 5 | ✗ **GAP CRÍTICO** |
| Cuautitlán Izcalli | 3 | ✗ **GAP CRÍTICO** |
| Cuautitlán | 3 | ✗ GAP |
| Monterrey | 2 | ✓ sí |
| Phoenix | 2 | ✗ no |
| Miami | 1 | ✗ no |

**Marcas/Empresas top mencionadas — TODAS sin página propia:**

| Marca | Apariciones | Categoría |
|---|---|---|
| Samsara | 48 | Telemática (competencia Pulpo) |
| Geotab | 22 | Telemática (competencia) |
| Motive | 14 | Telemática (competencia) |
| WEX | 13 | Fuel cards |
| Webfleet | 9 | Telemática (competencia) |
| Tesla | 9 | OEM |
| FedEx | 8 | Logístico |
| Mercedes | 8 | OEM |
| Lytx | 7 | Video telemática |
| Volkswagen | 6 | OEM |
| Reynasa | 6 | Distribuidor recambios (caso adquisición) |
| BYD | 5 | OEM eléctrico |
| Uber | 5 | Movilidad |
| Mutua Madrileña | 5 | Aseguradora (caso adquisición) |
| Keeper Cargo | 3 | Aseguradora carga |
| Edenred | 3 | Fuel cards |

**Corredores logísticos mencionados:**
- Cali-Baja (3x) — sin página
- California-Baja California (1x) — sin página

### 1.3 Entidades CON página pero sin auto-link

Verificado en Magazine Nº 8: **Madrid se menciona 13 veces SIN link**, a
pesar de que existen 7 pillars de ciudades-Madrid. Idem Monterrey (2x sin link).

Los scripts `linkify_topics.py`, `linkify_brands.py` e `linkify_institutions.py`
NO cubren:
- Ciudades
- Marcas grandes (Tesla, BYD, Volkswagen, Mercedes, etc.)
- Operadores logísticos (DHL, FedEx, UPS, Amazon)
- Corredores
- Aseguradoras
- Términos genéricos relevantes ("gestión de flotas", "control de gasto")

### 1.4 Linking density (ratio enlaces/100 palabras)

| Magazine | Ratio actual | Best practice B2B editorial |
|---|---|---|
| Nº 1 | **0.06** | 0.4-1.0 ⚠️ catastrófico |
| Nº 2-8 | 0.77-1.21 | aceptable bajo, mejorable a 1.5-2.0 |

Las páginas pillar tienen mejor ratio pero también con margen.

### 1.5 Hub `/ciudades/` roto (queja específica del usuario)

**Diagnóstico** (del agente UX):

1. **El intro MIENTE**: meta-description, og:description y H1 prometen
   "Madrid, Barcelona, CDMX, Guadalajara, **Buenos Aires, Bogotá, Santiago,
   Lima** y más". En realidad solo hay 5 ciudades MX+ES en disco
   (Madrid, Barcelona, CDMX, Guadalajara, Monterrey). LatAm = 0 páginas.

2. **"Mismas dos cajas duplicadas"**: en sección España, cada topic
   (electrificación, fuel cards, logística, mantenimiento, renting,
   telemática, ZBE) genera 2 cards prácticamente idénticas (Madrid +
   Barcelona). El usuario percibe redundancia, no riqueza.

3. **Cobertura desigual**: Bilbao 0, Valencia 0, Sevilla 0; mientras
   Madrid 7, Barcelona 7. Matriz "queso suizo" sin lógica visible.

4. **Sin agrupación por ciudad**: el hub agrupa por país (España/México),
   pero dentro cada ciudad aparece dispersa entre tarjetas de su topic.
   Visualmente parece más caótico de lo que es.

5. **Sin cross-linking** a otros hubs (temas, mercados, casos-uso).

### 1.6 Otros hubs con problemas estructurales

- **`/temas/`**: 12 páginas existentes NO listadas (fabricantes camiones,
  última milla eléctrica, transporte larga distancia, etc.)
- **`/casos-uso/`**: muestra duplicados pillar+guía sin distinción visual
- **`/sectores/`**: sin micro-descripciones
- **`/evergreen/`**: bug en BreadcrumbList (posiciones 2-3 repetidas)
- **`/mercados/`**: el ÚNICO bien diseñado — modelo a replicar

---

## 2. Best practice SEO B2B editorial — el marco

Antes de proponer, repaso la teoría aplicable:

### 2.1 Topic clusters + pillar pages
- Una pillar page central (long, comprehensive) por topic principal
- Cluster de páginas satélite (más específicas) enlazadas TODAS a la pillar
- La pillar enlaza a TODAS las satélite
- Cada satélite enlaza a sus pares relevantes

### 2.2 Entity-based SEO (post-2020)
Google indexa entidades (no solo keywords). Cada entidad mencionada
relevante debería tener:
- Un nodo en el knowledge graph del sitio (página dedicada o stub)
- Schema.org marcado correctamente
- Mentions desde múltiples páginas con anchor texts variados

### 2.3 Internal link velocity
Para que el "link juice" fluya:
- Cada página debería tener ≥3 inbound links internos (no orphan)
- Cada página debería tener ≥5 outbound links internos
- Anchor text variado (no siempre el mismo wording)

### 2.4 Stub strategy ("hub stubs")
Cuando se menciona una entidad recurrente sin contenido aún para una pillar:
- Stub page con noindex, follow
- Contenido: 100-300 palabras describiendo la entidad + lista de menciones en magazines
- Acumula link equity hasta justificar full page
- Cuando alcanza threshold → release a index, follow

### 2.5 Anchor diversification
La misma página NO debe linkearse siempre con el mismo anchor:
- "telemática" en una mención
- "plataformas de monitoreo" en otra
- "soluciones de tracking" en tercera
Google penaliza over-optimization.

### 2.6 Reciprocal & lateral linking
- Topic A pillar ↔ Topic B pillar (si relacionadas)
- Pillar ↔ casos de uso que la implementan
- Pillar ↔ ciudades donde aplica
- Pillar ↔ sectores donde se usa
- Mercado ↔ todas las pillars de ese mercado

### 2.7 Outbound (external) link strategy
Linkear FUERA a fuentes autoritativas también ayuda SEO:
- Organismos oficiales (gobierno) → ya tenemos `linkify_institutions.py`
- Estudios de mercado citables (no inventes, cita real)
- Wikipedia para entidades genéricas

### 2.8 Branded mentions strategy
Para empresas como Pulpo (publisher), best practice:
- Mencionar el brand de forma natural en contexto
- NO crear "Pulpo box" en cada página (saturación)
- Sí enlazar "gestión de flotas" genérica a la pillar correspondiente
  (no a getpulpo.com — eso sería self-promotion sospechosa)

---

## 3. Estrategia propuesta para Fleet Radar

### 3.1 Filosofía de páginas — qué crear, qué stub, qué no

**Crear página completa** (≥1.500 palabras, indexable):
- ✅ Cuando hay datos públicos suficientes (fabricantes, regulación, organismo)
- ✅ Cuando hay relevancia SEO clara (volumen de búsqueda, intención B2B)
- ✅ Cuando es asset propio editorial (pillar temática, hub mercado, ciudad clave)

**Crear stub** (200-400 palabras, `noindex, follow`):
- ✅ Cuando se menciona entidad ≥3 veces en magazines y no hay contenido full
- ✅ Cuando es ciudad/empresa/corredor relevante pero falta investigación
- ✅ Stub incluye: definición breve, lista de menciones en magazines + links

**NO crear página** (mantener mention sin destino):
- ❌ Empresas competencia directa de Pulpo (Samsara/Geotab/Motive/Webfleet)
  → razón: regalar SEO a competencia, riesgo de hablar mal/bien sin control
- ❌ Comparativas head-to-head con precios/specs (caducan en meses)
- ❌ Entidades muy efímeras (escándalo de la semana, mención puntual)

**Decisión sobre Samsara/Geotab/Motive/Webfleet/Lytx (telemáticas, competencia)**:

Hay 3 opciones:

**Opción A** — NO crear pages, mention solo (status quo):
- ✓ No regalamos SEO a competencia
- ✗ Perdemos 100+ menciones sin destino interno
- ✗ Lectores no saben "qué es Samsara" si llegan de magazine

**Opción B** — Crear pages PROPIAS de evaluación neutral:
- Title: "Samsara para flotas en México: criterios de evaluación 2026"
- Contenido: qué hace, dónde encaja, qué considerar antes de contratar,
  ALTERNATIVAS (incluyendo Pulpo cuando aplique)
- ✓ Capturamos SEO de búsqueda "samsara mexico flota"
- ✓ Lector recibe contenido editorial útil
- ✓ Pulpo aparece como alternativa contextualmente
- ⚠ Hablamos de competidor (con criterio editorial neutral)

**Opción C** — Solo páginas de CATEGORÍA agregada:
- "Plataformas de telemática para flotas en México 2026" (incluye Samsara,
  Geotab, Webfleet, Pulpo, etc. en formato listado neutral)
- ✓ Single page captura SEO comparativo
- ✓ No regalamos page individual a cada competidor
- ⚠ Menos profundidad por marca

**Recomendación**: **C** (categorías) + selectivamente **B** para Samsara y
Geotab (los 2 más mencionados, 70 menciones combinadas).

### 3.2 Páginas a crear — propuesta prioritizada

**Tier 1 — Crítico (24 nuevas pages)**:

Ciudades MX mencionadas pero sin página (stubs noindex):
1. `/ciudades/manzanillo-2026/` (puerto, hub logístico clave)
2. `/ciudades/cuautitlan-izcalli-2026/` (zona industrial CDMX-Toluca)
3. `/ciudades/lazaro-cardenas-2026/` (puerto Pacífico)
4. `/ciudades/veracruz-2026/` (puerto Golfo)
5. `/ciudades/nuevo-laredo-2026/` (cruce fronterizo T-MEC clave)
6. `/ciudades/altamira-2026/` (puerto)
7. `/ciudades/toluca-2026/` (industrial)
8. `/ciudades/puebla-2026/` (industrial-VW)

Ciudades LatAm core (stubs noindex + intro promete pero no tenemos):
9. `/ciudades/bogota-2026/`
10. `/ciudades/medellin-2026/`
11. `/ciudades/cali-2026/` (22 menciones!)
12. `/ciudades/santiago-2026/`
13. `/ciudades/buenos-aires-2026/`
14. `/ciudades/lima-2026/`

Ciudades ES sin cobertura (5 con 0 topics):
15. `/ciudades/valencia-2026/`
16. `/ciudades/sevilla-2026/`
17. `/ciudades/bilbao-2026/`
18. `/ciudades/zaragoza-2026/`
19. `/ciudades/malaga-2026/`

Corredores logísticos:
20. `/corredores/california-baja-california-2026/` (NUEVA dimensión)
21. `/corredores/nuevo-laredo-laredo-2026/`
22. `/corredores/bogota-buenaventura-2026/`

Categorías de marca (Opción C):
23. `/temas/plataformas-telematica-mexico-2026/` (listado neutral)
24. `/temas/plataformas-telematica-espana-2026/`

**Tier 2 — Importante (~12 nuevas)**:
- Páginas evaluación selectivas: `/players/samsara/`, `/players/geotab/`
- Fabricantes OEM individuales: Volkswagen, Tesla, BYD, Mercedes-Benz
  (panorama no comparativa)
- Operadores: DHL México, FedEx México, Amazon Logistics España
  (perfil neutral, sin cifras inventadas)

**Tier 3 — Nice to have**:
- Aseguradoras: Mutua Madrileña, AXA, MAPFRE (perfiles)
- Distribuidores recambios: Reynasa (caso adquisición → contexto)

### 3.3 Sistema de auto-linking expandido

**Scripts nuevos necesarios**:

1. `linkify_cities.py` — autoenlaza mentions de ciudades a sus pages/stubs
   - Detecta: Madrid, Barcelona, CDMX, Monterrey, Manzanillo, etc.
   - Primera mención por página
   - Skip si ya en `<a>` o en atributos
   - Por mercado: prefiere ciudad-mercado-actual

2. `linkify_companies.py` — autoenlaza marcas/empresas con pages
   - Solo las que TIENEN page (no crear forzar)
   - Variantes: "Mercedes-Benz" / "Mercedes" → misma URL
   - Skip si en lista negra competencia (decisión usuario)

3. `linkify_corridors.py` — corredores logísticos
   - "California-Baja", "Nuevo Laredo - Laredo", etc.

4. `linkify_generic_terms.py` — términos editoriales clave a pillars
   - "gestión de flotas" → `/temas/gestion-flota-{market}-2026/`
   - "control de gasto" → `/temas/control-gasto-flota-{market}-2026/`
   - "compliance vehicular" → `/temas/compliance-flotas-{market}-2026/`
   - Detección de mercado de la página actual

**Sistema unificado** (propuesta de arquitectura limpia):

En lugar de 7+ scripts separados, crear un `linkify_master.py` con un
diccionario unificado `ENTITY_DICTIONARY`:

```python
ENTITIES = {
    # Cities
    ("Madrid",): {"type": "city", "url": "/ciudades/madrid-2026/"},
    ("Manzanillo",): {"type": "city", "url": "/ciudades/manzanillo-2026/"},
    # Brands
    ("Samsara",): {"type": "brand", "url": "/players/samsara/"},
    # Topics
    ("gestión de flotas", "gestion de flotas"): {
        "type": "topic", "url_pattern": "/temas/gestion-flota-{market}-2026/"
    },
    # Institutions (ya cubiertas)
    ("SAT",): {"type": "inst", "url": "https://www.sat.gob.mx/", "external": True},
}
```

Beneficios:
- Single source of truth
- Resolución de conflictos centralizada
- Skip lists unificadas
- Métricas de coverage por entidad

### 3.4 Magazine cover-tags y story-tags

**Convertir TODOS los `<span class="cover-tag/story-tag">` en `<a>`** que apunten a:

| Tag value | Apunta a |
|---|---|
| `Seguridad`, `Cargo theft` | `/temas/cargo-theft-flotas-mexico-2026/` |
| `Ferrocarril` | nuevo `/temas/ferrocarril-flotas-mexico-2026/` o `/temas/intermodal-flotas-mexico-2026/` |
| `Componentes`, `Recambios` | `/temas/repuestos-componentes-flotas-mexico-2026/` (NUEVA) |
| `México` | `/mercados/mexico/` |
| `España` | `/mercados/espana/` |
| `Norteamérica` | `/temas/t-mec-autotransporte-mexico-2026/` |
| `EV`, `Electrificación` | `/temas/electrificacion-flotas-{market}-2026/` |
| `Regulación` | `/temas/regulacion-mexico/` |
| `Telemática` | `/temas/telematica-flotas-{market}-2026/` |

Modificar `inject_story_links.py` para que mapee tags → URLs automáticamente.

### 3.5 Reorganización de hubs

#### `/ciudades/` — reagrupar por ciudad, no por país

**Layout actual** (problema):
```
ESPAÑA                            MÉXICO
[Madrid · electrif]               [CDMX · electrif]
[Barcelona · electrif]            [Guadalajara · electrif]
[Madrid · fuel cards]             [Monterrey · electrif]
[Barcelona · fuel cards]          [CDMX · fuel cards]
...                               ...
```

**Layout propuesto**:
```
ESPAÑA
  Madrid (5 análisis)
    · electrificación  · fuel cards  · logística  · mantenimiento  · telemática  · ZBE
  Barcelona (7 análisis)
    · ...
  Bilbao  Valencia  Sevilla  ⤴ próximamente

MÉXICO
  CDMX (5 análisis)
    · cargo theft  · electrificación  · fuel cards  · mantenimiento  · telemática
  ...
  Manzanillo  Cuautitlán Izcalli  ⤴ próximamente

LATAM
  Bogotá  Medellín  Cali  Santiago  Buenos Aires  Lima  ⤴ próximamente
```

#### `/temas/` — sub-agrupar por categoría

5 sub-secciones dentro:
- **Compliance & Regulación**: DGT, SICT, T-MEC, NOM-012, Carta Porte,
  tacógrafo, ZBE, ITV, V-16, compliance MX/ES
- **Costes & Pagos**: control-gasto, fuel cards, renting, leasing, TCO
- **Operación**: gestión-flota, distribución, última milla, transporte
  larga distancia, mantenimiento, fabricantes
- **Tecnología**: telemática, video-telemática, ADAS, plataformas
- **Energía**: electrificación, V-16, CNE hidrocarburos, peaje europeo

#### `/casos-uso/` — diferenciar pillar vs guía con badge visual

- Pillar = análisis editorial del caso
- Guía = paso a paso operativo
- Badge color-coded en cada card

#### `/sectores/` — añadir micro-descripción por sector

Cada card debe decir, en una línea, qué incluye el sector.

#### `/evergreen/` — fix BreadcrumbList + añadir cards

### 3.6 Outbound linking strategy

**Mantener**: `linkify_institutions.py` (107 ext-links a SAT/DGT/etc.)

**Añadir**:
- Enlaces a estudios públicos cuando se citen (Statista, ANFAC reports,
  IDC LatAm, etc.)
- Enlaces a noticias originales cuando se mencionen casos (T21, Logística
  Profesional, El Economista, Expansión)

**NO añadir**:
- Enlaces a Pulpo en cada "gestión de flotas" (saturación, parece spam)
- Pulpo solo aparece en `pulpo-box` controlado

### 3.7 Anchor diversification

Para cada entidad, mantener un pool de anchors:

```python
ANCHORS = {
    "samsara": ["Samsara", "la plataforma Samsara", "Samsara (telemática)"],
    "madrid": ["Madrid", "la capital", "la comunidad de Madrid"],
    "gestion-flotas": ["gestión de flotas", "operación de flota", "fleet management"],
}
```

Linkify usa hash de la URL origen para elegir variante consistente
por página (mismo anchor en misma página, distinto entre páginas).

---

## 4. Plan de ejecución por fases

### FASE A — Infraestructura de linking (4-6 horas)

1. Crear `scripts/linkify_master.py` con `ENTITY_DICTIONARY` unificado
2. Reemplazar `linkify_topics`, `linkify_brands`, `linkify_institutions` por
   wrappers que llaman a master con su subset
3. Añadir cobertura ciudades, marcas, corredores, términos genéricos
4. Anchor diversification por hash de URL

### FASE B — Páginas Tier 1 (24 stubs/full ~6-10 horas)

1. 8 stubs ciudades MX (Manzanillo, Cuautitlán Izcalli, Veracruz...)
2. 6 stubs ciudades LatAm (Bogotá, Medellín, Cali, Santiago, BuenosAires, Lima)
3. 5 stubs ciudades ES (Valencia, Sevilla, Bilbao, Zaragoza, Málaga)
4. 3 stubs corredores (CalBaja, NuevoLaredo, BogotaBuenaventura)
5. 2 categorías plataformas-telematica MX/ES

### FASE C — Magazine tags clickables (2 horas)

1. Convertir 79 `<span class="cover-tag/story-tag">` en `<a>`
2. Extender `inject_story_links.py` con mapping tag→URL
3. Re-run en los 7 magazines

### FASE D — Reorganización hubs (4-6 horas)

1. Reescribir `/ciudades/index.html` con agrupación por ciudad
2. Corregir intro/meta (no prometer LatAm hasta tenerlo)
3. Sub-agrupar `/temas/index.html` por categoría
4. Añadir badges visuales en `/casos-uso/`
5. Mini-descripciones en `/sectores/`
6. Fix BreadcrumbList `/evergreen/`

### FASE E — Páginas Tier 2 (full pillars, 6-8 horas)

1. OEMs individuales (Volkswagen, Tesla, BYD, Mercedes-Benz panorama)
2. Operadores: DHL México, FedEx México, Amazon Logistics España
3. Categorías plataformas restantes

### FASE F — Decisión sobre Samsara/Geotab (1-2 horas, requiere user input)

Implementar Opción A/B/C según decisión del usuario.

---

## 5. Estimación de impacto

**Antes** (estado actual):
- Linking density magazine Nº8: 1.21 enlaces/100 palabras
- 9 entidades clave sin link en Nº8
- 24+ ciudades/corredores mencionados sin página destino
- 79 magazine tags no clickables
- /ciudades/ con UX engañoso

**Después** (post FASE A-D):
- Linking density esperada: 2.5-3.0 enlaces/100 palabras
- 100% entidades clave linkeadas (cuando hay destino)
- 24 nuevas pages indexables (más 22 stubs)
- 79 tags clickables
- /ciudades/ honesto, organizado por ciudad, escalable

**Riesgos**:
- Crear demasiados stubs noindex puede sumarles "thin content" perceived
- Over-linking podría parecer keyword stuffing
- Opción B en Samsara/Geotab puede levantar quejas de competencia

**Mitigaciones**:
- Stubs con ≥200 palabras + lista de menciones reales en magazines
- Cap de auto-linking: máx 1 enlace por entidad por página
- Tono neutral editorial en pages de competencia, fact-only

---

## 6. Métricas para validar éxito

A medir 30 días post-implementación:

| Métrica | Hoy | Target T+30 |
|---|---|---|
| Páginas indexadas en Google | A medir | +25% |
| Sessions orgánicas/mes | A medir | +40% |
| Avg time on page magazines | A medir | +20% (más interlinks → más exploración) |
| Bounce rate magazines | A medir | -15% |
| Páginas por sesión | A medir | de ~1.5 a ~2.5 |
| Keywords ranking top 50 | A medir | +100 |
| Internal link velocity (avg) | 0.06-1.21 | 2.0-3.0 |

---

## 7. Preguntas abiertas que requieren decisión

1. **Samsara/Geotab/Motive/Webfleet/Lytx**: ¿Opción A (no pages), B (pages
   evaluación), o C (solo categoría agregada)? Recomendado: **C + selectivamente B**

2. **Aseguradoras** (Mutua Madrileña, MAPFRE, AXA): ¿pages?
   Recomendado: solo si tienen relevancia editorial recurrente (Mutua sí
   tras adquisición Reynasa)

3. **Corredores logísticos**: ¿nueva dimensión `/corredores/`?
   Recomendado: **sí**, son entidades editorialmente valiosas (T-MEC,
   nearshoring, peaje europeo)

4. **Pulpo internal link strategy**: ¿"gestión de flotas" enlaza a pillar
   propio o a getpulpo.com?
   Recomendado: **pillar propio** (`/temas/gestion-flota-{market}/`).
   getpulpo.com solo en `pulpo-box` ya existente.

5. **Stubs noindex strategy**: ¿OK crear 22 stubs de golpe o gradual?
   Recomendado: **gradual** — empezar con los más mencionados (Manzanillo
   5x, Cuautitlán Izcalli 3x, Cali 22x, Bogotá+Medellín)

---

## 8. Próximo paso

**Usuario decide**:
- ¿Fases A-D en orden, o priorizar diferente?
- Decisión sobre preguntas abiertas (especialmente Samsara/Geotab)
- ¿Quieres ver Fase A funcionar en 2-3 entidades antes de extender?

Una vez aprobado este plan, se ejecuta y se actualiza `docs/SEO-GUIDE.md`
con la nueva arquitectura de linking.
