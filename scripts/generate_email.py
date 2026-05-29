"""
generate_email.py — Genera el HTML del email newsletter (formato teaser).

Cada historia se presenta con:
  - Número + flag + mercado + tema
  - Titular original
  - Hook: dato más impactante (1 frase)
  - Question: pregunta que crea tensión → obliga el click
  - Botón → Leer

El contenido (hooks/questions) viene de generate_newsletter_copy.py (Claude).
Si no hay API key, usa fallback con resúmenes truncados.

Uso:
  python -m scripts.generate_email --date 2026-05-18
  python -m scripts.generate_email --date 2026-05-18 --output email.html
"""
from __future__ import annotations
import argparse
import datetime as dt
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.lib.paths import ROOT, DECISIONS_DIR, iso_week_key, magazine_paths
from scripts.lib.templating import human_date_es, FLAGS, MARKET_LABELS


EMAIL_ACCENT  = "#c9a84c"
EMAIL_DARK    = "#0d1521"
EMAIL_BODY    = "#f5f4ef"
EMAIL_CARD    = "#ffffff"
EMAIL_MUTED   = "rgba(0,0,0,0.55)"

_FLAG_TO_MARKET = {
    "🇲🇽": "mexico", "🇪🇸": "espana", "🇺🇸": "usa",
    "🌎": "latam", "🌍": "global", "🌐": "global", "🇪🇺": "europa",
    "🇨🇴": "colombia", "🇨🇱": "chile", "🇦🇷": "argentina",
    "🇵🇪": "peru", "🇪🇨": "ecuador", "🇺🇾": "uruguay",
}


# ── Parseo HTML de la revista ────────────────────────────────────────────────

def _enrich_from_html(compose_meta: dict) -> dict:
    from bs4 import BeautifulSoup
    html_path = ROOT / compose_meta.get("html_path", "")
    if not html_path.exists():
        return compose_meta
    soup = BeautifulSoup(html_path.read_text(encoding="utf-8"), "html.parser")

    cover_h1   = soup.select_one(".cover-issue")
    deck_el    = soup.select_one(".cover-deck")
    overline_el = soup.select_one(".cover-overline")

    stories = []
    for article in soup.select("article.story"):
        head_el = article.select_one(".story-headline")
        summ_el = article.select_one(".story-summary")
        if not head_el:
            continue
        market = "global"
        meta = article.select_one(".story-meta")
        if meta:
            text = meta.get_text()
            for flag, mkt in _FLAG_TO_MARKET.items():
                if flag in text:
                    market = mkt
                    break
        stories.append({
            "headline": head_el.get_text(" ", strip=True),
            "summary":  summ_el.get_text(" ", strip=True) if summ_el else "",
            "market":   market,
            "flag":     FLAGS.get(market, "🌐"),
        })

    enriched = dict(compose_meta)
    enriched["cover_headline"] = cover_h1.get_text(" ", strip=True) if cover_h1 else ""
    enriched["cover_deck"]     = deck_el.get_text(" ", strip=True)  if deck_el  else ""
    enriched["overline"]       = overline_el.get_text(" ", strip=True) if overline_el else ""
    enriched["stories"]        = stories
    return enriched


def load_compose_info(date: dt.date | None = None) -> dict | None:
    if date:
        week = iso_week_key(date)
        path = DECISIONS_DIR / f"{week}-compose.json"
        if path.exists():
            return _enrich_from_html(json.loads(path.read_text(encoding="utf-8")))
        return None
    candidates = sorted(DECISIONS_DIR.glob("*-compose.json"), reverse=True)
    for c in candidates:
        meta = json.loads(c.read_text(encoding="utf-8"))
        if meta.get("status") not in ("pause",):
            return _enrich_from_html(meta)
    return None


# ── Bloque de historia teaser ────────────────────────────────────────────────

