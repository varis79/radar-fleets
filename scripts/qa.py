"""
QA bloqueante mínimo para el MVP.

Evalúa la edición HTML y el summary generados por compose. Emite informe
legible (Markdown) y un exit code claro: 0 si todo OK, 1 si hay bloqueantes.

Checks implementados (bloqueantes):
  C1. Framing interno prohibido (usa scripts/lib/forbidden.py).
  C2. Thin content total (edición < umbral) y por story (< min_words_story).
  C3. Voz editorial: em dashes en prosa, estructuras "no es X, es Y" simples.
  C4. Metadatos: title, meta description, canonical, og:url, article:published_time.
  C5. Estructura HTML: H1 único, cover section, editors-note, CTA, closing.
  C6. Enlaces internos: fichero existente en el repo.
  C7. Repetición obvia sin novedad: headline cover vs últimas 8 ediciones.
  C8. Claims sensibles sin fuente: afirmaciones "líder", "único", "el mejor",
       "más barato", "[n]% menos" sin contexto/fuente.
  C9. Stub marker: si el HTML contiene "[stub:" → bloqueo.

Checks "aviso" (no bloquean):
  A1. Mix geográfico (ratio MX+ES bajo).
  A2. Diversidad de topics baja.

Uso:
  python -m scripts.qa [--date YYYY-MM-DD]
"""
from __future__ import annotations
import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup

from scripts.lib.config import config
from scripts.lib.paths import (
    ROOT, QA_DIR, DECISIONS_DIR, EDITORIAL_MEMORY, magazine_paths,
    iso_week_key, next_monday, ensure_dirs
)
from scripts.lib.forbidden import scan_text


def _get_compose_info(week: str) -> dict | None:
    p = DECISIONS_DIR / f"{week}-compose.json"
    if not p.exists():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def _count_words(text: str) -> int:
    return len([w for w in re.split(r"\s+", text) if w])


def check_framing(visible_text: str, html_raw: str) -> list[dict]:
    """C1. Framing interno prohibido en texto visible o en HTML crudo
       (captura también pills/tags con clasificación interna)."""
    issues = []
    for human, matched in scan_text(visible_text):
        issues.append({"check": "C1-framing", "severity": "block", "message": human, "sample": matched})
    # Escanea también HTML crudo por pills/labels
    for human, matched in scan_text(html_raw):
        if (human, matched) in [(i["message"], i["sample"]) for i in issues]:
            continue
        issues.append({"check": "C1-framing", "severity": "block", "message": human, "sample": matched})
    return issues


def check_thin(visible_text: str, stories: list[dict]) -> list[dict]:
    """C2. Thin content total y por story."""
    cfg = config()["qa"]
    issues = []
    total_words = _count_words(visible_text)
    mode_short_min = int(cfg["min_words_edition_short"])
    mode_normal_min = int(cfg["min_words_edition_normal"])

    # Usamos el min de ambos para bloquear solo en casos muy flojos
    threshold = mode_short_min
    if total_words < threshold:
        issues.append({
            "check": "C2-thin",
            "severity": "block",
            "message": f"Edición demasiado corta ({total_words} palabras, mínimo {threshold})",
        })

    min_words_story = int(cfg["min_words_story"])
    for s in stories:
        headline = s.get("headline", "")
        summary = s.get("summary", "")
        body = f"{summary} {s.get('why_operator', '')} {s.get('why_business', '')}"
        w = _count_words(body)
        if w < min_words_story:
            issues.append({
                "check": "C2-thin",
                "severity": "block",
                "message": f"Story corta: '{headline[:60]}' tiene {w} palabras (mínimo {min_words_story})",
            })
    return issues


def check_voice(visible_text: str) -> list[dict]:
    """C3. Voz editorial. Em dashes en prosa + 'no es X, es Y' básico."""
    issues = []
    # Em dashes
    em_count = visible_text.count("—")
    max_em = int(config()["qa"].get("max_em_dash_in_prose", 0))
    if em_count > max_em:
        issues.append({
            "check": "C3-voice",
            "severity": "block",
            "message": f"Encontrados {em_count} em dashes en prosa (máximo permitido {max_em})",
            "sample": "—"
        })
    # "no es X, es Y"
    rx = re.compile(r"\bno\s+es\s+[a-záéíóú][^.,]{3,40}[,.]?\s*es\s+[a-záéíóú]", re.IGNORECASE)
    for m in rx.finditer(visible_text):
        issues.append({
            "check": "C3-voice",
            "severity": "block",
            "message": "Estructura 'no es X, es Y' detectada",
            "sample": m.group(0)[:120],
        })
    return issues


