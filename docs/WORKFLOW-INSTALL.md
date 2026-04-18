# Instalación manual del workflow semanal

Cuando este PR se mergee, el pipeline del MVP queda listo pero **sin activar**
todavía, porque `.github/workflows/weekly-edition.yml` no se puede empujar
desde esta rama (el PAT actual no tiene scope `workflow`, por seguridad).

Instalación en 3 clics desde la UI de GitHub:

1. En la web del repo → **Add file → Create new file**.
2. Nombre del fichero: `.github/workflows/weekly-edition.yml` (GitHub creará
   la carpeta automáticamente).
3. Pegar el contenido de **`docs/workflow-install.yml`** (este mismo PR lo
   incluye como referencia).
4. Commit directo a `main`.

Alternativa vía CLI con un PAT que tenga scope `workflow`:

```bash
git checkout main
git pull
cp docs/workflow-install.yml .github/workflows/weekly-edition.yml
git add .github/workflows/weekly-edition.yml
git commit -m "Instalar workflow semanal del MVP"
git push
```

## Requisitos tras instalar

1. Repo → **Settings → Secrets and variables → Actions → New repository secret**
   - Name: `ANTHROPIC_API_KEY`
   - Value: tu API key de [console.anthropic.com/settings/keys](https://console.anthropic.com/settings/keys)

2. Repo → **Settings → Actions → General → Workflow permissions**
   - Marca `Read and write permissions`
   - Marca `Allow GitHub Actions to create and approve pull requests`

## Primera prueba manual

Actions → `Radar Fleet — Weekly edition` → **Run workflow** (botón arriba a
la derecha). Deja `edition_date` vacío y `allow_stub` en `false`. El runner
tardará 4-8 minutos y abrirá un PR contra `main` con label.

- `ready-to-review` → QA OK, lista la edición en preview de Vercel.
- `needs-editorial-fix` → QA bloqueó; mira `content/qa/YYYY-WW-report.md`.
- `editorial-pause` → el pipeline detectó material insuficiente; no hay edición.
- `pipeline-error` → fallo técnico (API key, fuente caída, etc.).

## Por qué este paso manual

GitHub bloquea que tokens sin scope `workflow` escriban en
`.github/workflows/`. Es correcto. Queremos que la persona humana apruebe
conscientemente la instalación del agente semanal. Una vez instalado, el
workflow se actualiza solo en PRs futuros (el runner sí tiene permisos
completos sobre el repo dentro de su ejecución).