def _story_teaser(i: int, story: dict, permalink: str) -> str:
    flag    = story.get("flag")  or FLAGS.get(story.get("market", "global"), "🌐")
    market  = MARKET_LABELS.get(story.get("market", "global"), "Global")
    num     = f"{i:02d}"
    headline = story.get("headline", "")
    hook     = story.get("hook", "")
    question = story.get("question", "")

    # Tag de tema si existe
    tag_html = ""

    return f"""
          <!-- Story {num} -->
          <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%"
                 style="margin-bottom:28px;padding-bottom:28px;
                        border-bottom:1px solid rgba(0,0,0,0.07);">
            <tr>
              <td style="padding-bottom:10px;">
                <span style="font-family:Arial,Helvetica,sans-serif;font-size:11px;
                             font-weight:700;color:{EMAIL_ACCENT};
                             letter-spacing:0.05em;">{num}</span>
                <span style="font-family:Arial,Helvetica,sans-serif;font-size:11px;
                             color:rgba(0,0,0,0.35);margin:0 6px;">·</span>
                <span style="font-family:Arial,Helvetica,sans-serif;font-size:11px;
                             color:rgba(0,0,0,0.45);">{flag} {market}</span>
              </td>
            </tr>
            <tr>
              <td>
                <h3 style="font-family:Georgia,'Times New Roman',serif;font-size:17px;
                           font-weight:700;color:{EMAIL_DARK};margin:0 0 10px;
                           line-height:1.3;">{headline}</h3>
              </td>
            </tr>
            <tr>
              <td style="padding-bottom:12px;">
                <p style="font-family:Arial,Helvetica,sans-serif;font-size:14px;
                          color:rgba(0,0,0,0.65);margin:0 0 6px;line-height:1.6;
                          font-style:normal;">{hook}</p>
                <p style="font-family:Georgia,'Times New Roman',serif;font-size:14px;
                          color:rgba(0,0,0,0.5);margin:0;line-height:1.5;
                          font-style:italic;">{question}</p>
              </td>
            </tr>
            <tr>
              <td style="text-align:right;">
                <a href="{permalink}" target="_blank"
                   style="font-family:Arial,Helvetica,sans-serif;font-size:12px;
                          font-weight:700;color:{EMAIL_ACCENT};text-decoration:none;
                          letter-spacing:0.04em;">Leer &rarr;</a>
              </td>
            </tr>
          </table>"""


# ── Template HTML completo ───────────────────────────────────────────────────