def check_meta(soup: BeautifulSoup) -> list[dict]:
    """C4. Metadatos mínimos."""
    issues = []
    def _get_meta(prop_or_name: str, value: str):
        return soup.find("meta", attrs={prop_or_name: value})

    if not soup.title or not soup.title.text.strip():
        issues.append({"check": "C4-meta", "severity": "block", "message": "<title> ausente o vacío"})
    md = _get_meta("name", "description")
    if not md or not md.get("content", "").strip():
        issues.append({"check": "C4-meta", "severity": "block", "message": "meta description ausente"})
    can = soup.find("link", rel="canonical")
    if not can or not can.get("href", "").startswith("https://"):
        issues.append({"check": "C4-meta", "severity": "block", "message": "canonical ausente o no absoluto"})
    og = _get_meta("property", "og:url")
    if not og or not og.get("content", "").strip():
        issues.append({"check": "C4-meta", "severity": "block", "message": "og:url ausente"})
    apub = _get_meta("property", "article:published_time")
    if not apub or not apub.get("content", "").strip():
        issues.append({"check": "C4-meta", "severity": "block", "message": "article:published_time ausente"})
    return issues


def check_structure(soup: BeautifulSoup) -> list[dict]:
    """C5. Estructura HTML mínima."""
    issues = []
    h1s = soup.find_all("h1")
    if len(h1s) != 1:
        issues.append({
            "check": "C5-structure", "severity": "block",
            "message": f"Se espera exactamente 1 <h1>, encontrados {len(h1s)}"
        })
    required = {
        ".cover": "cover",
        ".editors-note": "nota del editor",
        ".cta-band": "CTA",
        ".closing": "closing",
    }
    for sel, name in required.items():
        if not soup.select_one(sel):
            issues.append({
                "check": "C5-structure", "severity": "block",
                "message": f"Sección requerida ausente: {name} ({sel})"
            })
    return issues


def check_internal_links(soup: BeautifulSoup) -> list[dict]:
    """C6. Enlaces internos rotos (filesystem)."""
    issues = []
    seen: set[str] = set()
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        if not href.startswith("/"):
            continue
        if href.startswith("/_vercel/"):
            continue  # inyectado por Vercel
        if href in seen:
            continue
        seen.add(href)
        # normaliza: /temas/fuel-cards/ → fichero temas/fuel-cards/index.html
        target = href.split("#")[0].split("?")[0]
        candidate = (ROOT / target.lstrip("/")).resolve()
        # directorios → index.html dentro
        if target.endswith("/"):
            candidate = candidate / "index.html"
        if not candidate.exists():
            issues.append({
                "check": "C6-link", "severity": "block",
                "message": f"Enlace interno roto: {href}"
            })
    return issues


def check_repetition(cover_headline: str, stories: list[dict]) -> list[dict]:
    """C7. Repetición contra las últimas 8 ediciones en editorial-memory."""
    if not EDITORIAL_MEMORY.exists():
        return []
    memory = EDITORIAL_MEMORY.read_text(encoding="utf-8")
    issues: list[dict] = []
    # Check simple: cover headline exacto aparece en memoria
    from difflib import SequenceMatcher
    chunks = memory.split("\n## Nº ")[1:9]
    recent_headlines: list[str] = []
    for c in chunks:
        first_line = c.split("\n", 1)[0]
        recent_headlines.append(first_line.lower())
    ch = cover_headline.lower().strip().strip('"').strip("'")
    for rh in recent_headlines:
        r = SequenceMatcher(None, ch, rh).ratio()
        if r >= 0.85:
            issues.append({
                "check": "C7-repetition", "severity": "block",
                "message": f"Headline de cover muy similar a edición reciente (ratio {r:.2f})",
                "sample": rh[:160],
            })
            break
    return issues


