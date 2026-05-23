#!/usr/bin/env python3
"""
linkify_topics.py — Añade enlaces internos entre páginas pillar cuando una
página menciona temas cubiertos por otras páginas del mismo mercado.

Estrategia:
  - Usa BeautifulSoup (solo nodos de texto en <body>)
  - Solo primera mención de cada término por página
  - Idempotente: no re-enlaza si ya existe <a> con la misma href
  - No se autoenlaza (skip si el destino == página actual)
  - Solo enlaza a páginas publicadas (index.html existe en disco)
  - class="int-link" en cada enlace generado

Uso:
    python3 scripts/linkify_topics.py [--dry-run]
    python3 scripts/linkify_topics.py [--dir temas]
"""
import sys
import re
import csv
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString, Tag

DRY_RUN = "--dry-run" in sys.argv

ROOT = Path(__file__).parent.parent

# ── Directorios a procesar ──────────────────────────────────────────────────
TARGET_DIRS = ["temas", "mercados", "evergreen"]
for i, arg in enumerate(sys.argv):
    if arg == "--dir" and i + 1 < len(sys.argv):
        TARGET_DIRS = [sys.argv[i + 1]]

# ── PILLAR_INDEX: (topic_code, market) → url_path ───────────────────────────

def _build_pillar_index() -> dict[tuple[str, str], str]:
    """Builds (topic_code, market) → url_path from matrix.csv.
    Prefers informational intent, then lowest tier. Only published pages."""
    csv_path = ROOT / "content/pillar-matrix/matrix.csv"
    if not csv_path.exists():
        return {}
    index: dict[tuple[str, str], str] = {}
    priority: dict[tuple[str, str], tuple[int, int]] = {}
    intent_rank = {"informational": 0, "guia-practica": 1, "comparativo": 2, "regulatorio": 3}
    with csv_path.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            tc  = row.get("topic_code", "").strip()
            mkt = row.get("market", "").strip()
            url = row.get("url_path", "").strip()
            if not tc or not mkt or not url:
                continue
            page_dir = ROOT / url.strip("/")
            if not (page_dir / "index.html").exists():
                continue
            ir = intent_rank.get(row.get("intent", ""), 9)
            tr_raw = row.get("tier", "9")
            tr = int(tr_raw) if tr_raw.isdigit() else 9
            key = (tc, mkt)
            if key not in priority or (ir, tr) < priority[key]:
                index[key] = url
                priority[key] = (ir, tr)
    return index


PILLAR_INDEX: dict[tuple[str, str], str] = _build_pillar_index()

# ── Term → topic_code mapping ────────────────────────────────────────────────
# Ordered longest-first to avoid partial matches.
# Each entry: (phrase_to_match, topic_code)
TOPIC_TERMS: list[tuple[str, str]] = [
    # Multi-word phrases first
    ("tarjetas de flota",        "fuel-cards"),
    ("tarjeta de flota",         "fuel-cards"),
    ("tarjeta combustible",      "fuel-cards"),
    ("zona de bajas emisiones",  "zbe"),
    ("vehículos eléctricos",     "electrificacion-flotas"),
    ("vehículos eléctrico",      "electrificacion-flotas"),
    ("vehículo eléctrico",       "electrificacion-flotas"),
    ("última milla",             "reparto-ultima-milla"),
    ("ultimo milla",             "reparto-ultima-milla"),
    ("cadena de frío",           "perecederos-cadena-frio"),
    ("cadena de frio",           "perecederos-cadena-frio"),
    ("baliza V-16",              "v-16"),
    # Single terms
    ("telemática",               "telematica"),
    ("telematica",               "telematica"),
    ("electrificación",          "electrificacion-flotas"),
    ("electrificacion",          "electrificacion-flotas"),
    ("renting",                  "renting-leasing"),
    ("leasing",                  "renting-leasing"),
    ("tacógrafo",                "tacografo"),
    ("tacógrafo",                "tacografo"),
    ("tacografos",               "tacografo"),
    ("tacografo",                "tacografo"),
    ("T-MEC",                    "t-mec"),
    ("TMEC",                     "t-mec"),
    ("V-16",                     "v-16"),
    ("ZBE",                      "zbe"),
    ("ITV",                      "itv"),
]

# ── Detect market from file path ─────────────────────────────────────────────

def _detect_market(path: Path) -> str | None:
    s = str(path)
    if "mexico" in s or "-mx-" in s or "sict" in s or "t-mec" in s or "tmec" in s or "cne-" in s:
        return "mexico"
    if ("espana" in s or "spain" in s or "europa" in s
            or "dgt" in s or "baliza" in s or "-v16-" in s or "tacografo" in s
            or "tacógrafo" in s or "zbe" in s or "itv" in s):
        return "espana"
    if "colombia" in s:
        return "colombia"
    if "chile" in s:
        return "chile"
    if "argentina" in s:
        return "argentina"
    if "peru" in s:
        return "peru"
    return None


