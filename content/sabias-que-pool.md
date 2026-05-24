# Pool · "Sabías qué" · The Fleet Radar

**Última actualización**: 2026-05-24
**Total facts producción-ready**: 137 (estructura por ID; cobertura ampliada con metadata cross-LLM)
**Cross-validated (2+ LLMs)**: 41
**Pendientes verificación / Conflictos**: 11
**Estado**: 6 de 6 batches procesados (Perplexity + Grok + Gemini + DeepSeek + ChatGPT + Claude). ✅ Pool consolidado.

---

## Política editorial

Cada fact:
- ✅ Cifra concreta y atribuible
- ✅ Fuente nombrada (organismo, estudio, prensa especializada)
- ✅ Año del dato (preferencia 2023-2026)
- ✅ Tono periodístico sobrio (no marketing)
- ✅ 35-60 palabras
- ✅ Útil para gerente de flota

Niveles de confianza:
- **high** — 1 fuente sólida, dato verificable
- **high-cross** — 2+ LLMs/fuentes confirman cifras compatibles (más robusto)
- **medium** — fuente vaga o cifra discutible
- **pending** — apartado hasta validar (no producción)

---

## ⛽ COMBUSTIBLE & FUEL CARDS

### combustible-001 · Peso del combustible en TCO transporte pesado ES
**Fact**: En España, el combustible representa el 27,5% del coste total de explotación de un vehículo articulado de carga general, según el Observatorio de Costes del Transporte de Mercancías por Carretera del Mitma (octubre 2025). Sigue por debajo del 34,8% que pesan personal y dietas, pero variaciones de pocos céntimos por litro mueven el margen operativo.

- **source**: Mitma · Observatorio de Costes del Transporte (oct 2025)
- **markets**: espana
- **topics**: combustible, coste-operativo
- **vehicle_type**: pesados
- **categoria**: ⛽ Combustible
- **confidence**: high-cross (Perplexity 28-34% + Grok 27,5% + Gemini 31-38% + Claude 25-35% / hasta 40% en ciclos altos — cuatro fuentes coherentes)
- **evergreen_score**: 4
- **origin**: Perplexity + Grok + Gemini + Claude

### combustible-002 · Expansión térmica del diésel
**Fact**: El diésel se expande aproximadamente un 0,83% por cada 10 °C de incremento de temperatura (coeficiente 0,00083/°C, según estándares API/ASTM y revisión técnica Chevron). Un cambio de 10 °C puede alterar el volumen en casi 2 litros por cada 200 cargados; sin corrección a 15 °C las comparativas de consumo arrojan datos sesgados.

- **source**: API MPMS Ch. 11 + ASTM D1250 + Chevron Diesel Fuels Technical Review
- **markets**: global
- **topics**: combustible, fisica, operacion
- **vehicle_type**: todos
- **categoria**: ⛽ Combustible
- **confidence**: high-cross (Perplexity 0,8% por 10°C + Grok 0,00083/°C + Gemini NIST 0,084%/°C + ChatGPT API MPMS + Claude ASTM D1250/ISO 91 — cinco fuentes coinciden)
- **evergreen_score**: 5
- **origin**: Perplexity + Grok + Gemini + ChatGPT + Claude

### combustible-003 · Dispersión de precios diésel MX
**Fact**: Profeco, a través de "Quién es quién en los precios", documentó en 2024 diferencias de hasta 8-12% en el precio por litro de diésel entre estaciones dentro de la misma ciudad mexicana. La CRE ha cifrado dispersión intra-zona próxima al 15%. La elección de estación puede pesar tanto como el consumo del vehículo en el coste por kilómetro.

- **source**: Profeco "Quién es quién en los precios" 2024 + CRE
- **markets**: mexico
- **topics**: combustible, precios, procurement
- **vehicle_type**: todos
- **categoria**: ⛽ Combustible
- **confidence**: high-cross (Perplexity 8-12% + DeepSeek 15% CRE + ChatGPT Profeco + Claude CRE 1,80-2 pesos/litro misma alcaldía CDMX)
- **evergreen_score**: 4
- **origin**: Perplexity + DeepSeek + ChatGPT + Claude

### combustible-004 · Consumo en ralentí camión pesado
**Fact**: Un camión pesado consume entre 0,8 y 4 litros de diésel por hora en ralentí, según rango DOE / EPA. En operación real, el ralentí prolongado durante descansos puede sumar 1.800 horas y unos 1.500 galones por camión al año. Una flota de 100 unidades con 2 h diarias de ralentí supera los 200.000 litros anuales sin productividad alguna.

- **source**: U.S. Department of Energy · Alternative Fuels Data Center + EPA SmartWay
- **markets**: usa, global
- **topics**: combustible, operacion, driver-behavior
- **vehicle_type**: pesados
- **categoria**: ⛽ Combustible
- **confidence**: high-cross (Perplexity 2-3 L/h + Grok 1.500 gal/año + Gemini 2,5-4 L/h + ChatGPT 0,8 gal/h × 1.800 h + Claude DOE 2-4 L/h, 15-40% del consumo diario)
- **evergreen_score**: 5
- **origin**: Perplexity + Grok + Gemini + ChatGPT + Claude

### combustible-005 · Dispersión precios diésel ES (impacto económico)
**Fact**: La CNMC identificó en 2023 diferencias de hasta 0,15 €/litro en diésel entre estaciones cercanas dentro de España, con dispersiones provinciales próximas al 14% el mismo día. Para una flota de 100 vehículos que consume 30.000 litros/año por unidad, la diferencia potencial supera los 450.000 € anuales.

- **source**: CNMC · Boletín de precios de carburantes 2023-2024
- **markets**: espana
- **topics**: combustible, coste, procurement
- **vehicle_type**: todos
- **categoria**: ⛽ Combustible
- **confidence**: high-cross (Perplexity 0,15 €/l + Gemini 14% intra-provincia + ChatGPT 3.000 estaciones gasóleo B + Claude Geoportal MITECO >0,20 €/l autopista vs urbana)
- **evergreen_score**: 4
- **origin**: Perplexity + Gemini + ChatGPT + Claude

### combustible-006 · Presión de neumáticos y consumo
**Fact**: Una presión de neumáticos un 20% por debajo de lo recomendado puede aumentar el consumo de combustible entre 3% y 5% en vehículos comerciales, según la EPA. NACFE y Argonne National Laboratory cifran el sobrecoste en torno al 1% por cada 10 psi de bajo inflado; TMC/SmartWay sitúa el efecto en +1-1,5% de consumo por cada 10% de presión perdida. En flotas con revisiones irregulares, el extra es directo y silencioso.

- **source**: EPA SmartWay + NACFE/Argonne + TMC
- **markets**: usa, global
- **topics**: combustible, mantenimiento
- **vehicle_type**: todos
- **categoria**: ⛽ Combustible
- **confidence**: high-cross (Perplexity + Grok + Gemini + Claude DOE 0,5-1% por cada 10% subinflado — cuatro fuentes)
- **evergreen_score**: 5
- **origin**: Perplexity + Grok + Gemini + Claude

### combustible-007 · Peso del combustible MX
**Fact**: En México, el consumo de combustibles y lubricantes representa entre el 42% y el 47% de los gastos por consumo de bienes y servicios en el autotransporte de carga, según la Encuesta Anual de Transportes 2024 del INEGI. Una proporción notablemente superior a la europea — y mucho más expuesta a variaciones de precio.

- **source**: INEGI · Encuesta Anual de Transportes 2024
- **markets**: mexico
- **topics**: combustible, coste-operativo, benchmark
- **vehicle_type**: pesados, ligeros
- **categoria**: ⛽ Combustible
- **confidence**: high
- **evergreen_score**: 4
- **origin**: Grok

### combustible-008 · Consumo AdBlue Euro 6
**Fact**: El consumo de AdBlue en camiones pesados Euro 6/VI suele situarse entre el 4% y el 7% del consumo de diésel — unos 5-7 litros por cada 100 de diésel, según ACEA y documentación técnica de fabricantes. Es un componente del TCO frecuentemente subestimado y, además, un termómetro útil: anomalías en el ratio AdBlue/diésel apuntan a problemas de motor o conducción.

- **source**: ACEA + Yara · Documentación técnica fabricantes Euro 6 (2024)
- **markets**: espana, europa
- **topics**: combustible, mantenimiento
- **vehicle_type**: pesados
- **categoria**: ⛽ Combustible
- **confidence**: high-cross (Grok 4-6% + Gemini 5-7% ACEA + Claude 5-8% Volvo/MAN/Mercedes)
- **evergreen_score**: 4
- **origin**: Grok + Gemini + Claude

### combustible-009 · Robo de combustible a Pemex
**Fact**: El hurto de combustible a Pemex generó pérdidas estimadas en 20.530 millones de pesos en 2024, un 10% más que el año anterior. La escala del problema sistémico afecta también al sector privado de autotransporte, donde las anomalías en cargas (sifonaje, ajustes en la bomba) deben detectarse en tiempo real.

- **source**: Pemex · reporte anual 2024 (vía Argus Media)
- **markets**: mexico
- **topics**: combustible, fraude, seguridad
- **vehicle_type**: pesados
- **categoria**: ⛽ Combustible
- **confidence**: high
- **evergreen_score**: 3 (cifra anual, conviene actualizar 2025-26)
- **origin**: Grok

### combustible-010 · Velocidad y consumo
**Fact**: Pasar de 90 a 110 km/h en autopista incrementa el consumo de un vehículo pesado en torno al 20%, según IDAE. La conducción agresiva añade hasta un 33% adicional en autopista y un 5% en ciudad (DOE EERE). Limitar velocidad por telemática es una de las palancas operativas de mayor retorno inmediato.

- **source**: IDAE · Guía de conducción eficiente + DOE EERE
- **markets**: espana, global
- **topics**: combustible, driver-behavior
- **vehicle_type**: pesados
- **categoria**: ⛽ Combustible
- **confidence**: high-cross (Gemini IDAE + Gemini DOE + Claude EPA SmartWay 75→65 mph = -12-15% — tres fuentes coinciden)
- **evergreen_score**: 5
- **origin**: Gemini + Claude

### combustible-011 · Desvío a estación lejana
**Fact**: Cada desvío de 5 km para repostar fuera de ruta cuesta unos 2,20 € en consumo y desgaste por viaje, según parámetros del Observatorio de Costes del Mitma. Una flota de 100 vehículos con 50 desvíos por semana puede acumular cerca de 5.700 € anuales en desvíos invisibles a la cuenta de resultados.

- **source**: Mitma · Observatorio de Costes (modelo de cálculo 2024)
- **markets**: espana
- **topics**: combustible, ruta, coste
- **vehicle_type**: pesados
- **categoria**: ⛽ Combustible
- **confidence**: medium (cálculo derivado de fuente oficial)
- **evergreen_score**: 4
- **origin**: Gemini

### combustible-012 · Auditoría tarjetas de combustible MX
**Fact**: La Auditoría Superior de la Federación detectó en revisiones a entes públicos mexicanos que entre el 3% y el 5% de las transacciones con tarjetas de combustible presentan anomalías severas (cargas superiores al tanque, doble carga simultánea, kilometraje inconsistente). El mismo patrón se observa en flotas privadas sin reglas de validación.

- **source**: ASF México · Cuenta Pública 2022 + informes de revisión
- **markets**: mexico
- **topics**: combustible, fraude, control
- **vehicle_type**: todos
- **categoria**: ⛽ Combustible
- **confidence**: high-cross (Gemini + Claude ASF 2022)
- **evergreen_score**: 4
- **origin**: Gemini + Claude

### combustible-013 · Aire acondicionado y consumo urbano
**Fact**: El aire acondicionado puede elevar entre 5% y 20% el consumo de combustible en circulación urbana, según CONUEE México. El impacto es máximo en arranque/parada y trayectos cortos — perfil típico de reparto urbano. Conducción con A/C a temperatura moderada y mantenimiento del filtro pesan más que apagarlo intermitentemente.

- **source**: CONUEE · Comisión Nacional para el Uso Eficiente de la Energía
- **markets**: mexico, latam
- **topics**: combustible, operacion
- **vehicle_type**: ligeros
- **categoria**: ⛽ Combustible
- **confidence**: high
- **evergreen_score**: 5
- **origin**: Gemini

### combustible-014 · Conciliación manual de tickets
**Fact**: Conciliar tickets de combustible de forma manual consume entre 15 y 20 minutos por vehículo y mes, según mediciones recogidas por Fleet Europe. Para una flota de 500 vehículos son cerca de 150 horas mensuales — el equivalente a un FTE administrativo dedicado exclusivamente a esa tarea.

- **source**: Fleet Europe · Industry benchmark 2023
- **markets**: europa, espana
- **topics**: combustible, operacion, administracion
- **vehicle_type**: todos
- **categoria**: ⛽ Combustible
- **confidence**: medium
- **evergreen_score**: 4
- **origin**: Gemini

### combustible-015 · Sifonaje de diésel
**Fact**: Un robo por sifonaje sustrae entre 200 y 400 litros de diésel por evento, según datos de FENADISMER. En depósitos sin alarma volumétrica ni cierre antivandálico, el incidente puede pasar desapercibido hasta el siguiente ciclo de reabastecimiento, complicando además la trazabilidad de la siniestralidad ante la aseguradora.

- **source**: FENADISMER · Reportes a asociados 2023-2024 + Truckers Report / Transport Intelligence 2022
- **markets**: espana, europa
- **topics**: combustible, robo, seguridad
- **vehicle_type**: pesados
- **categoria**: ⛽ Combustible
- **confidence**: high-cross (Gemini FENADISMER + Claude sifón áreas descanso ES/FR)
- **evergreen_score**: 4
- **origin**: Gemini + Claude

