"""
generate_email.py — Genera el HTML del email newsletter para una edición.

El HTML resultante es compatible con email clients (Gmail, Outlook, Apple Mail):
- CSS interno + atributos inline en elementos clave (Outlook)
- Sin fuentes externas (Fraunces → Georgia serif fallback)
- Max-width 600px, tabla base
- Sin JavaScript
- Incluye texto plano alternativo (texto_plano)
- Unsubscribe link dinámico con {unsub_email} placeholder

Uso:
    python scripts/generate_email.py --date 2026-05-18
    python scripts/generate_email.py  # usa la edición más reciente
"""
from __future__ import annotations
import argparse
import datetime as dt
import json
import sys
from pathlib import Path

from scripts.lib.paths import ROOT, DECISIONS_DIR, iso_week_key, magazine_paths
from scripts.lib.templating import human_date_es, FLAGS, MARKET_LABELS


# ── Paleta de email (valores fijos — no dependen del acento semanal por
#    compatibilidad con clientes de email que no soportan CSS variables) ─────
EMAIL_ACCENT  = "#c9a84c"
EMAIL_BG_DARK = "#0d1521"
EMAIL_BG_BODY = "#f5f4ef"
EMAIL_BG_CARD = "#ffffff"
EMAIL_TEXT    = "#1a1a1a"
EMAIL_MUTED   = "rgba(0,0,0,0.55)"


def _story_row(i: int, story: dict) -> str:
    flag = FLAGS.get(story.get("market", "global"), "🌐")
    market = MARKET_LABELS.get(story.get("market", "global"), "Global")
    headline = story.get("headline", "")
    # Truncate summary for email — max ~200 chars
    summary = story.get("summary", "")
    if len(summary) > 220:
        summary = summary[:217].rsplit(" ", 1)[0] + "…"
    num = f"{i:02d}"
    return f"""
          <!-- Story {num} -->
          <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%"
                 style="margin-bottom:20px;padding-bottom:20px;border-bottom:1px solid rgba(0,0,0,0.08);">
            <tr>
              <td width="36" valign="top" style="padding-top:3px;">
                <div style="font-family:Georgia,'Times New Roman',serif;font-size:15px;font-weight:700;
                            color:{EMAIL_ACCENT};line-height:1;">{num}</div>
              </td>
              <td style="padding-left:12px;">
                <div style="font-family:Arial,Helvetica,sans-serif;font-size:11px;
                            color:rgba(0,0,0,0.4);margin-bottom:5px;letter-spacing:0.03em;">
                  {flag}&nbsp;{market}
                </div>
                <h3 style="font-family:Georgia,'Times New Roman',serif;font-size:16px;
                           font-weight:700;color:{EMAIL_BG_DARK};margin:0 0 8px;line-height:1.3;">
                  {headline}
                </h3>
                <p style="font-family:Arial,Helvetica,sans-serif;font-size:14px;
                          color:rgba(0,0,0,0.62);margin:0;line-height:1.65;">
                  {summary}
                </p>
              </td>
            </tr>
          </table>"""