def generate_email_html(compose_info: dict, newsletter_copy: dict | None = None) -> str:
    edition_date_str = compose_info.get("edition_date", "")
    edition_date  = dt.date.fromisoformat(edition_date_str) if edition_date_str else dt.date.today()
    number        = compose_info.get("number", 1)
    number_padded = f"{number:02d}"
    human_date    = human_date_es(edition_date)
    cover_headline = compose_info.get("cover_headline", "")
    cover_deck     = compose_info.get("cover_deck", "")
    overline       = compose_info.get("overline", "Edición semanal")
    permalink      = f"https://thefleetradar.com/magazines/{edition_date_str}-radar-fleet-by-pulpo.html"

    # Contenido generado por Claude (o fallback)
    copy        = newsletter_copy or {}
    intro       = copy.get("intro", cover_deck[:200] if cover_deck else "")
    subject_alt = copy.get("subject_line", "")
    top_stories = copy.get("stories", [])

    # Si no hay teasers de Claude, construye fallback desde compose_info
    if not top_stories:
        for i, s in enumerate(compose_info.get("stories", [])[:5]):
            summary = s.get("summary", "")
            top_stories.append({
                "index": i,
                "headline": s.get("headline", ""),
                "hook": summary[:120].rsplit(" ", 1)[0] + "…" if len(summary) > 120 else summary,
                "question": "¿Qué impacto tiene esto en tu flota?",
                "market": s.get("market", "global"),
                "flag": FLAGS.get(s.get("market", "global"), "🌐"),
            })

    preheader = f"{cover_headline[:90]} — The Fleet Radar Nº {number_padded}"
    stories_html = "".join(
        _story_teaser(i + 1, s, permalink)
        for i, s in enumerate(top_stories[:5])
    )

    return f"""<!DOCTYPE html>
<html lang="es" xmlns="http://www.w3.org/1999/xhtml" xmlns:o="urn:schemas-microsoft-com:office:office">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<meta name="x-apple-disable-message-reformatting">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<!--[if mso]><noscript><xml><o:OfficeDocumentSettings>
<o:PixelsPerInch>96</o:PixelsPerInch></o:OfficeDocumentSettings></xml></noscript><![endif]-->
<title>The Fleet Radar &middot; N&ordm; {number_padded} &middot; {cover_headline}</title>
<style type="text/css">
body,table,td,a{{-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;}}
table,td{{mso-table-lspace:0pt;mso-table-rspace:0pt;}}
img{{-ms-interpolation-mode:bicubic;border:0;height:auto;line-height:100%;outline:none;text-decoration:none;}}
table{{border-collapse:collapse!important;}}
body{{height:100%!important;margin:0!important;padding:0!important;width:100%!important;background-color:{EMAIL_BODY};}}
@media only screen and (max-width:620px){{
  .email-container{{width:100%!important;}}
  .mobile-pad{{padding:20px!important;}}
  .cover-hl{{font-size:23px!important;line-height:1.25!important;}}
  .intro-text{{font-size:14px!important;}}
}}
</style>
</head>
<body style="margin:0;padding:0;background-color:{EMAIL_BODY};">

<!-- Preheader oculto -->
<div style="display:none;font-size:1px;line-height:1px;max-height:0;max-width:0;
            opacity:0;overflow:hidden;color:{EMAIL_BODY};">{preheader} &zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;</div>

<table role="presentation" cellspacing="0" cellpadding="0" border="0"
       align="center" width="100%" style="background-color:{EMAIL_BODY};">
<tr><td align="center" style="padding:20px 12px;">

  <table class="email-container" role="presentation" cellspacing="0" cellpadding="0"
         border="0" align="center" width="600" style="max-width:600px;width:100%;">

    <!-- ── HEADER ─────────────────────────────────────────── -->
    <tr>
      <td class="mobile-pad"
          style="background-color:{EMAIL_DARK};padding:22px 32px;
                 border-bottom:2px solid {EMAIL_ACCENT};">
        <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
          <tr>
            <td>
              <div style="font-family:Georgia,'Times New Roman',serif;font-size:20px;
                          font-weight:700;color:#fff;letter-spacing:-0.01em;">
                The Fleet Radar
                <span style="font-weight:400;color:{EMAIL_ACCENT};"> by Pulpo</span>
              </div>
              <div style="font-family:Arial,Helvetica,sans-serif;font-size:11px;
                          color:rgba(255,255,255,0.4);margin-top:5px;
                          letter-spacing:0.07em;text-transform:uppercase;">
                N&ordm; {number_padded} &middot; {human_date} &middot; Edición semanal
              </div>
            </td>
          </tr>
        </table>
      </td>
    </tr>

    <!-- ── COVER ──────────────────────────────────────────── -->
    <tr>
      <td class="mobile-pad"
          style="background-color:{EMAIL_DARK};padding:32px 32px 12px;">
        <div style="font-family:Arial,Helvetica,sans-serif;font-size:10px;
                    color:{EMAIL_ACCENT};letter-spacing:0.12em;
                    text-transform:uppercase;margin-bottom:12px;">
          {overline}
        </div>
        <h1 class="cover-hl"
            style="font-family:Georgia,'Times New Roman',serif;font-size:27px;
                   font-weight:700;color:#fff;margin:0 0 16px;
                   line-height:1.22;letter-spacing:-0.01em;">
          {cover_headline}
        </h1>
      </td>
    </tr>

    <!-- ── INTRO editorial ────────────────────────────────── -->
    <tr>
      <td class="mobile-pad"
          style="background-color:{EMAIL_DARK};padding:0 32px 32px;">
        <p class="intro-text"
           style="font-family:Arial,Helvetica,sans-serif;font-size:15px;
                  color:rgba(255,255,255,0.65);margin:0;line-height:1.7;
                  border-left:3px solid {EMAIL_ACCENT};padding-left:16px;">
          {intro}
        </p>
      </td>
    </tr>

    <!-- ── CTA principal ──────────────────────────────────── -->
    <tr>
      <td class="mobile-pad"
          style="background-color:{EMAIL_DARK};padding:0 32px 36px;">
        <!--[if mso]>
        <v:roundrect xmlns:v="urn:schemas-microsoft-com:vml"
          xmlns:w="urn:schemas-microsoft-com:office:word"
          href="{permalink}"
          style="height:42px;v-text-anchor:middle;width:210px;"
          arcsize="7%" stroke="f" fillcolor="{EMAIL_ACCENT}">
          <w:anchorlock/>
          <center style="color:{EMAIL_DARK};font-family:Arial,Helvetica,sans-serif;
                         font-size:13px;font-weight:700;">
            Leer edición completa &rarr;
          </center>
        </v:roundrect>
        <![endif]-->
        <!--[if !mso]><!-->
        <a href="{permalink}" target="_blank"
           style="display:inline-block;background-color:{EMAIL_ACCENT};
                  color:{EMAIL_DARK};font-family:Arial,Helvetica,sans-serif;
                  font-size:13px;font-weight:700;letter-spacing:0.04em;
                  text-decoration:none;padding:12px 24px;border-radius:3px;
                  mso-hide:all;">
          Leer edición completa &rarr;
        </a>
        <!--<![endif]-->
      </td>
    </tr>

    <!-- ── STORIES TEASERS ────────────────────────────────── -->
    <tr>
      <td class="mobile-pad"
          style="background-color:{EMAIL_CARD};padding:32px 32px 4px;">
        <div style="font-family:Arial,Helvetica,sans-serif;font-size:10px;
                    color:rgba(0,0,0,0.35);letter-spacing:0.1em;
                    text-transform:uppercase;margin-bottom:28px;
                    padding-bottom:14px;border-bottom:2px solid {EMAIL_DARK};">
          5 historias de esta semana
        </div>
        {stories_html}
      </td>
    </tr>

    <!-- ── CTA secundario ─────────────────────────────────── -->
    <tr>
      <td class="mobile-pad"
          style="background-color:{EMAIL_CARD};padding:12px 32px 40px;text-align:center;">
        <a href="{permalink}" target="_blank"
           style="display:inline-block;border:2px solid {EMAIL_DARK};
                  color:{EMAIL_DARK};font-family:Arial,Helvetica,sans-serif;
                  font-size:13px;font-weight:700;text-decoration:none;
                  padding:12px 28px;border-radius:3px;">
          Ver las {len(top_stories)} historias completas &rarr;
        </a>
        <p style="font-family:Arial,Helvetica,sans-serif;font-size:12px;
                  color:rgba(0,0,0,0.35);margin:16px 0 0;">
          thefleetradar.com &middot; cada lunes a las 7:00
        </p>
      </td>
    </tr>

    <!-- ── FOOTER ─────────────────────────────────────────── -->
    <tr>
      <td class="mobile-pad"
          style="background-color:{EMAIL_DARK};padding:28px 32px;text-align:center;
                 border-top:2px solid rgba(255,255,255,0.06);">
        <div style="font-family:Georgia,'Times New Roman',serif;font-size:14px;
                    font-weight:700;color:#fff;margin-bottom:6px;">
          The Fleet Radar &middot; by Pulpo
        </div>
        <div style="font-family:Arial,Helvetica,sans-serif;font-size:11px;
                    color:rgba(255,255,255,0.35);margin-bottom:18px;line-height:1.7;">
          Inteligencia semanal para gestores de flota<br>
          México &middot; España &middot; LatAm
        </div>
        <div style="font-family:Arial,Helvetica,sans-serif;font-size:11px;
                    color:rgba(255,255,255,0.25);line-height:1.9;">
          Recibes esto porque te suscribiste en
          <a href="https://thefleetradar.com"
             style="color:rgba(255,255,255,0.4);text-decoration:none;">
            thefleetradar.com
          </a><br>
          <a href="https://thefleetradar.com/unsubscribe?email={{{{unsub_email}}}}"
             style="color:rgba(255,255,255,0.35);text-decoration:underline;">
            Cancelar suscripción
          </a>
          &nbsp;&middot;&nbsp;
          <a href="https://www.getpulpo.com"
             style="color:rgba(255,255,255,0.25);text-decoration:none;">
            Pulpo &mdash; gestión de flotas con IA
          </a>
        </div>
      </td>
    </tr>

  </table>
</td></tr>
</table>
</body>
</html>"""


