#!/usr/bin/env python3
"""
inject_newsletter_ctas.py — Inyecta las dos cajas de suscripción newsletter en todas las páginas HTML.

Caja 1 (nl-bar): Barra superior fina, justo debajo del <header class="topbar">.
  Tiene formulario inline, dismissable con sessionStorage.
  → Todas las páginas.

Caja 2 (nl-mid): Tarjeta editorial mid-content.
  → Magazines: después del 3er <article class="story">
  → Páginas pillar/hub: después del primer <h2> dentro de .pillar-body
  → index.html / archive.html / hub index pages: antes del newsletter-band existente

Idempotente: no duplica si ya está inyectada.

Uso:
  python scripts/inject_newsletter_ctas.py [--dry-run]
"""
from __future__ import annotations
import sys
from pathlib import Path
from bs4 import BeautifulSoup, Comment

DRY_RUN = "--dry-run" in sys.argv
ROOT = Path(__file__).parent.parent

# ── HTML de la barra superior ──────────────────────────────────────────────
NL_BAR_HTML = """<div class="nl-bar" id="nl-bar">
  <span class="nl-bar-text">📬 <strong>The Fleet Radar</strong> — inteligencia semanal para gestores de flota. Gratis.</span>
  <form class="nl-bar-form" onsubmit="nlBarSubmit(event)">
    <input type="email" class="nl-bar-input" placeholder="tu@empresa.com" required autocomplete="email">
    <button class="nl-bar-btn" type="submit">Suscribirme gratis →</button>
  </form>
  <p class="nl-bar-ok" id="nl-bar-ok">✓ Apuntado. Llega cada lunes.</p>
  <button class="nl-bar-close" onclick="nlBarClose()" aria-label="Cerrar">✕</button>
</div>"""

NL_BAR_SCRIPT = """<script>
(function(){try{if(sessionStorage.getItem('nla_ok'))document.getElementById('nl-bar').remove();}catch(e){}}());
function nlBarClose(){var b=document.getElementById('nl-bar');if(b)b.remove();try{sessionStorage.setItem('nla_ok','1');}catch(e){}}
async function nlBarSubmit(e){
  e.preventDefault();
  var btn=e.target.querySelector('button'),inp=e.target.querySelector('input');
  var email=inp.value.trim();
  btn.disabled=true;btn.textContent='…';
  try{
    var r=await fetch('/api/subscribe',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({email})});
    if(r.ok){
      e.target.style.display='none';
      document.querySelector('.nl-bar-text') && (document.querySelector('.nl-bar-text').textContent='');
      var ok=document.getElementById('nl-bar-ok');
      ok.style.display='block';
      setTimeout(nlBarClose,4000);
      try{sessionStorage.setItem('nla_ok','1');}catch(ex){}
    } else {btn.disabled=false;btn.textContent='Suscribirme gratis →';}
  } catch{btn.disabled=false;btn.textContent='Suscribirme gratis →';}
}
</script>"""

# ── HTML de la tarjeta mid-content ─────────────────────────────────────────
NL_MID_HTML = """<div class="nl-mid">
  <span class="nl-mid-icon" aria-hidden="true">📬</span>
  <div class="nl-mid-body">
    <p class="nl-mid-eyebrow">Gratis · cada lunes a las 7:00</p>
    <h3 class="nl-mid-title">¿Te está siendo útil? Llega a tu bandeja cada semana.</h3>
    <p class="nl-mid-desc">Regulación, telemática, financiación y mercado — lo que realmente mueve los números de una flota. Sin spam. Sin comunicaciones comerciales. Solo señal.</p>
    <form class="nl-mid-form" onsubmit="nlMidSubmit(this,event)">
      <input type="email" class="nl-mid-input" placeholder="tu@empresa.com" required autocomplete="email">
      <button class="nl-mid-btn" type="submit">Suscribirme gratis</button>
    </form>
    <p class="nl-mid-ok" id="nl-mid-ok"></p>
    <p class="nl-mid-err" id="nl-mid-err"></p>
    <p class="nl-mid-note">✓ Sin spam &nbsp;·&nbsp; ✓ Sin ventas &nbsp;·&nbsp; ✓ Cancela cuando quieras</p>
  </div>
</div>"""

NL_MID_SCRIPT = """<script>
async function nlMidSubmit(form,e){
  e.preventDefault();
  var btn=form.querySelector('button'),email=form.querySelector('input').value.trim();
  var ok=document.getElementById('nl-mid-ok'),err=document.getElementById('nl-mid-err');
  btn.disabled=true;btn.textContent='Enviando…';err.style.display='none';
  try{
    var r=await fetch('/api/subscribe',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({email})});
    if(r.ok){
      form.style.display='none';
      form.closest('.nl-mid').querySelector('.nl-mid-note').style.display='none';
      ok.textContent='✓ Apuntado. Te llegará cada lunes a las 7:00.';
      ok.style.display='block';
    } else {
      var d=await r.json().catch(()=>({}));
      btn.disabled=false;btn.textContent='Suscribirme gratis';
      err.textContent=d.error||'Algo fue mal. Inténtalo de nuevo.';
      err.style.display='block';
    }
  } catch{
    btn.disabled=false;btn.textContent='Suscribirme gratis';
    err.style.display='block';err.textContent='Error de conexión.';
  }
}
</script>"""


def _has_nl_bar(soup: BeautifulSoup) -> bool:
    return bool(soup.find(id="nl-bar") or soup.find(class_="nl-bar"))