def generate_email_html(compose_info: dict) -> str:
    """Devuelve el HTML completo del email a partir del compose_info dict."""
    edition_date_str = compose_info.get("edition_date", "")
    edition_date = dt.date.fromisoformat(edition_date_str) if edition_date_str else dt.date.today()
    number = compose_info.get("number", 1)
    number_padded = f"{number:02d}"
    human_date = human_date_es(edition_date)
    cover_headline = compose_info.get("cover_headline", "")
    cover_deck = compose_info.get("cover_deck", "")
    overline = compose_info.get("overline", "Edición semanal · Flotas, combustible, telemática y regulación")
    stories = compose_info.get("stories", [])
    permalink = f"https://thefleetradar.com/magazines/{edition_date_str}-radar-fleet-by-pulpo.html"

    # Preheader (hidden preview text in inbox)
    preheader = f"Nº {number} · {cover_headline[:80]}"

    # Stories HTML
    stories_html = "".join(_story_row(i + 1, s) for i, s in enumerate(stories[:7]))

    # Plain-text fallback stories (for text/plain part if needed)
    # (generate_email devuelve solo HTML; el script de envío añade el texto plano)

    html = f"""<!DOCTYPE html>
<html lang="es" xmlns="http://www.w3.org/1999/xhtml" xmlns:o="urn:schemas-microsoft-com:office:office">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="x-apple-disable-message-reformatting">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<!--[if mso]>
<noscript><xml><o:OfficeDocumentSettings>
<o:PixelsPerInch>96</o:PixelsPerInch>
</o:OfficeDocumentSettings></xml></noscript>
<![endif]-->
<title>The Fleet Radar · Nº {number_padded} · {cover_headline}</title>
<style type="text/css">
  /* Reset */
  body,table,td,a{{-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;}}
  table,td{{mso-table-lspace:0pt;mso-table-rspace:0pt;}}
  img{{-ms-interpolation-mode:bicubic;border:0;height:auto;line-height:100%;outline:none;text-decoration:none;}}
  table{{border-collapse:collapse!important;}}
  body{{height:100%!important;margin:0!important;padding:0!important;width:100%!important;
        background-color:{EMAIL_BG_BODY};}}
  a{{color:{EMAIL_ACCENT};}}
  /* Mobile */
  @media only screen and (max-width:620px){{
    .email-container{{width:100%!important;}}
    .story-num{{display:none!important;}}
    .mobile-pad{{padding:20px!important;}}
    .cover-headline{{font-size:22px!important;}}
  }}
</style>
</head>
<body style="margin:0;padding:0;background-color:{EMAIL_BG_BODY};">

<!-- Preheader oculto -->
<div style="display:none;font-size:1px;line-height:1px;max-height:0;max-width:0;
            opacity:0;overflow:hidden;color:{EMAIL_BG_BODY};">{preheader} &#847; &#847; &#847; &#847;</div>

<table role="presentation" cellspacing="0" cellpadding="0" border="0"
       align="center" width="100%" style="background-color:{EMAIL_BG_BODY};">
  <tr>
    <td align="center" style="padding:24px 12px;">
      <table class="email-container" role="presentation" cellspacing="0" cellpadding="0"
             border="0" align="center" width="600"
             style="max-width:600px;width:100%;">

        <!-- ── HEADER ────────────────────────────────────────── -->
        <tr>
          <td class="mobile-pad"
              style="background-color:{EMAIL_BG_DARK};padding:24px 32px;
                     border-bottom:2px solid {EMAIL_ACCENT};">
            <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
              <tr>
                <td>
                  <div style="font-family:Georgia,'Times New Roman',serif;font-size:21px;
                              font-weight:700;color:#ffffff;letter-spacing:-0.01em;">
                    The Fleet Radar
                    <span style="font-weight:400;color:{EMAIL_ACCENT};"> by Pulpo</span>
                  </div>
                  <div style="font-family:Arial,Helvetica,sans-serif;font-size:11px;
                              color:rgba(255,255,255,0.42);margin-top:5px;
                              letter-spacing:0.07em;text-transform:uppercase;">
                    Nº {number_padded} &middot; {human_date} &middot; Edición semanal
                  </div>
                </td>
              </tr>
            </table>
          </td>
        </tr>

        <!-- ── COVER ─────────────────────────────────────────── -->
        <tr>
          <td class="mobile-pad"
              style="background-color:{EMAIL_BG_DARK};padding:36px 32px 0;">
            <div style="font-family:Arial,Helvetica,sans-serif;font-size:10px;
                        color:{EMAIL_ACCENT};letter-spacing:0.12em;
                        text-transform:uppercase;margin-bottom:14px;">
              {overline}
            </div>
            <h1 class="cover-headline"
                style="font-family:Georgia,'Times New Roman',serif;font-size:28px;
                       font-weight:700;color:#ffffff;margin:0 0 16px;
                       line-height:1.22;letter-spacing:-0.01em;">
              {cover_headline}
            </h1>
            <p style="font-family:Arial,Helvetica,sans-serif;font-size:15px;
                      color:rgba(255,255,255,0.68);margin:0;line-height:1.7;">
              {cover_deck}
            </p>
          </td>
        </tr>

        <!-- ── CTA principal ──────────────────────────────────── -->
        <tr>
          <td class="mobile-pad"
              style="background-color:{EMAIL_BG_DARK};padding:28px 32px 36px;">
            <!--[if mso]>
            <v:roundrect xmlns:v="urn:schemas-microsoft-com:vml"
              xmlns:w="urn:schemas-microsoft-com:office:word"
              href="{permalink}" style="height:44px;v-text-anchor:middle;width:220px;"
              arcsize="8%" stroke="f" fillcolor="{EMAIL_ACCENT}">
              <w:anchorlock/>
              <center style="color:{EMAIL_BG_DARK};font-family:Arial,Helvetica,sans-serif;
                             font-size:13px;font-weight:700;">
                Leer edición completa →
              </center>
            </v:roundrect>
            <![endif]-->
            <!--[if !mso]><!-->
            <a href="{permalink}" target="_blank"
               style="display:inline-block;background-color:{EMAIL_ACCENT};
                      color:{EMAIL_BG_DARK};font-family:Arial,Helvetica,sans-serif;
                      font-size:13px;font-weight:700;letter-spacing:0.04em;
                      text-decoration:none;padding:13px 26px;border-radius:3px;
                      mso-hide:all;">
              Leer edición completa →
            </a>
            <!--<![endif]-->
          </td>
        </tr>

        <!-- ── DIVIDER ────────────────────────────────────────── -->
        <tr>
          <td style="background-color:{EMAIL_BG_DARK};padding:0 32px;">
            <div style="border-top:1px solid rgba(255,255,255,0.1);"></div>
          </td>
        </tr>

        <!-- ── STORIES ────────────────────────────────────────── -->
        <tr>
          <td class="mobile-pad"
              style="background-color:{EMAIL_BG_CARD};padding:32px 32px 8px;">
            <div style="font-family:Arial,Helvetica,sans-serif;font-size:10px;
                        color:rgba(0,0,0,0.35);letter-spacing:0.1em;
                        text-transform:uppercase;margin-bottom:28px;
                        padding-bottom:14px;border-bottom:1px solid rgba(0,0,0,0.1);">
              Las historias de esta semana
            </div>
            {stories_html}
          </td>
        </tr>

        <!-- ── CTA secundario ─────────────────────────────────── -->
        <tr>
          <td class="mobile-pad"
              style="background-color:{EMAIL_BG_CARD};padding:8px 32px 36px;text-align:center;">
            <a href="{permalink}" target="_blank"
               style="display:inline-block;border:2px solid {EMAIL_BG_DARK};
                      color:{EMAIL_BG_DARK};font-family:Arial,Helvetica,sans-serif;
                      font-size:13px;font-weight:700;text-decoration:none;
                      padding:12px 26px;border-radius:3px;">
              Leer edición completa en thefleetradar.com
            </a>
          </td>
        </tr>

        <!-- ── FOOTER ─────────────────────────────────────────── -->
        <tr>
          <td class="mobile-pad"
              style="background-color:{EMAIL_BG_DARK};padding:32px;text-align:center;">
            <div style="font-family:Georgia,'Times New Roman',serif;font-size:15px;
                        font-weight:700;color:#ffffff;margin-bottom:6px;">
              The Fleet Radar · by Pulpo
            </div>
            <div style="font-family:Arial,Helvetica,sans-serif;font-size:12px;
                        color:rgba(255,255,255,0.4);margin-bottom:20px;line-height:1.65;">
              Inteligencia semanal para el sector de gestión de flotas<br>
              Sale cada lunes a las 7:00 &middot;
              <a href="https://thefleetradar.com" style="color:rgba(255,255,255,0.5);
                                                         text-decoration:none;">
                thefleetradar.com
              </a>
            </div>
            <div style="font-family:Arial,Helvetica,sans-serif;font-size:11px;
                        color:rgba(255,255,255,0.28);line-height:1.8;">
              Recibes este email porque te suscribiste en thefleetradar.com<br>
              <a href="https://thefleetradar.com/unsubscribe?email={{{{unsub_email}}}}"
                 style="color:rgba(255,255,255,0.38);text-decoration:underline;">
                Cancelar suscripción
              </a>
              &nbsp;&middot;&nbsp;
              <a href="https://www.getpulpo.com" style="color:rgba(255,255,255,0.28);
                                                        text-decoration:none;">
                Pulpo &mdash; gestión de flotas con IA
              </a>
            </div>
          </td>
        </tr>

      </table>
    </td>
  </tr>
</table>
</body>
</html>"""
    return html


