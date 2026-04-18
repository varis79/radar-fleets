# Fleet types, verticals y use cases

Capa nueva. Existe para que el sistema entienda que **"flota" no es sinónimo de camión pesado**. Clasifica las historias, memoria y material por tipo de operación y tipo de vehículo.

Sirve para:

- clasificar noticias y señales,
- enriquecer la memoria editorial,
- detectar oportunidades de contenido evergreen por segmento,
- mejorar utilidad para distintos lectores (director de ops de ambulancias lee otra cosa que director de ops de tractocamiones),
- evitar el sesgo hacia transporte pesado.

## Formato de entrada

```
### {slug}
- Nombre editorial: {nombre}
- Cluster: {cluster}
- Vehículos típicos: {lista}
- Operadores típicos: {lista}
- Regulaciones con más peso: {lista}
- Players más relevantes: {lista}
- Criterio público: ¿puede ser página?
```

## Clusters

Agrupación alta para que el sistema pueda razonar por bloques:

| Cluster | Qué agrupa |
|---|---|
| `long-haul` | Transporte pesado, tractocamiones, operación interurbana de larga distancia |
| `distribucion` | Reparto intermedio, logística FMCG, refrigerado |
| `ligero-comercial` | Furgonetas, pickups, ligeros de reparto o servicio |
| `last-mile` | Reparto urbano, paquetería, e-commerce |
| `field-service` | Servicio técnico móvil, mantenimiento in-situ |
| `especializado` | Emergencias, construcción, minería, cementeras, residuos |
| `pasajeros` | Transporte escolar, ride-hailing, autoescuela |
| `no-motorizado` | Remolques, semirremolques, activos rastreables no motorizados |
| `mixto-corporativo` | Flotas corporativas con mix de vehículos, alquiler sin conductor, renting empresarial |

---

## Long-haul

### transporte-pesado

- Nombre editorial: Transporte pesado
- Cluster: long-haul
- Vehículos típicos: camión rígido, tractocamión, semirremolque
- Operadores típicos: transportistas de carga, logística industrial, exportadores
- Regulaciones con más peso: tacógrafo, peajes HDV, horas de conducción, ELD (USA), AETR (EU)
- Players más relevantes: Samsara, Motive, Geotab, Fleetio, WEX, Corpay, DKV
- Criterio público: evergreen posible (Q4)

### tractocamiones

- Nombre editorial: Tractocamiones
- Cluster: long-haul
- Vehículos típicos: Freightliner, Volvo VNL, Scania R, Kenworth, Iveco S-Way
- Operadores típicos: logística de línea, intermodal, puerto-tierra
- Regulaciones con más peso: ELD, tacógrafo G2V2, MCS (si eléctrico), peaje-por-km
- Players más relevantes: Scania, Volvo Trucks, DAF, MAN, Samsara, Motive
- Criterio público: no por ahora (subset de transporte-pesado)

---

## Distribución

### distribucion

- Nombre editorial: Distribución intermedia
- Cluster: distribucion
- Vehículos típicos: camión ligero-medio, furgón grande
- Operadores típicos: mayoristas, cadenas minoristas, food service
- Regulaciones con más peso: ZBE, ADAS, tacógrafo ligero
- Players más relevantes: Arval, Alphabet, Webfleet, Geotab
- Criterio público: Q4 si acumula material

### logistica-bebidas-fmcg

- Nombre editorial: Logística de bebidas y FMCG
- Cluster: distribucion
- Vehículos típicos: camión de reparto, furgón refrigerado, tractocamión de bebidas
- Operadores típicos: PepsiCo, Coca-Cola, AB InBev, Nestlé, food service
- Regulaciones con más peso: ZBE urbana, temperatura controlada, HACCP
- Players más relevantes: Samsara (PepsiCo LatAm caso), Webfleet, Geotab
- Criterio público: no por ahora

### frio-refrigerado

- Nombre editorial: Transporte refrigerado (reefer)
- Cluster: distribucion
- Vehículos típicos: semirremolque frigorífico, camión con grupo frío
- Operadores típicos: pharma cold chain, food service, lácteos
- Regulaciones con más peso: ATP, HACCP, trazabilidad de temperatura
- Players más relevantes: ORBCOMM, Samsara (reefer), Carrier Transicold
- Criterio público: Q4 si acumula material

---

