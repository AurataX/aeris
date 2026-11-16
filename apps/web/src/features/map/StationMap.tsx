"use client";

import { useState } from "react";
import type { Station } from "@/shared/lib/api";
import { categoryColor } from "@/shared/lib/aqi";
import { CategoryChip } from "@/shared/ui/CategoryChip";

// Plain SVG map from real coordinates, so it works without a map key. Google Maps can replace it later.
const BOX = { minLon: 76.85, maxLon: 77.55, minLat: 28.25, maxLat: 28.85 };
const px = (s: Station) => ({
  x: ((s.lon - BOX.minLon) / (BOX.maxLon - BOX.minLon)) * 100,
  y: (1 - (s.lat - BOX.minLat) / (BOX.maxLat - BOX.minLat)) * 100,
});

export function StationMap({ stations }: { stations: Station[] }) {
  const [picked, setPicked] = useState<Station | null>(null);
  return (
    <div className="grid gap-4 md:grid-cols-[2fr_1fr]">
      <div className="surface relative aspect-square overflow-hidden p-0 md:aspect-[4/3]">
        <svg viewBox="0 0 100 100" className="h-full w-full" role="group" aria-label="Monitoring stations">
          {stations.map((s) => {
            const { x, y } = px(s);
            return (
              <circle key={s.station_id} cx={x} cy={y} r={picked?.station_id === s.station_id ? 2.4 : 1.6}
                      fill={categoryColor(s.naqi_category)} opacity={s.is_stale ? 0.45 : 0.95}
                      stroke="#fff" strokeWidth={0.4} className="cursor-pointer transition-all"
                      onClick={() => setPicked(s)}>
                <title>{s.name}</title>
              </circle>
            );
          })}
        </svg>
      </div>
      <aside className="surface p-5" aria-live="polite">
        {picked ? (
          <>
            <h2 className="font-semibold">{picked.name}</h2>
            <p className="mb-3 text-sm text-ink-3">{picked.city}</p>
            <CategoryChip category={picked.naqi_category} />
            <p className="mt-4 text-4xl font-semibold">{picked.naqi_24h ?? "n/a"}</p>
            <p className="text-xs text-ink-3">NAQI · PM2.5 now {picked.pm25_latest ?? "n/a"} µg/m³</p>
            <p className="mt-3 text-xs text-ink-3">
              {picked.is_stale ? "Stale: no reading in the last 3 hours." : "Reporting."} Last reading {picked.last_observed_at ?? "n/a"} UTC
            </p>
          </>
        ) : (
          <p className="text-sm text-ink-2">Select a station to see its latest reading. Faded dots have not reported recently.</p>
        )}
      </aside>
    </div>
  );
}
