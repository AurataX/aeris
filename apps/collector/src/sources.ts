import { CITIES, CPCB_RESOURCE, CPCB_STATES, WEATHER_VARS, half } from "./config";

const UA = { "User-Agent": "Mozilla/5.0 (AERIS university project)" }; // data.gov.in blocks default agents

async function getJson(url: string, headers: Record<string, string> = {}) {
  const r = await fetch(url, { headers: { ...UA, ...headers } });
  if (!r.ok) throw new Error(`${r.status} ${url.split("?")[0]}`);
  return r.json();
}

export async function openaqLatest(apiKey: string, group: number) {
  const out = [];
  for (const id of half(group)) {
    const d: any = await getJson(`https://api.openaq.org/v3/locations/${id}/latest`, { "X-API-Key": apiKey });
    out.push({ locationsId: id, results: d.results });
  }
  return out;
}

export async function cpcbSnapshot(apiKey: string) {
  const rows = [];
  for (const state of CPCB_STATES) {
    const url = `https://api.data.gov.in/resource/${CPCB_RESOURCE}?api-key=${apiKey}&format=json&limit=1000&filters[state]=${encodeURIComponent(state)}`;
    const d: any = await getJson(url);
    rows.push(...d.records);
  }
  return rows;
}

export async function weatherNow() {
  const out: Record<string, unknown> = {};
  for (const [city, [lat, lon]] of Object.entries(CITIES)) {
    out[city] = await getJson(
      `https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&hourly=${WEATHER_VARS}&timezone=UTC&past_days=1&forecast_days=1`,
    );
  }
  return out;
}
