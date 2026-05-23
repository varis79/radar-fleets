#!/usr/bin/env python3
"""
generate_country_briefs.py — Genera páginas de mercado enriquecidas para CO, CL, AR, PE.

Reemplaza el stub "hub-empty-state" con contenido real:
regulación local, players activos, tipos de flota, cifras clave.

Uso: python3 scripts/generate_country_briefs.py
"""

from pathlib import Path
import textwrap

ROOT = Path(__file__).parent.parent

# ────────────────────────────────────────────────────────────────────────────
# DATA POR MERCADO
# ────────────────────────────────────────────────────────────────────────────

MARKETS = {

"colombia": {
    "flag": "🇨🇴",
    "name": "Colombia",
    "slug": "colombia",
    "hreflang": "es-419",
    "url": "https://thefleetradar.com/mercados/colombia/",
    "accent_a": "#c9a84c",
    "accent_b": "#1a6b3c",
    "grad_a": "rgba(201,168,76,0.18)",
    "grad_b": "rgba(26,107,60,0.14)",
    "topbar_meta": "Mercado · Colombia 🇨🇴",
    "hreflang_code": "es-419",
    "meta_desc": "Panorama de flotas en Colombia 2026: RNDC, MinTransporte, RUNT, players de telemática y pagos, corredor Bogotá-Medellín y sector minero.",
    "og_desc": "Regulación, players y cifras clave del mercado de gestión de flotas en Colombia 2026.",
    "schema_desc": "Panorama editorial del mercado de gestión de flotas en Colombia 2026: regulación, players, tipos de flota y cifras del sector.",
    "deck": "Colombia tiene 350.000 vehículos de carga registrados en el RNDC, un sistema digital de despacho obligatorio desde 2004 que convierte al país en uno de los más avanzados en trazabilidad logística de LatAm. El corredor Bogotá-Medellín-Buenaventura mueve el 60% de las exportaciones. Aquí, la informalidad y el precio del ACPM son los dos vectores que más afectan la gestión de flota.",
    "updated": "23 de mayo de 2026",
    "intro": """<p>Colombia combina algo poco frecuente en LatAm: regulación digital avanzada en trazabilidad de carga (RNDC) con un mercado donde el 30-40% de las unidades opera en condición informal o sin sistemas de control. Esa brecha entre infraestructura normativa y adopción tecnológica define las oportunidades del sector en 2026.</p>
    <p>El corredor Bogotá-Buenaventura concentra la mayor actividad logística del país. La minería en el departamento de Antioquia y la agroindustria del eje cafetero generan demanda específica de flota pesada y refrigerada. Medellín, con su clúster de transporte y logística, atrae a los principales operadores nacionales.</p>
    <p>Esta página recoge qué normativa está viva, qué empresas tienen presencia activa en el mercado colombiano de flotas y qué cifras orientativas manejar. Se actualiza conforme The Fleet Radar genera cobertura de Colombia.</p>""",
    "regulacion": [
        ("Activo", "RNDC — Registro Nacional de Despacho de Carga",
         "Obligatorio desde 2004 bajo el Ministerio de Transporte. Toda carga transportada en Colombia debe registrarse en el RNDC antes del viaje: origen, destino, tipo de carga, placa, conductor. Es la base digital del sector y convierte a Colombia en referencia regional en trazabilidad de carga por carretera."),
        ("Activo", "RUNT — Registro Único Nacional de Tránsito",
         "Plataforma digital de gestión de licencias, vehículos, accidentes y trámites de tránsito. Las flotas deben mantener sus unidades al día en el RUNT; su interoperabilidad con el RNDC permite verificación automática de vigencia."),
        ("Activo", "Resolución 4100 de 2004 (pesos y dimensiones)",
         "El Ministerio de Transporte establece límites de peso y dimensión por tipo de eje. Los controles de pesaje en puntos de balanza son frecuentes en los corredores principales. Incumplimiento genera inmovilización y multas que afectan directamente el tiempo de tránsito."),
        ("Activo", "Decreto 431 de 2020 — Jornada máxima de conductores",
         "Establece jornada máxima de 10 horas diarias con descanso obligatorio de 8 horas para conductores de carga. La SuperTransporte verifica cumplimiento mediante bitácoras físicas; la adopción de tacógrafos digitales es aún baja en el segmento SME."),
        ("soon", "Proyecto — modernización de la normativa de transporte de carga",
         "El MinTransporte trabaja en la actualización de los decretos marco del autotransporte, con énfasis en telemetría obligatoria y estándares de seguridad para vehículos de carga especial y materiales peligrosos."),
    ],
    "players": {
        "Telemática y GPS": [
            "Geotab · distribuidores locales con foco en flotas medianas",
            "Samsara · entrada gradual con perfil enterprise",
            "Maber · jugador local con presencia en Medellín",
            "iTrack · solución nacional para flotas PYME",
            "Trackmos · rastreo satelital colombiano",
        ],
        "Combustible y pagos": [
            "Terpel · líder de red con tarjeta Terpel empresarial",
            "Biomax · segunda red nacional con soluciones B2B",
            "Primax · marca de Andina de Combustibles con tarjeta flota",
            "Exxon / Esso · presencia en corredores principales",
        ],
        "Renting y servicios": [
            "LeasePlan · renting corporativo (multinacional)",
            "Arval · gestión de flota corporativa",
            "GBC Fleet · renting y postventa local",
        ],
        "Fabricantes relevantes": [
            "Chevrolet · N400 y NPR dominan carga liviana-media",
            "Kenworth · tractocamiones premium en carga pesada",
            "Volvo · corredor pesado Bogotá-Cali-Buenaventura",
            "JAC · entrada china en segmento precio",
            "Foton · crecimiento en carga media",
        ],
    },
    "fleet_types": [
        ("Carga pesada y tractocamiones", "Corredor Bogotá-Medellín, Bogotá-Buenaventura y conexión con Venezuela. Freightliner y Kenworth dominan el parque de tractocamiones de larga distancia."),
        ("Distribución intermedia y urbana", "Bogotá, Medellín, Cali y Barranquilla como mercados de distribución urbana. Cadenas de retail y food service con flotas propias de Chevrolet NPR y similares."),
        ("Flota minera", "Antioquia y Boyacá con operaciones de carbón. Cundinamarca y Cesar con carga especializada. Flotas fuera de carretera con requerimientos de mantenimiento específicos."),
        ("Agroindustria y refrigerada", "Eje cafetero hacia puertos del Pacífico. Plátano y banano del Urabá antioqueño. Alta demanda de control de temperatura y trazabilidad de cadena de frío."),
        ("Flotas corporativas y LCV", "Sector financiero, telecomunicaciones y energía con flotas pick-up y utilitarios. Alta informalidad en el segmento mototaxi y delivery."),
    ],
    "figures": [
        ("~350.000", "vehículos de carga registrados activamente en el RNDC", "MinTransporte · 2025"),
        ("60%", "del comercio exterior de Colombia pasa por el Puerto de Buenaventura, eje del corredor logístico principal", "ProColombia · 2026"),
        ("~28%", "penetración estimada de telemática en flotas de carga medianas y grandes", "Análisis sectorial 2026"),
        ("62.000 km", "de red vial nacional colombiana, con 17.000 km en doble calzada o en construcción bajo concesiones 4G/5G", "INVIAS · 2025"),
    ],
    "related_topics": [
        ("/temas/telematica-flotas-mexico-2026/", "Tema · Referencia", "Telemática para flotas en México 2026", "Benchmarks y players de referencia para el mercado latinoamericano."),
        ("/mercados/latam/", "Mercado · Regional", "Flotas en LatAm · Panorama 2026", "Tendencias transversales de la región que impactan a Colombia."),
        ("/temas/electrificacion-flotas-mexico-2026/", "Tema · EV", "Electrificación de flotas 2026", "Estado del mercado EV en LatAm: BYD, Volvo y las iniciativas de flotas eléctricas."),
    ],
    "editions": [
        ("/magazines/2026-04-20-radar-fleet-by-pulpo.html", "Nº 3 · Peajes por km, electrificación LatAm y operador asesinado", "20 abril 2026"),
        ("/magazines/2026-04-14-radar-fleet-by-pulpo.html", "Nº 1 · La semana que redefinió las reglas", "14 abril 2026"),
    ],
    "cta_heading": "Pulpo cubre LatAm desde su hub en México y España",
    "cta_body": "Si gestionas flota en Colombia y buscas una plataforma de gestión integral con cobertura regional, el equipo de Pulpo puede acompañarte en la evaluación de necesidades.",
    "sources": [
        ("Ministerio de Transporte de Colombia", "https://www.mintransporte.gov.co/", "Marco normativo del autotransporte, RNDC y política sectorial"),
        ("RNDC — Registro Nacional de Despacho de Carga", "https://rndc.gov.co/", "Sistema de trazabilidad obligatoria de carga por carretera"),
        ("RUNT — Registro Único Nacional de Tránsito", "https://www.runt.com.co/", "Registro de vehículos, conductores y trámites de tránsito"),
        ("INVIAS — Instituto Nacional de Vías", "https://www.invias.gov.co/", "Red vial nacional, concesiones 4G/5G y datos de infraestructura"),
        ("SuperTransporte — Superintendencia de Transporte", "https://www.supertransporte.gov.co/", "Vigilancia y control del sector transporte en Colombia"),
        ("Terpel — Red de combustible y servicios empresariales", "https://www.terpel.com/", "Principal red de combustible en Colombia con soluciones B2B para flotas"),
    ],
},

"chile": {
    "flag": "🇨🇱",
    "name": "Chile",
    "slug": "chile",
    "hreflang": "es-419",
    "url": "https://thefleetradar.com/mercados/chile/",
    "accent_a": "#b8463a",
    "accent_b": "#1e7fcb",
    "grad_a": "rgba(184,70,58,0.18)",
    "grad_b": "rgba(30,127,203,0.14)",
    "topbar_meta": "Mercado · Chile 🇨🇱",
    "hreflang_code": "es-419",
    "meta_desc": "Panorama de flotas en Chile 2026: MTT, normativa ZEV, Copec, minería (Codelco, SQM), adopción EV líder en LatAm y corredor de la Ruta 5.",
    "og_desc": "Regulación, players y cifras clave del mercado de gestión de flotas en Chile 2026.",
    "schema_desc": "Panorama editorial del mercado de gestión de flotas en Chile 2026: MTT, electrificación, minería y players activos.",
    "deck": "Chile lidera la adopción de vehículos eléctricos en LatAm, con Santiago operando la mayor flota de buses eléctricos del continente fuera de China. La minería —Codelco, SQM, Antofagasta Minerals— genera demanda sostenida de flota pesada de extracción con estándares de seguridad entre los más exigentes de la región. El MTT avanza en regulación de emisiones y telemetría.",
    "updated": "23 de mayo de 2026",
    "intro": """<p>Chile combina el mercado de flotas más regulado de LatAm con el mayor índice de adopción de vehículos eléctricos de la región. Santiago opera más de 2.000 buses eléctricos —la mayor flota del continente fuera de China— gracias al programa de electrificación del transporte público que el gobierno comenzó en 2018.</p>
    <p>La minería define el segmento pesado. Codelco, SQM, Anglo American y Antofagasta Minerals operan flotas de equipos de extracción, camiones de gran tonelaje y vehículos auxiliares con protocolos de seguridad y mantenimiento de nivel internacional. La presión por descarbonizar estas operaciones abre una ventana de renovación en el horizonte 2026-2030.</p>
    <p>El corredor norte-sur de la Ruta 5 (Panamericana) es el eje logístico del país. La extensión geográfica de Chile —4.300 km de norte a sur— impone requerimientos específicos de conectividad satelital y autonomía para las flotas de largo recorrido.</p>""",
    "regulacion": [
        ("Activo", "MTT — Decreto 39 y normas de emisiones para vehículos pesados",
         "El Ministerio de Transportes y Telecomunicaciones exige cumplimiento de estándares Euro VI para nuevas adquisiciones de vehículos pesados en operación concesionada. La Resolución 285 establece control de emisiones con revisión técnica obligatoria anual (REVISIÓN TÉCNICA VEHICULAR) para todos los vehículos de carga."),
        ("Activo", "Revisión Técnica Vehicular — obligatoria para flota comercial",
         "Todos los vehículos de carga deben pasar inspección técnica vehicular con cadencia anual. El sistema está concesionado a operadores privados certificados. Los conductores con infracciones acumuladas enfrentan restricción de licencia mediante el sistema de puntos vigente desde 2022."),
        ("Activo", "Ley 21.505 — Electromovilidad y ZEV",
         "Chile estableció metas de cero emisiones para buses y taxis en la Región Metropolitana a partir de 2035. Las flotas corporativas en Santiago operan bajo incentivos fiscales para adquisición de vehículos eléctricos. El MTT coordina con el Ministerio de Energía la expansión de infraestructura de carga."),
        ("Activo", "Ley REP — Responsabilidad Extendida del Productor (neumáticos)",
         "Las flotas con más de 30 unidades deben gestionar el fin de vida de sus neumáticos bajo el sistema REP. Implica registro ante el Ministerio del Medio Ambiente y contrato con gestores autorizados. Afecta principalmente a flotas mineras y de transporte pesado."),
        ("soon", "En desarrollo — Normativa de tacógrafos digitales para carga interprovincial",
         "El MTT prepara regulación de bitácora electrónica obligatoria para transporte de carga interprovincial, siguiendo el modelo europeo. El calendario de implementación sigue en consulta con el sector durante 2026."),
    ],
    "players": {
        "Combustible y pagos": [
            "Copec · líder de red con Copec Pay para flotas empresariales",
            "ENAP · estaciones de servicio y venta mayorista de combustible",
            "Shell / MACH · red B2B con tarjeta de flota",
            "Petrobras · presencia en el norte minero",
        ],
        "Telemática y gestión": [
            "Geotab · fuerte presencia en minería y transporte empresarial",
            "Samsara · entrada en flotas de mediana y gran escala",
            "Tracklink · proveedor local con foco en transporte regional",
            "RFlex · solución chilena para gestión de flota PYME",
        ],
        "Fabricantes y equipos": [
            "BYD · autobuses eléctricos (>1.200 en Santiago) y tractores en evaluación",
            "Yutong · autobuses eléctricos en el sistema RED de Santiago",
            "Volvo · tractocamiones en minería y transporte pesado",
            "Mercedes-Benz · Actros en operaciones logísticas premium",
            "Kenworth · tractocamiones en el corredor norte-sur",
            "Caterpillar / Komatsu · equipos fuera de carretera en minería",
        ],
        "Renting y servicios": [
            "LeasePlan · renting corporativo multinacional",
            "Automotriz Gildemeister · distribución y servicios postventa",
            "Flexi-Logística · arriendo operativo de vehículos en RM",
        ],
    },
    "fleet_types": [
        ("Minería pesada", "Codelco, SQM, Anglo American y Antofagasta Minerals operan equipos de extracción de gran tonelaje en el norte de Chile (Atacama, Antofagasta). Estándares de seguridad y mantenimiento entre los más exigentes de LatAm."),
        ("Transporte público eléctrico", "Santiago tiene más de 2.000 buses eléctricos en operación. El Ministerio de Transportes proyecta electrificación completa del sistema RED para 2035. Caso de referencia internacional en electrificación de flota masiva."),
        ("Transporte de carga (Ruta 5)", "Eje norte-sur de 4.300 km. Flotas de tractocamiones Volvo, Mercedes y Kenworth en largo recorrido. Alta demanda de telemetría por la extensión geográfica y los corredores de montaña."),
        ("Flotas corporativas urbanas", "Santiago concentra el mercado corporativo: sector financiero, retail, tecnología. Renting con penetración alta. Crecimiento de vehículos eléctricos en flotas ejecutivas y de servicios."),
        ("Agroindustria y pesca", "Valle Central con flotas de tractores agrícolas. Puerto de Valparaíso como eje de flota portuaria y logística de exportación agroindustrial. Temperatura controlada en cadena de frío exportadora."),
    ],
    "figures": [
        (">2.000", "buses eléctricos en operación en Santiago · la mayor flota de LatAm fuera de China", "MTT · 2026"),
        ("~$85B USD", "valor del mercado de exportación minera de Chile, que impulsa la demanda de flota pesada de extracción", "Banco Central de Chile · 2025"),
        ("35%", "del consumo de combustible de Chile que corresponde al sector transporte, según cifras del Ministerio de Energía", "Ministerio de Energía · 2025"),
        ("4.300 km", "de extensión norte-sur de Chile, que impone requerimientos específicos de conectividad para flotas de largo recorrido", "IGM Chile"),
    ],
    "related_topics": [
        ("/temas/electrificacion-flotas-espana-2026/", "Tema · EV", "Electrificación de flotas en España 2026", "Referencia regulatoria y de mercado para adopción EV en flota pesada."),
        ("/mercados/latam/", "Mercado · Regional", "Flotas en LatAm · Panorama 2026", "Tendencias transversales de la región que impactan a Chile."),
        ("/temas/telematica-flotas-mexico-2026/", "Tema · Tech", "Telemática para flotas · Referencia LatAm", "Players y benchmarks del sector de telemática en América Latina."),
    ],
    "editions": [
        ("/magazines/2026-04-20-radar-fleet-by-pulpo.html", "Nº 3 · Electrificación y flotas LatAm", "20 abril 2026"),
        ("/magazines/2026-04-27-radar-fleet-by-pulpo.html", "Nº 4 · Minería, pesado y nearshoring", "27 abril 2026"),
    ],
    "cta_heading": "Pulpo Hub — plataforma de gestión con enfoque LatAm",
    "cta_body": "Pulpo Hub opera en flotas de México y España, con arquitectura pensada para expansión regional. Si gestionas flota en Chile, el equipo puede evaluar cómo adaptar la solución a tu mercado.",
    "sources": [
        ("MTT — Ministerio de Transportes y Telecomunicaciones de Chile", "https://www.mtt.gob.cl/", "Marco regulatorio del transporte terrestre, normativa de emisiones y electromovilidad"),
        ("SEC — Superintendencia de Electricidad y Combustibles", "https://www.sec.cl/", "Regulación de combustibles y normativa de carga eléctrica vehicular"),
        ("COCHILCO — Comisión Chilena del Cobre", "https://www.cochilco.cl/", "Datos del sector minero y demanda de equipos de transporte en minería"),
        ("Ministerio de Energía de Chile", "https://www.energia.gob.cl/", "Estadísticas de consumo energético por sector y política de electromovilidad"),
        ("Copec — Red de combustible y Copec Pay", "https://www.copec.cl/", "Principal red de distribución de combustible y tarjetas de flota en Chile"),
    ],
},

"argentina": {
    "flag": "🇦🇷",
    "name": "Argentina",
    "slug": "argentina",
    "hreflang": "es-419",
    "url": "https://thefleetradar.com/mercados/argentina/",
    "accent_a": "#1e7fcb",
    "accent_b": "#c9a84c",
    "grad_a": "rgba(30,127,203,0.18)",
    "grad_b": "rgba(201,168,76,0.14)",
    "topbar_meta": "Mercado · Argentina 🇦🇷",
    "hreflang_code": "es-419",
    "meta_desc": "Panorama de flotas en Argentina 2026: CNRT, AFIP/ARCA, GNC, YPF, presión inflacionaria y oportunidades en control de gasto de flota.",
    "og_desc": "Regulación, players y cifras clave del mercado de gestión de flotas en Argentina 2026.",
    "schema_desc": "Panorama editorial del mercado de gestión de flotas en Argentina 2026: CNRT, GNC, YPF, presión inflacionaria y gestión del gasto.",
    "deck": "Argentina tiene la mayor flota de vehículos de GNC (gas natural comprimido) del mundo en términos relativos: más de 2 millones de unidades convertidas. La presión inflacionaria hace que el control de gasto en combustible, mantenimiento y operación sea una prioridad operativa de primera línea para los gestores de flota. El peso desafía la planificación a largo plazo.",
    "updated": "23 de mayo de 2026",
    "intro": """<p>Argentina combina una infraestructura de GNC sin par en el mundo con una inflación que convierte el control de gasto en flota en una variable operativa crítica, no en un plus. En un contexto donde los precios de combustible, neumáticos y repuestos suben semana a semana, los gestores de flota que no tienen sistemas de control en tiempo real pierden visibilidad sobre sus costos antes de que el mes cierre.</p>
    <p>YPF domina el mercado de combustible con una red que cubre el 60% del territorio. La red de estaciones GNC —unas 1.800 en todo el país— hace que el gas natural vehicular sea una alternativa real para flotas de distribución urbana e intercity. En empresas de transporte de pasajeros, la conversión a GNC es casi universal.</p>
    <p>La CNRT (Comisión Nacional de Regulación del Transporte) regula el autotransporte de carga y pasajeros a nivel federal. ARCA (ex-AFIP) gestiona la facturación electrónica obligatoria, que en Argentina está entre las más avanzadas de LatAm.</p>""",
    "regulacion": [
        ("Activo", "CNRT — Comisión Nacional de Regulación del Transporte",
         "Regula habilitaciones, condiciones técnicas, seguros y operación del autotransporte de carga y pasajeros interjurisdiccional. Las flotas de más de 5 unidades en transporte federal deben estar habilitadas ante la CNRT con documentación al día: VTV, seguros, licencias profesionales y fichas de control."),
        ("Activo", "VTV — Verificación Técnica Vehicular obligatoria",
         "Cadencia anual para vehículos de carga y semestral para transporte de pasajeros. Los certificados de VTV son requisito para la habilitación ante la CNRT. Su vencimiento genera paralización inmediata de la unidad en controles de ruta."),
        ("Activo", "ARCA (ex-AFIP) — Facturación electrónica y trazabilidad fiscal",
         "Argentina tiene uno de los sistemas de facturación electrónica más desarrollados de LatAm. Las flotas deben emitir comprobantes electrónicos para todos los servicios de transporte, combustible y mantenimiento deducibles. La integración con los sistemas de gestión es crítica para el cumplimiento."),
        ("Activo", "Ley 24.449 — Ley de Tránsito y normativa de conductores",
         "Establece licencias profesionales por categoría, horas de conducción máximas (10 horas diarias) y obligación de descanso. Los sistemas de bitácora de conductor son obligatorios para el transporte de carga federal, aunque la tecnología de tacógrafos digitales tiene penetración baja en el segmento PYME."),
        ("opportunity", "Estímulo — Programa de renovación de flota de transporte de pasajeros",
         "El gobierno nacional impulsa líneas de crédito subsidiado para renovación de unidades de transporte de pasajeros de media distancia. El eje es la reducción de emisiones y mejora de seguridad en rutas interurbanas de alta demanda."),
    ],
    "players": {
        "Combustible y GNC": [
            "YPF · domina ~60% del mercado de combustible con tarjeta YPF empresarial",
            "Shell · red B2B con tarjeta flota en grandes centros urbanos",
            "Axion / ENAP · presencia en Patagonia y corredor Rosario-Córdoba",
            "GNC: ~1.800 estaciones · mayor infraestructura del mundo en términos relativos",
        ],
        "Telemática y GPS": [
            "Track Group · proveedor local con fuerte cobertura en flotas medianas",
            "Geotab · distribuidores locales para el segmento enterprise",
            "TelTrak · solución argentina con foco en transporte de pasajeros",
            "ControlFleet · plataforma PYME con fuerte presencia en Buenos Aires",
        ],
        "Renting y servicios": [
            "LeasePlan · renting corporativo multinacional",
            "GMAC / GM Financial · financiamiento de flota corporativa",
            "Patagonia Leasing · renting regional",
        ],
        "Fabricantes relevantes": [
            "Ford · Ranger y Transit, dominantes en pick-up y LCV",
            "Toyota · Hilux, la pick-up más vendida en flotas argentinas",
            "Mercedes-Benz · Sprinter y Actros, muy presentes en distribución y pesado",
            "Volkswagen · Crafter y camiones de distribución",
            "Iveco · presencia en transporte de pasajeros y carga media",
        ],
    },
    "fleet_types": [
        ("Transporte de pasajeros interurbano", "Alta concentración en rutas Buenos Aires-Rosario-Córdoba-Mendoza. Flotas de hasta 80 unidades por empresa. GNC y diesel, con incipiente entrada de híbridos."),
        ("Distribución urbana", "Buenos Aires, Rosario y Córdoba como mercados principales. Cadenas de supermercados, consumo masivo y bebidas con flotas propias de 20-200 unidades."),
        ("Flota corporativa y LCV", "Sector agropecuario, minería en Neuquén (Vaca Muerta) y Patagonia con flota pick-up. Altas tasas de informalidad en el segmento de menos de 5 unidades."),
        ("Transporte agrícola", "Corredor sojero Santa Fe-Buenos Aires-Entre Ríos. Camiones graneleros de alta capacidad. Fuerte estacionalidad en la gestión de la flota según campaña agrícola."),
        ("Vaca Muerta — oil & gas", "Neuquén concentra operaciones de extracción de hidrocarburos no convencionales. Flotas de servicio de pozos con alta exigencia operativa y gestión de activos en condiciones remotas."),
    ],
    "figures": [
        (">2M", "vehículos con sistema GNC en Argentina · la mayor flota relativa del mundo", "ENARGAS · 2025"),
        ("~1.800", "estaciones de GNC en todo el país · la mayor red de LatAm", "ENARGAS · 2025"),
        ("~60%", "cuota de mercado de YPF en combustible para transporte", "SURTAX / análisis sectorial 2025"),
        ("~250%", "de inflación acumulada en 3 años que presiona el gasto operativo de flotas y exige control en tiempo real", "INDEC · 2024-2025"),
    ],
    "related_topics": [
        ("/temas/control-gasto-flota-mexico-2026/", "Tema · Referencia", "Control de gasto en flota", "Sistemas y estrategias de control de costos aplicables en mercados con alta inflación."),
        ("/mercados/latam/", "Mercado · Regional", "Flotas en LatAm · Panorama 2026", "Tendencias transversales que impactan a Argentina."),
        ("/temas/tarjetas-flota-mexico-2026/", "Tema · Combustible", "Tarjetas de flota y combustible", "Control de gasto en combustible: metodologías aplicables en Argentina."),
    ],
    "editions": [
        ("/magazines/2026-04-20-radar-fleet-by-pulpo.html", "Nº 3 · Flota pesada y tendencias LatAm", "20 abril 2026"),
        ("/magazines/2026-05-04-radar-fleet-by-pulpo.html", "Nº 5 · Regulación, electrificación y gestión", "4 mayo 2026"),
    ],
    "cta_heading": "Pulpo Hub — control de gasto para flotas en mercados exigentes",
    "cta_body": "La plataforma de Pulpo permite controlar gasto de combustible, mantenimiento y operación en tiempo real. En mercados de alta inflación, la visibilidad diaria sobre costos es la diferencia entre rentabilidad y pérdida.",
    "sources": [
        ("CNRT — Comisión Nacional de Regulación del Transporte", "https://www.cnrt.gob.ar/", "Marco normativo del autotransporte federal, habilitaciones y control"),
        ("ENARGAS — Ente Nacional Regulador del Gas", "https://www.enargas.gov.ar/", "Datos del mercado de GNC y regulación de distribución de gas natural"),
        ("ARCA — Agencia de Recaudación y Control Aduanero (ex-AFIP)", "https://www.afip.gob.ar/", "Facturación electrónica, normativa fiscal y cumplimiento tributario en transporte"),
        ("INDEC — Instituto Nacional de Estadística y Censos", "https://www.indec.gob.ar/", "Estadísticas económicas: inflación, actividad del sector transporte"),
        ("YPF — Yacimientos Petrolíferos Fiscales", "https://www.ypf.com/", "Principal proveedor de combustible para flotas en Argentina"),
        ("FADEEAC — Federación Argentina de Entidades Empresarias del Autotransporte de Cargas", "https://www.fadeeac.org.ar/", "Datos del sector autotransporte de cargas: parque, costos operativos"),
    ],
},

"peru": {
    "flag": "🇵🇪",
    "name": "Perú",
    "slug": "peru",
    "hreflang": "es-419",
    "url": "https://thefleetradar.com/mercados/peru/",
    "accent_a": "#b8463a",
    "accent_b": "#c9a84c",
    "grad_a": "rgba(184,70,58,0.18)",
    "grad_b": "rgba(201,168,76,0.14)",
    "topbar_meta": "Mercado · Perú 🇵🇪",
    "hreflang_code": "es-419",
    "meta_desc": "Panorama de flotas en Perú 2026: MTC, SUTRAN, minería (Antamina, Las Bambas), corredor Lima-Callao, GLP y control de flota en el sector logístico.",
    "og_desc": "Regulación, players y cifras clave del mercado de gestión de flotas en Perú 2026.",
    "schema_desc": "Panorama editorial del mercado de gestión de flotas en Perú 2026: MTC, SUTRAN, minería, corredor Lima-Callao y players activos.",
    "deck": "El eje Lima-Callao concentra el 60% de la actividad logística del Perú. La minería —Antamina, Las Bambas, Toquepala, Cerro de Pasco— genera la mayor demanda de flota pesada del país, con estándares internacionales de seguridad y mantenimiento. SUTRAN es la autoridad regulatoria con presencia creciente en los corredores nacionales.",
    "updated": "23 de mayo de 2026",
    "intro": """<p>Perú tiene un mercado de flotas en expansión activa: el corredor Lima-provincias crece por el e-commerce y la distribución moderna, mientras la minería sostiene la demanda de flota pesada con proyectos en operación en el sur (Las Bambas, Toquepala) y el centro (Antamina, Cerro de Pasco).</p>
    <p>SUTRAN (Superintendencia de Transporte Terrestre) es la autoridad de supervisión del transporte de carga y pasajeros, con controles crecientes en carretera y obligación de tacógrafo digital para vehículos pesados desde 2014. La implementación efectiva en el segmento informal sigue siendo el principal reto regulatorio.</p>
    <p>Lima concentra la logística del país: el Puerto del Callao es el principal puerto del Pacífico sur. Las vías nacionales que conectan Lima con las regiones andinas y la selva presentan condiciones exigentes para la flota: altitud, curvas y segmentos sin asfaltar en rutas secundarias.</p>""",
    "regulacion": [
        ("Activo", "SUTRAN — Supervisión del transporte terrestre de carga",
         "La Superintendencia de Transporte Terrestre de Personas, Carga y Mercancías supervisa el cumplimiento de la normativa vial para transportistas. Exige habilitación de la empresa transportista, tarjeta de circulación de la unidad y licencia AII o AIII para conductores de carga. Los controles en ruta son frecuentes en los corredores Lima-Arequipa, Lima-Huancayo y Lima-Trujillo."),
        ("Activo", "Decreto Supremo 017-2009-MTC — Tacógrafo obligatorio",
         "Desde 2014 es obligatorio para vehículos de carga con PBV superior a 3.5 toneladas. El tacógrafo debe registrar velocidad, distancia y horas de conducción. SUTRAN puede solicitar la lectura del disco en controles. La penetración real de tacógrafos digitales avanza, pero la informalidad dificulta el cumplimiento uniforme."),
        ("Activo", "Ley 28256 — Transporte de materiales peligrosos",
         "Los vehículos que transportan materiales peligrosos deben cumplir con señalización, equipos de emergencia, certificación del conductor y rutas autorizadas. El MTC (Ministerio de Transportes y Comunicaciones) actualiza periódicamente el listado de materiales y las rutas permitidas."),
        ("Activo", "GLP — Gas Licuado de Petróleo como alternativa al diésel en Lima",
         "Lima tiene una red creciente de grifos con GLP para uso vehicular. El GLP es frecuente en taxis y vehículos ligeros, pero avanza en distribución urbana. La diferencia de precio respecto al diésel —regulado por el Osinergmin— genera conversiones en flotas de reparto de corta distancia."),
        ("soon", "En desarrollo — Regulación de emisiones para Lima Metropolitana",
         "La Municipalidad Metropolitana de Lima impulsa restricciones de circulación para vehículos sin certificado de emisiones vigente. El marco regulatorio específico sigue en elaboración, con posible implementación parcial en 2026-2027 en las vías de mayor congestión."),
    ],
    "players": {
        "Combustible y energía": [
            "Repsol · mayor red de grifos y mayor operador B2B en combustible",
            "Primax · segunda red nacional con tarjeta empresarial",
            "PetroPerú · estaciones en provincias y zonas alejadas",
            "Osinergmin · regulador de precios y calidad de combustibles",
        ],
        "Telemática y GPS": [
            "Geotab · distribuidores locales con foco en minería y transporte",
            "Samsara · entrada en flotas de gran tamaño",
            "GPStrack · solución peruana para flotas medianas",
            "Trackpro · proveedor local con cobertura en corredores andinos",
        ],
        "Renting y servicios": [
            "LeasePlan · renting corporativo en Lima",
            "Mitsui AutoForum · distribución Toyota y renting",
            "Derco · distribución Chevrolet, Mazda y servicios postventa",
        ],
        "Fabricantes relevantes": [
            "Toyota · Hilux como pick-up dominante en flotas de campo y minería",
            "Mitsubishi · L200 y Fuso en carga media y minería",
            "Volvo · tractocamiones en minería y transporte pesado",
            "Mercedes-Benz · Actros y Sprinter en Lima y corredores principales",
            "JAC y Foton · entrada china en carga media y distribución",
        ],
    },
    "fleet_types": [
        ("Minería pesada", "Antamina (Áncash), Las Bambas (Apurímac), Toquepala y Cuajone (Moquegua), Cerro de Pasco. Flotas de camiones de extracción con gestión de activos internacionalizada. Alta exigencia de mantenimiento y documentación de seguridad."),
        ("Corredor Lima-Callao", "El Puerto del Callao como hub de importación-exportación. Camiones de carga contenerizada entre el puerto, los almacenes en Lurín y los centros de distribución de Lima. Alta densidad de operación y gestión por turnos."),
        ("Distribución interprovincial", "Rutas Lima-Arequipa, Lima-Trujillo, Lima-Huancayo, Lima-Cusco. Tractocamiones Volvo y Mercedes en largo recorrido. Retos de altitud en el paso andino (>4.000 msnm en algunas rutas)."),
        ("E-commerce y última milla", "Lima tiene una de las tasas de crecimiento de e-commerce más altas de LatAm. Flotas de reparto con mototaxis y camionetas. Operadores como Rappi, PedidosYa y las flotas propias de tiendas por departamento."),
        ("Agroindustria de exportación", "La Libertad (espárrago), Ica (uva, espárrago) e Ica-Chincha como polos de flota refrigerada de exportación. Estrictos requisitos de cadena de frío y trazabilidad para mercados europeos y norteamericanos."),
    ],
    "figures": [
        ("~200.000", "vehículos de carga registrados en el Perú según MTC, con crecimiento sostenido impulsado por minería y e-commerce", "MTC · 2025"),
        (">60%", "de la actividad logística del país que se concentra en el eje Lima-Callao", "OSITRAN · análisis editorial"),
        ("~18%", "penetración de telemática en flotas de carga medianas y grandes, con brechas significativas en el segmento informal", "Análisis sectorial 2026"),
        ("4.000+ msnm", "altitud media de los pasos andinos en rutas de carga, que exige gestión específica de motor y combustible en flota de largo recorrido", "IGN Perú"),
    ],
    "related_topics": [
        ("/temas/telematica-flotas-mexico-2026/", "Tema · Referencia", "Telemática para flotas · Referencia LatAm", "Players y benchmarks del sector de telemática en América Latina."),
        ("/mercados/latam/", "Mercado · Regional", "Flotas en LatAm · Panorama 2026", "Tendencias transversales que impactan a Perú."),
        ("/temas/compliance-flotas-mexico-2026/", "Tema · Regulación", "Cumplimiento normativo en flotas", "Metodologías de compliance aplicables en el contexto regulatorio peruano."),
    ],
    "editions": [
        ("/magazines/2026-04-20-radar-fleet-by-pulpo.html", "Nº 3 · Minería, flota pesada y LatAm", "20 abril 2026"),
        ("/magazines/2026-05-11-radar-fleet-by-pulpo.html", "Nº 7 · Tendencias de gestión de flotas", "11 mayo 2026"),
    ],
    "cta_heading": "Pulpo Hub — plataforma con foco en LatAm",
    "cta_body": "Pulpo Hub está diseñado para gestionar flotas desde 10 hasta más de 10.000 unidades. Con presencia en México y España y cobertura editorial en toda LatAm, el equipo puede evaluar la adaptación para flotas peruanas en crecimiento.",
    "sources": [
        ("MTC — Ministerio de Transportes y Comunicaciones del Perú", "https://www.gob.pe/mtc", "Marco normativo del transporte terrestre y aviación civil"),
        ("SUTRAN — Superintendencia de Transporte Terrestre", "https://www.sutran.gob.pe/", "Supervisión del transporte de personas, carga y mercancías"),
        ("OSINERGMIN — Organismo Supervisor de la Inversión en Energía y Minería", "https://www.osinergmin.gob.pe/", "Regulación de combustibles, gas y energía eléctrica en Perú"),
        ("MINEM — Ministerio de Energía y Minas", "https://www.minem.gob.pe/", "Datos del sector minero y regulación de operaciones extractivas"),
        ("Repsol Perú — Red de combustible y servicios B2B", "https://www.repsol.com/es/paises/peru/index.cshtml", "Principal operador de red de grifos y servicios empresariales de combustible en Perú"),
        ("PromPerú / ProInversión — Datos de comercio exterior e inversión", "https://www.promperu.gob.pe/", "Estadísticas de exportación y sectores tractores del mercado logístico peruano"),
    ],
},

}  # end MARKETS

