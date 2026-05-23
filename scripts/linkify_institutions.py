#!/usr/bin/env python3
"""
linkify_institutions.py — Añade enlaces externos a organismos e instituciones
mencionados en el cuerpo de texto de páginas pilar y hubs de mercado.

Estrategia:
  - Usa BeautifulSoup para operar SOLO en nodos de texto dentro de elementos
    <p>, <li>, <td>, <div class="pillar-body|mkt-intro|e-body|rule-list">
  - Nunca toca atributos HTML (meta, href, alt, title, etc.)
  - Solo primera mención de cada institución por página
  - Idempotente: no re-enlaza si el texto ya está dentro de un <a>
  - class="ext-link" en cada enlace generado

Uso:
    python3 scripts/linkify_institutions.py [--dry-run]
    python3 scripts/linkify_institutions.py [--dir temas]
"""
import sys
import re
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString, Tag

DRY_RUN = "--dry-run" in sys.argv

ROOT = Path(__file__).parent.parent

# ── Directorios a procesar ──────────────────────────────────────────────────
TARGET_DIRS = ["temas", "mercados", "evergreen"]
for i, arg in enumerate(sys.argv):
    if arg == "--dir" and i + 1 < len(sys.argv):
        TARGET_DIRS = [sys.argv[i + 1]]

# ── Organismos → URL oficial ────────────────────────────────────────────────
INSTITUTIONS: list[tuple[str, str]] = [
    # ── México ──
    ("SAT",         "https://www.sat.gob.mx/"),
    ("SICT",        "https://www.sct.gob.mx/"),
    ("SCT",         "https://www.sct.gob.mx/"),
    ("CANACAR",     "https://www.canacar.com.mx/"),
    ("CNH",         "https://www.gob.mx/cnh"),
    ("CNBV",        "https://www.cnbv.gob.mx/"),
    ("CRE",         "https://www.gob.mx/cre"),
    ("IMSS",        "https://www.imss.gob.mx/"),
    ("INFONAVIT",   "https://portalmx.infonavit.org.mx/"),
    ("NAFIN",       "https://www.nafin.com.mx/"),
    ("AMEG",        "https://www.amegasolineros.org.mx/"),
    ("IMT",         "https://www.imt.mx/"),
    ("INEGI",       "https://www.inegi.org.mx/"),
    ("Pemex",       "https://www.pemex.com/"),
    # ── España ──
    ("DGT",         "https://www.dgt.es/"),
    ("IDAE",        "https://www.idae.es/"),
    ("CNMC",        "https://www.cnmc.es/"),
    ("AEAT",        "https://www.agenciatributaria.es/"),
    # ── Colombia ──
    ("RNDC",        "https://www.mintransporte.gov.co/micrositios/rndc/"),
    ("RUNT",        "https://www.runt.com.co/"),
    ("SuperTransporte", "https://www.supertransporte.gov.co/"),
    # ── Chile ──
    ("MTT",         "https://www.mtt.gob.cl/"),
    # ── Argentina ──
    ("CNRT",        "https://www.argentina.gob.ar/cnrt"),
    # ── Perú ──
    ("SUTRAN",      "https://www.sutran.gob.pe/"),
]

# ── Selectores: qué elementos procesar ──────────────────────────────────────
# Solo elementos de contenido editorial, no navegación ni meta
BODY_SELECTORS = [
    "p.pillar-intro",
    "div.pillar-body",
    "p.mkt-intro",
    "div.mkt-intro",
    "div.rule-list",
    "p.intro-body",
    "div.e-body",
    "p",          # fallback: párrafos dentro de las secciones de arriba
]

# ── Helpers ──────────────────────────────────────────────────────────────────

def _inline_link(label: str, url: str) -> Tag:
    """Crea un elemento <a> BS4."""
    a = Tag(name="a")
    a["href"] = url
    a["class"] = "ext-link"
    a["target"] = "_blank"
    a["rel"] = "noopener nofollow"
    a.string = label
    return a


