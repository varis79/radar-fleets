# Micro-tags — vocabulario controlado

Capa granular interna. Sirve para clustering editorial, memoria semántica, long-tail SEO y retrieval por IA.

**Regla dura:** los micro-tags **nunca** generan página pública. Cero excepciones. Su función es clasificar, no publicar.

## Familias (prefijos obligatorios)

El prefijo es parte del tag. Siempre en minúsculas, kebab-case.

### `dispositivo:` — hardware concreto

- `dispositivo:geotab-go9`
- `dispositivo:samsara-vg55`
- `dispositivo:samsara-ai-dashcam`
- `dispositivo:motive-ai-dashcam`
- `dispositivo:lytx-dv6`
- `dispositivo:queclink-gb120`
- `dispositivo:webfleet-link-740`
- `dispositivo:bosch-fleetboard`

### `regulacion:` — reglas y órdenes concretas

- `regulacion:v16-conectada`
- `regulacion:orden-trm-282-2026`
- `regulacion:tacografo-g2v2`
- `regulacion:cne-hidrocarburos`
- `regulacion:fmcsa-eld`
- `regulacion:eurovignette-fin`
- `regulacion:per-km-holanda-2026`
- `regulacion:austria-co2-ruido-2026`
- `regulacion:programa-atencion-inmediata-mx`
- `regulacion:iniciativa-olinia-mx`

### `norma:` — normas técnicas

- `norma:mcs`
- `norma:ccs`
- `norma:iso-39001`
- `norma:euro-vi`
- `norma:euro-vii`
- `norma:aetr`

### `sigla:` — siglas y acrónimos

- `sigla:ELD`
- `sigla:FMCSA`
- `sigla:DOF`
- `sigla:BOE`
- `sigla:CNE`
- `sigla:SICT`
- `sigla:DGT`
- `sigla:ZBE`
- `sigla:ADAS`
- `sigla:MCS`
- `sigla:CCS`
- `sigla:AETR`
- `sigla:OBD2`
- `sigla:FMS`
- `sigla:EV`
- `sigla:HDV`
- `sigla:LCV`
- `sigla:LEZ`

### `organismo:` — organismos reguladores y de prensa oficial

- `organismo:dgt`
- `organismo:fmcsa`
- `organismo:sict`
- `organismo:cne-mexico`
- `organismo:sct-mexico`
- `organismo:boe`
- `organismo:dof`
- `organismo:abi-research`
- `organismo:g2`

### `peaje:` — tipos de peaje

- `peaje:per-km`
- `peaje:eurovignette`
- `peaje:co2`
- `peaje:ruido`
- `peaje:ejes`
- `peaje:LEZ`
- `peaje:AP-espana`

### `tecnologia:` — tech concreta

- `tecnologia:ia-generativa`
- `tecnologia:voice-agent`
- `tecnologia:mcs-charging`
- `tecnologia:video-ia`
- `tecnologia:obd2`
- `tecnologia:fms-bus`
- `tecnologia:v2g`
- `tecnologia:telemetria-satelital`
- `tecnologia:5g-c-v2x`

### `producto:` — productos y features concretos

- `producto:geotab-ace`
- `producto:geotab-ace-voice`
- `producto:pulpopay`
- `producto:select-fleet-card`
- `producto:motive-card`
- `producto:wex-fuel-ev-card`
- `producto:samsara-voice-agent`
- `producto:edenred-essentials`
- `producto:webfleet-plus-questar`

### `integracion:` — integraciones declaradas entre players

- `integracion:fleetio-motive`
- `integracion:corpay-voltempo`
- `integracion:ncr-corpay`
- `integracion:verifone-wex`
- `integracion:webfleet-questar`

### `categoria-op:` — categorías operativas

- `categoria-op:last-mile`
- `categoria-op:long-haul`
- `categoria-op:distribucion`
- `categoria-op:reparto-urbano`
- `categoria-op:servicio-campo`
- `categoria-op:construccion-obra`
- `categoria-op:mineria-obra`

### `fabricante:` — fabricantes de vehículo

- `fabricante:ford`
- `fabricante:mercedes-benz`
- `fabricante:vw`
- `fabricante:renault`
- `fabricante:peugeot`
- `fabricante:citroen`
- `fabricante:iveco`
- `fabricante:scania`
- `fabricante:volvo`
- `fabricante:daf`
- `fabricante:man`
- `fabricante:byd`
- `fabricante:foton`
- `fabricante:hino`
- `fabricante:isuzu`
- `fabricante:toyota`

### `modelo-vehiculo:` — modelos concretos

- `modelo-vehiculo:ford-transit`
- `modelo-vehiculo:ford-f150`
- `modelo-vehiculo:mercedes-sprinter`
- `modelo-vehiculo:mercedes-vito`
- `modelo-vehiculo:renault-master`
- `modelo-vehiculo:renault-trafic`
- `modelo-vehiculo:iveco-daily`
- `modelo-vehiculo:vw-crafter`
- `modelo-vehiculo:toyota-hiace`
- `modelo-vehiculo:toyota-hilux`
- `modelo-vehiculo:nissan-frontier`
- `modelo-vehiculo:scania-r`
- `modelo-vehiculo:volvo-vnl`
- `modelo-vehiculo:iveco-sway`

### `evento:` — eventos del sector

- `evento:geotab-connect-2026`
- `evento:nafa-expo-2026`
- `evento:fleet-latam-conference`
- `evento:iaa-transportation-2026`

---

## Cómo se usan

- Cada historia de la edición lleva 3-8 micro-tags en su ficha interna (no se muestran al lector).
- Se guardan en el summary de la edición en una sección dedicada (`MICROTAGS: regulacion:v16-conectada, organismo:dgt, sigla:V16, peaje:per-km, ...`).
- La memoria editorial (`editorial-memory.md`) agrega los micro-tags usados en cada bloque de edición.
- Se pueden usar para:
  - detectar repetición entre ediciones sin contexto nuevo,
  - agrupar contenido afín para evergreen,
  - alimentar retrieval de AI search (cuando se monte),
  - construir disambiguation en long tail.

## Evolución

- El vocabulario crece. Cada edición puede añadir tags nuevos a la familia correspondiente.
- Si un tag se usa 5+ veces en ediciones distintas, se marca en memoria como candidato a entidad con ficha propia (subir a `players.md` si es actor, a `topics.md` si es tema).
- Ningún tag se mueve a capa pública sin revisión humana.