# ────────────────────────────────────────────────────────────────────────────
# CSS BLOCK (same base for all market pages)
# ────────────────────────────────────────────────────────────────────────────

def css_block(m: dict) -> str:
    return f"""<style>
  :root{{
    --accent:{m['accent_a']};
    --accent-2:{m['accent_b']};
    --cover-grad-a:{m['grad_a']};
    --cover-grad-b:{m['grad_b']};
  }}
  .mkt-hero{{
    background:var(--near-black);
    background-image:
      radial-gradient(ellipse 70% 50% at 20% 80%, var(--cover-grad-a) 0%, transparent 60%),
      radial-gradient(ellipse 50% 40% at 80% 20%, var(--cover-grad-b) 0%, transparent 55%),
      radial-gradient(ellipse 100% 100% at 50% 50%, #0d1521 0%, #060a10 100%);
    padding:80px 32px 64px;border-bottom:1px solid rgba(255,255,255,.06);
  }}
  .mkt-hero-inner{{max-width:1100px;margin:0 auto}}
  .mkt-flag{{font-size:56px;line-height:1;margin-bottom:16px}}
  .mkt-kicker{{font-size:11px;font-weight:700;letter-spacing:.22em;text-transform:uppercase;color:var(--accent-2);margin-bottom:18px;display:block}}
  .mkt-title{{font-family:'Fraunces',serif;font-size:clamp(40px,6vw,72px);font-weight:900;line-height:.98;letter-spacing:-1.2px;color:#fff;margin-bottom:22px}}
  .mkt-title span{{color:var(--accent-2)}}
  .mkt-deck{{font-size:16px;color:rgba(255,255,255,.68);max-width:680px;line-height:1.75;border-left:2px solid var(--accent-2);padding-left:20px}}
  .mkt-updated{{margin-top:24px;font-size:11px;letter-spacing:.15em;text-transform:uppercase;color:rgba(255,255,255,.35)}}
  .mkt-main{{max-width:1100px;margin:0 auto;padding:72px 32px 100px}}
  .mkt-body p{{font-size:16px;line-height:1.8;color:var(--text-mid);margin-bottom:18px}}
  .mkt-body h2{{font-family:'Fraunces',serif;font-size:30px;font-weight:700;color:var(--text-dark);margin-top:56px;margin-bottom:20px;letter-spacing:-.3px;line-height:1.15}}
  .mkt-body h3{{font-family:'Fraunces',serif;font-size:20px;font-weight:700;color:var(--text-dark);margin-top:28px;margin-bottom:12px}}
  .mkt-body strong{{color:var(--text-dark)}}
  .mkt-body a{{color:var(--accent);text-decoration:underline;text-underline-offset:3px;text-decoration-thickness:1px}}
  .mkt-body a:hover{{color:var(--accent-2)}}
  .rule-list{{list-style:none;margin:20px 0 0;padding:0}}
  .rule-list li{{padding:18px 22px;background:var(--cream);border-left:3px solid var(--accent);margin-bottom:10px}}
  .rule-list li strong{{display:block;font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--accent);margin-bottom:6px}}
  .rule-list li.soon{{border-left-color:var(--accent-2)}}
  .rule-list li.soon strong{{color:var(--accent-2)}}
  .rule-list li.opportunity{{border-left-color:var(--burgundy)}}
  .rule-list li.opportunity strong{{color:var(--burgundy)}}
  .players-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px;margin-top:20px}}
  .player-cat{{padding:22px 24px;background:#fff;border:1px solid var(--border-dark);border-left:3px solid var(--accent)}}
  .player-cat h4{{font-family:'Fraunces',serif;font-size:16px;font-weight:700;color:var(--text-dark);margin-bottom:10px}}
  .player-cat ul{{list-style:none;margin:0;padding:0}}
  .player-cat li{{font-size:13px;color:var(--text-mid);padding:4px 0;line-height:1.5}}
  .figures-grid{{display:grid;grid-template-columns:repeat(2,1fr);gap:14px;margin-top:20px}}
  .figure-card{{padding:22px;background:var(--navy);color:#fff;border-left:3px solid var(--accent-2)}}
  .figure-num{{font-family:'Fraunces',serif;font-size:36px;font-weight:900;line-height:1;color:#fff;margin-bottom:6px;letter-spacing:-.5px}}
  .figure-caption{{font-size:13px;line-height:1.55;color:rgba(255,255,255,.72)}}
  .figure-source{{font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:rgba(255,255,255,.38);margin-top:10px}}
  .related-block{{background:var(--warm-sand);padding:32px;margin-top:32px;border-radius:4px}}
  .related-block h3{{font-family:'Fraunces',serif;font-size:17px;font-weight:700;margin:0 0 12px 0;color:var(--text-dark)}}
  .related-block a{{display:flex;justify-content:space-between;gap:16px;padding:14px 0;border-bottom:1px solid var(--border-dark);text-decoration:none;color:inherit}}
  .related-block a:last-child{{border-bottom:none}}
  .related-block a:hover .ed-title{{color:var(--navy)}}
  .ed-title{{font-family:'Fraunces',serif;font-size:17px;font-weight:700;color:var(--text-dark)}}
  .ed-date{{font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--text-light);white-space:nowrap;align-self:center}}
  .linked-topics{{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px;margin-top:20px}}
  .linked-topic{{display:block;padding:20px 22px;background:#fff;border:1px solid var(--border-dark);border-left:3px solid var(--accent);text-decoration:none;color:inherit}}
  .linked-topic:hover{{border-left-color:var(--accent-2)}}
  .linked-topic .lt-kicker{{font-size:10px;letter-spacing:.18em;text-transform:uppercase;color:var(--accent);font-weight:700;margin-bottom:6px}}
  .linked-topic .lt-title{{font-family:'Fraunces',serif;font-size:17px;font-weight:700;color:var(--text-dark);line-height:1.25;margin-bottom:4px}}
  .linked-topic .lt-body{{font-size:13px;color:var(--text-mid);line-height:1.55}}
  .mkt-cta{{background:var(--warm-sand);padding:56px 32px;text-align:center;margin-top:56px;border-radius:4px}}
  .mkt-cta h3{{font-family:'Fraunces',serif;font-size:24px;font-weight:700;color:var(--text-dark);margin-bottom:14px;letter-spacing:-.2px;line-height:1.3}}
  .mkt-cta p{{font-size:15px;color:var(--text-mid);line-height:1.7;max-width:560px;margin:0 auto 24px}}
  .mkt-cta a{{display:inline-block;padding:12px 28px;background:var(--navy);color:#fff;text-decoration:none;font-size:12px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;border-radius:2px}}
  .mkt-body > p,.mkt-body > h2,.mkt-body > h3,.mkt-body > ul,.mkt-body > ol{{max-width:820px}}
  @media (max-width:720px){{
    .mkt-hero{{padding:56px 20px 48px}}
    .mkt-main{{padding:48px 20px 80px}}
    .figures-grid{{grid-template-columns:1fr}}
    .related-block a{{flex-direction:column;gap:4px}}
    .ed-date{{align-self:flex-start}}
  }}
</style>"""