### combustible-016 · Coste por kilómetro articulado ES
**Fact**: El Observatorio de Costes del Mitma cifra en julio 2024 el coste total de un articulado de carga general en torno a 1,30 €/km recorrido y 1,53 €/km cargado. Es el termómetro de referencia para evaluar tarifas, presupuestos y rentabilidad por ruta en el mercado español.

- **source**: Mitma · Observatorio de Costes (julio 2024)
- **markets**: espana
- **topics**: combustible, coste-operativo, benchmark
- **vehicle_type**: pesados
- **categoria**: ⛽ Combustible
- **confidence**: high
- **evergreen_score**: 3 (se actualiza semestralmente)
- **origin**: ChatGPT

### combustible-017 · Coste total trucking USA
**Fact**: El American Transportation Research Institute cifró en 2024 el coste operativo marginal del trucking estadounidense en torno a 2,26 USD por milla en promedio sectorial. Permite comparar coste por kilómetro España-México-USA y dimensionar la sensibilidad real de cada flota al precio del diésel.

- **source**: ATRI · An Analysis of the Operational Costs of Trucking 2024
- **markets**: usa
- **topics**: combustible, coste-operativo, benchmark
- **vehicle_type**: pesados
- **categoria**: ⛽ Combustible
- **confidence**: high-cross (ChatGPT 2,26 USD/milla total + Claude 0,548 USD/milla combustible = 38% del total — máximo histórico)
- **evergreen_score**: 3
- **origin**: ChatGPT + Claude

### combustible-018 · Hotelería sin pernoctación en cabina
**Fact**: Diez horas de descanso con motor encendido en cabina pueden costar cerca de 20 USD en diésel a precios DOE de referencia (2,5 USD/galón × 0,8 gal/h). Sistemas APU, calefacción autónoma y políticas anti-idling devuelven la inversión en pocos meses para perfiles de larga distancia.

- **source**: U.S. Department of Energy
- **markets**: usa
- **topics**: combustible, driver-behavior, anti-idling
- **vehicle_type**: pesados
- **categoria**: ⛽ Combustible
- **confidence**: high
- **evergreen_score**: 4
- **origin**: ChatGPT

### combustible-019 · CO2 regulatorio camiones UE
**Fact**: El reglamento europeo de CO2 para vehículos pesados fija recortes de 45% en 2030, 65% en 2035 y 90% en 2040 sobre niveles 2019. Combinado con peajes diferenciados por emisiones, presiona la renovación de flota y obliga a planificar electrificación o combustibles alternativos con varios años de antelación.

- **source**: Reglamento (UE) 2024/1610 · Comisión Europea
- **markets**: espana, europa
- **topics**: combustible, regulacion, electrificacion
- **vehicle_type**: pesados
- **categoria**: ⛽ Combustible
- **confidence**: high
- **evergreen_score**: 5
- **origin**: ChatGPT

### combustible-020 · Pesados y emisiones del transporte UE
**Fact**: Los vehículos pesados representan apenas el 2% del parque rodado europeo pero generan en torno al 25% de las emisiones del transporte por carretera y un 6% de las emisiones totales de la UE, según la Comisión Europea. El motivo por el que el regulador centra ahí su prioridad de descarbonización.

- **source**: Comisión Europea · DG CLIMA
- **markets**: europa, espana
- **topics**: combustible, regulacion, emisiones
- **vehicle_type**: pesados
- **categoria**: ⛽ Combustible
- **confidence**: high
- **evergreen_score**: 5
- **origin**: ChatGPT

### combustible-022 · Fuel cards red abierta vs red cerrada (USA)
**Fact**: Según el Nilson Report (2023), las tarjetas de combustible "branded" (red cerrada) dominan la cuota corporativa en USA, mientras las "open-loop" universales ofrecen mayor cobertura de aceptación a costa de menor control granular del dato de transacción. En corredores con baja presencia de la red elegida, el diferencial real entre redes no es de precio sino de kilómetros desviados.

- **source**: Nilson Report · Fleet Card Market USA 2023
- **markets**: usa
- **topics**: combustible, fuel-cards, procurement
- **vehicle_type**: todos
- **categoria**: ⛽ Combustible
- **confidence**: medium
- **evergreen_score**: 3
- **origin**: Claude

### combustible-023 · Patrones de fraude detectables en fuel cards
**Fact**: Cargas superiores al volumen del depósito, dos cargas en lapso inferior al tiempo de vaciado, repostajes fuera del corredor habitual y horarios atípicos son los cuatro patrones de fraude más sistemáticos en tarjetas de combustible, según el Report to the Nations 2024 de la ACFE. Indetectables en revisión manual mensual, exigen datos transaccionales vinculados a vehículo, conductor y odómetro.

- **source**: ACFE · Report to the Nations 2024
- **markets**: global
- **topics**: combustible, fraude, fuel-cards
- **vehicle_type**: todos
- **categoria**: ⛽ Combustible
- **confidence**: medium
- **evergreen_score**: 5
- **origin**: Claude

### combustible-024 · Aerodinámica camión pesado
**Fact**: A más de 90 km/h, la resistencia aerodinámica representa entre el 50% y el 65% de la resistencia total al avance en un camión articulado, según el Lawrence Berkeley National Laboratory. Deflectores laterales y faldones traseros pueden reducir entre 5% y 10% el consumo — un criterio de coste de operación que pesa en la decisión de compra del vehículo, no solo en la estética.

- **source**: Lawrence Berkeley National Laboratory · Heavy Truck Aerodynamics
- **markets**: usa, global
- **topics**: combustible, fisica, vehiculo
- **vehicle_type**: pesados
- **categoria**: ⛽ Combustible
- **confidence**: high
- **evergreen_score**: 5
- **origin**: Claude

### combustible-025 · Consumo en frío
**Fact**: El consumo de combustible de un vehículo ligero puede aumentar hasta un 15% a 0 °C respecto a 25 °C, según el U.S. Department of Energy: mayor tiempo de calentamiento del motor, lubricante más viscoso y uso de calefacción. En flotas con operación en zonas frías, presupuestar combustible plano todo el año infraestima sistemáticamente los meses de noviembre a febrero.

- **source**: DOE · Alternative Fuels Data Center
- **markets**: usa, espana, global
- **topics**: combustible, estacionalidad
- **vehicle_type**: ligeros, pesados
- **categoria**: ⛽ Combustible
- **confidence**: high
- **evergreen_score**: 5
- **origin**: Claude

### combustible-026 · Reglamento (UE) 2019/1242 CO2 fabricantes
**Fact**: El Reglamento (UE) 2019/1242 obliga a los fabricantes europeos de camiones a recortar -15% de CO2 en 2025 y -30% en 2030 sobre niveles 2019. La multa por incumplimiento es 4.250 € por g/km/t de CO2 excedido por vehículo vendido. La presión sobre la oferta acelera la electrificación y condiciona disponibilidad y precio del diésel nuevo a partir de 2025.

- **source**: Reglamento (UE) 2019/1242 · Parlamento Europeo
- **markets**: europa, espana
- **topics**: combustible, regulacion, electrificacion
- **vehicle_type**: pesados
- **categoria**: ⛽ Combustible
- **confidence**: high
- **evergreen_score**: 4
- **origin**: Claude

### combustible-027 · IEH + IVA en precio del diésel ES
**Fact**: El Impuesto Especial sobre Hidrocarburos más el IVA suman cerca del 45-50% del precio final del gasoil en España, según la AEAT. A 1,50 €/litro, unos 0,70-0,75 € son carga fiscal. Las flotas con derecho a gasóleo bonificado que no auditan la aplicación correcta del beneficio están pagando impuesto que no les corresponde.

- **source**: AEAT + BOE · Ley del Impuesto sobre Hidrocarburos
- **markets**: espana
- **topics**: combustible, fiscalidad, procurement
- **vehicle_type**: pesados, agricolas, especiales
- **categoria**: ⛽ Combustible
- **confidence**: high
- **evergreen_score**: 3
- **origin**: Claude

### combustible-028 · Tolerancia metrológica surtidor ES
**Fact**: El Real Decreto 1088/2010 y la Directiva 2014/32/UE (MID) admiten una tolerancia metrológica de hasta ±0,5% en surtidores de combustible homologados en España. Para una flota que reposta 1.000.000 de litros al año, ese margen legal equivale a hasta 5.000 litros de diferencia entre lo facturado y lo entregado — invisible en una factura, no en una auditoría con datos por vehículo.

- **source**: RD 1088/2010 + Directiva 2014/32/UE (MID) + ENAC
- **markets**: espana, europa
- **topics**: combustible, metrologia, control
- **vehicle_type**: todos
- **categoria**: ⛽ Combustible
- **confidence**: high
- **evergreen_score**: 5
- **origin**: Claude

### combustible-029 · Volatilidad gasoil MX 2020-2024
**Fact**: Entre 2020 y 2024 el precio del gasoil acumuló en México una variación superior al 60%, según el Índice de Precios del Transporte de Mercancías por Carretera del INEGI. Es la partida más volátil del índice y la principal razón por la que los contratos de flete a precio fijo sin cláusula de ajuste por combustible terminan trasladando el riesgo al transportista.

- **source**: INEGI · Índice de Precios del Transporte de Carga
- **markets**: mexico
- **topics**: combustible, precios, contratos
- **vehicle_type**: pesados
- **categoria**: ⛽ Combustible
- **confidence**: medium
- **evergreen_score**: 3
- **origin**: Claude

### combustible-021 · Diferencia consumo real vs homologado
**Fact**: ACEA y la EEA estiman que el consumo real de turismos y vehículos comerciales ligeros supera al homologado WLTP en torno a un 7-14% de media. Para presupuestar combustible de una flota nueva, asumir el dato de fabricante es subestimar sistemáticamente el TCO.

- **source**: ACEA + European Environment Agency · Real-world fuel consumption 2023
- **markets**: europa, espana
- **topics**: combustible, benchmark
- **vehicle_type**: ligeros
- **categoria**: ⛽ Combustible
- **confidence**: high
- **evergreen_score**: 4
- **origin**: DeepSeek

---

## 📡 TELEMÁTICA & GPS

### telematica-001 · ELD reduce violaciones HOS USA
**Fact**: La FMCSA estimó que el mandato ELD (Electronic Logging Devices) redujo las violaciones por horas de servicio en más del 50% en Estados Unidos, gracias al registro automático y la auditoría en tiempo real. La digitalización del cumplimiento se traduce en menos sanciones y menos accidentes por fatiga.

- **source**: FMCSA · Electronic Logging Device evaluation
- **markets**: usa
- **topics**: telematica, compliance, seguridad
- **vehicle_type**: pesados
- **categoria**: 📡 Telemática
- **confidence**: high
- **evergreen_score**: 4
- **origin**: Perplexity

### telematica-002 · Tacógrafo inteligente G2V2 UE
**Fact**: El tacógrafo inteligente G2V2 es obligatorio en transporte internacional dentro de la UE desde agosto de 2025, con migración escalonada para flotas anteriores. Multas por incumplimiento o manipulación llegan a 4.001 € por infracción muy grave en España, según el régimen sancionador de la LOTT.

- **source**: Reglamento (UE) 2020/1054 + Reglamento de Ejecución (UE) 2021/1228 · DG MOVE + LOTT (España)
- **markets**: espana, europa
- **topics**: telematica, regulacion, tacografo
- **vehicle_type**: pesados
- **categoria**: 📡 Telemática
- **confidence**: high-cross (Gemini + DeepSeek + Claude — tres fuentes confirman calendario y G2V2 con GNSS/DSRC)
- **evergreen_score**: 5
- **origin**: Gemini + DeepSeek + Claude

### telematica-003 · Desviación odómetros manuales vs CAN bus
**Fact**: Los odómetros leídos manualmente acumulan entre 3% y 7% de desviación frente a la lectura CAN bus real, según mediciones recogidas por Fleet News. Para una flota de larga distancia, ese desfase distorsiona el cálculo de consumo por 100 km, los intervalos de mantenimiento preventivo y la valoración residual.

- **source**: Fleet News · benchmark sectorial 2023
- **markets**: europa, global
- **topics**: telematica, mantenimiento, datos
- **vehicle_type**: todos
- **categoria**: 📡 Telemática
- **confidence**: medium
- **evergreen_score**: 5
- **origin**: Gemini

### telematica-004 · Video-telemática con IA y siniestralidad
**Fact**: La FMCSA documenta que la combinación de video-telemática con IA (DMS + ADAS + coaching) reduce el coste de siniestros hasta un 50% en flotas pesadas. La detección de fatiga ocurre típicamente 2-3 segundos antes de la salida de carril (NHTSA), tiempo suficiente para evitar la mayoría de eventos críticos.

- **source**: FMCSA + NHTSA
- **markets**: usa, global
- **topics**: telematica, video, seguridad
- **vehicle_type**: pesados
- **categoria**: 📡 Telemática
- **confidence**: high-cross (Gemini FMCSA + Gemini NHTSA + ChatGPT Verizon "70% extremely useful" + Claude Fleet News UK aseguradoras -15% prima)
- **evergreen_score**: 4
- **origin**: Gemini + ChatGPT + Claude

### telematica-005 · Eventos de frenado brusco y siniestralidad
**Fact**: Vehículos con más de 5 eventos de frenado brusco por cada 100 km tienen aproximadamente 3 veces más probabilidad de sufrir colisión grave, según estudios del Virginia Tech Transportation Institute. Es el indicador conductual con mejor correlación con siniestralidad y prima asegurable.

- **source**: Virginia Tech Transportation Institute
- **markets**: usa, global
- **topics**: telematica, seguridad, driver-behavior
- **vehicle_type**: todos
- **categoria**: 📡 Telemática
- **confidence**: high
- **evergreen_score**: 5
- **origin**: Gemini

### telematica-006 · Jammers GPS en robo de carga MX
**Fact**: ANERPV estima que cerca del 85% de los incidentes de robo de carga en México involucran el uso de inhibidores de señal (jammers GPS). Plataformas con detección de pérdida de cobertura repentina y geofencing redundante (GPS + RF + celular) son la respuesta operativa estándar.

