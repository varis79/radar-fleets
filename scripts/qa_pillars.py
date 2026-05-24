#!/usr/bin/env python3
"""
qa_pillars.py — Validator editorial específico para páginas pillar.

Detecta el patrón de auditoría 2026-05-24: cifras específicas atribuidas
a empresas privadas sin fuente verificable. Bloquea la build/PR si una
página tiene riesgo editorial alto.

Reglas:
  - R1: >5 porcentajes "[Empresa privada] N%" sin fuente cercana → FAIL
  - R2: Menciones de cifras absolutas (>3 dígitos) atribuidas a empresa
        privada sin link en mismo párrafo → WARN (≥3) / FAIL (≥6)
  - R3: Frases "el X% del mercado" sin source → WARN
  - R4: Empresas privadas mencionadas con número exacto + sin <a href=> en
        mismo párrafo → counted como sospechoso

Uso:
  # Auditar todas las pillars
  python3 scripts/qa_pillars.py

  # Auditar una sola
  python3 scripts/qa_pillars.py --file temas/foo/index.html

  # Solo páginas modificadas vs main
  python3 scripts/qa_pillars.py --changed-only

Exit codes:
  0 — OK (ninguna página falla)
  1 — Al menos una página falla (R1 o R2 ≥ 6)
"""
import sys
# Python añade scripts/ a sys.path[0] al ejecutar este file; eso hace que
# `import select` resuelva nuestro scripts/select.py en vez del stdlib.
# Limpiamos antes de cualquier import que pueda llevar a `select`.
if sys.path and sys.path[0].endswith("/scripts"):
    sys.path.pop(0)

import os
import re
import argparse
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).parent.parent

# Empresas privadas frecuentemente mencionadas (riesgo editorial)
PRIVATE_BRANDS = [
    "DHL", "FedEx", "UPS", "Amazon", "MercadoLibre", "Mercado Libre", "MeLi",
    "Uber", "Cabify", "Didi", "Rappi", "Cornershop", "99 Minutos", "Estafeta",
    "Redpack", "Bimbo", "Coca-Cola", "FEMSA", "Sigma", "Lala", "OXXO",
    "Walmart", "Soriana", "Chedraui", "Liverpool", "El Palacio",
    "Mercadona", "Inditex", "Zara", "El Corte Inglés", "Carrefour",
    "Iberia", "Repsol", "Cepsa", "BP", "Shell", "TotalEnergies", "Mobil",
    "BYD", "Tesla", "Volvo", "Mercedes", "Scania", "MAN", "Iveco",
    "Renault", "Ford", "Chevrolet", "Kenworth", "Freightliner",
    "International", "Hino", "Foton", "JAC", "Toyota", "Nissan",
    "Samsara", "Geotab", "Webfleet", "Position Logic", "Omnitracs",
    "WEX", "Edenred", "Solred", "Pluxee", "Sodexo",
    "Endesa", "Iberdrola", "Naturgy", "EDP", "Engie",
    "Telcel", "AT&T", "Movistar", "Telefónica", "Telmex",
    "Grupo Modelo", "Grupo Aralo", "Grupo Bimbo", "Grupo TMM", "Castores",
    "Traxión", "Grupo Nabeiro", "American Tower",
    "ICA", "Carso", "IDEAL", "Hycsa", "Cemex", "Domicem",
    "Pemex Logística", "CFE",  # CFE/Pemex normalmente públicos pero a veces específicos
    "PepsiCo", "Nestlé",
    "SEUR", "MRW", "GLS", "Correos Express", "Nacex",
    "Wenea", "Endesa X", "BeMobile",
    "Avatel", "Megacable", "Totalplay", "Izzi",
]

# Whitelist: instituciones públicas / fuentes citables (no cuentan como riesgo)
PUBLIC_INSTITUTIONS = [
    "SAT", "SICT", "SCT", "DGT", "IMSS", "INFONAVIT", "INEGI", "ANFAC",
    "CANACAR", "AMEG", "AMVO", "ANT", "MTOP", "CRE", "CNH", "CNBV",
    "Pemex", "CFE",  # tratadas como publicas
    "Pulpo", "PulpoPay",  # propias
    "Banco Central", "BCE",
    "DOF", "BOE",
    "Samsara", # cuando es su propio dato (auto-fuente)
]


def _has_nearby_source(text: str, position: int, window: int = 200) -> bool:
    """¿Hay una fuente EXTERNA citada cerca? Solo links externos cuentan
    como source (link interno = no source). Frases de atribución + nombres
    de instituciones públicas también cuentan.
    """
    nearby = text[max(0, position - window):position + window]
    # Link EXTERNO (no a thefleetradar.com, no relativo)
    for m in re.finditer(r'<a\s+[^>]*href=["\']([^"\']+)', nearby, re.IGNORECASE):
        href = m.group(1)
        if href.startswith("http") and "thefleetradar.com" not in href:
            return True
    if re.search(r'\b(según|fuente|reportó|publicó|comunicado|informe|estudio|cita)\b',
                 nearby, re.IGNORECASE):
        return True
    # Match institution con word boundaries (evita falsos positivos:
    # "ANT" no debe matchear "mANTenimiento", "BCE" no "compraBCE")
    for inst in PUBLIC_INSTITUTIONS:
        if re.search(rf'\b{re.escape(inst)}\b', nearby):
            return True
    return False


def _body_text(soup: BeautifulSoup) -> str:
    """Devuelve solo el cuerpo editorial (sin head/nav/script/style)."""
    for el in soup.find_all(["script", "style", "nav", "header", "footer",
                              "meta", "aside"]):
        el.decompose()
    main = soup.find("main") or soup
    return str(main)