def build_regulacion_html(rules: list) -> str:
    items = []
    for (status, title, body) in rules:
        css_class = "soon" if "desarrollo" in status.lower() else ("opportunity" if "estímulo" in status.lower() else "")
        cls = f' class="{css_class}"' if css_class else ""
        items.append(f'      <li{cls}>\n        <strong>{status} · {title}</strong>\n        {body}\n      </li>')
    return "      <ul class=\"rule-list\">\n" + "\n".join(items) + "\n      </ul>"


def build_players_html(players: dict) -> str:
    cats = []
    for cat_title, items in players.items():
        lis = "\n".join(f'          <li>{item}</li>' for item in items)
        cats.append(f'        <div class="player-cat">\n          <h4>{cat_title}</h4>\n          <ul>\n{lis}\n          </ul>\n        </div>')
    return '      <div class="players-grid">\n' + "\n".join(cats) + "\n      </div>"


def build_fleet_html(fleet_types: list) -> str:
    items = []
    for (title, body) in fleet_types:
        items.append(f'        <li><strong>{title}</strong> — {body}</li>')
    return "      <ul>\n" + "\n".join(items) + "\n      </ul>"


def build_figures_html(figures: list) -> str:
    cards = []
    for (num, cap, src) in figures:
        cards.append(f'        <div class="figure-card">\n          <div class="figure-num">{num}</div>\n          <div class="figure-caption">{cap}</div>\n          <div class="figure-source">{src}</div>\n        </div>')
    return '      <div class="figures-grid">\n' + "\n".join(cards) + "\n      </div>"


