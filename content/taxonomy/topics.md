# Topics — ejes editoriales

13 matrices editoriales. Cada una puede convertirse en página pública si cumple los 5 criterios del README (evergreen, material suficiente, intro útil, aporte real, no thin content).

## Formato de entrada

```
## {slug}
- Nombre editorial: {nombre}
- Descripción breve: {una línea}
- Alcance: {qué entra, qué no}
- Relación con otros topics: {subset de, hermano de, etc.}
- Estado público: internal-only | candidato | público | pendiente
- URL pública (si existe): /temas/{slug}/
- Material actual: {ediciones y páginas donde aparece}
- Próxima revisión: YYYY-MM-DD
```

---

## combustible

- Nombre editorial: Combustible, consumo y eficiencia
- Descripción breve: Gestión, consumo, fraude y control del gasto energético (diésel, gasolina, GNC) en flota.
- Alcance: operación, eficiencia y control. **No incluye** tarjetas (van en `fuel-cards`) ni electrificación (va en `electrificacion-flotas`).
- Relación: matriz. Lee cruzado con `control-gasto`, `fuel-cards`, `fraude`.
- Estado público: candidato (Q3)
- Material actual: en todas las ediciones como señal transversal
- Próxima revisión: 2026-07-01

## fuel-cards

- Nombre editorial: Tarjetas de flota (fuel cards)
- Descripción breve: Tarjetas de combustible, red de aceptación, carga EV, peajes, mantenimiento y control de gasto desde el medio de pago.
- Alcance: WEX, Corpay, Edenred, DKV, Solred/Repsol, Ruta Card, Coast, PulpoPay, etc. Integraciones POS.
- Relación: hijo de `combustible` en operación, pero con identidad propia de producto.
- Estado público: candidato (prioritario en PR #6)
- Material actual: Nº 1 (WEX fuel+EV), Nº 2 (Corpay+Voltempo, Verifone Commander Fleet, Edenred Essentials, DKV)
- Próxima revisión: 2026-05-01

## telematica

- Nombre editorial: Telemática y flota conectada
- Descripción breve: Hardware + plataformas de datos para flota: GPS, ELD, FMS, scoring, reporting.
- Alcance: Samsara, Motive, Geotab, Webfleet, Fleetio, Verizon Connect, Powerfleet, Lytx (parte plataforma).
- Relación: matriz. Hermano de `video-telematica` y `mantenimiento`.
- Estado público: candidato (Q3)
- Material actual: Nº 1 (Samsara $1.59B), Nº 2 (Samsara vs Motive, Geotab Ace voz)
- Próxima revisión: 2026-06-01

## video-telematica

- Nombre editorial: Video telemática, dashcams y ADAS
- Descripción breve: Cámaras embarcadas con IA, detección de comportamiento, ADAS y scoring de conductor por vídeo.
- Alcance: Lytx, Samsara dashcam, Motive AI Dashcam, Netradyne, Nauto, Queclink, SmartDrive.
- Relación: hermano de `telematica` y `seguridad`.
- Estado público: candidato (Q3)
- Material actual: Nº 1 (Geotab GO Focus Pro), Nº 2 (ranking ABI Lytx #1)
- Próxima revisión: 2026-06-01

## mantenimiento

- Nombre editorial: Mantenimiento de flota
- Descripción breve: Preventivo, predictivo, talleres, integración OBD/FMS, reporting.
- Alcance: Fleetio, ServiceChannel, Openbay, Bosch Car Service, integraciones telemática + taller.
- Relación: matriz. Sub-tema público potencial: `mantenimiento-predictivo`.
- Estado público: candidato (Q3)
- Material actual: Nº 1 (Webfleet + Questar), Nº 2 (Fleetio 110k talleres)
- Próxima revisión: 2026-06-01

## mantenimiento-predictivo

- Nombre editorial: Mantenimiento predictivo
- Descripción breve: Predicción de fallas por datos de uso, sensores y telemetría. TCO y downtime.
- Alcance: módulos de Samsara, Motive, Webfleet+Questar, Geotab Ace, algoritmos de OEMs.
- Relación: subset de `mantenimiento`. Pensado como evergreen, no como topic hub.
- Estado público: candidato para evergreen/explicadores
- Material actual: Nº 1 (89% precisión Webfleet+Questar)
- Próxima revisión: 2026-07-01

## electrificacion-flotas

- Nombre editorial: Electrificación de flotas
- Descripción breve: Vehículos eléctricos comerciales, infraestructura de carga (MCS, CCS), TCO, hubs compartidos, corredores.
- Alcance: camión eléctrico, furgoneta EV, fabricantes (Scania, BYD, Volvo), charging (EV Realty, Voltempo, VEV), tarifas específicas.
- Relación: matriz. Cruza con `combustible` (mix ICE+EV) y `fuel-cards` (pago unificado).
- Estado público: candidato (prioritario, PR siguiente)
- Material actual: Nº 1 (EV Realty contexto), Nº 2 (San Bernardino 9 MW, Corpay+Voltempo, Scania MCS, VEV UK)
- Próxima revisión: 2026-05-01

## compliance

- Nombre editorial: Compliance y regulación (matriz)
- Descripción breve: Normativa, plazos, sanciones, documentación y herramientas de cumplimiento.
- Alcance: matriz con instancias por país. No es página en sí misma. Las páginas reales son:
  - `/temas/compliance-espana/` — creada
  - `/temas/compliance-mexico/` — Q3 (ahora cubierto por `/temas/regulacion-mexico/` hasta que convenga separar)
  - `/temas/compliance-usa/` — Q4
- Estado público: padre abstracto (no URL propia)
- Material actual: ediciones 1 y 2 con V-16, G2V2, ADAS, ZBE, FMCSA
- Próxima revisión: 2026-07-01

## routing

- Nombre editorial: Routing, dispatch y optimización de rutas
- Descripción breve: Software de planificación, despacho, cumplimiento de ventanas, last-mile orchestration.
- Alcance: OneRail, Bringg, Onfleet, Onro, integraciones con ERPs.
- Relación: cruza con `reparto-ultima-milla` (fleet-type).
- Estado público: candidato (Q4)
- Material actual: Nº 2 (FedEx + OneRail same-day)
- Próxima revisión: 2026-09-01

## seguridad

- Nombre editorial: Seguridad de flota
- Descripción breve: Siniestralidad, scoring de conductor, formación, seguro telemático, dashcams, ADAS.
- Alcance: todo lo que reduce riesgo operativo por comportamiento o tecnología.
- Relación: hermano de `video-telematica`. Cruza con `seguros-telematicos` (player category).
- Estado público: candidato (Q4)
- Material actual: Nº 1 (Flock+Admiral), Nº 2 (Lytx #1 ABI)
- Próxima revisión: 2026-09-01

## fraude

- Nombre editorial: Fraude y abuso
- Descripción breve: Fraude de combustible, uso indebido de tarjeta, manipulación de tacógrafo, abusos de gasto.
- Alcance: detección, auditoría, scoring y controles.
- Relación: subset de `combustible` y `control-gasto` en operación.
- Estado público: candidato para evergreen/explicadores
- Material actual: mención transversal en Nº 1 y Nº 2
- Próxima revisión: 2026-06-01

## control-gasto

- Nombre editorial: Control de gasto de flota
- Descripción breve: Vista financiera unificada de costes del vehículo: combustible, mantenimiento, peaje, seguro, amortización.
- Alcance: reporting por vehículo/conductor, cierre contable, análisis por ruta.
- Relación: matriz financiera. Cruza con `fuel-cards`, `combustible`, `mantenimiento`.
- Estado público: candidato (Q3)
- Material actual: Nº 1 y Nº 2 como ángulo transversal
- Próxima revisión: 2026-07-01

## operacion-flotas

- Nombre editorial: Operación de flotas
- Descripción breve: Día a día operativo: turnos, documentación, flota disponible, incidencias.
- Alcance: lectura "general manager" más que técnica o financiera.
- Relación: matriz blanda, evergreen. Cruza con casi todo.
- Estado público: candidato para evergreen/guias
- Material actual: transversal
- Próxima revisión: 2026-08-01

## checklists-guias (contenedor evergreen)

- No es topic propio, es contenedor de piezas evergreen. Ver `content/evergreen-plan.md`.