## Ligero comercial

### vehiculos-comerciales-ligeros

- Nombre editorial: Vehículos comerciales ligeros (LCV)
- Cluster: ligero-comercial
- Vehículos típicos: Mercedes Sprinter, Ford Transit, Renault Master, VW Crafter, Iveco Daily
- Operadores típicos: PYMES, servicio técnico, e-commerce urbano, transporte internacional < 3,5 t
- Regulaciones con más peso: tacógrafo G2V2 (internacional), Orden TRM/282/2026, ZBE
- Players más relevantes: Ford, Mercedes-Benz Vans, Renault Pro+, Peugeot Pro, Citroën Business
- Criterio público: Q3 (material abundante en 2026)

### pickups-utilitarios

- Nombre editorial: Pickups y utilitarios
- Cluster: ligero-comercial
- Vehículos típicos: Ford F-150, Toyota Hilux, Ram 1500, Chevrolet Silverado, Nissan Frontier
- Operadores típicos: construcción ligera, servicio técnico, flotas corporativas MX y LatAm
- Regulaciones con más peso: pocas específicas; depende del uso
- Players más relevantes: Ford, Toyota, Ram, Chevrolet, Nissan
- Criterio público: no por ahora (aunque tag interno activo)

---

## Last mile

### reparto-ultima-milla

- Nombre editorial: Reparto y última milla
- Cluster: last-mile
- Vehículos típicos: furgoneta urbana, moto de reparto, cargo-bike, furgón eléctrico
- Operadores típicos: paquetería, e-commerce, dark stores, food delivery
- Regulaciones con más peso: ZBE, ADAS, reparto nocturno, LEZ en USA
- Players más relevantes: OneRail, Bringg, Onfleet, Onro, FedEx, UPS, Amazon Logistics
- Criterio público: Q3-Q4

---

## Field service

### field-service

- Nombre editorial: Field service (servicio técnico móvil)
- Cluster: field-service
- Vehículos típicos: furgoneta técnica, pickup, van equipada
- Operadores típicos: servicio técnico eléctrico/HVAC/telecom, mantenimiento industrial
- Regulaciones con más peso: tiempos de intervención, seguro, ADAS
- Players más relevantes: Samsara, Fleetio, Webfleet (tracking), ServiceTitan (software)
- Criterio público: Q4 si acumula material

### mantenimiento-tecnico

- Nombre editorial: Flotas de mantenimiento técnico
- Cluster: field-service
- Vehículos típicos: furgoneta de intervención, pickup
- Operadores típicos: utility companies (energía, agua), telecom, facility management
- Regulaciones con más peso: seguridad en carretera, ADAS
- Players más relevantes: Samsara, Webfleet, Fleetio
- Criterio público: no por ahora

---

## Especializado

### ambulancias-emergencias

- Nombre editorial: Ambulancias y emergencias
- Cluster: especializado
- Vehículos típicos: ambulancia básica, UCI móvil, bomberos, policía
- Operadores típicos: SAMUR, Cruz Roja, 112, 911, seguros privados
- Regulaciones con más peso: homologación de vehículo sanitario, ITV, códigos de emergencia
- Players más relevantes: Webfleet, Samsara, Trimble, fabricantes especializados
- Criterio público: evergreen específico posible

### construccion

- Nombre editorial: Flota de construcción
- Cluster: especializado
- Vehículos típicos: camión volquete, grúa móvil, hormigonera, maquinaria pesada
- Operadores típicos: constructoras, subcontratas
- Regulaciones con más peso: matriculación especial, peso máximo, seguridad en obra
- Players más relevantes: Geotab, Fleetio, Trimble, fabricantes OEM de maquinaria
- Criterio público: Q4 si acumula

### cementeras

- Nombre editorial: Flota cementera
- Cluster: especializado
- Vehículos típicos: camión hormigonera, volquete
- Operadores típicos: Cemex, Holcim, Heidelberg, nacionales
- Regulaciones con más peso: peso, emisiones, horarios de descarga
- Players más relevantes: Geotab, Webfleet, Samsara
- Criterio público: no por ahora

### mineria

- Nombre editorial: Flota minera
- Cluster: especializado
- Vehículos típicos: camión minero (CAT, Komatsu), camión de apoyo
- Operadores típicos: mineras de Chile, Perú, México, USA, Australia
- Regulaciones con más peso: seguridad minera, fatiga, ADAS específico
- Players más relevantes: Komatsu, Caterpillar, Scania, Samsara, Wenco
- Criterio público: no por ahora (lector LatAm con nicho)