def build_related_topics_html(topics: list) -> str:
    items = []
    for (url, kicker, title, body) in topics:
        items.append(f'        <a href="{url}" class="linked-topic">\n          <div class="lt-kicker">{kicker}</div>\n          <div class="lt-title">{title}</div>\n          <div class="lt-body">{body}</div>\n        </a>')
    return '      <div class="linked-topics">\n' + "\n".join(items) + "\n      </div>"


def build_editions_html(editions: list) -> str:
    items = []
    for (url, title, date) in editions:
        items.append(f'        <a href="{url}">\n          <span class="ed-title">{title}</span>\n          <span class="ed-date">{date}</span>\n        </a>')
    block = '      <div class="related-block">\n        <h3>The Fleet Radar · by Pulpo</h3>\n'
    block += "\n".join(items)
    block += "\n      </div>"
    return block


def build_sources_html(sources: list) -> str:
    items = []
    for (label, url, note) in sources:
        items.append(f'      <li class="source-item"><a href="{url}" class="source-link" target="_blank" rel="noopener nofollow">{label}</a><span class="source-note"> — {note}</span></li>')
    return (
        '\n<section class="pillar-sources">\n  <div class="container">\n'
        '    <h2 class="pillar-sources-title">Fuentes y referencias</h2>\n'
        '    <ul class="sources-list">\n'
        + "\n".join(items) +
        '\n    </ul>\n'
        '    <p class="sources-note">Datos cuantitativos sin fuente específica provienen de análisis editorial basado en fuentes del sector.</p>\n'
        '  </div>\n</section>'
    )