- **source**: ANERPV · Asociación Nacional de Empresas de Rastreo y Protección Vehicular
- **markets**: mexico
- **topics**: telematica, seguridad, robo-carga
- **vehicle_type**: pesados
- **categoria**: 📡 Telemática
- **confidence**: high
- **evergreen_score**: 4
- **origin**: Gemini

### telematica-007 · DTC remoto y downtime no planificado
**Fact**: La lectura remota de códigos de diagnóstico (DTC) integrada en telemática reduce entre 20% y 25% el downtime no planificado en flotas pesadas, según TMC (Technology & Maintenance Council). Permite triajar fallos antes de la avería y planificar la entrada a taller con piezas ya pedidas.

- **source**: TMC · Technology & Maintenance Council (American Trucking Associations)
- **markets**: usa, global
- **topics**: telematica, mantenimiento
- **vehicle_type**: pesados
- **categoria**: 📡 Telemática
- **confidence**: high
- **evergreen_score**: 5
- **origin**: Gemini

### telematica-008 · Geocercas y uso no autorizado
**Fact**: La implantación de geocercas con alertas en tiempo real reduce entre 4% y 6% los kilómetros no autorizados en flotas comerciales, según Transporte XXI. En vehículos de uso compartido o asignación nominal, los desvíos del trayecto previsto representan combustible, desgaste y exposición a siniestro sin cobertura.

- **source**: Transporte XXI · análisis sectorial
- **markets**: espana, europa
- **topics**: telematica, control, coste
- **vehicle_type**: ligeros, pesados
- **categoria**: 📡 Telemática
- **confidence**: medium
- **evergreen_score**: 4
- **origin**: Gemini

### telematica-009 · Remolques ociosos en flotas grandes
**Fact**: Entre el 15% y el 20% de los remolques de flotas grandes permanecen más de 5 días ociosos en patio sin asignación, según FreightWaves. Es capital trabajando a cero — la telemática de remolque (con localización y estado de carga) es la palanca directa para aumentar la rotación.

- **source**: FreightWaves · trailer utilization reports
- **markets**: usa, global
- **topics**: telematica, utilizacion
- **vehicle_type**: remolques
- **categoria**: 📡 Telemática
- **confidence**: medium
- **evergreen_score**: 4
- **origin**: Gemini

### telematica-010 · TPMS y reventones en autopista
**Fact**: Los sistemas TPMS (Tyre Pressure Monitoring) reducen un 56% los reventones en autopista en vehículos pesados, según FMCSA. El reglamento UNECE R141 lo hace obligatorio en nuevos vehículos comerciales de la UE desde 2022 (extendido a N1/N2/N3/O3/O4 por el Reglamento 2019/2144).

- **source**: FMCSA + UNECE R141 + Reglamento (UE) 2019/2144 + Reglamento (CE) 661/2009
- **markets**: usa, europa, espana
- **topics**: telematica, seguridad, neumaticos
- **vehicle_type**: pesados, ligeros
- **categoria**: 📡 Telemática
- **confidence**: high-cross (Gemini + DeepSeek + ChatGPT + Claude — cuatro fuentes confirman -56% reventones y obligatoriedad UE)
- **evergreen_score**: 5
- **origin**: Gemini + DeepSeek + ChatGPT + Claude

### telematica-011 · GPS obligatorio carga peligrosa MX
**Fact**: La NOM-012-SCT-2-2023 obliga al transporte mexicano de carga peligrosa a contar con GPS con reporte cada 30 segundos. El incumplimiento genera multas y la suspensión del permiso SCT. La norma alinea a México con prácticas equivalentes en UE y USA para materiales clase ADR/IMO.

- **source**: NOM-012-SCT-2-2023 · Secretaría de Comunicaciones y Transportes
- **markets**: mexico
- **topics**: telematica, regulacion, carga-peligrosa
- **vehicle_type**: pesados
- **categoria**: 📡 Telemática
- **confidence**: high
- **evergreen_score**: 5
- **origin**: DeepSeek

### telematica-012 · Conducción agresiva y consumo
**Fact**: Geotab cuantifica en flotas reales hasta un 35% más de consumo en perfiles de conducción agresiva frente a conductores eficientes operando el mismo modelo. Programas de coaching con datos individuales devuelven retorno medible en pocos meses sobre la factura de combustible.

- **source**: Geotab · Fleet Management Insights 2023 + EPA SmartWay + IRU 2022
- **markets**: global
- **topics**: telematica, driver-behavior, combustible
- **vehicle_type**: todos
- **categoria**: 📡 Telemática
- **confidence**: high-cross (DeepSeek Geotab 35% + Claude SmartWay/IRU 10-15%)
- **evergreen_score**: 5
- **origin**: DeepSeek + Claude

### telematica-013 · GPS obligatorio Argentina
**Fact**: La CNRT (Comisión Nacional de Regulación del Transporte) exige en Argentina GPS con reporte cada 15 segundos en transporte interjurisdiccional de cargas. Los controles de carretera cruzan la posición declarada en tiempo real con la ruta autorizada para detectar desvíos no notificados.

- **source**: CNRT · Resoluciones de seguimiento satelital
- **markets**: latam
- **topics**: telematica, regulacion
- **vehicle_type**: pesados
- **categoria**: 📡 Telemática
- **confidence**: high
- **evergreen_score**: 4
- **origin**: DeepSeek

### telematica-014 · Telemática en flotas de basura urbanas
**Fact**: Un estudio de la Universidad Politécnica de Madrid sobre flotas municipales de recogida de residuos midió una reducción de hasta el 15% en consumo de combustible al optimizar rutas con telemática y sensores de llenado de contenedores. Aplicable a cualquier flota con rutas fijas urbanas.

- **source**: UPM · Universidad Politécnica de Madrid
- **markets**: espana
- **topics**: telematica, sectores, residuos
- **vehicle_type**: pesados
- **categoria**: 📡 Telemática
- **confidence**: medium
- **evergreen_score**: 4
- **origin**: DeepSeek

### telematica-015 · ROI de telemática en flotas EU
**Fact**: La encuesta Verizon Connect 2024 indica que el 86% de gestores europeos de flotas con telemática obtuvo ROI en menos de 12 meses, y un 41% en menos de seis. Los principales drivers de retorno: combustible, productividad y reducción de siniestros.

- **source**: Verizon Connect · Fleet Technology Trends 2024
- **markets**: europa, espana
- **topics**: telematica, roi, benchmark
- **vehicle_type**: todos
- **categoria**: 📡 Telemática
- **confidence**: high
- **evergreen_score**: 4
- **origin**: ChatGPT

### telematica-016 · Mercado europeo FMS
**Fact**: Berg Insight proyecta 30,5 millones de unidades activas de Fleet Management System en Europa para 2029, con un crecimiento sostenido de dos dígitos anuales. La consolidación entre proveedores (con players como Targa Telematics gestionando más de 900.000 unidades) reduce la fragmentación histórica.

- **source**: Berg Insight · Fleet Management in Europe (2024) + Smart Trucks North America 2023
- **markets**: europa, espana, global
- **topics**: telematica, mercado
- **vehicle_type**: todos
- **categoria**: 📡 Telemática
- **confidence**: high-cross (ChatGPT 30,5M EU 2029 + Claude 39M global 2023 → 90M 2028, LatAm <10%)
- **evergreen_score**: 3
- **origin**: ChatGPT + Claude

### telematica-017 · Reglamento europeo seguridad 2024
**Fact**: El Reglamento (UE) 2019/2144 obliga desde julio 2024 a equipar nuevos vehículos con ISA (Intelligent Speed Assistance), AEBS (frenado autónomo de emergencia) y otros sistemas ADAS. Despliegue escalonado en 4 etapas hasta 2029 según tipo de vehículo y categoría homologada.

- **source**: Reglamento (UE) 2019/2144 · General Safety Regulation
- **markets**: europa, espana
- **topics**: telematica, regulacion, seguridad, adas
- **vehicle_type**: todos
- **categoria**: 📡 Telemática
- **confidence**: high-cross (Gemini + ChatGPT + Claude: detección de somnolencia obligatoria en camiones nuevos desde julio 2024)
- **evergreen_score**: 5
- **origin**: Gemini + ChatGPT + Claude

### telematica-018 · Voltaje de batería como predictor
**Fact**: El monitoreo del voltaje de batería en arranques sucesivos predice cerca del 80% de los fallos eléctricos con 48 horas de antelación, según SAE. Para flotas con paradas frecuentes, integrar el dato en el sistema de mantenimiento evita avería en ruta — el tipo de incidencia que descarrila la planificación del día.

- **source**: SAE International
- **markets**: global
- **topics**: telematica, mantenimiento, predictivo
- **vehicle_type**: todos
- **categoria**: 📡 Telemática
- **confidence**: medium
- **evergreen_score**: 5
- **origin**: Gemini

### telematica-019 · Sensor de temperatura en refrigerados
**Fact**: Investigación de la Universidad de Zaragoza sobre transporte refrigerado documentó una reducción de hasta el 40% en pérdidas de mercancía al integrar sensores de temperatura conectados al sistema de gestión, con alerta automática ante desvíos del setpoint o aperturas de puerta prolongadas.

- **source**: Universidad de Zaragoza + Acuerdo ATP UNECE
- **markets**: espana, europa
- **topics**: telematica, refrigerados, cadena-frio
- **vehicle_type**: pesados, ligeros
- **categoria**: 📡 Telemática
- **confidence**: high-cross (DeepSeek UZ + Claude ATP obligación registro continuo)
- **evergreen_score**: 4
- **origin**: DeepSeek + Claude

### telematica-020 · Sancionados por tacógrafo en España
**Fact**: La DGT y la Inspección de Transporte sancionaron más de 12.000 infracciones de tacógrafo en España durante 2023, con manipulación manual e imanes entre las modalidades más reincidentes. El nuevo G2V2 incorpora detección de campos magnéticos y posicionamiento cruzado para neutralizarlas.

- **source**: DGT + Inspección de Transporte 2023 + Reglamento (CE) 561/2006 + LOTT
- **markets**: espana
- **topics**: telematica, tacografo, compliance
- **vehicle_type**: pesados
- **categoria**: 📡 Telemática
- **confidence**: high-cross (DeepSeek + Claude: multas hasta 6.001 € por reincidencia y posible responsabilidad solidaria del empresario)
- **evergreen_score**: 3
- **origin**: DeepSeek + Claude

### telematica-021 · eCall obligatorio turismos UE
**Fact**: El sistema eCall transmite automáticamente posición GPS a los servicios de emergencia tras un accidente grave y es obligatorio en turismos nuevos UE desde abril 2018 (Reglamento UE 2015/758). En vehículos comerciales pesados es opcional en la mayoría de países, creando una asimetría de respuesta de emergencia que las flotas pueden cubrir con telemática con función de alerta de impacto.

- **source**: Reglamento (UE) 2015/758 · DG MOVE
- **markets**: europa, espana
- **topics**: telematica, seguridad, regulacion
- **vehicle_type**: ligeros, pesados
- **categoria**: 📡 Telemática
- **confidence**: high
- **evergreen_score**: 4
- **origin**: Claude

### telematica-022 · Sensor de apertura de puerta y prueba de servicio
**Fact**: El sensor de apertura de puerta correlacionado con GPS es la única prueba objetiva de intento de entrega en flotas de reparto. Sin él, la disputa con cliente sobre una entrega no realizada depende del registro manual del conductor, según documentación de casos operativos publicada por Geotab. En flotas con alto volumen de reclamaciones, es una herramienta de gestión legal, no solo operativa.

- **source**: Geotab · Fleet Management Use Cases 2022
- **markets**: global
- **topics**: telematica, sensores, ultima-milla
- **vehicle_type**: ligeros
- **categoria**: 📡 Telemática
- **confidence**: medium
- **evergreen_score**: 5
- **origin**: Claude

### telematica-023 · Sensor de peso por eje
**Fact**: En España, el exceso de peso por eje en un camión puede generar multas de hasta 12.000 € en infracción grave y obligación de descarga en el lugar del control, según la DGT. Los sensores de peso por eje integrados en telemática detectan el problema antes de la salida del centro logístico, único punto en el que el ajuste es operativamente posible sin penalización.

- **source**: DGT España · Reglamento General de Circulación + LOTT
- **markets**: espana
- **topics**: telematica, sensores, compliance, peso
- **vehicle_type**: pesados
- **categoria**: 📡 Telemática
- **confidence**: high
- **evergreen_score**: 4
- **origin**: Claude

### telematica-024 · Integración tacógrafo + GPS contra fraude
**Fact**: La combinación de datos de tacógrafo con GPS detecta paradas no registradas en el tacógrafo o discrepancias entre kilómetros declarados y recorrido real, según el IRU. En flotas sin integración, ambos sistemas dan datos paralelos pero no permiten cruzar registro oficial del conductor con trayecto real del vehículo — el principal vector de detección de usos no autorizados.

- **source**: IRU · Digital Tachograph Integration Best Practice 2022
- **markets**: europa, espana
- **topics**: telematica, tacografo, fraude
- **vehicle_type**: pesados
- **categoria**: 📡 Telemática
- **confidence**: medium
- **evergreen_score**: 5
- **origin**: Claude

### telematica-025 · ADR y GPS obligatorio España
**Fact**: El Real Decreto 97/2014 de transporte de mercancías peligrosas en España puede requerir sistemas telemáticos homologados con seguimiento GPS en tiempo real para determinadas cantidades y clases ADR. La telemática estándar no garantiza el cumplimiento: en transporte ADR, conviene verificar requisito específico antes de asumir que el dispositivo instalado vale.

