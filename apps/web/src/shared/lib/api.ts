import { cacheLife, cacheTag } from "next/cache";

const BASE = process.env.API_URL ?? "http://localhost:8000";

export type City = {
  city: string; as_of_date: string; naqi: number | null; naqi_category: string | null;
  dominant_pollutant: string | null; pm25_avg_24h: number | null; pm10_avg_24h: number | null;
  stations_reporting: number; temperature_c: number | null; humidity_pct: number | null;
  wind_speed_kmh: number | null; index_standard: string;
};
export type Day = { city: string; date_ist: string; naqi: number | null; naqi_category: string | null; pm25_avg: number | null };
export type Station = {
  station_id: string; name: string; city: string; lat: number; lon: number; naqi_24h: number | null;
  naqi_category: string | null; pm25_latest: number | null; is_stale: boolean; last_observed_at: string | null;
};
export type TableStat = { layer: string; table_name: string; row_count: number; computed_at: string };

// Cached for 5 minutes. The pipeline's sync step calls /api/revalidate, which clears the "gold" tag at once.
async function get<T>(path: string): Promise<T | null> {
  "use cache";
  cacheLife({ stale: 60, revalidate: 300, expire: 3600 });
  cacheTag("gold");
  try {
    const r = await fetch(`${BASE}/api/v1${path}`);
    return r.ok ? ((await r.json()) as T) : null;
  } catch {
    return null; // the page shows an honest "data unavailable" state instead of crashing
  }
}

export const getCities = () => get<{ data: City[] }>("/cities/latest");
export const getStations = () => get<{ data: Station[] }>("/stations");
export async function getDaily(city: string, days = 90) {
  "use cache"; // the date math below must run inside a cache scope (Cache Components rule)
  cacheLife({ stale: 60, revalidate: 300, expire: 3600 });
  cacheTag("gold");
  const end = new Date().toISOString().slice(0, 10);
  const start = new Date(Date.now() - days * 864e5).toISOString().slice(0, 10);
  return get<{ data: Day[] }>(`/cities/${city}/daily?start=${start}&end=${end}`);
}
export const getTables = () => get<{ data: TableStat[]; meta: { last_sync: { finished_at: string } | null } }>("/pipeline/tables");
