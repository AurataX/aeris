import { CITIES, CPCB_RESOURCE, CPCB_STATES, WEATHER_VARS, half } from "./config";

const UA = { "User-Agent": "Mozilla/5.0 (AERIS university project)" }; // data.gov.in blocks default agents

// Responses stay raw text: no JSON.parse/stringify, so the free plan's 10 ms CPU limit is never an issue.
async function getText(url: string, headers: Record<string, string> = {}): Promise<string> {
  const r = await fetch(url, { headers: { ...UA, ...headers } });
  if (!r.ok) throw new Error(`${r.status} ${url.split("?")[0]}`);
  return r.text();
}

export async function openaqLatest(apiKey: string, group: number): Promise<string> {
  const parts = [];
  for (const id of half(group)) {
    parts.push(await getText(`https://api.openaq.org/v3/locations/${id}/latest`, { "X-API-Key": apiKey }));
  }
  return `[${parts.join(",")}]`;
}

// data.gov.in answers 521 to Cloudflare Workers, so we ask our Supabase Edge Function (AWS Mumbai) to fetch it.
export const cpcbState = (supabaseUrl: string, proxyToken: string, state: string) =>
  getText(`${supabaseUrl}/functions/v1/cpcb?state=${encodeURIComponent(state)}`, { "x-aeris-token": proxyToken, "x-region": "ap-south-1" }); // data.gov.in only accepts connections from India, so pin the function to Mumbai

export const cpcbStates = CPCB_STATES;

export const weatherCity = (city: string) => {
  const [lat, lon] = CITIES[city];
  return getText(`https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&hourly=${WEATHER_VARS}&timezone=UTC&past_days=1&forecast_days=1`);
};
