# Pool · "Sabías qué" · The Fleet Radar

**Última actualización**: 2026-05-24
**Total facts en pool**: 12 (Perplexity batch 1)
**Estado**: En construcción — esperando batches de Grok, ChatGPT, Claude, Gemini, DeepSeek

---

## Política editorial

Cada fact debe cumplir:
- ✅ Cifra concreta y atribuible
- ✅ Fuente nombrada (organismo público, estudio sectorial, prensa especializada)
- ✅ Año del dato (preferencia 2022-2026)
- ✅ Tono periodístico sobrio (no marketing, no opinión)
- ✅ 35-60 palabras
- ✅ Útil para gerente de flota (operacional, regulatorio, costes)

Cada fact normalizado lleva metadata:
- `markets`: mexico, espana, latam, usa, uk, europa, global
- `topics`: combustible, telematica, electrificacion, mantenimiento, compliance, etc.
- `categoria`: emoji + tag visible en la caja
- `confidence`: high / medium / low (revisar si pasamos low a producción)
- `source`: organismo + año
- `evergreen_score`: 1-5 (5 = aplica 5+ años, 1 = caduca en meses)
- `origin`: de qué batch viene (Perplexity, Grok, ChatGPT, Claude, Gemini, DeepSeek)

---

## ⛽ COMBUSTIBLE & FUEL CARDS

### combustible-001 · Peso del combustible en TCO transporte pesado ES
**Fact**: En España, el combustible representa entre el 28% y el 34% del coste total de un camión articulado de largo recorrido, según el Observatorio de Costes del Transporte del Ministerio de Transportes (2024). Variaciones de pocos céntimos por litro tienen impacto directo en el margen operativo.

- **source**: Mitma · Observatorio de Costes del Transporte 2024
- **markets**: espana
- **topics**: combustible, coste-operativo
- **vehicle_type**: pesados
- **categoria**: ⛽ Combustible
- **confidence**: high
- **evergreen_score**: 4
- **origin**: Perplexity

### combustible-002 · Expansión térmica del diésel
**Fact**: El diésel se expande aproximadamente un 0,8% por cada 10 °C de incremento de temperatura, según estándares API y ASTM. Repostar en condiciones cálidas o desde tanques grandes significa recibir menos energía por litro facturado; sin corrección a 15 °C las comparativas de consumo arrojan datos sesgados.

- **source**: API / ASTM — estándares de combustible
- **markets**: global
- **topics**: combustible, fisica, operacion
- **vehicle_type**: todos
- **categoria**: ⛽ Combustible
- **confidence**: high
- **evergreen_score**: 5
- **origin**: Perplexity

### combustible-003 · Dispersión de precios diésel MX
**Fact**: Profeco reportó en 2024 diferencias de hasta 8-12% en el precio por litro entre estaciones dentro de la misma ciudad mexicana, dependiendo de marca y ubicación. La elección de estación puede pesar tanto como el consumo del vehículo en el coste final por kilómetro.

- **source**: Profeco · "Quién es quién en los precios" 2024
- **markets**: mexico
- **topics**: combustible, precios, procurement
- **vehicle_type**: todos
- **categoria**: ⛽ Combustible
- **confidence**: high
- **evergreen_score**: 4
- **origin**: Perplexity

### combustible-004 · Consumo en ralentí camión pesado
**Fact**: Un camión pesado consume entre 2 y 3 litros de diésel por hora en ralentí, según el U.S. Department of Energy (2023). En flotas con esperas largas en carga/descarga, el ralentí puede representar varios puntos porcentuales del consumo anual sin generar productividad alguna.

- **source**: U.S. Department of Energy 2023
- **markets**: usa, global
- **topics**: combustible, operacion, driver-behavior
- **vehicle_type**: pesados
- **categoria**: ⛽ Combustible
- **confidence**: high
- **evergreen_score**: 5
- **origin**: Perplexity

### combustible-005 · Dispersión precios diésel ES (impacto económico)
**Fact**: La CNMC identificó en 2023 diferencias de hasta 0,15 €/litro en diésel entre estaciones cercanas dentro de España. Para una flota de 100 vehículos que consume 30.000 litros/año por unidad, la diferencia potencial supera los 450.000 € anuales — el equivalente a varios sueldos completos de operación.

- **source**: CNMC 2023
- **markets**: espana
- **topics**: combustible, coste, procurement
- **vehicle_type**: todos
- **categoria**: ⛽ Combustible
- **confidence**: high
- **evergreen_score**: 4
- **origin**: Perplexity