def _page_url(path: Path) -> str:
    """Convert file path to canonical URL path, e.g. /temas/foo/"""
    rel = path.relative_to(ROOT)
    parts = rel.parts[:-1]  # drop index.html
    return "/" + "/".join(parts) + "/"


# ── Helpers ───────────────────────────────────────────────────────────────────

def _inline_link(label: str, url: str) -> Tag:
    a = Tag(name="a")
    a["href"] = url
    a["class"] = "int-link"
    a.string = label
    return a


def _inject_link_in_text_node(node: NavigableString, pattern: re.Pattern,
                               url: str) -> bool:
    """Replace first match of pattern in node with an <a> tag. Returns True on success."""
    text = str(node)
    m = pattern.search(text)
    if not m:
        return False

    parent = node.parent
    idx = list(parent.children).index(node)

    before = text[:m.start()]
    label  = text[m.start():m.end()]
    after  = text[m.end():]

    node.replace_with(NavigableString(before))
    a_tag = _inline_link(label, url)
    parent.insert(idx + 1, a_tag)
    parent.insert(idx + 2, NavigableString(after))
    return True


def _is_in_anchor(node: NavigableString) -> bool:
    for parent in node.parents:
        if parent.name == "a":
            return True
        if parent.name in ("body", "[document]"):
            break
    return False


def _already_linked(body: Tag, target_url: str) -> bool:
    """True if there is already an int-link pointing to target_url in this body."""
    return bool(body.find("a", class_="int-link", href=target_url))


# ── Core linkify ──────────────────────────────────────────────────────────────

def linkify_soup(soup: BeautifulSoup, market: str | None, self_url: str) -> int:
    added = 0
    linked: set[str] = set()  # topic_codes already linked

    body = soup.find("body")
    if not body:
        return 0

    for phrase, topic_code in TOPIC_TERMS:
        if topic_code in linked:
            continue

        # Resolve target URL
        target_url: str | None = None
        if market:
            target_url = PILLAR_INDEX.get((topic_code, market))
        if target_url is None:
            # Try generic markets as fallback (e.g. for evergreen pages)
            for fallback in ("mexico", "espana"):
                target_url = PILLAR_INDEX.get((topic_code, fallback))
                if target_url:
                    break
        if target_url is None:
            continue

        # Never self-link
        if target_url.rstrip("/") == self_url.rstrip("/"):
            linked.add(topic_code)
            continue

        # Idempotency: already linked to this URL?
        if _already_linked(body, target_url):
            linked.add(topic_code)
            continue

        # Build regex — case-insensitive, word-boundary aware
        pattern = re.compile(rf'(?<!\w){re.escape(phrase)}(?!\w)', re.IGNORECASE | re.UNICODE)

        text_nodes = body.find_all(string=pattern)
        for node in text_nodes:
            if not isinstance(node, NavigableString):
                continue
            if _is_in_anchor(node):
                continue
            parent_names = {p.name for p in node.parents if isinstance(p, Tag)}
            if parent_names & {"script", "style", "meta", "head", "nav", "title"}:
                continue
            if _inject_link_in_text_node(node, pattern, target_url):
                linked.add(topic_code)
                added += 1
                break

    return added


# ── CSS (idempotent) ──────────────────────────────────────────────────────────

def add_css_if_needed() -> None:
    css_path = ROOT / "assets/radar.css"
    css = css_path.read_text(encoding="utf-8")
    if "int-link" in css:
        return
    block = (
        "\n/* ── Internal topic links ───────────────────────────────────────── */\n"
        ".int-link{color:inherit;text-decoration:underline;"
        "text-underline-offset:2px;text-decoration-thickness:1px;"
        "text-decoration-color:rgba(45,105,180,.30)}\n"
        ".int-link:hover{text-decoration-color:var(--accent)}\n"
    )
    if DRY_RUN:
        print("  [DRY] añadiría CSS .int-link a radar.css")
        return
    css_path.write_text(css + block, encoding="utf-8")
    print("  ✅ CSS .int-link añadido a radar.css")


# ── Process directory ─────────────────────────────────────────────────────────

def process_dir(directory: Path) -> dict:
    paths = sorted(directory.rglob("index.html"))
    total_links = 0
    total_files = 0

    for path in paths:
        market   = _detect_market(path)
        self_url = _page_url(path)
        text     = path.read_text(encoding="utf-8")
        soup     = BeautifulSoup(text, "html.parser")
        n        = linkify_soup(soup, market, self_url)
        if n > 0:
            total_links += n
            total_files += 1
            if DRY_RUN:
                print(f"  [DRY] {path.relative_to(ROOT)} ({market}): {n} enlaces")
            else:
                path.write_text(str(soup), encoding="utf-8")
                print(f"  ✅  {path.relative_to(ROOT)} ({market}): {n} enlaces")

    return {"files": total_files, "links": total_links}


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    mode = "[DRY-RUN]" if DRY_RUN else "[LIVE]"
    print(f"\nlinkify_topics.py {mode}\n")

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

    print(f"Total: {total['links']} enlaces internos añadidos en {total['files']} archivos")
