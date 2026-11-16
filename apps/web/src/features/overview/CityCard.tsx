import { calendar } from "@/shared/lib/calendar";
import Link from "next/link";
import type { City, Day } from "@/shared/lib/api";
import { categoryColor } from "@/shared/lib/aqi";
import { number, observed } from "@/shared/lib/format";
import { CategoryChip } from "@/shared/ui/CategoryChip";
import { Sparkline } from "./Sparkline";
export function CityCard({
  city,
  days,
  source,
}: {
  city: City;
  days: Day[];
  source: string;
}) {
  return (
    <article className="surface city-card">
      <header>
        <h2>{city.city}</h2>
        <CategoryChip category={city.naqi_category} />
      </header>
      <p
        className="aqi-number"
        style={{ color: categoryColor(city.naqi_category) }}
      >
        {number(city.naqi)}
      </p>
      <p className="caption">
        {city.index_standard} · {source}
        <br />
        Dominant pollutant:{" "}
        {city.dominant_pollutant === "pm25"
          ? "PM2.5"
          : (city.dominant_pollutant ?? "Unavailable")}
      </p>
      <Sparkline
        values={calendar(days).map((d) => d.naqi)}
        color={categoryColor(city.naqi_category)}
      />
      <p className="caption">30-day NAQI · gaps mean insufficient coverage</p>
      <dl className="metrics">
        <div>
          <dt>PM2.5 · 24h</dt>
          <dd>{number(city.pm25_avg_24h, 1)} µg/m³</dd>
        </div>
        <div>
          <dt>Temperature</dt>
          <dd>{number(city.temperature_c, 1)} °C</dd>
        </div>
        <div>
          <dt>Wind</dt>
          <dd>{number(city.wind_speed_kmh, 1)} km/h</dd>
        </div>
      </dl>
      <p className="caption">Weather: Open-Meteo model data</p>
      <footer>
        <p>Observed {observed(city.as_of)}</p>
        <p>
          {city.stations_reporting} stations reporting now · historical AQI
          retained
        </p>
      </footer>
      <Link className="text-primary" href={`/trends?city=${city.city}`}>
        Explore {city.city} ·
      </Link>
    </article>
  );
}
