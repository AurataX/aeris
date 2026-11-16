"use client";
import { useState } from "react";
import type { Station } from "@/shared/lib/api";
import { CategoryChip } from "@/shared/ui/CategoryChip";
import { observed } from "@/shared/lib/format";
export function StationMap({ stations }: { stations: Station[] }) {
  const [city, setCity] = useState("All");
  const [query, setQuery] = useState("");
  const shown = stations.filter(
    (s) =>
      (city === "All" || s.city === city) &&
      s.name.toLowerCase().includes(query.toLowerCase()),
  );
  return (
    <>
      <div className="surface p-4 flex flex-wrap gap-4 mb-5">
        <label>
          City
          <select
            value={city}
            onChange={(e) => setCity(e.target.value)}
            className="block bg-bg p-3 rounded-xl"
          >
            <option>All</option>
            {[...new Set(stations.map((s) => s.city))].map((c) => (
              <option key={c}>{c}</option>
            ))}
          </select>
        </label>
        <label>
          Find a station
          <input
            className="block bg-bg p-3 rounded-xl"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Station name"
          />
        </label>
      </div>
      <p role="status" className="caption mb-4">
        {shown.length} stations · IN_NAQI_CPCB · OpenAQ
      </p>
      <div className="grid gap-4 md:grid-cols-2">
        {shown.map((s) => (
          <article key={s.station_id} className="surface p-5">
            <h2>{s.name}</h2>
            <p className="caption">
              {s.city} · {s.lat}, {s.lon}
            </p>
            <p className="text-3xl my-3">
              {s.naqi_24h ?? "Unavailable"}{" "}
              <span className="caption">NAQI</span>
            </p>
            <CategoryChip category={s.naqi_category} />
            <p className="caption mt-3">
              PM2.5: {s.pm25_latest ?? "Unavailable"} µg/m³
            </p>
            <p className="caption">
              {s.is_stale ? "Stale" : "Recent"} · {observed(s.last_observed_at)}
            </p>
          </article>
        ))}
      </div>
      {!shown.length && <p>No stations match these filters.</p>}
    </>
  );
}
