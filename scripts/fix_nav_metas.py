#!/usr/bin/env python3
"""
fix_nav_metas.py — Arregla labels mal asignados de topbar-meta por sección.

Antes:
  casos-uso/  →  "Página pilar · México" (WRONG, no son pillars)
  sectores/   →  "Página pilar · España" (WRONG)
  ciudades/   →  "Página pilar · México" (WRONG)
  evergreens variantes inconsistentes

Después:
  casos-uso/  →  "Caso de uso · México"
  sectores/   →  "Sector · México"
  ciudades/   →  "Ciudad · CDMX" (deriva de slug)
  evergreen/checklists/   →  "Checklist · México" o "España"
  evergreen/guias/        →  "Guía · Europa"

Idempotente.
"""
import re
import sys
from pathlib import Path
from bs4 import BeautifulSoup

DRY_RUN = "--dry-run" in sys.argv
ROOT = Path(__file__).parent.parent


def _market_from_path(name: str) -> str:
    if "-mexico-" in name or name.endswith("-mexico") or "-mx-" in name or name.endswith("-mx"):
        return "México"
    if "-espana-" in name or name.endswith("-espana") or "-es-" in name or name.endswith("-es"):
        return "España"
    if "-europa-" in name or name.endswith("-europa"):
        return "Europa"
    return ""


def _city_from_slug(slug: str) -> str:
    """ciudades/telematica-flotas-cdmx-2026 → CDMX"""
    cities = {
        "cdmx": "CDMX", "ciudad-de-mexico": "CDMX",
        "guadalajara": "Guadalajara", "monterrey": "Monterrey",
        "puebla": "Puebla", "leon": "León", "queretaro": "Querétaro",
        "tijuana": "Tijuana", "merida": "Mérida", "juarez": "Cd. Juárez",
        "madrid": "Madrid", "barcelona": "Barcelona", "valencia": "Valencia",
        "sevilla": "Sevilla", "bilbao": "Bilbao", "zaragoza": "Zaragoza",
        "malaga": "Málaga",
        "bogota": "Bogotá", "medellin": "Medellín", "cali": "Cali",
        "barranquilla": "Barranquilla", "santiago": "Santiago",
        "buenos-aires": "Buenos Aires", "lima": "Lima",
    }
    parts = slug.split("-")
    # Probar cualquier subsecuencia contigua (cubre slugs como "telematica-flotas-monterrey-2026")
    for i in range(len(parts)):
        for j in range(len(parts), i, -1):
            candidate = "-".join(parts[i:j])
            if candidate in cities:
                return cities[candidate]
    return ""


def label_for(path: Path) -> str | None:
    """Devuelve el label correcto para el topbar-meta, o None si no toca."""
    rel = str(path.relative_to(ROOT))
    parts = rel.split("/")

    if parts[0] == "casos-uso" and parts[1] != "index.html":
        m = _market_from_path(parts[1])
        return f"Caso de uso · {m}" if m else "Caso de uso"
    if parts[0] == "sectores" and parts[1] != "index.html":
        m = _market_from_path(parts[1])
        return f"Sector · {m}" if m else "Sector"
    if parts[0] == "ciudades" and parts[1] != "index.html":
        city = _city_from_slug(parts[1])
        return f"Ciudad · {city}" if city else "Ciudad"
    if parts[0] == "evergreen" and len(parts) >= 3:
        cat = parts[1]
        m = _market_from_path(parts[2])
        if cat == "checklists":
            return f"Checklist · {m}" if m else "Checklist"
        if cat == "guias":
            return f"Guía · {m}" if m else "Guía"
    return None  # other sections: leave alone


def process_file(path: Path) -> bool:
    new_label = label_for(path)
    if new_label is None:
        return False
    text = path.read_text(encoding="utf-8")
    soup = BeautifulSoup(text, "html.parser")
    meta = soup.find(class_="topbar-meta")
    if not meta:
        return False
    if meta.get_text(strip=True) == new_label:
        return False
    meta.clear()
    meta.append(new_label)
    if not DRY_RUN:
        path.write_text(str(soup), encoding="utf-8")
    return True


def main():
    mode = "[DRY-RUN]" if DRY_RUN else "[LIVE]"
    print(f"\nfix_nav_metas.py {mode}\n")
    n = 0
    for sec in ("casos-uso", "sectores", "ciudades", "evergreen"):
        d = ROOT / sec
        if not d.exists():
            continue
        for p in sorted(d.rglob("index.html")):
            if process_file(p):
                n += 1
                rel = p.relative_to(ROOT)
                lbl = label_for(p)
                marker = "[DRY]" if DRY_RUN else "  ✅"
                print(f"  {marker} {rel} → {lbl!r}")
    print(f"\n  Total updated: {n}")


if __name__ == "__main__":
    main()