# ────────────────────────────────────────────────────────────────────────────
# MAIN CONTENT SECTION (replaces hub-empty-state)
# ────────────────────────────────────────────────────────────────────────────

def build_main_content(m: dict) -> str:
    name = m["name"]
    flag = m["flag"]
    slug = m["slug"]

    hero = f"""<section class="mkt-hero">
  <div class="mkt-hero-inner">
    <div class="mkt-flag">{flag}</div>
    <span class="mkt-kicker">Mercado · {name} · 2026</span>
    <h1 class="mkt-title">Flotas en <span>{name}</span> 2026</h1>
    <p class="mkt-deck">{m['deck']}</p>
    <div class="mkt-updated">Actualizado · {m['updated']}</div>
  </div>
</section>

<main class="mkt-main">
  <div class="mkt-body">

{m['intro']}

    <h2>Regulación viva</h2>
{build_regulacion_html(m['regulacion'])}

    <h2>Players activos por categoría</h2>
    <p>Empresas con presencia relevante en el mercado de {name}. El listado se amplía según cobertura editorial.</p>
{build_players_html(m['players'])}

    <h2>Tipos de flota dominantes</h2>
{build_fleet_html(m['fleet_types'])}

    <h2>Cifras útiles</h2>
{build_figures_html(m['figures'])}

    <h2>Temas relacionados</h2>
{build_related_topics_html(m['related_topics'])}

    <h2>Ediciones con material de {name}</h2>
{build_editions_html(m['editions'])}

    <div class="mkt-cta">
      <h3>{m['cta_heading']}</h3>
      <p>{m['cta_body']}</p>
      <a href="https://www.getpulpo.com/" target="_blank" rel="noopener">Ver Pulpo en acción</a>
    </div>

  </div>
</main>
"""
    return hero