### combustible-006 · Presión de neumáticos y consumo
**Fact**: La EPA estima que una presión de neumáticos un 20% por debajo de lo recomendado puede aumentar el consumo de combustible entre 3% y 5% en vehículos comerciales (2023). En flotas con revisiones de mantenimiento irregulares, el sobrecoste acumulado es directo y silencioso.

- **source**: EPA 2023
- **markets**: usa, global
- **topics**: combustible, mantenimiento
- **vehicle_type**: todos
- **categoria**: ⛽ Combustible
- **confidence**: high
- **evergreen_score**: 5
- **origin**: Perplexity

---

## 📡 TELEMÁTICA & GPS

### telematica-001 · ELD reduce violaciones HOS USA
**Fact**: La FMCSA estimó en 2023 que el uso de ELD (Electronic Logging Devices) redujo las violaciones por horas de servicio en más del 50% en Estados Unidos, gracias al registro automático y la auditoría en tiempo real. La digitalización del cumplimiento se traduce en menos sanciones y menos accidentes por fatiga.

- **source**: FMCSA 2023
- **markets**: usa
- **topics**: telematica, compliance, seguridad
- **vehicle_type**: pesados
- **categoria**: 📡 Telemática
- **confidence**: high
- **evergreen_score**: 4
- **origin**: Perplexity

---

## 🚨 SEGURIDAD & ROBO DE CARGA

### seguridad-001 · Robos al transporte de carga MX 2023
**Fact**: El Secretariado Ejecutivo de Seguridad Pública (SESNSP) reportó más de 13.000 robos al transporte de carga en México durante 2023, con concentración en corredores como Puebla-Veracruz. La recurrencia geográfica permite anticipar el riesgo y ajustar rutas, horarios y escoltas.

- **source**: SESNSP 2023
- **markets**: mexico
- **topics**: seguridad, robo-carga, ruta
- **vehicle_type**: pesados
- **categoria**: 🚨 Seguridad
- **confidence**: high
- **evergreen_score**: 4
- **origin**: Perplexity

---

## 📦 ÚLTIMA MILLA & E-COMMERCE

### ultima-milla-001 · Coste de entregas fallidas
**Fact**: McKinsey estimó en 2023 que las entregas fallidas pueden incrementar el coste logístico de un pedido hasta un 15%, contando reintentos, reprogramación y carga administrativa. En operaciones de alto volumen este efecto erosiona directamente el margen de la última milla.

- **source**: McKinsey 2023
- **markets**: global, europa
- **topics**: ultima-milla, coste, ecommerce
- **vehicle_type**: ligeros
- **categoria**: 📦 Última milla
- **confidence**: medium
- **evergreen_score**: 4
- **origin**: Perplexity

---

## 🟡 Pendientes de verificar (claims sin source confirmado)

Listas de candidatos que aparecieron en los batches pero NO se incluyen
en producción hasta validar fuente:

### Combustible
- "Redes abiertas de fuel cards pueden reducir coste total ~1% vs cerradas"
  → Origin: Perplexity. Pendiente: buscar fuente exacta en Fleet Europe / ATA / McKinsey.

### Coverage gaps (anotados por Perplexity)
- Fraude de combustible en flotas privadas LatAm — buscar en auditorías judiciales o prensa especializada
- Telemática avanzada y última milla fuera de México y Colombia — datos LatAm escasos

---

## Backlog (esperando batches)

| Origen | Status | Esperado |
|---|---|---|
| Perplexity | ✅ recibido (12 facts) | combustible 6 + telemática 1 + seguridad 1 + última milla 1 |
| Grok | ⏳ pendiente | |
| ChatGPT | ⏳ pendiente | |
| Claude | ⏳ pendiente | |
| Gemini | ⏳ pendiente | |
| DeepSeek | ⏳ pendiente | |

**Target final**: 250-300 facts normalizados, ~15-25 por cada una de las 15 categorías editoriales.

---

## Categorías target (recordatorio)

1. ⛽ Combustible & Fuel cards
2. 📡 Telemática & GPS
3. ⚖️ Regulación España (DGT, V-16, ZBE, ITV, tacógrafo)
4. ⚖️ Regulación México (SICT, NOM, T-MEC, Carta Porte, CNE)
5. ⚡ Electrificación
6. 🔧 Mantenimiento
7. 🛡️ Compliance & Multas
8. 🚨 Seguridad & Robo de carga
9. 📦 Última milla & E-commerce
10. 🚛 Renting & Leasing
11. 🏭 Sectores verticales
12. 🌎 Geopolítica & Comercio (T-MEC, nearshoring, Brexit)
13. 🚢 Logística & Corredores (puertos, ferrocarril, peajes)
14. 💼 Operadores & 3PL
15. 🏢 Gestión de flotas / fleet management (genéricos)
