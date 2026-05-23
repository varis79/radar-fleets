/**
 * POST /api/subscribe
 * Body: { email: string }
 *
 * Añade el email a la Audience de Resend configurada en las variables
 * de entorno RESEND_API_KEY y RESEND_AUDIENCE_ID.
 *
 * Respuestas:
 *   200 { ok: true }
 *   400 { error: "Email inválido" }
 *   409 { ok: true }  ← ya estaba suscrito, no es un error real
 *   500 { error: "..." }
 */

export const config = { runtime: "edge" };

const ALLOWED_ORIGINS = [
  "https://thefleetradar.com",
  "https://www.thefleetradar.com",
];

function corsHeaders(origin) {
  const allowed = ALLOWED_ORIGINS.includes(origin)
    ? origin
    : ALLOWED_ORIGINS[0];
  return {
    "Access-Control-Allow-Origin": allowed,
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Content-Type": "application/json",
  };
}

function json(data, status = 200, origin = "") {
  return new Response(JSON.stringify(data), {
    status,
    headers: corsHeaders(origin),
  });
}

export default async function handler(req) {
  const origin = req.headers.get("origin") || "";

  // Preflight CORS
  if (req.method === "OPTIONS") {
    return new Response(null, { status: 204, headers: corsHeaders(origin) });
  }

  if (req.method !== "POST") {
    return json({ error: "Method not allowed" }, 405, origin);
  }

  // Parse body
  let email;
  try {
    const body = await req.json();
    email = (body.email || "").trim().toLowerCase();
  } catch {
    return json({ error: "Body inválido" }, 400, origin);
  }

  // Validación básica
  if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return json({ error: "Email inválido" }, 400, origin);
  }

  const apiKey = process.env.RESEND_API_KEY;
  const audienceId = process.env.RESEND_AUDIENCE_ID;

  if (!apiKey || !audienceId) {
    console.error("Faltan variables de entorno RESEND_API_KEY o RESEND_AUDIENCE_ID");
    return json({ error: "Configuración incompleta" }, 500, origin);
  }

  // Llamada a Resend Contacts API
  try {
    const res = await fetch(
      `https://api.resend.com/audiences/${audienceId}/contacts`,
      {
        method: "POST",
        headers: {
          Authorization: `Bearer ${apiKey}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email,
          unsubscribed: false,
        }),
      }
    );

    // 200 o 201 → éxito
    if (res.status === 200 || res.status === 201) {
      return json({ ok: true }, 200, origin);
    }

    // 409 → ya existe, lo tratamos como éxito silencioso
    if (res.status === 409) {
      return json({ ok: true }, 200, origin);
    }

    const errorBody = await res.json().catch(() => ({}));
    console.error("Resend error:", res.status, errorBody);
    return json({ error: "Error al registrar el email" }, 500, origin);
  } catch (err) {
    console.error("Fetch error:", err);
    return json({ error: "Error de conexión" }, 500, origin);
  }
}