### residuos-limpieza-urbana

- Nombre editorial: Residuos y limpieza urbana
- Cluster: especializado
- Vehículos típicos: camión compactador, camión cisterna, barredora
- Operadores típicos: concesionarias municipales, ayuntamientos, FCC, Urbaser, Veolia
- Regulaciones con más peso: ZBE, horarios, pliegos públicos
- Players más relevantes: Webfleet, Geotab, Fleetio, fabricantes especializados
- Criterio público: no por ahora

---

## Pasajeros

### transporte-escolar

- Nombre editorial: Transporte escolar
- Cluster: pasajeros
- Vehículos típicos: autobús escolar, van de transporte escolar
- Operadores típicos: concesionarias, colegios privados, ayuntamientos
- Regulaciones con más peso: homologación sanitaria, conductor específico, seguridad
- Players más relevantes: Geotab, Samsara, Webfleet
- Criterio público: no por ahora

### ride-hailing

- Nombre editorial: Ride-hailing y movilidad
- Cluster: pasajeros
- Vehículos típicos: turismo, SUV
- Operadores típicos: Uber, Cabify, Didi, Bolt, taxi con app
- Regulaciones con más peso: VTC, ZBE, horarios, seguro específico
- Players más relevantes: las plataformas + fabricantes de turismo
- Criterio público: no por ahora

### autoescuela

- Nombre editorial: Autoescuela
- Cluster: pasajeros
- Vehículos típicos: turismo de autoescuela, camión de prácticas
- Operadores típicos: autoescuelas y grupos de formación
- Regulaciones con más peso: homologación de vehículo instructivo
- Players más relevantes: fabricantes, software de gestión de autoescuela
- Criterio público: no por ahora

---

## No motorizado

### remolques-activos-no-motorizados

- Nombre editorial: Remolques y activos rastreables no motorizados
- Cluster: no-motorizado
- Vehículos típicos: semirremolque, trailer frigorífico, contenedor, generador, compresor
- Operadores típicos: logística intermodal, alquiler de maquinaria
- Regulaciones con más peso: matriculación de remolques, trazabilidad
- Players más relevantes: ORBCOMM, Queclink, Fleet Complete, Samsara (trailer), Geotab (asset)
- Criterio público: Q4 si acumula

---

## Mixto corporativo

### flotas-corporativas

- Nombre editorial: Flotas corporativas
- Cluster: mixto-corporativo
- Vehículos típicos: turismo ejecutivo, SUV, ligero comercial
- Operadores típicos: multinacionales, banca, farma, consultoría
- Regulaciones con más peso: fiscal (beneficio en especie), ZBE, seguros
- Players más relevantes: Arval, Alphabet, Ayvens, Athlon, Element Fleet
- Criterio público: candidato Q4

### operaciones-mixtas

- Nombre editorial: Operaciones mixtas (ICE + EV, distintos segmentos)
- Cluster: mixto-corporativo
- Vehículos típicos: mezcla ICE + EV, mezcla ligero + pesado
- Operadores típicos: grandes flotas con fases de transición
- Regulaciones con más peso: fiscal EV, ZBE, ADAS
- Players más relevantes: Corpay, WEX, Edenred, Samsara, Geotab
- Criterio público: evergreen posible

### alquiler-sin-conductor

- Nombre editorial: Alquiler sin conductor (rent-a-car empresarial)
- Cluster: mixto-corporativo
- Vehículos típicos: turismo + ligero comercial
- Operadores típicos: Hertz Business, Sixt, Europcar, Enterprise, Goldcar
- Regulaciones con más peso: fiscal, seguro de flota de alquiler
- Players más relevantes: rentals + plataformas de booking
- Criterio público: no por ahora

---

## Cómo se usa en el flujo semanal

- Cada historia con un tipo de flota relevante lleva 1 fleet-type primario + opcional 1 secundario.
- Ediciones nuevas revisan si han tocado un segmento que no tenía cobertura y lo anotan en memoria para compensar en próximas.
- El evergreen se construye preguntando: "¿qué fleet-type no tiene hoy una guía útil en español y sí tiene una audiencia razonable?"
