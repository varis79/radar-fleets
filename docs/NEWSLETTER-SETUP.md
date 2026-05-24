# Newsletter — setup operativo

The Fleet Radar usa **[Resend](https://resend.com)** como provider de
newsletter (broadcasts + audiences). El endpoint `/api/subscribe`
(`api/subscribe.js`) ya está implementado y desplegado en Vercel.

## Estado actual

✅ **Endpoint funcionando**: `POST /api/subscribe` con `{ email: string }`
✅ **Form integrado** en `index.html` (sección `.newsletter-band`)
✅ **CORS configurado** para `thefleetradar.com`
✅ **Validación de email** + manejo idempotente de duplicados (409 → ok)

⚠️ **Faltan env vars en Vercel** (por eso el form devuelve 500 ahora).

## Setup (15 min, una vez)

### 1. Crear cuenta y audience en Resend

1. https://resend.com → Sign up (free hasta 3.000 emails/mes)
2. Settings → API Keys → Create API Key (full access)
3. Audiences → Create Audience → "The Fleet Radar Subscribers"
4. Copia el `audience_id` de la URL (formato: `abc123de-f456-...`)

### 2. Configurar variables de entorno en Vercel

```
vercel env add RESEND_API_KEY production
# pega la API key cuando lo pida

vercel env add RESEND_AUDIENCE_ID production
# pega el audience_id

vercel deploy --prod
```

O via UI: https://vercel.com/[org]/radar-fleets/settings/environment-variables

### 3. Configurar dominio sender en Resend

1. Resend → Domains → Add `thefleetradar.com`
2. Añadir los registros DNS que muestra (SPF, DKIM, DMARC) en Vercel/Cloudflare
3. Verificar (suele tardar <30 min)

### 4. Crear el broadcast template

1. Resend → Broadcasts → Create Broadcast
2. Subject: `Nº {N} · {Cover headline} · The Fleet Radar`
3. From: `team@thefleetradar.com`
4. HTML: usar el contenido del magazine de la semana (o un wrapper simplificado)

### 5. Automatizar envío semanal (opcional, segunda fase)

Añadir paso a `.github/workflows/weekly-edition.yml` tras `publish.py`:

```yaml
- name: Send newsletter broadcast
  if: success()
  run: |
    EDITION_FILE=$(ls magazines/2026-*.html | sort | tail -1)
    python3 scripts/send_newsletter.py --file "$EDITION_FILE"
  env:
    RESEND_API_KEY: ${{ secrets.RESEND_API_KEY }}
    RESEND_AUDIENCE_ID: ${{ secrets.RESEND_AUDIENCE_ID }}
```

(El script `scripts/send_newsletter.py` queda como deuda; el endpoint API
de Resend para crear y enviar broadcasts es directo.)

## Cambiar de provider

Si más adelante quieres cambiar a Mailchimp, Beehiiv, ConvertKit, etc.,
solo hay que reescribir `api/subscribe.js` (el form HTML no cambia).
Las opciones más populares:

| Provider | Fortaleza | Free tier |
|---|---|---|
| **Resend** (actual) | Devs friendly, transactional + lists | 3k emails/mes |
| Beehiiv | Newsletter-first, gran analítica | 2.5k subs |
| ConvertKit / Kit | Creator-focused, automation | 1k subs |
| Mailchimp | Ubicuo, marketing completo | 500 subs |
| Buttondown | Minimalista, MDX support | 100 subs |

## Testing local

```bash
# Local con stub (sin enviar a Resend):
unset RESEND_API_KEY RESEND_AUDIENCE_ID
vercel dev
# Forma → devuelve 500 "Configuración incompleta" (esperado sin vars)

# Local conectado a Resend:
export RESEND_API_KEY=re_xxx
export RESEND_AUDIENCE_ID=abc-xxx
vercel dev
# Forma → 200 OK, suscripción real
```
