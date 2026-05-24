# Setup · Weekly freshness workflow

El workflow `.github/workflows/weekly-freshness.yml` activa el cron de
frescura editorial (miércoles 06:00 UTC) que ejecuta:

1. `rotate_facts.py` — rota la caja "Sabías qué" en ~158 páginas
2. `refresh_freshness.py` — actualiza `article:modified_time` en ~30
   páginas seleccionadas por rotación (cycle 6 semanas)
3. `rebuild_sitemap.py` — regenera el sitemap con lastmod real
4. Commit auto + push + trigger Vercel deploy

## Por qué este setup manual

El PAT actual (Personal Access Token) configurado en el keychain de macOS
NO incluye el scope `workflow`. Sin ese scope, GitHub rechaza pushes que
creen o modifiquen archivos en `.github/workflows/`.

## Solución A — Actualizar PAT (recomendado)

1. https://github.com/settings/tokens
2. Edita tu token actual (o crea uno nuevo)
3. Añade el scope **`workflow`** (tick en la sección "Update GitHub Action workflows")
4. Save y copia el nuevo token
5. Actualiza en el keychain macOS:

   ```bash
   # Borra el viejo
   git credential-osxkeychain erase <<EOF
   protocol=https
   host=github.com
   EOF
   # Próximo push pedirá usuario y token; pega el nuevo
   ```

6. Push directo:

   ```bash
   cp .github/workflows/weekly-freshness.yml.staged .github/workflows/weekly-freshness.yml
   git add .github/workflows/weekly-freshness.yml
   git commit -m "feat: enable weekly freshness cron"
   git push
   ```

## Solución B — Crear via GitHub UI (5 min)

Si prefieres no tocar el PAT:

1. Ve a https://github.com/varis79/radar-fleets/actions
2. Click "New workflow"
3. Skip templates → "set up a workflow yourself"
4. Nombre del archivo: `weekly-freshness.yml`
5. Pega el contenido completo del archivo local
   (`.github/workflows/weekly-freshness.yml` o el doc al final de este file)
6. Commit directly to `main`

## Verificación

Después de añadir el workflow:

1. https://github.com/varis79/radar-fleets/actions/workflows/weekly-freshness.yml
2. Click "Run workflow" para test manual
3. Verifica que el commit auto-generado aparece con prefijo `chore(freshness):`

## Variables de entorno necesarias

El workflow usa `secrets.VERCEL_DEPLOY_HOOK` si está configurado. Para
añadirlo:

1. https://vercel.com → tu proyecto → Settings → Git → Deploy Hooks
2. Crea un hook llamado "weekly-freshness", branch `main`
3. Copia la URL
4. https://github.com/varis79/radar-fleets/settings/secrets/actions
5. New repository secret → `VERCEL_DEPLOY_HOOK` → pega URL

Si no configuras el deploy hook, el cron sigue funcionando — solo no
fuerza el deploy automáticamente (Vercel detecta el push de commits
y deploya solo en cualquier caso).

## Contenido del workflow (referencia)

```yaml
name: Weekly freshness rotation

on:
  schedule:
    - cron: '0 6 * * 3'  # Miércoles 06:00 UTC
  workflow_dispatch:

jobs:
  refresh:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pull-requests: write
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install deps
        run: pip install beautifulsoup4 lxml pyyaml
      - name: Rotate "Sabías qué" boxes
        run: python3 scripts/rotate_facts.py
      - name: Refresh freshness meta (rotation cycle)
        run: python3 scripts/refresh_freshness.py
      - name: Rebuild sitemap
        run: python3 scripts/rebuild_sitemap.py
      - name: Commit & push if changes
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
          git add -A
          if git diff --cached --quiet; then
            echo "No freshness changes this week"
            exit 0
          fi
          WEEK=$(date +%V)
          git commit -m "chore(freshness): rotación semanal W${WEEK}"
          git push
      - name: Trigger Vercel deploy
        if: success()
        run: |
          if [ -n "${{ secrets.VERCEL_DEPLOY_HOOK }}" ]; then
            curl -X POST "${{ secrets.VERCEL_DEPLOY_HOOK }}"
          fi
```