def check_claims(visible_text: str) -> list[dict]:
    """C8. Claims sensibles.

    Los claims absolutos sin comparación son bloqueantes (hiperbólicos).
    Los porcentajes sin fuente son aviso, no bloqueo: Claude redacta cifras
    legítimas tipo '28% YoY' sin escribir 'fuente' al lado; el master
    prompt ya empuja a citar origen. Dejarlo como bloqueo genera demasiado
    falso positivo en MVP.
    """
    issues = []
    block_patterns = [
        (r"\bel (mejor|peor|único|unico|líder|lider)\s+(del|de)\s+(mundo|mercado|sector|planeta)\b", "claim absoluto de liderazgo sin fuente"),
        (r"\bmás (barato|caro) que\b", "comparativa de precio sin fuente"),
    ]
    warn_patterns = [
        (r"\b\d{1,3}%\s+(menos|más)\b", "porcentaje sin fuente explícita"),
    ]
    for pat, label in block_patterns:
        for m in re.finditer(pat, visible_text, re.IGNORECASE):
            sample = visible_text[max(0, m.start() - 40):m.end() + 40].strip()
            issues.append({
                "check": "C8-claim", "severity": "block",
                "message": f"{label}: {m.group(0)}",
                "sample": sample[:200]
            })
    for pat, label in warn_patterns:
        # Solo contamos 1 aviso por tipo para no inflar el informe
        first = next(re.finditer(pat, visible_text, re.IGNORECASE), None)
        if first:
            sample = visible_text[max(0, first.start() - 40):first.end() + 40].strip()
            issues.append({
                "check": "C8-claim", "severity": "warn",
                "message": f"{label}: {first.group(0)} (revisar que la cifra tenga contexto)",
                "sample": sample[:200]
            })
    return issues


def check_stub_marker(html_raw: str) -> list[dict]:
    if "[stub:" in html_raw:
        return [{"check": "C9-stub", "severity": "block",
                 "message": "Edición en modo stub; no publicable"}]
    return []


def check_geo_mix(stories: list[dict]) -> list[dict]:
    """A1. Aviso mix geográfico bajo."""
    if not stories:
        return []
    cfg = config()["selection"]
    prim = sum(1 for s in stories if s.get("market") in ("mexico", "espana"))
    ratio = prim / len(stories)
    if ratio < float(cfg["geo_min_primary_ratio"]):
        return [{
            "check": "A1-geo", "severity": "warn",
            "message": f"Ratio MX+ES bajo ({ratio:.2f}). Esperado ≥ {cfg['geo_min_primary_ratio']}"
        }]
    return []


def check_topic_diversity(stories: list[dict]) -> list[dict]:
    """A2. Aviso diversidad de topics baja."""
    if not stories:
        return []
    topics = {s.get("topic") for s in stories if s.get("topic")}
    min_t = int(config()["selection"]["topic_min_diversity"])
    if len(topics) < min_t:
        return [{
            "check": "A2-topic", "severity": "warn",
            "message": f"Pocos topics distintos ({len(topics)}). Esperado ≥ {min_t}"
        }]
    return []


def visible_text_from_html(soup: BeautifulSoup) -> str:
    # Excluye estilos, scripts y atributos
    for s in soup(["style", "script", "noscript"]):
        s.decompose()
    return soup.get_text(separator=" ", strip=True)