def generate_text(compose_info: dict, newsletter_copy: dict | None = None) -> str:
    """Texto plano alternativo."""
    edition_date_str = compose_info.get("edition_date", "")
    number        = compose_info.get("number", 1)
    cover_headline = compose_info.get("cover_headline", "")
    edition_date  = dt.date.fromisoformat(edition_date_str) if edition_date_str else dt.date.today()
    human_date    = human_date_es(edition_date)
    permalink     = f"https://thefleetradar.com/magazines/{edition_date_str}-radar-fleet-by-pulpo.html"

    copy       = newsletter_copy or {}
    intro      = copy.get("intro", "")
    top_stories = copy.get("stories", [])

    lines = [
        f"THE FLEET RADAR · BY PULPO — Nº {number:02d} · {human_date}",
        "=" * 60,
        "",
        cover_headline.upper(),
        "",
    ]
    if intro:
        lines += [intro, ""]
    lines += [f"Leer edición: {permalink}", "", "-" * 60,
              "5 HISTORIAS DE ESTA SEMANA", "-" * 60, ""]

    for i, s in enumerate(top_stories[:5], 1):
        flag   = s.get("flag", "🌐")
        market = MARKET_LABELS.get(s.get("market", "global"), "Global")
        lines.append(f"{i:02d}. {flag} {market}")
        lines.append(s.get("headline", ""))
        if s.get("hook"):
            lines.append(s["hook"])
        if s.get("question"):
            lines.append(s["question"])
        lines += [f"→ {permalink}", ""]

    lines += ["=" * 60,
              "The Fleet Radar · by Pulpo · thefleetradar.com",
              "",
              "Cancelar suscripción: https://thefleetradar.com/unsubscribe"]
    return "\n".join(lines)


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--date", help="YYYY-MM-DD")
    p.add_argument("--output", help="Archivo HTML de salida (default: stdout)")
    p.add_argument("--text", action="store_true", help="Genera texto plano")
    p.add_argument("--no-claude", action="store_true", help="Desactiva la llamada a Claude")
    args = p.parse_args(argv)

    date = dt.date.fromisoformat(args.date) if args.date else None
    info = load_compose_info(date)
    if not info:
        print("ERROR: No se encontró compose-info", file=sys.stderr)
        return 1

    newsletter_copy = None
    if not args.text and not args.no_claude:
        from scripts.generate_newsletter_copy import generate_copy
        newsletter_copy = generate_copy(info)

    content = generate_text(info, newsletter_copy) if args.text \
              else generate_email_html(info, newsletter_copy)

    if args.output:
        Path(args.output).write_text(content, encoding="utf-8")
        print(f"Guardado en {args.output}", file=sys.stderr)
    else:
        print(content)
    return 0


if __name__ == "__main__":
    sys.exit(main())