def _inject_link_in_text_node(node: NavigableString, label: str, url: str) -> bool:
    """
    Divide el NavigableString en partes, insertando un <a> en la primera
    aparición de `label`. Devuelve True si se hizo el reemplazo.
    """
    text = str(node)
    pattern = re.compile(rf'\b{re.escape(label)}\b')
    m = pattern.search(text)
    if not m:
        return False

    parent = node.parent
    idx = list(parent.children).index(node)

    before = text[:m.start()]
    after  = text[m.end():]

    node.replace_with(NavigableString(before))
    # Reinsertamos los fragmentos en el mismo parent
    a_tag = _inline_link(label, url)
    parent.insert(idx + 1, a_tag)
    parent.insert(idx + 2, NavigableString(after))
    return True


def _is_in_anchor(node: NavigableString) -> bool:
    """True si el nodo ya está dentro de un <a>."""
    for parent in node.parents:
        if parent.name == "a":
            return True
        if parent.name in ("body", "[document]"):
            break
    return False


def linkify_soup(soup: BeautifulSoup) -> int:
    """
    Procesa el documento BS4, añadiendo ext-links a instituciones.
    Devuelve el número de enlaces añadidos.
    """
    added = 0
    # Rastreamos qué labels ya hemos enlazado en esta página
    linked: set[str] = set()

    # Recorremos solo el body (nada de <head>)
    body = soup.find("body")
    if not body:
        return 0

    for label, url in INSTITUTIONS:
        if label in linked:
            continue

        # Idempotencia: si ya existe un ext-link con este label, lo saltamos
        existing = body.find(
            lambda tag: tag.name == "a"
            and "ext-link" in (tag.get("class") or [])
            and tag.get_text(strip=True) == label
        )
        if existing:
            linked.add(label)
            continue

        # Buscar todos los nodos de texto en el body que contengan el label
        text_nodes = body.find_all(string=re.compile(rf'\b{re.escape(label)}\b'))
        for node in text_nodes:
            if not isinstance(node, NavigableString):
                continue
            if _is_in_anchor(node):
                continue
            # Solo procesar nodos dentro de elementos de contenido (no nav, no script, etc.)
            parent_names = {p.name for p in node.parents if isinstance(p, Tag)}
            if parent_names & {"script", "style", "meta", "head", "nav", "title"}:
                continue
            if _inject_link_in_text_node(node, label, url):
                linked.add(label)
                added += 1
                break  # primera mención; pasar al siguiente label

    return added


# ── CSS (idempotente) ─────────────────────────────────────────────────────────

def add_css_if_needed() -> None:
    css_path = ROOT / "assets/radar.css"
    css = css_path.read_text(encoding="utf-8")
    if "ext-link" in css:
        return
    block = (
        "\n/* ── External institution links ─────────────────────────────────── */\n"
        ".ext-link{color:inherit;text-decoration:underline;"
        "text-underline-offset:2px;text-decoration-thickness:1px;"
        "text-decoration-color:rgba(45,55,70,.28)}\n"
        ".ext-link:hover{text-decoration-color:var(--accent)}\n"
    )
    if DRY_RUN:
        print("  [DRY] añadiría CSS .ext-link a radar.css")
        return
    css_path.write_text(css + block, encoding="utf-8")
    print("  ✅ CSS .ext-link añadido a radar.css")


# ── Procesar directorio ───────────────────────────────────────────────────────

def process_dir(directory: Path) -> dict:
    paths = sorted(directory.rglob("index.html"))
    total_links = 0
    total_files = 0

    for path in paths:
        text = path.read_text(encoding="utf-8")
        soup = BeautifulSoup(text, "html.parser")
        n = linkify_soup(soup)
        if n > 0:
            total_links += n
            total_files += 1
            if DRY_RUN:
                print(f"  [DRY] {path.relative_to(ROOT)}: {n} enlaces")
            else:
                path.write_text(str(soup), encoding="utf-8")
                print(f"  ✅  {path.relative_to(ROOT)}: {n} enlaces")

    return {"files": total_files, "links": total_links}


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    mode = "[DRY-RUN]" if DRY_RUN else "[LIVE]"
    print(f"\nlinkify_institutions.py {mode}\n")

    add_css_if_needed()
    print()

    total = {"files": 0, "links": 0}
    for d in TARGET_DIRS:
        target = ROOT / d
        if not target.exists():
            continue
        print(f"── {d}/ ──")
        stats = process_dir(target)
        total["files"] += stats["files"]
        total["links"] += stats["links"]
        print()

    print(f"Total: {total['links']} enlaces externos añadidos en {total['files']} archivos")
