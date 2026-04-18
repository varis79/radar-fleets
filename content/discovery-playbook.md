# Discovery playbook — descubrimiento de actores nuevos

El ecosistema cambia cada semana. Aparecen productos, partnerships, adquisiciones, entran jugadores locales y vuelven a reposicionarse jugadores maduros. El sistema editorial debe detectar todo esto, clasificarlo y decidir si merece seguimiento, sin producir páginas públicas a ciegas.

Este playbook define cómo.

## Cuándo se ejecuta

Cada lunes, **al cerrar la edición**, no antes. Se ejecuta sobre las historias y señales ya seleccionadas para publicación. También puede ejecutarse fuera de edición cuando se ve un anuncio relevante entre semana.

## Qué vigilar

El descubrimiento mira especialmente estos focos:

- Renting y leasing (nuevos actores locales, fusiones, nuevos productos)
- Peajes (nuevos sistemas, operadores de peaje electrónico)
- Telemática y video telemática (hardware, SaaS, locales LatAm)
- Combustible y fuel cards (entrantes PYME, verticales especializadas)
- Mantenimiento y talleres (marketplaces, software)
- Software de flotas (competencia directa de Pulpo)
- Electrificación y charging (HDV, hubs compartidos, OEM)
- Fabricantes de vehículos comerciales (OEM con producto nuevo para flota)
- Dashcams, ADAS y video telemática (hardware y SaaS)
- Compliance y tooling operativo (tacógrafo, ELD, documentación)

Fuera de estos ejes, se aplica criterio editorial.

## Paso a paso

### 1. Lista de empresas mencionadas

Al cerrar la edición, listar todas las empresas, productos, organismos y plataformas mencionados en las 10 historias, las señales del mercado, las tendencias y las secciones regionales.

### 2. Cruce contra `players.md`

Para cada entidad:

- **Si ya existe** en `players.md`:
  - Actualizar `ultima-aparicion` con la fecha de la edición actual.
  - Incrementar `menciones-sustanciales` si la mención es editorialmente relevante (no es solo un nombre citado al pasar).
  - Añadir una línea corta al campo `historico` con `Nº N · YYYY-MM-DD · {qué hizo}`.
  - No duplicar la ficha.

- **Si no existe**:
  - Crear ficha mínima con el formato de `players.md`.
  - Clasificar en una categoría (software, pagos, renting, mantenimiento, charging, last mile, fabricante, compliance, dashcam, seguro).
  - Rellenar `geografia-primaria` con la mejor señal actual (si una empresa es global pero la noticia es en MX, se deja `global` y se anota MX como geografía activa).
  - Marcar `estado-pagina-publica: no-candidato` por defecto.

### 3. Clasificación

- **Actor con ficha nueva**: no genera nada más. Queda en memoria.
- **Actor que alcanza 3+ menciones sustanciales**: se marca `estado-pagina-publica: candidato` y se anota en `content/pages-proposal.md` para revisión editorial.
- **Actor que deja de aparecer 6+ meses**: se marca `estado-pagina-publica: inactivo`. No se borra.

### 4. Evaluación editorial

Antes de promover un `candidato` a página pública, responder a estas cuatro preguntas:

1. ¿Hay un ángulo editorial propio redactable? (No basta con "describir la empresa". Tiene que haber una lectura).
2. ¿Hay material cruzado (2+ ediciones de The Fleet Radar + fuentes externas fiables)?
3. ¿Hay hueco en búsqueda en español, o la SERP ya está saturada por el propio player?
4. ¿Aporta a captación de Pulpo sin convertirse en un favor gratuito al player?

Si las 4 responden sí, se crea página pública. Si no, se espera.

### 5. Caso especial: OEM y fabricantes

Los fabricantes de vehículo (Ford, Mercedes, Iveco, BYD…) tienen ficha propia en `players.md` pero **rara vez tienen página propia**. Su contenido útil vive en:

- Páginas de fleet-type (ligero comercial, pesado).
- Páginas evergreen específicas (comparativas de furgonetas, transición a EV).
- Secciones regionales (si un OEM tiene posición fuerte en un mercado).

### 6. Caso especial: organismos reguladores

Organismos (DGT, FMCSA, SICT, CNE, BOE, DOF) no se tratan como players. Van en `micro-tags.md` bajo `organismo:`. Pueden dar título a páginas evergreen ("Guía: cómo leer un BOE para flotas"), pero nunca tienen ficha.

## Formato de registro semanal

Al final de cada edición, se añade este bloque a `editorial-memory.md`, debajo de las etiquetas habituales:

```
### Discovery pass · Nº N · YYYY-MM-DD
Nuevos: {lista de slugs añadidos a players.md}
Actualizados: {lista de slugs con ficha refrescada}
Candidatos a página pública (nuevo): {lista}
Promovidos a página pública: {lista o "ninguno"}
```

## Reglas duras

- **Nunca** crear página pública automáticamente, ni siquiera tras alcanzar umbrales. La promoción requiere revisión humana.
- **Nunca** borrar una ficha. Máximo marcarla `inactivo`.
- **Nunca** duplicar. Si aparece "Corpay" y "FleetCor" en distintas semanas, se unifica bajo `corpay` con nota explicativa.
- **Nunca** fichar a un cliente de Pulpo como "player" sin validarlo. Los clientes van en `pulpo-facts.md` con permiso explícito.