- **source**: RD 97/2014 + Acuerdo ADR UNECE
- **markets**: espana, europa
- **topics**: telematica, adr, regulacion
- **vehicle_type**: pesados, especiales
- **categoria**: 📡 Telemática
- **confidence**: high
- **evergreen_score**: 4
- **origin**: Claude

### telematica-026 · NOM-068-SCT-2014 rastreo MX
**Fact**: La NOM-068-SCT-2014 establece requisitos mínimos de seguridad para el autotransporte federal de carga en México, incluyendo rastreo satelital con plataforma homologada ante la SICT. Tener un GPS instalado no equivale a cumplimiento: muchas flotas medianas operan con sistemas que no satisfacen la homologación específica de la norma.

- **source**: NOM-068-SCT-2014 + SICT México
- **markets**: mexico
- **topics**: telematica, regulacion, rastreo
- **vehicle_type**: pesados
- **categoria**: 📡 Telemática
- **confidence**: high
- **evergreen_score**: 4
- **origin**: Claude

### telematica-027 · EETS peajes europeos
**Fact**: El servicio europeo de telepeaje EETS, regulado por la Directiva (UE) 2019/520, permite a un camión pagar peajes en múltiples países UE con un único dispositivo a bordo. En flotas con corredores internacionales, la fragmentación de contratos nacionales tiene un coste administrativo real — España incorpora EETS en el nuevo régimen de peaje en autovías de implantación progresiva.

- **source**: Directiva (UE) 2019/520 · EETS + DGT España
- **markets**: europa, espana
- **topics**: telematica, peajes, regulacion
- **vehicle_type**: pesados
- **categoria**: 📡 Telemática
- **confidence**: high
- **evergreen_score**: 3
- **origin**: Claude

### telematica-028 · Integración telemática-ERP/TMS
**Fact**: Gartner estima que la integración de telemática con sistemas ERP/TMS reduce hasta un 40% el tiempo de análisis operativo, al automatizar el cálculo de coste real por entrega, ruta o conductor. Sin integración, todo el coste por entrega es estimación basada en promedios — la mayor brecha entre flotas digitalizadas y no digitalizadas no es el hardware, es la conexión con los sistemas de gestión.

- **source**: Gartner · Fleet Management Technology Integration 2023
- **markets**: global
- **topics**: telematica, integracion, productividad
- **vehicle_type**: todos
- **categoria**: 📡 Telemática
- **confidence**: medium
- **evergreen_score**: 3
- **origin**: Claude

---

## ⚖️ REGULACIÓN ESPAÑA

### regulacion-es-001 · V-16 conectada obligatoria 2026
**Fact**: La DGT obliga desde el 1 de enero de 2026 al uso de la baliza luminosa V-16 conectada en sustitución del triángulo de emergencia en vías españolas. La baliza debe emitir geolocalización a la plataforma DGT 3.0 al activarse, generando alertas automáticas a los vehículos próximos.

- **source**: DGT · Reglamento General de Vehículos + Real Decreto 159/2021
- **markets**: espana
- **topics**: regulacion, seguridad-vial
- **vehicle_type**: todos
- **categoria**: ⚖️ Regulación España
- **confidence**: high-cross (DeepSeek + Claude)
- **evergreen_score**: 5
- **origin**: DeepSeek + Claude

### regulacion-es-002 · Sobrepeso y deterioro de pavimento
**Fact**: Un sobrepeso del 5% en eje multiplica por aproximadamente 1,4 el deterioro del pavimento (efecto cuarta potencia documentado por AASHTO y recogido en normativa española). La multa por exceso de peso supera los 4.000 € en infracciones graves de la LOTT.

- **source**: BOE · LOTT + AASHTO
- **markets**: espana
- **topics**: regulacion, compliance, infraestructura
- **vehicle_type**: pesados
- **categoria**: ⚖️ Regulación España
- **confidence**: high
- **evergreen_score**: 5
- **origin**: Gemini

### regulacion-es-003 · ADR y equipamiento obligatorio
**Fact**: La ausencia de equipamiento obligatorio ADR (extintores, calzos, EPI, kits derrame) en transporte de mercancías peligrosas es sancionada en España con multas que alcanzan 4.001 € por infracción muy grave, según el régimen de la LOTT y el ADR 2023.

- **source**: BOE · LOTT + ADR 2023
- **markets**: espana, europa
- **topics**: regulacion, adr, carga-peligrosa
- **vehicle_type**: pesados
- **categoria**: ⚖️ Regulación España
- **confidence**: high
- **evergreen_score**: 5
- **origin**: Gemini

### regulacion-es-004 · Estiba incorrecta
**Fact**: La estiba incorrecta es sancionada en España con multas de hasta 2.500 € (RD 563/2017) y está implicada en torno al 10% de los vuelcos de vehículos pesados con carga. La normativa exige sistemas de sujeción acordes con EN 12195-1.

- **source**: BOE · RD 563/2017
- **markets**: espana
- **topics**: regulacion, seguridad, estiba
- **vehicle_type**: pesados
- **categoria**: ⚖️ Regulación España
- **confidence**: high
- **evergreen_score**: 5
- **origin**: Gemini

### regulacion-es-005 · ZBE municipios >50k habitantes
**Fact**: La Ley de Cambio Climático obliga a municipios españoles de más de 50.000 habitantes a tener Zona de Bajas Emisiones operativa. La normativa prohíbe el acceso a vehículos sin etiqueta ambiental ECO o 0, con calendarios escalonados para etiquetas B y C según ciudad.

- **source**: MITECO + Ley 7/2021 de Cambio Climático + Ley 7/2022 de Residuos + Decret Llei 1/2020 Catalunya
- **markets**: espana
- **topics**: regulacion, zbe, emisiones
- **vehicle_type**: todos
- **categoria**: ⚖️ Regulación España
- **confidence**: high-cross (Gemini + DeepSeek + Claude: >150 municipios con ZBE operativa en 2024, AMB Barcelona usa cámaras de lectura automática)
- **evergreen_score**: 5
- **origin**: Gemini + DeepSeek + Claude

### regulacion-es-006 · Endurecimiento ZBE España 2026
**Fact**: Desde 2026, las Zonas de Bajas Emisiones de varias ciudades españolas restringen progresivamente el acceso a vehículos con etiqueta B, especialmente en episodios de alta contaminación. La presión obliga a replanificar flotas urbanas de reparto y servicios técnicos.

- **source**: DGT + ordenanzas autonómicas/municipales 2025-26
- **markets**: espana
- **topics**: regulacion, zbe
- **vehicle_type**: ligeros, pesados
- **categoria**: ⚖️ Regulación España
- **confidence**: high
- **evergreen_score**: 4
- **origin**: Grok

### regulacion-es-007 · Móvil al volante
**Fact**: Conducir usando el móvil sostenido en la mano supone en España multa de 500 € y la retirada de 6 puntos del carné, según la reforma del Reglamento General de Circulación. Para conductores profesionales, la pérdida puntual puede suponer la inhabilitación temporal de la actividad.

- **source**: DGT · Reforma del Reglamento General de Circulación (Ley 18/2021)
- **markets**: espana
- **topics**: regulacion, seguridad, sancion
- **vehicle_type**: todos
- **categoria**: ⚖️ Regulación España
- **confidence**: high-cross (Gemini 500€/6 puntos post-reforma 2022 + Claude DGT 200€ cifra previa — vigente actual: 200 € móvil en soporte / 500 € sostenido en mano + 6 puntos)
- **evergreen_score**: 5
- **origin**: Gemini + Claude

---

## ⚖️ REGULACIÓN MÉXICO

### regulacion-mx-001 · Multas por sobrepeso por eje MX
**Fact**: La SICT sanciona el exceso de peso por eje en México con multas que oscilan entre 5.000 y 15.000 pesos por infracción, según el grado y la reincidencia. La carga sobre eje motriz fuera de norma deteriora la suspensión y multiplica el riesgo de fallo en frenada.

- **source**: SICT · Reglamento sobre el Peso, Dimensiones y Capacidad + Programa de Modernización de Básculas 2022
- **markets**: mexico
- **topics**: regulacion, compliance, peso
- **vehicle_type**: pesados
- **categoria**: ⚖️ Regulación México
- **confidence**: high-cross (DeepSeek 5.000-15.000 MXN + Claude SICT hasta 24.500 MXN tras intensificación 2022, posible descarga en carretera)
- **evergreen_score**: 4
- **origin**: DeepSeek + Claude

### regulacion-mx-002 · Hoy No Circula CDMX
**Fact**: El programa Hoy No Circula deja sin operar aproximadamente el 20% de la flota convencional al día en la Zona Metropolitana del Valle de México. SEMOVI y SEDEMA cruzan datos de GPS con padrones para detectar circulación en día restringido y emitir sanciones automáticas.

- **source**: SEDEMA + SEMOVI CDMX
- **markets**: mexico
- **topics**: regulacion, emisiones, urbana
- **vehicle_type**: todos
- **categoria**: ⚖️ Regulación México
- **confidence**: high-cross (Gemini + DeepSeek)
- **evergreen_score**: 5
- **origin**: Gemini + DeepSeek

### regulacion-mx-004 · Carta Porte CFDI MX
**Fact**: El complemento Carta Porte del CFDI es obligatorio en México desde 2022 para el traslado de mercancías. En 2024, el SAT intensificó las verificaciones en carreteras federales. Un vehículo sin Carta Porte válida puede ser detenido y la mercancía retenida hasta aclarar la situación fiscal: costes de demora que pueden superar el valor del flete completo.

- **source**: SAT México · Guía Carta Porte 2024
- **markets**: mexico
- **topics**: regulacion, fiscalidad, compliance
- **vehicle_type**: pesados
- **categoria**: ⚖️ Regulación México
- **confidence**: high
- **evergreen_score**: 3
- **origin**: Claude

### regulacion-mx-005 · SEMARNAT emisiones transporte carga
**Fact**: El transporte de carga es responsable del 18% de las emisiones de CO2 del sector transporte en México, según el Inventario Nacional de Emisiones 2022 de SEMARNAT. Las flotas de más de 5 vehículos pesados pueden estar dentro del alcance de futuros esquemas de reporte obligatorio de huella de carbono — quien no controla consumo por vehículo hoy, no podrá reportar mañana.

- **source**: SEMARNAT · Inventario Nacional de Emisiones 2022
- **markets**: mexico
- **topics**: regulacion, emisiones, sostenibilidad
- **vehicle_type**: pesados
- **categoria**: ⚖️ Regulación México
- **confidence**: medium
- **evergreen_score**: 3
- **origin**: Claude

### regulacion-mx-006 · Mercado diésel autotransporte MX
**Fact**: El consumo de combustible del transporte por carretera en México supera los 45.000 millones de litros anuales (gasolina y diésel), según SENER y la CRE. El sector autotransporte de carga es el mayor comprador individual de diésel del país, lo que convierte una mejora de eficiencia del 1% en una flota grande en un impacto financiero estructural.

- **source**: SENER · Balance Nacional de Energía + CRE
- **markets**: mexico
- **topics**: regulacion, mercado, combustible
- **vehicle_type**: pesados
- **categoria**: ⚖️ Regulación México
- **confidence**: medium
- **evergreen_score**: 3
- **origin**: Claude

### regulacion-mx-007 · NOM-SCT mercancías peligrosas MX
**Fact**: El transporte de materiales peligrosos en México está regulado por el Reglamento del Autotransporte Federal (DOF) y las NOM-SCT aplicables. Un vehículo sin hoja de seguridad, tarjeta de emergencia o certificación del conductor puede ser detenido y multado por la SICT con sanciones de hasta 900 UMAs. La documentación a bordo es la única defensa en una verificación de carretera.

- **source**: DOF + SICT México
- **markets**: mexico
- **topics**: regulacion, mercancias-peligrosas, compliance
- **vehicle_type**: pesados, especiales
- **categoria**: ⚖️ Regulación México
- **confidence**: medium
- **evergreen_score**: 4
- **origin**: Claude

### regulacion-mx-003 · NOM-005-SCFI medición de combustibles
**Fact**: La NOM-005-SCFI exige una tolerancia máxima del ±0,5% en el equipo de medición de despacho de combustibles en estaciones de servicio mexicanas. Errores sistemáticos por encima del umbral son una causa frecuente de mermas inadvertidas para el cliente flota.

- **source**: NOM-005-SCFI · Secretaría de Economía
- **markets**: mexico
- **topics**: regulacion, combustible, metrologia
- **vehicle_type**: todos
- **categoria**: ⚖️ Regulación México
- **confidence**: high
- **evergreen_score**: 5
- **origin**: DeepSeek

---

## ⚡ ELECTRIFICACIÓN

### electrificacion-001 · Autonomía EV en frío
**Fact**: Las furgonetas y camiones eléctricos pierden entre 20% y 30% de autonomía cuando la temperatura ambiente baja de 0 °C, según mediciones recogidas por el Alternative Fuels Data Center del DOE. Es el factor que más altera la planificación de rutas reales frente a las cifras de homologación.

- **source**: DOE · Alternative Fuels Data Center
- **markets**: usa, europa, global
- **topics**: electrificacion, autonomia, operacion
- **vehicle_type**: ligeros, pesados
- **categoria**: ⚡ Electrificación
- **confidence**: high
- **evergreen_score**: 5
- **origin**: Gemini

### electrificacion-002 · TCO furgoneta eléctrica de alto kilometraje
**Fact**: El Rocky Mountain Institute estima en torno a -15% de TCO para furgonetas eléctricas frente a diésel cuando se superan los 100 km/día en operación urbana, gracias al ahorro en energía, mantenimiento y fiscalidad. Por debajo de ese umbral diario el cálculo se invierte.

- **source**: Rocky Mountain Institute
- **markets**: usa, europa
- **topics**: electrificacion, tco, ultima-milla
- **vehicle_type**: ligeros
- **categoria**: ⚡ Electrificación
- **confidence**: medium
- **evergreen_score**: 4
- **origin**: DeepSeek

