#!/usr/bin/env python3
"""
rotate_facts.py — Inyecta/actualiza una caja "💡 Sabías qué" rotatoria en
páginas pilar. El contenido rota cada semana basado en (isoweek + page_hash).

Esto cambia el contenido visible de cada página cada ~30 semanas (pool de 30
facts), generando cambios reales para Google sin reescribir cuerpo editorial.

Estrategia:
  - Pool de 30 facts factuales sobre el sector flota (MX/ES/LatAm)
  - Cada página recibe: fact[(isoweek + sha1(page_url)) % len(pool)]
  - Inyecta <aside class="did-you-know"> después de la primera <section>
  - Idempotente dentro de la misma semana

Uso:
    python3 scripts/rotate_facts.py [--dry-run]
"""
import sys
import hashlib
import datetime as dt
from pathlib import Path
from bs4 import BeautifulSoup, Tag

DRY_RUN = "--dry-run" in sys.argv
ROOT = Path(__file__).parent.parent

# ── Pool de 30 facts editoriales (rota cada ~30 semanas por página) ──────────
FACTS = [
    # ── Combustible / fuel cards ──
    ("⛽ Combustible", "En México, el combustible representa entre el 38% y el 45% del coste operativo de una flota comercial — la categoría más impactante en el TCO según análisis del sector."),
    ("⛽ Combustible", "España exige tacógrafo digital en todos los vehículos >3,5 t desde 2006. La sanción por manipulación puede superar los 4.600 € por unidad, según la DGT."),
    ("⛽ Combustible", "Las flotas con tarjetas de combustible reportan entre 5% y 12% de reducción de fraude vs. reembolsos manuales, según benchmarks del sector en MX y ES."),
    ("⛽ Combustible", "El consumo de diésel en México pasó de subsidiado a libre mercado en 2014. Hoy el precio se ajusta semanalmente y representa el ~32% del precio final como impuestos."),

    # ── Telemática / GPS ──
    ("📡 Telemática", "Una flota con telemática reduce el siniestros entre 18% y 31% según datos de Geotab y Samsara aplicados a flotas LatAm de >100 unidades."),
    ("📡 Telemática", "El mercado de telemática para flotas en México crece a tasas del 18-22% anual, según ABI Research y análisis del sector publicados en 2025."),
    ("📡 Telemática", "La penetración de telemática en flotas medianas españolas supera el 60%, frente al 35% estimado en México — una de las brechas regulatorias más visibles."),
    ("📡 Telemática", "Samsara, Geotab y Webfleet (Bridgestone) concentran ~55% del mercado enterprise de telemática en LatAm, con un parque competidor local fragmentado."),

    # ── Regulación ──
    ("⚖️ Regulación", "Desde el 1 de enero de 2026, la baliza V-16 conectada es obligatoria en España para todos los vehículos. Sustituye a los triángulos clásicos y emite ubicación al sistema DGT 3.0."),
    ("⚖️ Regulación", "México cuenta con más de 800 reglas técnicas (NOM) aplicables al autotransporte. La NOM-012-SCT-2 regula pesos y dimensiones; la NOM-068 los requisitos físico-mecánicos."),
    ("⚖️ Regulación", "España tiene 149 municipios obligados a desplegar Zonas de Bajas Emisiones (ZBE) por la Ley 7/2021. Madrid Central, Rondes de Barcelona y Valencia están entre las más activas."),
    ("⚖️ Regulación", "El T-MEC obliga a México, EE.UU. y Canadá a homologar progresivamente normativas de transporte. La auditoría intermedia de 2026 marcará el avance del sector."),

    # ── Electrificación ──
    ("⚡ Electrificación", "Las matriculaciones de vehículos comerciales eléctricos en España crecieron 34% en 2025 según ANFAC. Madrid y Barcelona concentran el 58% del parque."),
    ("⚡ Electrificación", "Santiago de Chile opera más de 2.000 buses eléctricos: la mayor flota fuera de China. BYD y Yutong son los proveedores dominantes del sistema RED."),
    ("⚡ Electrificación", "El programa Olinia de México busca producir un vehículo eléctrico nacional accesible. Coordinado por la Secretaría de Economía con apoyo industrial mixto público-privado."),
    ("⚡ Electrificación", "El TCO de una furgoneta eléctrica vs. diésel se iguala a partir de los 35.000 km/año, según análisis IDAE 2025. Por debajo de ese umbral, sigue ganando el diésel."),

    # ── Mantenimiento ──
    ("🔧 Mantenimiento", "El mantenimiento preventivo bien planificado representa entre el 10% y 16% del TCO. El correctivo, sin preventivo, dispara la cifra al 18-22%."),
    ("🔧 Mantenimiento", "El mantenimiento predictivo basado en telemetría reduce paradas no planificadas entre 25% y 40% según casos publicados por DHL y Saint-Gobain."),
    ("🔧 Mantenimiento", "Un neumático mal inflado puede aumentar el consumo de combustible entre 3% y 6%. Es el control de bajo coste con mayor retorno operativo en flota."),

    # ── Compliance / fraude ──
    ("🛡️ Compliance", "El fraude de combustible en México oscila entre 4% y 9% del consumo total de flotas según estimaciones de la AMEG y proveedores de fuel cards."),
    ("🛡️ Compliance", "El robo de carga en México registró 10.367 incidentes en 2025, según Samsara. El 72% se recupera en menos de 48 horas si la flota tiene telemetría."),
    ("🛡️ Compliance", "El IMSS multa con hasta 100 UMAs (~10.000 MXN) por unidad sin alta correcta de conductor. Las flotas grandes acumulan riesgo significativo."),

    # ── Operación ──
    ("📦 Operación", "La última milla representa entre 28% y 53% del coste total de la cadena logística urbana, según McKinsey 2024 — la mayor presión está en MX y ES."),
    ("📦 Operación", "Cada 1% de mejora en la utilización de la flota (vehículo en marcha vs. parado) puede traducirse en ~$50.000 USD/año de ahorro en una flota de 100 unidades."),
    ("📦 Operación", "El churn de conductores en transporte mexicano supera el 25% anual. El programa de retención y bonos por kilómetro es el principal lever operativo."),

    # ── Mercado / players ──
    ("🏢 Mercado", "El parque vehicular comercial mexicano supera los 4,5 millones de unidades. Solo 35% opera con software de gestión integral, según análisis sectorial."),
    ("🏢 Mercado", "ALD y Arval (Société Générale) lideran el mercado de renting corporativo en España con más de 25% combinado del nuevo registro empresarial."),
    ("🏢 Mercado", "El sector logístico mexicano representa ~14% del PIB, según el IMT. España: 8% del PIB, con tendencia al alza por nearshoring europeo."),

    # ── Datos & costes ──
    ("💰 Costes", "Una unidad mediana en México (Sprinter o NPR) tiene un coste operativo medio de $4.80 MXN/km, con rango de $3.50 a $6.20 según uso y tecnología."),
    ("💰 Costes", "El coste por km de un tractocamión en España oscila entre 1,15 € y 1,42 € según el Observatorio del Transporte del Ministerio de Transportes (2025)."),
]


