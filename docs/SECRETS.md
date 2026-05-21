# Secrets necesarios en GitHub Actions

Settings → Secrets and variables → Actions → New repository secret.

## Obligatorios

| Secret | Para qué | Cómo obtenerlo |
|---|---|---|
| `ANTHROPIC_API_KEY` | Compose editorial con Claude | console.anthropic.com → API Keys |

## Recomendados (resiliencia)

| Secret | Para qué | Cómo obtenerlo |
|---|---|---|
| `VERCEL_DEPLOY_HOOK` | Forzar redeploy explícito tras cada merge automático. Sin esto, dependemos del webhook implícito GitHub→Vercel, que se ha quedado dormido al menos una vez (N°8 del 2026-05-18). | Vercel Dashboard → proyecto `thefleetradar` → Settings → Git → Deploy Hooks → Create Hook. Nombre: `weekly-edition-redeploy`. Branch: `main`. Copia la URL completa. |

## Opcionales (notificaciones)

| Secret | Para qué | Cómo obtenerlo |
|---|---|---|
| `SLACK_WEBHOOK_URL` | Notifica al canal de publicación cuando sale una edición nueva. Si no está, `notify` salta silenciosamente. | Slack → App → Incoming Webhooks → crear webhook para el canal donde quieras publicar. **NO** uses #general si no quieres mezclar publicaciones con alertas. |
| `SLACK_WEBHOOK_ALERTS_URL` | Alertas del canary cuando una edición no llega a producción. Si no está, el canary solo abre GitHub Issue. | Slack → otro canal separado (ej. #radar-alerts). Webhook independiente. |

## Verificar configuración

Tras crear los secrets, dispara manualmente cada workflow desde Actions UI:
- `Radar Fleet — Weekly edition` → workflow_dispatch (puedes usar fecha pasada para probar sin pisar la próxima edición real).
- `Radar Fleet — Weekly deploy canary` → workflow_dispatch (con `target_date` vacío usa el lunes de esta semana).