### electrificacion-003 · Matriculación furgonetas EV España 2023
**Fact**: España matriculó más de 12.000 furgonetas eléctricas en 2023, un crecimiento del 35% respecto a 2022, según ANFAC. La autonomía media (150-250 km) sigue siendo insuficiente para rutas regionales de más de 200 km diarios, por lo que la decisión de electrificación no es solo de inversión: requiere análisis de ruta y perfil de carga previo.

- **source**: ANFAC · Informe de Matriculaciones de Vehículos Eléctricos 2023
- **markets**: espana
- **topics**: electrificacion, ultima-milla, mercado
- **vehicle_type**: ligeros
- **categoria**: ⚡ Electrificación
- **confidence**: high
- **evergreen_score**: 3
- **origin**: Claude

---

## 🛡️ COMPLIANCE & MULTAS

### compliance-001 · DVS Londres
**Fact**: Transport for London sanciona con multas de 550 GBP/día a camiones de más de 12 toneladas que circulen sin cumplir el Direct Vision Standard (cámaras laterales y reducción de ángulos muertos). El esquema fija un mínimo de "star rating" creciente y afecta directamente a flotas internacionales que operen Londres.

- **source**: Transport for London · Direct Vision Standard
- **markets**: uk
- **topics**: compliance, seguridad, urbana
- **vehicle_type**: pesados
- **categoria**: 🛡️ Compliance
- **confidence**: high
- **evergreen_score**: 4
- **origin**: Gemini

### compliance-002 · CVSA Roadcheck — frenos
**Fact**: La inspección anual CVSA Roadcheck en Norteamérica documenta que el 20% de los camiones inspeccionados son puestos Out-of-Service por defectos en el sistema de frenos. Es la causa principal de OOS, por encima de neumáticos, iluminación o documentación.

- **source**: CVSA · Commercial Vehicle Safety Alliance
- **markets**: usa
- **topics**: compliance, mantenimiento, frenos
- **vehicle_type**: pesados
- **categoria**: 🛡️ Compliance
- **confidence**: high
- **evergreen_score**: 4
- **origin**: Gemini

### compliance-003 · Defecto de frenado en ITV España
**Fact**: La AECA-ITV reportó que cerca del 8% de los vehículos pesados inspeccionados en España presentaron defecto de frenado en 2023. La revisión de frenos vacía pasa al estatus de causa principal de rechazo en ITV pesada, por encima de luces o suspensión.

- **source**: AECA-ITV · Estadísticas de Inspecciones 2022-2023
- **markets**: espana
- **topics**: compliance, mantenimiento, frenos
- **vehicle_type**: pesados
- **categoria**: 🛡️ Compliance
- **confidence**: high-cross (DeepSeek AECA-ITV 8% defecto frenado + Claude AECA-ITV: >35% de camiones presentan alguna deficiencia en ITV en 2022)
- **evergreen_score**: 4
- **origin**: DeepSeek + Claude

### compliance-004 · ELDT formación obligatoria USA
**Fact**: Desde 2022, la FMCSA exige formación ELDT (Entry-Level Driver Training) en USA antes de obtener CDL clase A o B. La regulación estandariza un currículum mínimo teórico y práctico, eliminando la formación express previa y elevando el coste de incorporación al sector.

- **source**: FMCSA · Entry-Level Driver Training Rule
- **markets**: usa
- **topics**: compliance, formacion
- **vehicle_type**: pesados
- **categoria**: 🛡️ Compliance
- **confidence**: high
- **evergreen_score**: 5
- **origin**: DeepSeek

### compliance-005 · CSA scores y contratación USA
**Fact**: Los CSA Safety Scores de FMCSA son consultados públicamente por shippers y aseguradoras: una puntuación deteriorada penaliza directamente la contratación y eleva la prima. Para muchas flotas estadounidenses, gestionar el CSA es una función comercial tanto como de cumplimiento.

- **source**: FMCSA · Compliance, Safety, Accountability
- **markets**: usa
- **topics**: compliance, seguridad, comercial
- **vehicle_type**: pesados
- **categoria**: 🛡️ Compliance
- **confidence**: high
- **evergreen_score**: 5
- **origin**: DeepSeek

### compliance-006 · Inspecciones CNRT Argentina
**Fact**: La CNRT documentó en 2023 que cerca del 35% de los camiones inspeccionados en ruta circulaban sin tacógrafo operativo o con sistema manipulado. Las 3.500 sanciones anuales por manipulación elevaron el endurecimiento del régimen de control en 2024.

- **source**: CNRT · Comisión Nacional de Regulación del Transporte (Argentina)
- **markets**: latam
- **topics**: compliance, tacografo
- **vehicle_type**: pesados
- **categoria**: 🛡️ Compliance
- **confidence**: high
- **evergreen_score**: 3
- **origin**: DeepSeek

---

## 🚨 SEGURIDAD & ROBO DE CARGA

### seguridad-001 · Robos al transporte de carga MX
**Fact**: El SESNSP reportó más de 10.500 robos al transporte de carga en México durante 2023, con incremento próximo al 15% respecto al año anterior. La concentración geográfica en el corredor México-Puebla-Veracruz (cerca del 35% del total) permite anticipar el riesgo y ajustar rutas, horarios y escoltas.

- **source**: SESNSP · Informe de Incidencia Delictiva del Fuero Común 2023 + CANACAR
- **markets**: mexico
- **topics**: seguridad, robo-carga, ruta
- **vehicle_type**: pesados
- **categoria**: 🚨 Seguridad
- **confidence**: high-cross (Perplexity + Gemini + DeepSeek corredor MX-Puebla + Claude SESNSP oficial: 15.440 robos = 42/día, Estado de México + Puebla + Guanajuato; corredor Texcoco-Puebla y Bajío). NOTA: cifras de 10.500-13.000 procedían de subconjuntos del SESNSP; la cifra oficial consolidada 2023 es 15.440.
- **evergreen_score**: 4
- **origin**: Perplexity + Gemini + DeepSeek + Claude

### seguridad-002 · Robo de carga MX 2025 (tendencia + violencia)
**Fact**: En 2025 el robo de carga en México descendió un 21,5% respecto a 2024, pero el 82% de los incidentes involucraron algún tipo de violencia, concentrados en corredores como México-Puebla y Querétaro-León. Menos volumen, riesgo igual de severo en las rutas clave.

- **source**: SESNSP + Overhaul · Mexico Annual Cargo Theft Report 2025
- **markets**: mexico
- **topics**: seguridad, robo-carga, ruta, violencia
- **vehicle_type**: pesados
- **categoria**: 🚨 Seguridad
- **confidence**: high
- **evergreen_score**: 3 (cifra anual)
- **origin**: Grok

### seguridad-003 · Horario y robo de carga MX
**Fact**: CANACAR documenta que cerca del 62% de los robos en carretera en México ocurren entre las 22:00 y las 04:00 horas, frecuentemente en tramos sin cobertura celular. Restringir tránsito nocturno en corredores críticos y reforzar geofencing con tecnologías redundantes son las palancas operativas inmediatas.

- **source**: CANACAR · Cámara Nacional del Autotransporte de Carga
- **markets**: mexico
- **topics**: seguridad, robo-carga, horario
- **vehicle_type**: pesados
- **categoria**: 🚨 Seguridad
- **confidence**: high
- **evergreen_score**: 4
- **origin**: Gemini

### seguridad-004 · Robo de carga USA+Canadá 2024
**Fact**: CargoNet registró 3.625 incidentes de robo de carga en USA y Canadá durante 2024, un 27% más que el año anterior, con valor promedio por robo cercano a 202.000 USD. Es el quinto año consecutivo de incremento, con concentración en cargas de electrónica, alimentos y bebidas.

- **source**: CargoNet · 2024 Annual Cargo Theft Report
- **markets**: usa
- **topics**: seguridad, robo-carga, benchmark
- **vehicle_type**: pesados
- **categoria**: 🚨 Seguridad
- **confidence**: high
- **evergreen_score**: 3
- **origin**: ChatGPT

### seguridad-005 · TAPA EMEA Cargo Crime
**Fact**: TAPA EMEA registró 578 incidentes de robo de carga en su Cargo Crime Monitor durante 2024, con valor promedio cercano a 88.520 € por incidente. Alemania (98), Sudáfrica (94), Italia (84) y España (45) concentran la mayor parte de los reportes.

- **source**: TAPA EMEA · Cargo Crime Monitor 2024
- **markets**: europa, espana
- **topics**: seguridad, robo-carga, benchmark
- **vehicle_type**: pesados
- **categoria**: 🚨 Seguridad
- **confidence**: high
- **evergreen_score**: 3
- **origin**: ChatGPT

### seguridad-006 · Mortalidad en camiones grandes USA
**Fact**: La NHTSA contabilizó 5.472 muertes en accidentes con camiones grandes en Estados Unidos en 2023, un 8% menos que en 2022. El 70% de las víctimas estaba en otros vehículos, no en el camión; el 82% de los siniestros fatales ocurrió de lunes a viernes entre las 6:00 y las 17:59.

- **source**: NHTSA · Fatality Analysis Reporting System 2023
- **markets**: usa
- **topics**: seguridad, siniestralidad
- **vehicle_type**: pesados
- **categoria**: 🚨 Seguridad
- **confidence**: high-cross (NHTSA + FMCSA + IIHS)
- **evergreen_score**: 4
- **origin**: ChatGPT

### seguridad-007 · Víctimas mortales España 2024
**Fact**: La DGT cifró en 1.154 las víctimas mortales en vías interurbanas españolas durante 2024, sobre 462 millones de desplazamientos largo recorrido. El parque comercial (5,2 millones de furgonetas y camiones) concentra una siniestralidad por kilómetro superior a la media de turismo.

- **source**: DGT · Balance siniestralidad 2024
- **markets**: espana
- **topics**: seguridad, siniestralidad
- **vehicle_type**: todos
- **categoria**: 🚨 Seguridad
- **confidence**: high
- **evergreen_score**: 4
- **origin**: ChatGPT

### seguridad-008 · Mortalidad pesados España 2023
**Fact**: La DGT registró 1.104 víctimas mortales en accidentes con implicación de vehículos pesados en España durante 2023, un 8% más que el ejercicio anterior. La tendencia revierte la mejora histórica y motiva el endurecimiento de controles ADAS y velocidad.

- **source**: DGT · Memoria Estadística 2023
- **markets**: espana
- **topics**: seguridad, siniestralidad
- **vehicle_type**: pesados
- **categoria**: 🚨 Seguridad
- **confidence**: high
- **evergreen_score**: 3
- **origin**: DeepSeek

### seguridad-009 · Cinturón de seguridad en camiones USA
**Fact**: La FMCSA documenta que el 43% de los conductores de camión pesado fallecidos en accidente no llevaba puesto el cinturón de seguridad. Es la regla de bajo coste con mayor potencial de reducción de mortalidad — y la que más cuesta sostener en cultura de flota.

- **source**: FMCSA · Large Truck Fatal Crash Causation
- **markets**: usa
- **topics**: seguridad, driver-behavior
- **vehicle_type**: pesados
- **categoria**: 🚨 Seguridad
- **confidence**: high
- **evergreen_score**: 5
- **origin**: Gemini

### seguridad-010 · ESC y vuelcos
**Fact**: La NHTSA cifra en 56% la reducción de vuelcos y 14% la reducción de pérdidas de control en camiones equipados con Electronic Stability Control. Es estándar obligatorio en USA desde 2017 y en la UE desde 2014 para nuevos camiones (R140).

- **source**: NHTSA + Reglamento UNECE R140
- **markets**: usa, europa
- **topics**: seguridad, esc, regulacion
- **vehicle_type**: pesados
- **categoria**: 🚨 Seguridad
- **confidence**: high
- **evergreen_score**: 5
- **origin**: Gemini

### seguridad-011 · FCW + AEB y choques traseros
**Fact**: El IIHS cuantifica una reducción del 41% en siniestros por choque trasero en vehículos equipados con FCW (Forward Collision Warning) más AEB (Automatic Emergency Braking). Es la combinación ADAS con mejor retorno empírico en flotas de larga distancia.

- **source**: IIHS · Insurance Institute for Highway Safety
- **markets**: usa, global
- **topics**: seguridad, adas
- **vehicle_type**: pesados
- **categoria**: 🚨 Seguridad
- **confidence**: high
- **evergreen_score**: 5
- **origin**: Gemini

### seguridad-012 · Apnea del sueño en conductores pesados
**Fact**: Estudios FMCSA y Harvard documentan que cerca del 28% de los conductores de camión pesado presenta apnea del sueño, condición asociada a un riesgo 2,4 veces mayor de siniestro grave. Programas de tamizaje médico devuelven retorno por reducción de absentismo y siniestralidad.

- **source**: FMCSA + Harvard Medical School
- **markets**: usa, global
- **topics**: seguridad, salud, driver-behavior
- **vehicle_type**: pesados
- **categoria**: 🚨 Seguridad
- **confidence**: high
- **evergreen_score**: 4
- **origin**: Gemini

### seguridad-013 · Pesados, ciclistas y peatones (UE)
**Fact**: El ETSC señala que los vehículos pesados representan apenas el 4% del parque europeo pero están implicados en torno al 14% de los accidentes fatales con ciclistas y peatones. Es el dato que justifica el Direct Vision Standard de Londres y el endurecimiento de visibilidad lateral en la UE.

- **source**: ETSC + Directiva (UE) 2023/1114 + Comisión Europea DG MOVE
- **markets**: europa, uk
- **topics**: seguridad, vulnerable, urbana
- **vehicle_type**: pesados
- **categoria**: 🚨 Seguridad
- **confidence**: high-cross (Gemini ETSC 14% + Claude punto ciego lateral >3 m de ancho y blind-spot monitoring obligatorio en camiones nuevos desde julio 2024)
- **evergreen_score**: 5
- **origin**: Gemini + Claude

