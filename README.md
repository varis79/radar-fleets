# Radar Fleet by Pulpo

Publicación editorial semanal en español sobre gestión de flotas, combustible, telemática, mantenimiento, regulación, electrificación e IA aplicada a operaciones. Editada por [Pulpo](https://www.getpulpo.com/).

- **Producción:** [radar-fleets.vercel.app](https://radar-fleets.vercel.app/)
- **Cadencia:** cada lunes a las 7:00 (Europa/Madrid)

## Estructura del repo

```
/
├── index.html                       # Home = copia de la edición más reciente
├── archive.html                     # Índice de todas las ediciones
├── sitemap.xml
├── rss.xml
├── robots.txt
├── 404.html
├── vercel.json                      # clean URLs, headers, redirects
├── magazines/
│   ├── 2026-04-14-radar-fleet-by-pulpo.html          # Nº 1
│   ├── 2026-04-14-radar-fleet-by-pulpo-summary.txt
│   ├── 2026-04-20-radar-fleet-by-pulpo.html          # Nº 2 (última)
│   └── 2026-04-20-radar-fleet-by-pulpo-summary.txt
├── prompts/
│   └── radar-master-prompt.md       # Fuente única de verdad para generar ediciones
└── content/
    └── pulpo-update.md              # Material para la sección "Desde Pulpo"
```

## Flujo de cada edición

1. Recopilar y curar contenido (noticias reales de la semana, geo-priorizadas: MX → ES → USA → LatAm → EU).
2. Revisar `content/pulpo-update.md` — si está vacío, se omite la sección "Desde Pulpo".
3. Generar `magazines/YYYY-MM-DD-radar-fleet-by-pulpo.html` y su `…-summary.txt`.
4. Copiar la nueva edición a `index.html` y ajustar `<link rel="canonical">` a la raíz + añadir `<link rel="alternate">` al permalink.
5. Añadir fila en `archive.html` (primera posición, pill `Última`; quitar `Última` de la anterior).
6. Añadir entrada en `sitemap.xml` y `rss.xml`.
7. Commit en rama `claude/edition-NNN-YYYY-MM-DD` y abrir PR contra `main`.

El prompt maestro completo vive en [`prompts/radar-master-prompt.md`](./prompts/radar-master-prompt.md).

## Deploy

Vercel conectado al repo, deploy automático en cada push a `main` (y preview en PRs).

- **Analytics:** Vercel Analytics activado vía `<script defer src="/_vercel/insights/script.js"></script>` en cada página. Activar desde el dashboard de Vercel (Analytics → Enable).
- **GA4:** aún no integrado. Cuando toque, pegar el snippet `gtag.js` con el Measurement ID en `index.html`, `archive.html`, `404.html` y en cualquier edición futura (puede centralizarse en un partial si se complica).

## Desarrollo local

```bash
# Servidor estático en :4173 sirviendo el repo entero
python3 -m http.server 4173
```

Con Claude Code, también:
```bash
# Usa .claude/launch.json del workspace padre → "radar-fleet-static"
```

## Reglas editoriales clave

- **No** es memo interno, **no** es digest, **no** es folleto comercial.
- Prioridad al lector externo. Pulpo aparece con elegancia, no como protagonista.
- Si no hay novedades reales de Pulpo, la sección "Desde Pulpo" se omite.
- Fraunces + Inter. Paleta editorial premium.
- Cada historia lleva: headline, short summary, why-for-operators, why-commercial, país/mercado, tag.