def generate_text(compose_info: dict) -> str:
    """Genera la versión texto plano del email (fallback)."""
    edition_date_str = compose_info.get("edition_date", "")
    edition_date = dt.date.fromisoformat(edition_date_str) if edition_date_str else dt.date.today()
    number = compose_info.get("number", 1)
    cover_headline = compose_info.get("cover_headline", "")
    cover_deck = compose_info.get("cover_deck", "")
    stories = compose_info.get("stories", [])
    permalink = f"https://thefleetradar.com/magazines/{edition_date_str}-radar-fleet-by-pulpo.html"
    human_date = human_date_es(edition_date)

    lines = [
        f"THE FLEET RADAR · BY PULPO — Nº {number:02d} · {human_date}",
        "=" * 60,
        "",
        cover_headline.upper(),
        "",
        cover_deck,
        "",
        f"Leer edición completa: {permalink}",
        "",
        "-" * 60,
        "HISTORIAS DE ESTA SEMANA",
        "-" * 60,
        "",
    ]
    for i, s in enumerate(stories[:7], 1):
        flag = FLAGS.get(s.get("market", "global"), "🌐")
        market = MARKET_LABELS.get(s.get("market", "global"), "Global")
        lines.append(f"{i:02d}. {flag} {market}")
        lines.append(s.get("headline", ""))
        summary = s.get("summary", "")
        if summary:
            lines.append(summary[:200])
        lines.append("")

    lines += [
        "=" * 60,
        "The Fleet Radar · by Pulpo · thefleetradar.com",
        f"Nº {number:02d} · {human_date}",
        "",
        "Para cancelar tu suscripción visita:",
        "https://thefleetradar.com/unsubscribe",
        "",
        "Editado por Pulpo — getpulpo.com",
    ]
    return "\n".join(lines)