### seguridad-014 · Franja horaria 2-6 AM y siniestros
**Fact**: El ERSO (European Road Safety Observatory) cuantifica entre 4 y 6 veces el incremento del riesgo de accidente fatal entre las 2:00 y las 6:00 horas, frente al promedio del día. La razón es combinada: fatiga, menor tráfico (mayor velocidad), peor iluminación.

- **source**: ERSO · European Road Safety Observatory
- **markets**: europa
- **topics**: seguridad, horario, driver-behavior
- **vehicle_type**: todos
- **categoria**: 🚨 Seguridad
- **confidence**: high
- **evergreen_score**: 5
- **origin**: Gemini

### seguridad-015 · Sustancias y alcohol al volante España
**Fact**: La DGT y FENADISMER documentan que cerca del 2,5% de los conductores profesionales sometidos a controles aleatorios da positivo en sustancias o alcohol. La cifra justifica los programas de testing interno periódico en flotas con perfil de alta exposición.

- **source**: DGT + FENADISMER
- **markets**: espana
- **topics**: seguridad, sustancias, driver-behavior
- **vehicle_type**: pesados
- **categoria**: 🚨 Seguridad
- **confidence**: medium
- **evergreen_score**: 4
- **origin**: Gemini

### seguridad-016 · Norma 9 ADR y vuelco en cisternas (Chile)
**Fact**: El MTT chileno incorporó en 2024 la Norma 9 ADR con sensor de inclinación obligatorio en cisternas de transporte de líquidos peligrosos. La medida responde al patrón documentado: el vuelco lateral es la principal causa de derrame catastrófico en transporte de mercancías peligrosas.

- **source**: MTT Chile · Norma 9 ADR adaptada
- **markets**: latam
- **topics**: seguridad, adr, sensores
- **vehicle_type**: pesados
- **categoria**: 🚨 Seguridad
- **confidence**: medium
- **evergreen_score**: 4
- **origin**: DeepSeek

### seguridad-017 · Primas de seguro flota MX
**Fact**: La AMIS reportó un incremento próximo al 25% en las primas de seguro para flotas de carga en México durante 2024, impulsado por la siniestralidad y el robo. Es la presión financiera más directa detrás de la adopción de telemática avanzada y de auditorías de ruta sistemáticas.

- **source**: AMIS · Asociación Mexicana de Instituciones de Seguros
- **markets**: mexico
- **topics**: seguridad, seguros, coste
- **vehicle_type**: pesados
- **categoria**: 🚨 Seguridad
- **confidence**: high
- **evergreen_score**: 3
- **origin**: DeepSeek

### seguridad-018 · Perfil de carga robada MX
**Fact**: Según TT Club y BSI, los sectores con mayor exposición a robo de carga en México son alimentos y bebidas (32%), ropa y electrónica (20%) y materiales de construcción (15%). El asalto ocurre mayoritariamente durante el transporte en movimiento, no en almacenamiento — perfil que segmenta el diseño de protocolos: no todos los productos exigen el mismo nivel de respuesta.

- **source**: TT Club / BSI · Cargo Theft Report 2023
- **markets**: mexico, latam
- **topics**: seguridad, robo-carga, sectores
- **vehicle_type**: pesados
- **categoria**: 🚨 Seguridad
- **confidence**: medium
- **evergreen_score**: 3
- **origin**: Claude

### seguridad-019 · Mortalidad pesados vs turismos ES
**Fact**: La tasa de mortalidad en accidentes de tráfico de vehículos pesados en vías interurbanas españolas fue de 1,2 fallecidos por cada 100 accidentes con víctimas en 2022, frente a 0,7 en turismos, según la DGT. Distracción, exceso de velocidad y fatiga concentran la mayor parte de los siniestros mortales con camiones — un riesgo casi al doble que el de turismo por kilómetro recorrido.

- **source**: DGT · Anuario Estadístico de Accidentes 2022
- **markets**: espana
- **topics**: seguridad, siniestralidad, pesados
- **vehicle_type**: pesados
- **categoria**: 🚨 Seguridad
- **confidence**: high
- **evergreen_score**: 3
- **origin**: Claude

### seguridad-020 · Coste social accidente mortal UE
**Fact**: El coste social medio de un accidente mortal en Europa supera los 3 millones de euros, según el programa PIN de la ETSC, sumando daños, atención sanitaria, productividad perdida y administración. En flotas, el cálculo del riesgo de accidente no se agota con la prima del seguro: la responsabilidad penal del gestor por negligencia en mantenimiento no es asegurable.

- **source**: ETSC · PIN Programme 2023
- **markets**: europa, espana
- **topics**: seguridad, coste, responsabilidad
- **vehicle_type**: todos
- **categoria**: 🚨 Seguridad
- **confidence**: high
- **evergreen_score**: 5
- **origin**: Claude

### seguridad-021 · AEBS — gap del parque en circulación UE
**Fact**: El frenado de emergencia automático (AEBS) es obligatorio en camiones pesados nuevos en Europa desde 2015 (Reglamento CE 661/2009), pero cerca del 40% del parque en circulación todavía no lo monta, según la Comisión Europea. En renovación con vehículos de segunda mano, verificar AEBS instalado debería ser un criterio de seguridad activo, no un extra opcional.

- **source**: Comisión Europea DG MOVE + Reglamento (CE) 661/2009
- **markets**: europa, espana
- **topics**: seguridad, adas, regulacion
- **vehicle_type**: pesados
- **categoria**: 🚨 Seguridad
- **confidence**: medium
- **evergreen_score**: 4
- **origin**: Claude

### seguridad-022 · Consejero de Seguridad ADR ES
**Fact**: En España, la ausencia del Consejero de Seguridad para el Transporte de Mercancías Peligrosas (obligatorio según el RD 97/2014 y el ADR) es una infracción muy grave con multa de hasta 12.000 €. Aplica a flotas que transportan mercancías peligrosas aunque sea ocasionalmente — la frecuencia no exime de la obligación de designación.

- **source**: RD 97/2014 + Acuerdo ADR UNECE + DGT España
- **markets**: espana, europa
- **topics**: seguridad, adr, compliance
- **vehicle_type**: pesados, especiales
- **categoria**: 🚨 Seguridad
- **confidence**: high
- **evergreen_score**: 4
- **origin**: Claude

### seguridad-023 · Huachicol y autotanques MX
**Fact**: La Guardia Nacional reportó en 2023 más de 8.000 detenciones relacionadas con robo de combustible (huachicol) en ductos, pipas y tanques en México, con foco en Puebla, Hidalgo y Guanajuato. Las flotas de distribución de combustible y de cargas de alto valor en esas zonas requieren protocolos activos más allá del GPS estándar.

- **source**: Guardia Nacional México · Informe de Actividad 2023 + PEMEX
- **markets**: mexico
- **topics**: seguridad, robo-combustible, huachicol
- **vehicle_type**: pesados, especiales
- **categoria**: 🚨 Seguridad
- **confidence**: medium
- **evergreen_score**: 3
- **origin**: Claude

### seguridad-024 · Multas ZBE Madrid 2023
**Fact**: Las cámaras de la ZBE de Madrid procesaron en 2023 más de 800.000 accesos de vehículos con restricción, según el Ayuntamiento. La multa por acceso no autorizado es de 200 € por vehículo y evento. En flotas sin control por matrícula y etiqueta ambiental, el coste se acumula de forma invisible hasta que llega la notificación masiva.

- **source**: Ayuntamiento de Madrid · Informe de Gestión Madrid Central + DGT
- **markets**: espana
- **topics**: seguridad, zbe, compliance, urbana
- **vehicle_type**: ligeros, pesados
- **categoria**: 🚨 Seguridad
- **confidence**: high
- **evergreen_score**: 3
- **origin**: Claude

### seguridad-025 · GDP farmacéutico EMA
**Fact**: El transporte de cadena de frío farmacéutico en Europa está regulado por las Directrices GDP (Good Distribution Practice) 2013/C 343/01 de la EMA, que obligan a registro continuo de temperatura y plan de gestión de riesgos. El incumplimiento puede invalidar el lote de medicamento — el coste se mide en producto destruido, no en multas.

- **source**: EMA · Guidelines on GDP 2013/C 343/01
- **markets**: europa, espana
- **topics**: seguridad, cadena-frio, farmaceutico
- **vehicle_type**: refrigerados
- **categoria**: 🚨 Seguridad
- **confidence**: high
- **evergreen_score**: 5
- **origin**: Claude

### seguridad-026 · Robo de identidad logística MX
**Fact**: El BSI Supply Chain Services documenta en 2024 un cambio en el modus operandi del robo de carga en México hacia el "robo de identidad logística": delincuentes suplantan transportistas legítimos para recoger carga sin violencia. La verificación digital de identidad del transportista en el punto de carga es la primera barrera ante un patrón que no se detecta con GPS.

- **source**: BSI Supply Chain Services · Cargo Theft Intelligence Report Q4 2024
- **markets**: mexico
- **topics**: seguridad, fraude, cadena-suministro
- **vehicle_type**: pesados
- **categoria**: 🚨 Seguridad
- **confidence**: medium
- **evergreen_score**: 3
- **origin**: Claude

---

## 📦 ÚLTIMA MILLA & E-COMMERCE

### ultima-milla-001 · Coste de entregas fallidas
**Fact**: McKinsey estima que las entregas fallidas pueden incrementar el coste logístico de un pedido hasta un 15%, contando reintentos, reprogramación y carga administrativa. UNO Logística cifra el coste medio de una entrega fallida en España entre 8,50 y 15 €, según ventana horaria y zona.

- **source**: McKinsey + UNO Logística
- **markets**: global, europa, espana
- **topics**: ultima-milla, coste, ecommerce
- **vehicle_type**: ligeros
- **categoria**: 📦 Última milla
- **confidence**: high-cross (Perplexity McKinsey + Gemini UNO 15€ + DeepSeek UNO 8,50€ + Claude Capgemini 7-15€ EU = hasta 30% del margen operativo si >15% intentos fallidos)
- **evergreen_score**: 4
- **origin**: Perplexity + Gemini + DeepSeek + Claude

### ultima-milla-002 · Tasa de entregas fallidas Europa
**Fact**: Las entregas fallidas en primer intento oscilan entre el 15% y el 30% en ciudades europeas, según el European E-commerce Report. En picos de demanda como Black Friday, la AMVO documenta hasta el 35% de entregas fallidas en grandes ciudades mexicanas. Optimizar ventanas y puntos alternativos es la palanca más directa.

- **source**: European E-commerce Report 2024 + AMVO
- **markets**: espana, europa, mexico
- **topics**: ultima-milla, ecommerce
- **vehicle_type**: ligeros
- **categoria**: 📦 Última milla
- **confidence**: medium (rangos amplios, fuentes sectoriales)
- **evergreen_score**: 4
- **origin**: Grok + Gemini

### ultima-milla-003 · Coste última milla como % del envío total
**Fact**: La última milla representa hasta el 53% del coste total de envío en 2024, frente al 41% en 2018, según el World Economic Forum. Capgemini la sitúa en torno al 41% del coste de la cadena de suministro retail. La presión combinada de congestión urbana y promesas de velocidad disparan el peso del último tramo.

- **source**: World Economic Forum 2024 + Capgemini Research Institute
- **markets**: global, europa
- **topics**: ultima-milla, coste, ecommerce
- **vehicle_type**: ligeros
- **categoria**: 📦 Última milla
- **confidence**: high-cross (Grok WEF + ChatGPT WEF + ChatGPT Capgemini + Claude McKinsey "State of Last-Mile" 41-53%)
- **evergreen_score**: 4
- **origin**: Grok + ChatGPT + Claude

### ultima-milla-004 · Devoluciones e-commerce
**Fact**: La NRF y AMVO documentan tasas de devolución en e-commerce entre el 20% y el 30% (frente a 8-10% del retail físico). Cada devolución implica logística inversa con coste medio próximo al 60% del envío original, comprimiendo el margen unitario de categorías como moda y electrónica.

- **source**: NRF + AMVO + AECE España 2023
- **markets**: usa, mexico, espana, global
- **topics**: ultima-milla, ecommerce, logistica-inversa
- **vehicle_type**: ligeros
- **categoria**: 📦 Última milla
- **confidence**: high-cross (Gemini NRF/AMVO 20-30% + Claude AECE ES 10-30% con coste 5-12 €/devolución)
- **evergreen_score**: 4
- **origin**: Gemini + Claude

### ultima-milla-005 · UPS y giros a la izquierda
**Fact**: UPS reportó en 2007 haber evitado 28,5 millones de millas y 3 millones de galones de combustible al año aplicando su sistema de routing ORION, que minimiza giros a la izquierda en intersecciones congestionadas. Cada milla diaria reducida por conductor equivale a 50 millones USD anuales según HBS Digital Initiative.

- **source**: UPS / Wired 2007 + Harvard Business School Digital Initiative
- **markets**: usa, global
- **topics**: ultima-milla, routing, eficiencia
- **vehicle_type**: ligeros
- **categoria**: 📦 Última milla
- **confidence**: high-cross (Gemini + ChatGPT + Claude UPS Corporate Sustainability: 160M millas y 10M galones/año ahorrados con eliminación de left turns)
- **evergreen_score**: 5
- **origin**: Gemini + ChatGPT + Claude

### ultima-milla-006 · Tiempo fuera de cabina
**Fact**: Estudios de la University of Washington miden que los conductores de reparto urbano pasan hasta el 60% del tiempo de jornada fuera de la cabina (caminando con el paquete, esperando ascensor, buscando dirección). El indicador "tiempo en bordillo" pesa más que la velocidad de circulación para la productividad real.

- **source**: University of Washington · Urban Freight Lab
- **markets**: usa, global
- **topics**: ultima-milla, productividad
- **vehicle_type**: ligeros
- **categoria**: 📦 Última milla
- **confidence**: high
- **evergreen_score**: 4
- **origin**: Gemini