def run_qa(today: dt.date | None = None) -> dict:
    ensure_dirs()
    week = iso_week_key(today)
    compose_info = _get_compose_info(week)
    if compose_info is None:
        return {"error": "no-compose-info", "week": week}
    if compose_info.get("status") == "pause":
        # En pausa no hay edición. QA devuelve ok y lo registra.
        out = {"status": "pause", "week": week, "checks": []}
        (QA_DIR / f"{week}-report.md").write_text(
            f"# QA · {week}\n\nModo: **pause**. Sin edición que evaluar.\n",
            encoding="utf-8"
        )
        return out

    edition_date = dt.date.fromisoformat(compose_info["edition_date"])
    paths = magazine_paths(edition_date)
    html_raw = paths["html"].read_text(encoding="utf-8")
    soup = BeautifulSoup(html_raw, "html.parser")
    visible = visible_text_from_html(BeautifulSoup(html_raw, "html.parser"))

    # Cargar stories del selection para evaluar per-story
    sel = json.loads((DECISIONS_DIR / f"{week}-selection.json").read_text(encoding="utf-8"))
    # Sin embargo necesitamos las redactadas: las obtenemos del HTML (título+summary aprox).
    stories_struct: list[dict] = []
    for a in soup.select("article.story"):
        h = a.select_one(".story-headline")
        sm = a.select_one(".story-summary")
        why_op = a.select_one(".why-item .why-text")
        why_bs = a.select_one(".why-item.commercial .why-text")
        meta = a.select_one(".story-meta")
        market_text = meta.get_text(" ", strip=True) if meta else ""
        # Inferir slug de market por bandera/label
        market = "global"
        for slug, lbl in (("mexico", "México"), ("espana", "España"), ("usa", "USA"),
                         ("colombia", "Colombia"), ("brasil", "Brasil"), ("chile", "Chile"),
                         ("peru", "Perú"), ("argentina", "Argentina"),
                         ("latam", "LatAm"), ("europa", "Europa")):
            if lbl in market_text:
                market = slug
                break
        stories_struct.append({
            "headline": h.get_text(strip=True) if h else "",
            "summary": sm.get_text(strip=True) if sm else "",
            "why_operator": why_op.get_text(strip=True) if why_op else "",
            "why_business": why_bs.get_text(strip=True) if why_bs else "",
            "market": market,
            "topic": None,  # no lo mostramos visible; se valida aparte por selection
        })
    # Enriquecer con topics de selection
    for it, s in zip(sel.get("chosen", []), stories_struct):
        s["topic"] = it.get("topic")

    cover_h1 = soup.select_one(".cover-issue")
    cover_headline = cover_h1.get_text(" ", strip=True) if cover_h1 else ""

    all_issues: list[dict] = []
    all_issues.extend(check_stub_marker(html_raw))
    all_issues.extend(check_framing(visible, html_raw))
    all_issues.extend(check_thin(visible, stories_struct))
    all_issues.extend(check_voice(visible))
    all_issues.extend(check_meta(soup))
    all_issues.extend(check_structure(soup))
    all_issues.extend(check_internal_links(soup))
    all_issues.extend(check_repetition(cover_headline, stories_struct))
    all_issues.extend(check_claims(visible))
    all_issues.extend(check_geo_mix(stories_struct))
    all_issues.extend(check_topic_diversity(stories_struct))

    block = [i for i in all_issues if i["severity"] == "block"]
    warns = [i for i in all_issues if i["severity"] == "warn"]

    # Informe
    report = [f"# QA · {week} · {'BLOQUEADO' if block else 'OK'}", ""]
    report.append(f"- Edición: {compose_info.get('html_path')}")
    report.append(f"- Número: Nº {compose_info.get('number')} · Modo: {compose_info.get('mode')}")
    report.append(f"- Stories evaluadas: {len(stories_struct)}")
    report.append(f"- Palabras visibles: {_count_words(visible)}")
    report.append("")
    if block:
        report.append("## Bloqueantes")
        for i in block:
            report.append(f"- **{i['check']}** · {i['message']}" + (f"\n  - `{i.get('sample','')}`" if i.get("sample") else ""))
        report.append("")
    if warns:
        report.append("## Avisos")
        for i in warns:
            report.append(f"- {i['check']} · {i['message']}")
        report.append("")
    if not block and not warns:
        report.append("Sin incidencias. QA pasa limpia.")

    (QA_DIR / f"{week}-report.md").write_text("\n".join(report), encoding="utf-8")

    return {
        "status": "fail" if block else "ok",
        "week": week,
        "blockers": len(block),
        "warnings": len(warns),
        "issues": all_issues,
    }


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--date", help="YYYY-MM-DD (default: hoy)")
    args = p.parse_args(argv)
    today = dt.date.fromisoformat(args.date) if args.date else None
    result = run_qa(today)
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    if "error" in result:
        return 1
    if result.get("status") == "fail":
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