def _has_nl_mid(soup: BeautifulSoup) -> bool:
    return bool(soup.find(class_="nl-mid"))


def _inject_bar(soup: BeautifulSoup) -> bool:
    """Inyecta la barra debajo del <header class="topbar">. Devuelve True si cambió."""
    if _has_nl_bar(soup):
        return False
    topbar = soup.find("header", class_="topbar")
    if not topbar:
        return False
    bar_soup = BeautifulSoup(NL_BAR_HTML, "html.parser")
    topbar.insert_after(bar_soup)
    # Script al final del body
    body = soup.find("body")
    if body:
        script_soup = BeautifulSoup(NL_BAR_SCRIPT, "html.parser")
        body.append(script_soup)
    return True


def _inject_mid(soup: BeautifulSoup, page_type: str) -> bool:
    """Inyecta la tarjeta mid-content según el tipo de página."""
    if _has_nl_mid(soup):
        return False

    mid_soup = BeautifulSoup(NL_MID_HTML, "html.parser")
    inserted = False

    if page_type == "magazine":
        # Después del 3er article.story (o 2º si no hay 3)
        articles = soup.find_all("article", class_="story")
        idx = min(2, len(articles) - 1)  # 0-indexed: posición 3 = índice 2
        if idx >= 0:
            articles[idx].insert_after(mid_soup)
            inserted = True

    elif page_type == "pillar":
        # Después del primer <h2> dentro de .pillar-body
        pillar_body = soup.find(class_="pillar-body")
        if pillar_body:
            h2 = pillar_body.find("h2")
            if h2:
                # Busca el primer párrafo después del h2
                sib = h2.find_next_sibling()
                if sib and sib.name == "p":
                    sib.insert_after(mid_soup)
                else:
                    h2.insert_after(mid_soup)
                inserted = True

    elif page_type == "hub":
        # Antes del newsletter-band existente
        band = soup.find(class_="newsletter-band")
        if band:
            band.insert_before(mid_soup)
            inserted = True
        else:
            # Fallback: antes del site-footer
            footer = soup.find("footer", class_="site-footer")
            if footer:
                footer.insert_before(mid_soup)
                inserted = True

    if inserted:
        body = soup.find("body")
        if body and not _has_nl_mid_script(soup):
            script_soup = BeautifulSoup(NL_MID_SCRIPT, "html.parser")
            body.append(script_soup)
    return inserted


def _has_nl_mid_script(soup: BeautifulSoup) -> bool:
    for s in soup.find_all("script"):
        if "nlMidSubmit" in (s.string or ""):
            return True
    return False


def _detect_page_type(path: Path) -> str:
    """Clasifica la página para decidir dónde inyectar nl-mid."""
    parts = path.parts
    name = path.name
    # Magazines
    if "magazines" in parts and name.endswith(".html"):
        return "magazine"
    # Pillar pages (temas, casos-uso, sectores, evergreen, corredores, ciudades, players)
    pillar_dirs = {"temas", "casos-uso", "sectores", "evergreen", "corredores", "ciudades", "players"}
    if any(p in parts for p in pillar_dirs) and name == "index.html":
        return "pillar"
    # Market hubs and other hub indexes
    return "hub"


def process(path: Path) -> dict[str, bool]:
    text = path.read_text(encoding="utf-8")
    soup = BeautifulSoup(text, "html.parser")

    page_type = _detect_page_type(path)
    bar_added = _inject_bar(soup)
    mid_added = _inject_mid(soup, page_type)

    changed = bar_added or mid_added
    if changed and not DRY_RUN:
        path.write_text(str(soup), encoding="utf-8")

    return {"bar": bar_added, "mid": mid_added, "type": page_type}


def collect_targets() -> list[Path]:
    targets: list[Path] = []
    # Magazines
    targets.extend((ROOT / "magazines").glob("*-radar-fleet-by-pulpo.html"))
    # Home, archive, 404
    for f in ["index.html", "archive.html", "404.html"]:
        p = ROOT / f
        if p.exists():
            targets.append(p)
    # Pillar dirs
    for sub in ("temas", "mercados", "casos-uso", "sectores", "evergreen",
                "corredores", "ciudades", "players", "about", "legal"):
        d = ROOT / sub
        if d.exists():
            targets.extend(d.rglob("index.html"))
    return sorted(set(targets))


def main():
    mode = "[DRY-RUN]" if DRY_RUN else "[LIVE]"
    print(f"\ninject_newsletter_ctas.py {mode}\n")

    targets = collect_targets()
    print(f"  Páginas a procesar: {len(targets)}\n")

    bars = mids = skipped = 0
    for path in targets:
        if not path.exists():
            continue
        try:
            result = process(path)
            rel = path.relative_to(ROOT)
            if result["bar"] or result["mid"]:
                tag = "[DRY]" if DRY_RUN else "✅"
                print(f"  {tag} {rel} ({result['type']})"
                      f"  bar={'NEW' if result['bar'] else '—'}"
                      f"  mid={'NEW' if result['mid'] else '—'}")
                if result["bar"]:
                    bars += 1
                if result["mid"]:
                    mids += 1
            else:
                skipped += 1
        except Exception as exc:
            print(f"  ⚠ {path.relative_to(ROOT)}: {exc}")

    print(f"\n  Resumen: {bars} barras inyectadas · {mids} tarjetas mid inyectadas · {skipped} ya tenían / sin cambios")


if __name__ == "__main__":
    main()
