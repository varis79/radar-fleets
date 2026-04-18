# Propuesta — páginas temáticas y de players

Arquitectura acumulativa del sitio para SEO, navegación y captación. **No queremos páginas automáticas vacías por cada tag.** Solo creamos páginas indexables cuando:

1. El tema o player tiene valor evergreen (no es una noticia puntual).
2. Hay suficiente contenido en ediciones para enlazar.
3. Se puede escribir una introducción útil de 300–500 palabras sin relleno.
4. Aporta a navegación, autoridad y captación.

Cualquier página nueva debe incluir: intro editorial, selección curada de ediciones relacionadas, 3–5 datos/cifras de referencia, CTA suave a Pulpo, metadatos SEO propios.

---

## Estructura propuesta

```
/
├── /temas/                     ← Paraguas de páginas temáticas
│   ├── peajes-europa/
│   ├── electrificacion-flotas/
│   ├── telematica-flotas/
│   ├── compliance-espana/
│   ├── regulacion-mexico/
│   ├── tarjetas-combustible/
│   └── ia-operativa-flotas/
│
├── /players/                   ← Paraguas de páginas de players
│   ├── samsara/
│   ├── geotab/
│   ├── motive/
│   ├── fleetio/
│   ├── corpay/
│   ├── wex/
│   └── pulpo/                  ← casa
│
└── /magazines/...
```

URLs cortas, sin fechas, en español. Cleans URLs activadas en `vercel.json`.

---

## Qué CREAR AHORA (valor evergreen con material suficiente)

### Temas

#### 1. `temas/peajes-europa/`
Por qué ahora: dos eventos calientes (NL 1-jul, AT enero) + obligación coste externo 2026. El tema va a crecer todo el año y atrae búsqueda alta-intención ("peaje camión Holanda 2026", "coste CO₂ peaje Austria").
Material de apoyo: ediciones Nº 2 y siguientes (se esperan 8–10 en 2026).
Tono: explicativo, con tabla por país.
KPI a observar: CTR desde búsqueda genérica a CTA de Pulpo.

#### 2. `temas/electrificacion-flotas/`
Por qué ahora: MCS, hubs compartidos, LatAm 8% EV, corredores reales. Tema estructural para la década.
Material: hub San Bernardino, VEV UK, Scania MCS, Corpay+Voltempo, hubs MX cuando lleguen.
Tono: mezcla de roadmap y práctico (TCO, infraestructura).

#### 3. `temas/compliance-espana/`
Por qué ahora: 2026 es año clave (V-16, ADAS, tacógrafo, ZBE). Búsqueda fiscal y operativa fuerte.
Material: V-16 retirada, Orden TRM/282/2026, G2V2 ligeros, ZBE.
Tono: práctico, casi checklist, actualizable por BOE.

#### 4. `temas/regulacion-mexico/`
Por qué ahora: CNE, Programa 6.000 MDP, Olinia, restricciones SICT. Contenido que hoy no tiene equivalente en medios ES-LatAm de flota.
Material: CNE hidrocarburos, Programa, restricciones Semana Santa, iniciativa Olinia.
Tono: operativo, con referencias a DOF.

### Players

#### 5. `players/pulpo/`
La casa. Propósito: punto de aterrizaje para quien llega por SEO buscando "Pulpo software flotas". Extracto de `pulpo-facts.md` + testimonios + CTA fuerte a getpulpo.com. No es un landing comercial: es la página editorial de Pulpo dentro de Radar Fleet.

---

## Qué CREAR EN Q3 2026 (cuando haya masa crítica)

### Temas

#### 6. `temas/telematica-flotas/`
Esperar a tener 3–4 ediciones con historias cruzadas Samsara/Motive/Geotab/Lytx para escribir una intro con jerarquía real. Crear cuando ocurra el primer evento mayor post-IPO de Motive.

#### 7. `temas/tarjetas-combustible/`
Esperar 2–3 ediciones más que consoliden la narrativa "tarjeta absorbe redes". Crear cuando haya suficientes historias cruzadas WEX/Corpay/Edenred/DKV.

#### 8. `temas/ia-operativa-flotas/`
Esperar al "second wave" de voice agents (post Geotab Connect 2026 y anuncios de Motive post-IPO). Crear cuando haya 3–4 casos reales de uso contados.

### Players

Crear página por player cuando tenga 3+ apariciones sustanciales en ediciones y alguna perspectiva editorial propia (no solo ficha corporativa):

- `players/samsara/` — trigger: cuarto trimestre con noticia sustancial.
- `players/motive/` — trigger: IPO efectiva + primer earnings público.
- `players/geotab/` — trigger: post-Geotab Connect con cobertura de voice agent.
- `players/fleetio/` — trigger: segunda adquisición después de Auto Integrate.
- `players/corpay/` — trigger: segundo movimiento de ecosistema (EV, POS).

---

## Qué NO crear (al menos de momento)

- Páginas por tag genérico ("Pagos", "IA", "Regulación") — son ejes transversales, se cubren en las temáticas narrativas de arriba, no en taxonomía paralela.
- Páginas por país fuera del top-4 (MX, ES, USA, Europa). LatAm merece una página agregada, no una por país.
- Páginas por autor/editor — no aporta, dispersa.
- Páginas "Sobre Radar Fleet" — vive bien en `about` dentro del footer si se pide.
- Páginas de "newsletter subscribe" — RSS + archivo son suficientes. Si hace falta email, se integra más adelante con Buttondown o Beehiiv vía embed.

---

## Requisitos técnicos comunes para las páginas de `temas/` y `players/`

Cada página debe:

1. **Estructura:**
   - `<h1>` claro (máx 10 palabras).
   - Intro editorial de 300–500 palabras.
   - Sección "Ediciones que hablan de esto" con 3–N enlaces a permalinks de `/magazines/...`.
   - Sección "Cifras de referencia" (3–5 datos de `market-watch.md`).
   - CTA suave a Pulpo (tono editorial, no banner).

2. **Metadatos:**
   - `<title>` y `<meta description>` únicos y orientados a búsqueda.
   - OG tags propios.
   - `<link rel="canonical">` a la URL propia.
   - Entrada en `sitemap.xml`.

3. **CSS:**
   - Carga `/assets/radar.css`.
   - Puede declarar acento propio si conviene temática.

4. **Update cadence:**
   - Actualizarse cuando una edición nueva añada una historia relevante.
   - Revisión mínima trimestral.
   - Sección "Actualizado por última vez: YYYY-MM-DD" visible al pie.

---

## Propuesta de orden de implementación

Siguiente iteración (después de que la base editorial esté estable):

1. `temas/compliance-espana/` — hay material más fresco y claro para redactar hoy.
2. `temas/regulacion-mexico/` — combinación de ventaja editorial (poca competencia) y material denso.
3. `temas/peajes-europa/` — aprovecha el evento del 1-jul como pico de búsqueda.
4. `players/pulpo/` — la casa, cuando queramos mover leads por SEO directo.
5. `temas/electrificacion-flotas/` — una vez haya otra edición con material EV sustancial.

Cada una debería poder publicarse en una sesión de 45–60 minutos de edición + maquetado.