def _format_box(category: str, text: str) -> str:
    """HTML de la caja Sabías qué."""
    return (
        f'<aside class="did-you-know">'
        f'<span class="dyk-eyebrow">💡 Sabías qué · {category}</span>'
        f'<p class="dyk-body">{text}</p>'
        f'</aside>'
    )


def _pick_fact(rel_path: str, today: dt.date) -> tuple[str, str]:
    iso_year, iso_week, _ = today.isocalendar()
    page_hash = int(hashlib.sha1(rel_path.encode()).hexdigest(), 16)
    idx = (iso_week + page_hash) % len(FACTS)
    return FACTS[idx]


def process_file(path: Path, today: dt.date) -> bool:
    text = path.read_text(encoding="utf-8")
    soup = BeautifulSoup(text, "html.parser")

    rel = str(path.relative_to(ROOT))
    cat, fact_text = _pick_fact(rel, today)
    new_html = _format_box(cat, fact_text)
    new_soup = BeautifulSoup(new_html, "html.parser")
    new_box = new_soup.find("aside")

    # Buscar caja existente para reemplazar/comparar
    existing = soup.find("aside", class_="did-you-know")
    if existing:
        if existing.get_text(" ", strip=True) == new_box.get_text(" ", strip=True):
            return False  # mismo fact, no tocar (idempotente esta semana)
        existing.replace_with(new_box)
    else:
        # Inyectar después del primer .pillar-body o .mkt-main o equivalente
        anchor = (soup.find(class_="pillar-body") or soup.find(class_="mkt-main")
                  or soup.find(class_="pillar-section") or soup.find("section"))
        if anchor is None:
            return False
        anchor.insert_after(new_box)

    if not DRY_RUN:
        path.write_text(str(soup), encoding="utf-8")
    return True


def main():
    today = dt.date.today()
    iso_year, iso_week, _ = today.isocalendar()
    mode = "[DRY-RUN]" if DRY_RUN else "[LIVE]"
    print(f"\nrotate_facts.py {mode}  today={today.isoformat()} (W{iso_week})\n")
    print(f"  Pool de facts: {len(FACTS)}\n")

    files = []
    for section in ("temas", "mercados", "casos-uso", "sectores", "ciudades"):
        d = ROOT / section
        if d.exists():
            files.extend(sorted(d.rglob("index.html")))

    touched = 0
    for path in files:
        if process_file(path, today):
            touched += 1
            if DRY_RUN:
                rel = str(path.relative_to(ROOT))
                cat, _ = _pick_fact(rel, today)
                print(f"  [DRY] {rel}  → {cat}")

    print(f"\n  Total cajas actualizadas: {touched} / {len(files)}")


if __name__ == "__main__":
    main()
