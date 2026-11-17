// CPCB proxy: data.gov.in refuses Cloudflare Workers (error 521) but answers from here (AWS Mumbai).
// The collector Worker calls this function; this function calls data.gov.in with our key.
const RESOURCE = "3b01bcb8-0b14-4abf-b6f2-c1bfd384ba69";
const STATES = ["Delhi", "Haryana", "Uttar Pradesh"];

Deno.serve(async (req) => {
  if (req.headers.get("x-aeris-token") !== Deno.env.get("CPCB_PROXY_TOKEN")) {
    return new Response("unauthorised", { status: 401 });
  }
  const state = new URL(req.url).searchParams.get("state") ?? "";
  if (!STATES.includes(state)) return new Response("unknown state", { status: 400 });

  const key = Deno.env.get("DATA_GOV_IN_API_KEY");
  const url = `https://api.data.gov.in/resource/${RESOURCE}?api-key=${key}&format=json&limit=1000&filters[state]=${encodeURIComponent(state)}`;
  // data.gov.in often answers 5xx right at :00/:30 while it refreshes, so retry a few times.
  let r = await fetch(url, { headers: { "User-Agent": "Mozilla/5.0 (AERIS university project)" } });
  for (let i = 1; i <= 3 && r.status >= 500; i++) {
    await new Promise((ok) => setTimeout(ok, 2000 * i));
    r = await fetch(url, { headers: { "User-Agent": "Mozilla/5.0 (AERIS university project)" } });
  }
  return new Response(r.body, { status: r.status, headers: { "content-type": "application/json" } });
});
