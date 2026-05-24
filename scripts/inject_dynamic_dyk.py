#!/usr/bin/env python3
"""
inject_dynamic_dyk.py — Inyecta 2 cajas "Sabías qué" DINÁMICAS (JS) en
home, archive y magazines. Cada recarga muestra facts distintos.

Diferencia vs rotate_facts.py:
  - rotate_facts.py: caja estática inyectada en HTML, una por página,
    rota una vez por semana. PILLARS / hubs / casos-uso / sectores /
    ciudades / corredores / players / evergreen.
  - inject_dynamic_dyk.py: 2 contenedores vacíos + JS que carga
    `/assets/sabias-que.json` y rellena en cliente con facts random
    cada recarga. SOLO home + archive + magazines.

Por qué la diferencia:
  - Pillars necesitan cambios reales en HTML para que Google detecte
    actualizaciones (señal SEO de freshness).
  - Home/archive/magazines reciben mucho tráfico recurrente; los lectores
    quieren riqueza visual y variedad ("¿qué fact veré hoy?"), no necesitan
    rotación SEO.

Las 2 cajas tienen estilos diferenciados:
  - "primary": diseño completo arriba/post-cover
  - "secondary": más compacta, accent invertido (azul en lugar de dorado),
    al pie antes del newsletter

Uso:
    python3 scripts/inject_dynamic_dyk.py [--dry-run]
"""
import sys
from pathlib import Path
from bs4 import BeautifulSoup, Tag

DRY_RUN = "--dry-run" in sys.argv
ROOT = Path(__file__).parent.parent

# ── HTML que se inyecta (placeholders + script) ─────────────────────────────

DYK_PRIMARY = (
    '<aside class="did-you-know dyk-dynamic" data-dyk-slot="primary" '
    'data-dyk-loading>'
    '<span class="dyk-eyebrow">💡 Sabías qué</span>'
    '<p class="dyk-body">Cargando dato del sector…</p>'
    '</aside>'
)

DYK_SECONDARY = (
    '<aside class="did-you-know dyk-dynamic dyk-secondary" '
    'data-dyk-slot="secondary" data-dyk-loading>'
    '<span class="dyk-eyebrow">💡 Otro dato</span>'
    '<p class="dyk-body">Cargando…</p>'
    '</aside>'
)

DYK_SCRIPT = """
<script id="dyk-loader">
(async function(){
  try {
    const r = await fetch('/assets/sabias-que.json', {cache:'force-cache'});
    if(!r.ok) return;
    const data = await r.json();
    const facts = data.facts || [];
    if(!facts.length) return;
    const slots = document.querySelectorAll('[data-dyk-slot]');
    if(!slots.length) return;
    const used = new Set();
    function pick(){
      for(let i=0;i<25;i++){
        const f = facts[Math.floor(Math.random()*facts.length)];
        if(!used.has(f.text)){ used.add(f.text); return f; }
      }
      return facts[Math.floor(Math.random()*facts.length)];
    }
    slots.forEach((slot, i)=>{
      const f = pick();
      const eyebrow = slot.querySelector('.dyk-eyebrow');
      const body = slot.querySelector('.dyk-body');
      const label = (i===0) ? '💡 Sabías qué' : '💡 Otro dato';
      if(eyebrow) eyebrow.textContent = label + ' · ' + (f.emoji||'💡') + ' ' + (f.category||'Fleet Radar');
      if(body) body.textContent = f.text;
      slot.removeAttribute('data-dyk-loading');
    });
  } catch(e){ /* silent */ }
})();
</script>
"""


def has_dynamic_dyk(soup: BeautifulSoup) -> bool:
    return soup.find(id="dyk-loader") is not None


def inject_home(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    soup = BeautifulSoup(text, "html.parser")
    if has_dynamic_dyk(soup):
        return _refresh_static(soup, path)  # ya inyectado, solo verificar limpiezas

    # Quitar caja estática existente (de rotate_facts.py) para no duplicar
    for old in soup.find_all("aside", class_="did-you-know"):
        if "dyk-dynamic" not in (old.get("class") or []):
            old.decompose()

    # Punto de inyección primary: tras el último <section class="cover"> o tras header
    primary_anchor = (soup.find("section", class_="cover")
                      or soup.find("section", class_="editors-note")
                      or soup.find("main") or soup.find("header"))
    if primary_anchor is None:
        return False
    primary = BeautifulSoup(DYK_PRIMARY, "html.parser").find("aside")
    primary_anchor.insert_after(primary)

    # Punto de inyección secondary: antes del .newsletter-band o antes del footer
    secondary_anchor = (soup.find(class_="newsletter-band")
                        or soup.find("footer", class_="site-footer")
                        or soup.find("footer"))
    if secondary_anchor is None:
        return False
    secondary = BeautifulSoup(DYK_SECONDARY, "html.parser").find("aside")
    secondary_anchor.insert_before(secondary)

    # Inyectar script antes del cierre </body>
    body = soup.find("body")
    if body is None:
        return False
    script = BeautifulSoup(DYK_SCRIPT, "html.parser").find("script")
    body.append(script)

    if not DRY_RUN:
        path.write_text(str(soup), encoding="utf-8")
    return True


def _refresh_static(soup: BeautifulSoup, path: Path) -> bool:
    """Si ya tiene dyk-dynamic, no hace falta tocar (idempotente)."""
    return False  # nothing changed


def main():
    mode = "[DRY-RUN]" if DRY_RUN else "[LIVE]"
    print(f"\ninject_dynamic_dyk.py {mode}\n")

    # Targets: home + archive + magazines
    files = []
    if (ROOT / "index.html").exists():
        files.append(ROOT / "index.html")
    if (ROOT / "archive.html").exists():
        files.append(ROOT / "archive.html")
    files.extend(sorted((ROOT / "magazines").glob("*.html")))

    touched = 0
    for path in files:
        if inject_home(path):
            touched += 1
            marker = "[DRY]" if DRY_RUN else "  ✅"
            print(f"  {marker} {path.relative_to(ROOT)}")

    print(f"\n  Total páginas con DYK dinámica: {touched} / {len(files)}")


if __name__ == "__main__":
    main()