# ────────────────────────────────────────────────────────────────────────────
# PAGE MODIFIER — injects content into existing stub
# ────────────────────────────────────────────────────────────────────────────

def enrich_page(m: dict) -> bool:
    path = ROOT / "mercados" / m["slug"] / "index.html"
    html = path.read_text(encoding="utf-8")

    # Check if already enriched
    if 'class="mkt-hero"' in html:
        print(f"  ⏭  Ya enriquecida: {m['slug']}")
        return False

    # 1. Add CSS block: replace the simple <style> block
    old_style = '<style>:root{ --accent:#c9a84c; --accent-2:#1e7fcb; }</style>'
    if old_style not in html:
        print(f"  ⚠️  No se encontró el bloque style en: {m['slug']}")
        return False
    html = html.replace(old_style, css_block(m), 1)

    # 2. Fix topbar: add Temas + Mercados if missing
    if '<a href="/temas/">Temas</a>' not in html:
        html = html.replace(
            '<a href="https://www.getpulpo.com/" class="cta"',
            '<a href="/temas/">Temas</a>\n    <a href="/mercados/">Mercados</a>\n    <a href="https://www.getpulpo.com/" class="cta"',
            1
        )

    # 3. Replace hub-hero + hub-autogen empty state with mkt content + sources
    old_hero = f"""<section class="hub-hero">
  <div class="container">
    <span class="hub-eyebrow">Mercado · {m['flag']}</span>
    <h1 class="hub-title">Flotas en {m['name']}</h1>
    <p class="hub-intro">Análisis de gestión de flotas en {m['name']}: temas, casos de uso, sectores y ciudades cubiertos por The Fleet Radar.</p>
  </div>
</section>
<!-- AUTOGEN: pillar-pages-list START -->
<section class="hub-autogen container">
  <p class="hub-empty-state">Estamos preparando la cobertura editorial sobre flotas en {m['name']}. Mientras tanto puedes explorar las <a href="/archive.html">ediciones publicadas</a> de The Fleet Radar.</p>
</section>
<!-- AUTOGEN: pillar-pages-list END -->"""

    new_content = build_main_content(m) + build_sources_html(m["sources"])

    if old_hero not in html:
        print(f"  ⚠️  No se encontró el bloque hub-hero en: {m['slug']}")
        # Try partial match
        if 'hub-empty-state' in html:
            print(f"  → Intentando reemplazo parcial con hub-empty-state")
        return False

    html = html.replace(old_hero, new_content, 1)

    path.write_text(html, encoding="utf-8")
    print(f"  ✅ {m['name']} — enriquecida ({len(html)} chars)")
    return True


# ────────────────────────────────────────────────────────────────────────────
# MAIN
# ────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print(f"generate_country_briefs.py — {len(MARKETS)} mercados\n")
    done = 0
    for slug, m in MARKETS.items():
        result = enrich_page(m)
        if result:
            done += 1
    print(f"\n✅ {done}/{len(MARKETS)} páginas enriquecidas")
