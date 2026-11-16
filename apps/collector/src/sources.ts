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

export const cpcbState = (apiKey: string, state: string) =>
  getText(`https://api.data.gov.in/resource/${CPCB_RESOURCE}?api-key=${apiKey}&format=json&limit=1000&filters[state]=${encodeURIComponent(state)}`);

export const cpcbStates = CPCB_STATES;

export const weatherCity = (city: string) => {
  const [lat, lon] = CITIES[city];
  return getText(`https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&hourly=${WEATHER_VARS}&timezone=UTC&past_days=1&forecast_days=1`);
};
