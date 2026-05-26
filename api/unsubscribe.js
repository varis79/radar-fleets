/**
 * GET /api/unsubscribe?email=xxx
 *
 * Marca el contacto como unsubscribed en la Audience de Resend.
 * Usa upsert: si no existe, lo crea ya como unsubscribed.
 *
 * Respuestas:
 *   200 { ok: true }
 *   400 { error: "Email inválido" }
 *   500 { error: "..." }
 */

export const config = { runtime: "edge" };

export default async function handler(req) {
  const url = new URL(req.url);
  const email = (url.searchParams.get("email") || "").trim().toLowerCase();

  if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return new Response(JSON.stringify({ error: "Email inválido" }), {
      status: 400,
      headers: { "Content-Type": "application/json" },
    });
  }

  const apiKey = process.env.RESEND_API_KEY;
  const audienceId = process.env.RESEND_AUDIENCE_ID;

  if (!apiKey || !audienceId) {
    return new Response(JSON.stringify({ error: "Configuración incompleta" }), {
      status: 500,
      headers: { "Content-Type": "application/json" },
    });
  }

  try {
    // Upsert contact with unsubscribed=true — works whether they exist or not
    const res = await fetch(
      `https://api.resend.com/audiences/${audienceId}/contacts`,
      {
        method: "POST",
        headers: {
          Authorization: `Bearer ${apiKey}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, unsubscribed: true }),
      }
    );

    if (res.status === 200 || res.status === 201 || res.status === 409) {
      return new Response(JSON.stringify({ ok: true }), {
        status: 200,
        headers: { "Content-Type": "application/json" },
      });
    }

    const err = await res.json().catch(() => ({}));
    console.error("Resend unsubscribe error:", res.status, err);
    return new Response(JSON.stringify({ error: "No se pudo procesar" }), {
      status: 500,
      headers: { "Content-Type": "application/json" },
    });
  } catch (err) {
    console.error("Fetch error:", err);
    return new Response(JSON.stringify({ error: "Error de conexión" }), {
      status: 500,
      headers: { "Content-Type": "application/json" },
    });
  }
}