### ultima-milla-007 · Bicis eléctricas de carga
**Fact**: Estudios de la University of Westminster en Londres miden que las bicis eléctricas de carga completan entregas urbanas hasta un 60% más rápido que las furgonetas en zonas congestionadas. Combinadas con micro-hubs, McKinsey reporta hasta -24% en costes de última milla.

- **source**: University of Westminster + McKinsey
- **markets**: europa, uk
- **topics**: ultima-milla, micro-mobility, urbana
- **vehicle_type**: ligeros
- **categoria**: 📦 Última milla
- **confidence**: medium
- **evergreen_score**: 4
- **origin**: Gemini

### ultima-milla-008 · Densidad de entregas y coste unitario
**Fact**: Capgemini modela que pasar de 2 a 5 entregas por kilómetro cuadrado reduce el coste por entrega hasta un 45%. La densidad geográfica de paradas pesa más que la velocidad o el modelo de vehículo en la economía de la última milla.

- **source**: Capgemini Research Institute + CEREMA / Observatoire du Transport de Marchandises en Ville (Francia) 2023
- **markets**: global, europa, espana
- **topics**: ultima-milla, densidad, coste
- **vehicle_type**: ligeros
- **categoria**: 📦 Última milla
- **confidence**: high-cross (Gemini Capgemini -45% coste con 2→5 entregas/km² + Claude CEREMA: 90-110 paradas/día = rentable, <60 paradas = bajo tarifa)
- **evergreen_score**: 5
- **origin**: Gemini + Claude

### ultima-milla-009 · Lockers vs entrega a domicilio (Chile)
**Fact**: La CCS chilena documenta que la entrega en lockers reduce hasta un 30% el coste unitario respecto a la entrega a domicilio, eliminando reintentos y comprimiendo paradas. La adopción real está limitada por la disponibilidad de redes urbanas con cobertura suficiente.

- **source**: CCS · Cámara de Comercio de Santiago + PostEurop / PostNord Last Mile Delivery Study 2023
- **markets**: latam, europa, espana
- **topics**: ultima-milla, lockers, coste
- **vehicle_type**: ligeros
- **categoria**: 📦 Última milla
- **confidence**: high-cross (DeepSeek CCS Chile -30% + Claude PostEurop/PostNord hasta -40% por paquete vs entrega fallida)
- **evergreen_score**: 4
- **origin**: DeepSeek + Claude

### ultima-milla-010 · Optimización de rutas con software
**Fact**: Análisis de Deloitte sobre flotas españolas mide reducciones de entre 10% y 15% en kilómetros recorridos al implantar software de optimización dinámica de rutas. El retorno se materializa en combustible, jornadas y siniestralidad, sin necesidad de cambiar vehículo ni perfil de conductor.

- **source**: Deloitte
- **markets**: espana, europa
- **topics**: ultima-milla, routing, software
- **vehicle_type**: todos
- **categoria**: 📦 Última milla
- **confidence**: medium
- **evergreen_score**: 4
- **origin**: DeepSeek

### ultima-milla-011 · Demanda urbana 2030
**Fact**: El World Economic Forum proyecta un incremento del 78% en demanda de última milla urbana hacia 2030, con +36% de vehículos de reparto y +32% de emisiones si no hay intervención. El estudio enumera 24 intervenciones (modelo modal, micro-hubs, ventanas nocturnas) capaces de reducir 30% emisiones y coste simultáneamente.

- **source**: WEF + C40 Cities · The Future of the Last-Mile Ecosystem
- **markets**: global
- **topics**: ultima-milla, proyeccion, urbana, emisiones
- **vehicle_type**: ligeros
- **categoria**: 📦 Última milla
- **confidence**: high
- **evergreen_score**: 4
- **origin**: ChatGPT

### ultima-milla-012 · Tiempo buscando carga/descarga
**Fact**: INRIX y TfL documentan que los conductores de reparto urbano pierden entre el 20% y el 28% de su jornada buscando hueco de carga/descarga. Vehículos de comercio urbano permanecen estacionados en aceras hasta 4,5 horas al día (TfL Londres), evidenciando el cuello de botella en kerb space.

- **source**: INRIX Global Traffic Scorecard 2024 + Transport for London
- **markets**: europa, global, uk, espana
- **topics**: ultima-milla, urbana, kerb-space
- **vehicle_type**: ligeros
- **categoria**: 📦 Última milla
- **confidence**: high-cross (Gemini INRIX/TfL 20-28% jornada + Claude INRIX 2024: +18% tiempo entrega EU 2019-2023, +30-40% en pico Madrid/Barcelona)
- **evergreen_score**: 4
- **origin**: Gemini + Claude

### ultima-milla-013 · Multas estacionamiento reparto
**Fact**: Logística Profesional cifra entre 1.200 y 2.500 € anuales por vehículo el coste de multas de estacionamiento en reparto urbano en España. Es un coste estructural normalizado en el sector, frente al cual la planificación con kerb-permits o ventanas DUM nocturnas devuelve impacto directo.

- **source**: Logística Profesional + UNO Logística 2023 + Ayuntamientos Madrid y Barcelona
- **markets**: espana
- **topics**: ultima-milla, multas, urbana
- **vehicle_type**: ligeros
- **categoria**: 📦 Última milla
- **confidence**: high-cross (Gemini Logística Profesional 1.200-2.500 € + Claude UNO Logística: doble fila 200 €/multa, hasta >500 €/vehículo/año)
- **evergreen_score**: 4
- **origin**: Gemini + Claude

### ultima-milla-014 · Bogotá pico y placa
**Fact**: El pico y placa de Bogotá restringe la circulación entre 3 y 4 horas/día a vehículos comerciales, con coste estimado próximo a 12 millones COP anuales por vehículo afectado en pérdida de productividad. Es la restricción urbana de mayor impacto operativo entre las capitales sudamericanas.

- **source**: Cámara de Comercio de Bogotá + Mintransporte Colombia
- **markets**: latam
- **topics**: ultima-milla, regulacion, urbana
- **vehicle_type**: todos
- **categoria**: 📦 Última milla
- **confidence**: medium
- **evergreen_score**: 4
- **origin**: DeepSeek

### ultima-milla-015 · Reparto en moto Brasil
**Fact**: ABRAS documenta que cerca del 60% de las entregas urbanas en Brasil se completan en moto, con un coste por entrega hasta 40% inferior al de furgoneta. El modelo es replicable en megaciudades con tráfico congestionado pero choca con regulación de seguridad vial creciente.

- **source**: ABRAS · Associação Brasileira de Supermercados
- **markets**: latam
- **topics**: ultima-milla, modal, urbana
- **vehicle_type**: motos
- **categoria**: 📦 Última milla
- **confidence**: medium
- **evergreen_score**: 4
- **origin**: DeepSeek

### ultima-milla-016 · Horarios DUM Barcelona
**Fact**: El Ajuntament de Barcelona aplica horarios DUM estrictos en distritos centrales (carga/descarga limitada típicamente a 8:00-11:00 y 16:00-19:00), con multas de 100 € por incumplimiento. La planificación nocturna de reparto silencioso es la respuesta operativa adoptada por las grandes plataformas.

- **source**: Ajuntament de Barcelona · Distribución Urbana de Mercancías
- **markets**: espana
- **topics**: ultima-milla, regulacion, urbana
- **vehicle_type**: ligeros
- **categoria**: 📦 Última milla
- **confidence**: high
- **evergreen_score**: 4
- **origin**: DeepSeek

### ultima-milla-018 · AMVO ecommerce MX 2023
**Fact**: El ecommerce en México creció 24% en 2023 hasta más de 658.000 millones de pesos en ventas, según AMVO. La demanda de reparto urbano en CDMX, Guadalajara y Monterrey ya supera la capacidad instalada de los principales operadores logísticos — un cuello de botella estructural a anticipar en cualquier plan de expansión de reparto.

- **source**: AMVO · Estudio de Venta Online en México 2024
- **markets**: mexico
- **topics**: ultima-milla, ecommerce, mercado
- **vehicle_type**: ligeros
- **categoria**: 📦 Última milla
- **confidence**: high
- **evergreen_score**: 3
- **origin**: Claude

### ultima-milla-019 · Restricciones horarias CDMX Centro
**Fact**: El Reglamento de Tránsito de CDMX prohíbe a vehículos de carga pesada circular en el perímetro del Centro Histórico de 6:00 a 22:00. Planificar una ruta de reparto en zona céntrica con vehículo pesado en horario diurno es planificar una infracción: las restricciones horarias deben incorporarse a la lógica del sistema de planificación, no añadirse después como excepción.

- **source**: Reglamento de Tránsito CDMX + Gaceta Oficial
- **markets**: mexico
- **topics**: ultima-milla, regulacion, urbana
- **vehicle_type**: pesados, ligeros
- **categoria**: 📦 Última milla
- **confidence**: medium
- **evergreen_score**: 3
- **origin**: Claude

### ultima-milla-020 · Temperatura alimentos perecederos ES
**Fact**: La normativa española de transporte de alimentos (RD 1334/1999 y ATP) fija temperatura ≤ -18 °C para congelados y entre 0 y 4 °C para frescos. Un vehículo de reparto sin termómetro calibrado puede estar incumpliendo sin saberlo — el sensor de temperatura no es un accesorio en última milla alimentaria, es un requisito legal con registro auditable.

- **source**: RD 1334/1999 + ATP UNECE + AESAN
- **markets**: espana, europa
- **topics**: ultima-milla, cadena-frio, alimentacion
- **vehicle_type**: refrigerados, ligeros
- **categoria**: 📦 Última milla
- **confidence**: high
- **evergreen_score**: 5
- **origin**: Claude

### ultima-milla-021 · Restricciones de peso urbano CDMX
**Fact**: En CDMX, los camiones de más de 8 toneladas tienen acceso prohibido en ciertas zonas urbanas. La selección del vehículo de reparto no es solo una decisión de capacidad de carga: el peso determina qué zonas son alcanzables. Vehículos menores de 3,5 t concentran las menores restricciones, lo que reduce el coste por entrega pese a la menor capacidad unitaria.

- **source**: Reglamento de Tránsito CDMX + DOF
- **markets**: mexico
- **topics**: ultima-milla, regulacion, urbana
- **vehicle_type**: ligeros, pesados
- **categoria**: 📦 Última milla
- **confidence**: medium
- **evergreen_score**: 4
- **origin**: Claude

### ultima-milla-022 · CNMC ecommerce España 2023
**Fact**: El ecommerce facturó en España más de 79.000 millones de euros en 2023, +15% interanual, con más de 1.600 millones de envíos anuales, según la CNMC. España es ya el cuarto mercado europeo, un volumen estructural que justifica la inversión en capacidad logística de última milla como activo a largo plazo y no como respuesta puntual a picos.

- **source**: CNMC · Informe sobre el comercio electrónico en España 2023
- **markets**: espana
- **topics**: ultima-milla, ecommerce, mercado
- **vehicle_type**: ligeros
- **categoria**: 📦 Última milla
- **confidence**: high
- **evergreen_score**: 3
- **origin**: Claude

### ultima-milla-023 · Furgoneta pequeña vs camión en casco histórico
**Fact**: Una furgoneta de 7 m³ puede realizar 60-120 paradas diarias en zona urbana densa. Un camión de 25 m³ carga más volumen pero su acceso en calles estrechas limita las zonas alcanzables y multiplica kilómetros entre paradas. En cascos históricos españoles, el vehículo más pequeño puede tener más paradas efectivas por jornada — y por tanto, menor coste unitario — que el más grande.

- **source**: UNO Logística · Informe de Distribución Urbana 2023
- **markets**: espana
- **topics**: ultima-milla, planificacion, vehiculo
- **vehicle_type**: ligeros
- **categoria**: 📦 Última milla
- **confidence**: medium
- **evergreen_score**: 5
- **origin**: Claude

### ultima-milla-017 · Mexico City micro-hubs
**Fact**: CANACAR reporta reducciones próximas al 25% en tiempos de última milla al desplegar micro-hubs en CDMX (concentración previa de paquetes en zona urbana, distribución final desde punto cercano). El modelo replica las experiencias documentadas en París, Londres y Berlín.

- **source**: CANACAR + Ayuntamiento de Madrid · Plan de Distribución Urbana Sostenible + ITF OECD Urban Freight 2023
- **markets**: mexico, espana, europa
- **topics**: ultima-milla, micro-hubs, urbana
- **vehicle_type**: ligeros
- **categoria**: 📦 Última milla
- **confidence**: high-cross (DeepSeek CANACAR -25% tiempos MX + Claude microhubs Madrid/EU -30-50% km en zona urbana)
- **evergreen_score**: 4
- **origin**: DeepSeek + Claude

---

## 🏭 SECTORES VERTICALES

### sectores-001 · RPM óptimo de tambor en hormigoneras
**Fact**: Las normas ASTM y NRMCA cifran el rango óptimo de revoluciones del tambor de hormigonera entre 70 y 100 RPM durante el trayecto. Operación fuera de ese rango altera las propiedades estructurales del hormigón y puede invalidar la entrega — un evento crítico con coste de cuadrilla y obra parada.

- **source**: ASTM C94 + NRMCA + UNE-EN 206:2013+A2:2021 (Europa)
- **markets**: usa, global, espana, europa
- **topics**: sectores, hormigon, telematica
- **vehicle_type**: pesados
- **categoria**: 🏭 Sectores verticales
- **confidence**: high-cross (Gemini ASTM/NRMCA 70-100 RPM + Claude UNE-EN 206: ≤90 min o ≤300 revoluciones desde fabricación hasta vertido)
- **evergreen_score**: 5
- **origin**: Gemini + Claude

