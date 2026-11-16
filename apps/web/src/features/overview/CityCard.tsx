import { Icon } from "@/shared/icons/Icon";
import type { City, Day } from "@/shared/lib/api";
import { categoryColor } from "@/shared/lib/aqi";
import { CategoryChip } from "@/shared/ui/CategoryChip";
import { Sparkline } from "./Sparkline";

const pollutantName: Record<string, string> = { pm25: "PM2.5", pm10: "PM10", no2: "NO₂", so2: "SO₂", o3: "O₃" };
const fmt = (n: number | null, digits = 0) => (n == null ? "n/a" : n.toFixed(digits));

export function CityCard({ city, days, large }: { city: City; days: Day[]; large?: boolean }) {
  return (
    <article className={`surface flex flex-col gap-4 p-6 ${large ? "md:col-span-2 md:row-span-2" : ""}`}>
      <header className="flex items-center justify-between">
        <h2 className="text-lg font-semibold">{city.city}</h2>
        <CategoryChip category={city.naqi_category} />
      </header>

      <div>
        <p className={`font-semibold leading-none tracking-tight ${large ? "text-8xl" : "text-6xl"}`}
           style={{ color: categoryColor(city.naqi_category) }}>
          {fmt(city.naqi)}
        </p>
        <p className="mt-2 text-xs uppercase tracking-[0.08em] text-ink-3">
          NAQI · dominant {pollutantName[city.dominant_pollutant ?? ""] ?? "n/a"}
        </p>
      </div>

      <Sparkline values={days.map((d) => d.naqi)} color={categoryColor(city.naqi_category)} />

      <dl className="mt-auto grid grid-cols-3 gap-2 text-sm">
        <div><dt className="text-xs text-ink-3">PM2.5 24 h</dt><dd>{fmt(city.pm25_avg_24h)} µg/m³</dd></div>
        <div><dt className="text-xs text-ink-3">Temp</dt><dd>{fmt(city.temperature_c, 1)} °C</dd></div>
        <div><dt className="text-xs text-ink-3">Wind</dt><dd className="flex items-center gap-1"><Icon name="wind" size={14} />{fmt(city.wind_speed_kmh, 1)} km/h</dd></div>
      </dl>

      <p className="flex items-center gap-1.5 text-xs text-ink-3">
        <Icon name="clock" size={14} /> latest complete day {city.as_of_date} · {city.stations_reporting} stations reporting
      </p>
    </article>
  );
}