def check_page(path: Path) -> dict:
    """Devuelve dict con counts de issues encontrados."""
    text = path.read_text(encoding="utf-8")
    soup = BeautifulSoup(text, "html.parser")
    body_html = _body_text(soup)

    issues = {"r1_pct": [], "r2_abs": [], "r3_market_share": []}

    # R1: [Brand] [whitespace] [number]% — sin fuente cercana
    for brand in PRIVATE_BRANDS:
        # Patrón: Brand seguido de hasta 80 chars y un número%
        pattern = re.compile(
            rf'\b{re.escape(brand)}\b[^.]{{0,80}}\b(\d+(?:[.,]\d+)?)\s*%',
            re.IGNORECASE,
        )
        for m in pattern.finditer(body_html):
            if not _has_nearby_source(body_html, m.start()):
                snippet = body_html[max(0,m.start()-30):min(len(body_html),m.end()+30)]
                snippet = re.sub(r'<[^>]+>', '', snippet).strip()
                issues["r1_pct"].append((brand, m.group(1), snippet[:120]))

    # R2: [Brand] + número 3+ dígitos sin fuente
    # Incluye formatos: 1234, 1.234, 1,234, 1.234.567 (miles europeos)
    for brand in PRIVATE_BRANDS:
        pattern = re.compile(
            rf'\b{re.escape(brand)}\b[^.]{{0,80}}\b(\d{{1,3}}(?:[.,]\d{{3}})+|\d{{3,}})\b',
            re.IGNORECASE,
        )
        for m in pattern.finditer(body_html):
            if not _has_nearby_source(body_html, m.start()):
                num_raw = m.group(1)
                num_clean = num_raw.replace(".", "").replace(",", "")
                try:
                    num_int = int(num_clean)
                except ValueError:
                    continue
                # Filtros para evitar falsos positivos
                if num_int < 100:
                    continue
                # Año aislado (2020-2030)
                if 2020 <= num_int <= 2030 and "." not in num_raw and "," not in num_raw:
                    continue
                snippet = body_html[max(0,m.start()-30):min(len(body_html),m.end()+30)]
                snippet = re.sub(r'<[^>]+>', '', snippet).strip()
                issues["r2_abs"].append((brand, num_raw, snippet[:120]))

    # R3: cuota de mercado sin fuente
    for m in re.finditer(r'(\d+(?:[.,]\d+)?)\s*%\s*(?:del\s+)?mercado',
                         body_html, re.IGNORECASE):
        if not _has_nearby_source(body_html, m.start()):
            issues["r3_market_share"].append((m.group(1),))

    return issues


def assess(issues: dict) -> tuple[str, str]:
    """Devuelve (status, reason) — status ∈ {OK, WARN, FAIL}"""
    r1 = len(issues["r1_pct"])
    r2 = len(issues["r2_abs"])
    r3 = len(issues["r3_market_share"])
    if r1 >= 5 or r2 >= 6:
        return ("FAIL", f"R1={r1}, R2={r2} (umbral excedido)")
    if r1 >= 3 or r2 >= 3 or r3 >= 3:
        return ("WARN", f"R1={r1}, R2={r2}, R3={r3}")
    return ("OK", "")


def changed_files() -> list[Path]:
    """Files modified vs origin/main, pillars only.

    Usamos os.popen para evitar el conflicto entre `subprocess`→`select`
    y nuestro scripts/select.py.
    """
    cmd = "git diff --name-only origin/main"
    with os.popen(f"cd '{ROOT}' && {cmd}") as p:
        output = p.read()
    paths = []
    for line in output.splitlines():
        p = ROOT / line
        if p.exists() and p.name == "index.html" and any(
            seg in line for seg in ("temas/", "mercados/", "casos-uso/",
                                     "sectores/", "ciudades/", "evergreen/")
        ):
            paths.append(p)
    return paths


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="Audit a specific file")
    parser.add_argument("--changed-only", action="store_true",
                        help="Only files changed vs origin/main")
    parser.add_argument("--verbose", action="store_true",
                        help="Show all matches per page")
    args = parser.parse_args()

    if args.file:
        files = [Path(args.file)]
    elif args.changed_only:
        files = changed_files()
        if not files:
            print("No pillar files changed.")
            return 0
    else:
        files = []
        for section in ("temas", "mercados", "casos-uso", "sectores",
                        "ciudades", "evergreen"):
            d = ROOT / section
            if d.exists():
                files.extend(sorted(d.rglob("index.html")))

    print(f"\nqa_pillars.py — auditando {len(files)} páginas\n")
    fail_count = warn_count = ok_count = 0
    failures = []

    for p in files:
        issues = check_page(p)
        status, reason = assess(issues)
        rel = p.relative_to(ROOT)
        if status == "FAIL":
            fail_count += 1
            print(f"  ❌ FAIL  {rel}  {reason}")
            failures.append((rel, issues))
        elif status == "WARN":
            warn_count += 1
            if args.verbose:
                print(f"  ⚠️  WARN  {rel}  {reason}")
        else:
            ok_count += 1

    print(f"\nResumen: {ok_count} OK · {warn_count} WARN · {fail_count} FAIL")

    if failures and (args.verbose or fail_count <= 5):
        print("\n=== DETALLE FAILS ===")
        for rel, issues in failures[:5]:
            print(f"\n  {rel}:")
            for brand, pct, ctx in issues["r1_pct"][:5]:
                print(f"    R1 → {brand} {pct}%: {ctx!r}")
            for brand, num, ctx in issues["r2_abs"][:5]:
                print(f"    R2 → {brand} {num}: {ctx!r}")

    return 1 if fail_count > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