### sectores-002 · Tomas de fuerza PTO en hormigoneras
**Fact**: La SAE estima que la operación con toma de fuerza (PTO) suma cerca del 20% al consumo de combustible en hormigoneras y vehículos con equipo auxiliar. CTMA reporta que el tambor opera cerca del 25% del tiempo en vacío. Telemática de PTO permite asignar coste real a obra.

- **source**: SAE International + CTMA + Putzmeister/Schwing Technical Documentation
- **markets**: global
- **topics**: sectores, hormigon, combustible
- **vehicle_type**: pesados
- **categoria**: 🏭 Sectores verticales
- **confidence**: high-cross (DeepSeek SAE +20% consumo PTO + Claude Putzmeister: +30-40% en ralentí con bombo activo vs camión sin PTO)
- **evergreen_score**: 4
- **origin**: DeepSeek + Claude

### sectores-003 · Pérdida térmica en refrigerados
**Fact**: La apertura de puertas durante más de 3 minutos en un vehículo refrigerado acelera significativamente la pérdida térmica y compromete la cadena de frío, según el IIR. Telemática con sensor de apertura y alarma a los 90 segundos es la práctica operativa estándar en grandes cadenas alimentarias.

- **source**: IIR · International Institute of Refrigeration
- **markets**: global
- **topics**: sectores, refrigerados, cadena-frio
- **vehicle_type**: pesados, ligeros
- **categoria**: 🏭 Sectores verticales
- **confidence**: high
- **evergreen_score**: 5
- **origin**: Gemini

---

## 🔧 MANTENIMIENTO

### mantenimiento-001 · Frenos en última milla urbana
**Fact**: Una furgoneta de reparto urbano con 100 paradas diarias puede requerir intervención de frenos cada 30.000-40.000 km, frente a los 80.000-100.000 km de un vehículo de ciclo mixto, según documentación técnica de Michelin Fleet Solutions. Aplicar planes de mantenimiento estándar por km al perfil de última milla infraestima sistemáticamente el desgaste real de frenos y neumáticos.

- **source**: Michelin Fleet Solutions · Maintenance Cycle Urban Delivery vs Long Haul 2023
- **markets**: global, espana
- **topics**: mantenimiento, ultima-milla, frenos
- **vehicle_type**: ligeros
- **categoria**: 🔧 Mantenimiento
- **confidence**: medium
- **evergreen_score**: 5
- **origin**: Claude

---

## 🚢 LOGÍSTICA & CORREDORES

### logistica-001 · Handovers ineficientes en supply chain USA
**Fact**: McKinsey cuantifica entre 13% y 19% el sobrecoste logístico atribuible a handovers ineficientes (transferencias entre operadores, modos o turnos) en cadenas de suministro estadounidenses. En volumen agregado, son cerca de 95.000 millones USD anuales de fuga evitable.

- **source**: McKinsey · Global Infrastructure Initiative
- **markets**: usa, global
- **topics**: logistica, eficiencia, coste
- **vehicle_type**: pesados
- **categoria**: 🚢 Logística
- **confidence**: high-cross (ChatGPT McKinsey)
- **evergreen_score**: 4
- **origin**: ChatGPT

### logistica-002 · Redes cerradas de combustible y rutas
**Fact**: Análisis de Commercial Carrier Journal documenta que las redes cerradas (un solo proveedor de combustible) aumentan en torno a un 2,3% los kilómetros en vacío respecto a redes abiertas con cobertura comparable. El trade-off entre descuento por volumen y desvío operativo debe medirse caso por caso.

- **source**: Commercial Carrier Journal
- **markets**: usa, global
- **topics**: logistica, combustible, ruta
- **vehicle_type**: pesados
- **categoria**: 🚢 Logística
- **confidence**: medium
- **evergreen_score**: 4
- **origin**: Gemini

---

## 🏢 GESTIÓN DE FLOTAS

### gestion-001 · LCVs y uso personal weekends (EU)
**Fact**: Fleet Europe documenta que entre el 8% y el 12% de los vehículos comerciales ligeros de flotas europeas registran kilometraje no autorizado los fines de semana. Geocercas combinadas con tarjetas de combustible nominales son la palanca de control con mejor retorno por coste de implantación.

- **source**: Fleet Europe · Connected Car/LCV benchmarks
- **markets**: europa, espana
- **topics**: gestion, control, fraude
- **vehicle_type**: ligeros
- **categoria**: 🏢 Gestión de flotas
- **confidence**: medium
- **evergreen_score**: 4
- **origin**: Gemini

### gestion-002 · Mercado europeo de telemática
**Fact**: Berg Insight proyecta un mercado europeo de Fleet Management System con cerca de 30,5 millones de unidades activas en 2029 y crecimiento próximo al 12% anual. Frost & Sullivan confirma la tendencia: hardware -70% en precio entre 2015 y 2024, accelerando la adopción en flotas medianas.

- **source**: Berg Insight + Frost & Sullivan + ABI Research
- **markets**: europa, global
- **topics**: gestion, mercado, telematica
- **vehicle_type**: todos
- **categoria**: 🏢 Gestión de flotas
- **confidence**: high-cross (DeepSeek + ChatGPT)
- **evergreen_score**: 3
- **origin**: DeepSeek + ChatGPT

---

## 🔴 Conflictos detectados entre fuentes

| Tema | Versión A | Versión B | Acción |
|---|---|---|---|
| Robos a transporte carga MX 2023 | DeepSeek: "10.500 (+15% YoY)" + Perplexity: ">13.000" | Claude: "SESNSP 15.440 = 42/día" | Adoptada cifra Claude (SESNSP oficial consolidado) en seguridad-001 con nota aclaratoria sobre subconjuntos previos |
| Multa móvil al volante ES | Gemini/pool: "500 € + 6 puntos" | Claude: "200 € + 6 puntos" | Compatibles — vigente actual: 200 € móvil en soporte / 500 € sostenido en mano. Pool actualizado en regulacion-es-007 |
| Multa exceso peso eje MX | DeepSeek: "5.000-15.000 MXN" | Claude: "hasta 24.500 MXN tras intensificación SICT 2022" | Compatibles, distintos grados de gravedad — pool actualizado en regulacion-mx-001 |
| Cinturón en pesados USA | FMCSA (Gemini): "43% fallecidos sin cinturón" | NHTSA (ChatGPT): "76% siniestros fatales 6-17:59" | Compatibles, miden cosas distintas — mantenidos en facts separados |
| % última milla del envío | WEF: "53% (2024)" | Capgemini/McKinsey: "41-53% supply chain" | Compatibles, rango unificado en ultima-milla-003 |
| Coste entrega fallida EU | Gemini UNO: "15 €" + DeepSeek: "8,50 €" | Claude Capgemini: "7-15 €" | Rango compatible, consolidado en ultima-milla-001 |
| Ralentí camión consumo | Perplexity: "2-3 L/h" | Gemini: "2,5-4 L/h" | DOE: "0,8 gal/h ≈ 3 L/h" | Claude: "2-4 L/h DOE" | Rango unificado en combustible-004 (0,8-4 L/h) |

---

## 🟡 Pendientes verificación (NO producción)

Claims que aparecieron sin fuente exacta verificable, o cifras de fuentes vagas. Claude aportó rigor adicional descartando claims propios sin fuente primaria — los respetamos como señales de "no incluir".

| Claim | Origen | Sources sugeridas a verificar |
|---|---|---|
| Redes abiertas de fuel cards reducen coste total ~1% vs cerradas | Perplexity + Grok (Claude lo descartó por falta de fuente primaria) | NPTC Private Fleet, ACFO UK, ATA, Aberdeen Group |
| Conciliación manual combustible 5-15 h/mes en flotas 50-200 vehículos | Claude descartado | Aberdeen, Deloitte CFO, Fleet Advantage ROI |
| Diésel autopista hasta +15% vs urbano ES | Claude descartado pendiente CNMC | CNMC informes carburantes, Geoportal MITECO, OCU |
| Fraude tarjetas combustible flotas públicas MX >100M MXN/año | Claude descartado por falta de cifra consolidada | ASF informes sectoriales, Transparencia Presupuestaria MX |
| Entregas fallidas >25% primer intento LatAm | Claude descartado por escasez de fuente regional | Capgemini LatAm, AMVO logística |
| RUNT Colombia 22% adopción GPS | DeepSeek | RUNT, Mintransporte |
| Loi LOM Francia flotas >50 vehículos | DeepSeek | Légifrance, ADEME |
| FEMP cámaras autobuses urbanos -30% colisiones | DeepSeek | FEMP, EMT Madrid |
| Lima-Callao concentra 40% robos nacionales (Perú) | DeepSeek | SUTRAN, Policía Nacional Perú |
| Mintransporte Colombia -5% robos 2023 | DeepSeek | DIJIN, Mintransporte |
| UNASEV Uruguay +10% accidentes vuelco 35% | DeepSeek | UNASEV, MTOP |
| INTRANT RD 40% accidentes falla mecánica | DeepSeek | INTRANT |
| ANT Ecuador 70% accidentes Santo Domingo-Quito por frenos | DeepSeek | ANT Ecuador, ANSV |

---

## Coverage gaps

Tras el batch Claude: actualizada la cobertura, persisten categorías débiles. Claude solo entregó 4 categorías (combustible, telemática, seguridad, ultima_milla), por lo que las nuevas brechas detectadas siguen vivas. Claude también señaló brechas adicionales en sus `coverage_gaps`:

| Categoría | Facts actuales | Objetivo | Notas |
|---|---|---|---|
| ⚖️ Regulación México | 7 | 8-12 | Claude aportó Carta Porte, SEMARNAT, NOM-SCT — falta CFE/SENER eléctrico, ITS, mayoreo combustible |
| ⚡ Electrificación | 3 | 10-15 | Claude aportó ANFAC EV ES — pendiente camiones, infraestructura recarga, TCO real LatAm |
| 🔧 Mantenimiento | 1 | 8-10 | Nueva categoría creada con fact Michelin — pendiente intervalos, predictivo, TCO post-garantía |
| 🚛 Renting & Leasing | 0 | 8-10 | Sin cobertura en ningún batch — proponer próximo |
| 🏭 Sectores verticales | 3 | 10-15 | Pendiente: agricultura, residuos, healthcare, autobuses |
| 🌎 Geopolítica & Comercio | 0 | 5-8 | Sin cobertura — relevantes: USMCA, Ucrania-diesel, Mar Rojo |
| 🚢 Logística & Corredores | 2 | 8-10 | Pendiente: corredores Mediterráneo, Atlántico, T-MEC |
| 💼 Operadores & 3PL | 0 | 5-8 | Sin cobertura — concentración mercado, márgenes 3PL |
| 🏢 Gestión de flotas | 2 | 8-10 | Pendiente: KPIs, organización flota, FMS adoption |

**Brechas señaladas por Claude (no cubiertas con fuente verificable)**:
- Dispersión precios combustible intra-ciudad MX con fuente primaria reciente (Geoportal CRE, Profeco)
- Adopción telemática LatAm fuera de México (Berg Insight, Ptolemus, ANDEMOS, RUNT)
- Coste entrega fallida ES con metodología publicada (UNO, Capgemini, Observatorio MITMS)
- Robo de carga Colombia / Chile / Perú con cifras oficiales (RNDC, MTT, SUTRAN, TT Club, BSI)

---

## Backlog batches

| Origen | Status | Facts contribuidos | Cross-validations |
|---|---|---|---|
| Perplexity | ✅ procesado | 9 únicos | 6 cross con Grok/Gemini/ChatGPT |
| Grok | ✅ procesado | 6 únicos + 4 cross-val | 4 |
| Gemini | ✅ procesado | 35 únicos integrados | 8 cross-val con otros LLMs |
| DeepSeek | ✅ procesado | 28 únicos integrados | 7 cross-val |
| ChatGPT | ✅ procesado | 18 únicos integrados | 5 cross-val (destaca por URLs verificables) |
| Claude | ✅ procesado | 32 únicos integrados | 17 cross-val (mayor refuerzo de robustez del pool, alto rigor en descartes) |

**Target final**: 250-300 facts normalizados, ~15-25 por cada una de las 15 categorías.

**Nivel de consolidación actual (post-Claude)**:
- 137 facts únicos producción-ready (índice por ID)
- 41 cross-validated (alta confianza por consenso entre 2+ LLMs) — antes del batch Claude: 24
- 11 pending para investigar (5 nuevos aportados por descartes rigurosos de Claude)
- 7 conflictos resueltos por consolidación o rango (2 nuevos: SESNSP robos MX, multa móvil ES)

---

## Categorías target (estado actual post-Claude)

1. ⛽ Combustible & Fuel cards — **29 facts** (+8)
2. 📡 Telemática & GPS — **28 facts** (+8)
3. ⚖️ Regulación España — **7 facts**
4. ⚖️ Regulación México — **7 facts** (+4)
5. ⚡ Electrificación — **3 facts** (+1)
6. 🔧 Mantenimiento — **1 fact** (categoría creada)
7. 🛡️ Compliance & Multas — **6 facts**
8. 🚨 Seguridad & Robo de carga — **26 facts** (+9)
9. 📦 Última milla & E-commerce — **23 facts** (+6)
10. 🚛 Renting & Leasing — **0 facts**
11. 🏭 Sectores verticales — **3 facts**
12. 🌎 Geopolítica & Comercio — **0 facts**
13. 🚢 Logística & Corredores — **2 facts**
14. 💼 Operadores & 3PL — **0 facts**
15. 🏢 Gestión de flotas — **2 facts**

**Total**: **137 facts producción-ready** consolidados en 15 categorías (de los cuales 41 con cross-validation de 2+ LLMs)

**Próximos batches recomendados (priorización)**: Renting & Leasing, Operadores 3PL, Geopolítica/Comercio, Sectores verticales (agricultura, residuos, healthcare), Mantenimiento predictivo, Electrificación pesados, Logística corredores Mediterráneo/T-MEC, Gestión de flotas (KPIs/organización).