def load_compose_info(date: dt.date | None = None) -> dict | None:
    """Carga el compose-info JSON de la edición más reciente o de la fecha dada."""
    if date:
        week = iso_week_key(date)
        path = DECISIONS_DIR / f"{week}-compose.json"
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
        return None

    # Sin fecha: busca el más reciente
    candidates = sorted(DECISIONS_DIR.glob("*-compose.json"), reverse=True)
    for c in candidates:
        data = json.loads(c.read_text(encoding="utf-8"))
        if data.get("status") not in ("pause",):
            return data
    return None


def main(argv=None):
    p = argparse.ArgumentParser(description="Genera el HTML del email newsletter.")
    p.add_argument("--date", help="YYYY-MM-DD de la edición")
    p.add_argument("--output", help="Archivo de salida (default: stdout)")
    p.add_argument("--text", action="store_true", help="Genera texto plano en vez de HTML")
    args = p.parse_args(argv)

    date = dt.date.fromisoformat(args.date) if args.date else None
    info = load_compose_info(date)
    if not info:
        print("ERROR: No se encontró compose-info para la fecha dada", file=sys.stderr)
        return 1

    content = generate_text(info) if args.text else generate_email_html(info)

    if args.output:
        Path(args.output).write_text(content, encoding="utf-8")
        print(f"Guardado en {args.output}", file=sys.stderr)
    else:
        print(content)
    return 0


if __name__ == "__main__":
    sys.exit(main())
