"use client";
import { useState } from "react";
import { APIProvider, Map, AdvancedMarker } from "@vis.gl/react-google-maps";
import type { Station } from "@/shared/lib/api";
import { categoryColor } from "@/shared/lib/aqi";
import { observed } from "@/shared/lib/format";
export function GoogleMap({
  stations,
  apiKey,
  mapId,
}: {
  stations: Station[];
  apiKey: string;
  mapId: string;
}) {
  const [enabled, setEnabled] = useState(false);
  const [failed, setFailed] = useState(false);
  const [picked, setPicked] = useState<Station | null>(null);
  if (!apiKey || !mapId)
    return (
      <div className="notice">
        <strong>Map not configured</strong>
        <span>
          The map needs its browser key and Map ID. The station directory
          remains available.
        </span>
      </div>
    );
  if (!enabled)
    return (
      <div className="notice">
        <strong>Explore the station map</strong>
        <span>Load Google Maps to see monitoring locations.</span>
        <button onClick={() => setEnabled(true)}>Open interactive map →</button>
      </div>
    );
  return (
    <section className="surface p-4 mb-6">
      <APIProvider apiKey={apiKey} onError={() => setFailed(true)}>
        <Map
          mapId={mapId}
          defaultCenter={{ lat: 28.6, lng: 77.2 }}
          defaultZoom={10}
          style={{ height: 420 }}
          gestureHandling="cooperative"
        >
          {stations
            .filter((s) => Number.isFinite(s.lat) && Number.isFinite(s.lon))
            .map((s) => (
              <AdvancedMarker
                key={s.station_id}
                position={{ lat: s.lat, lng: s.lon }}
                title={s.name}
                onClick={() => setPicked(s)}
              >
                <span
                  className="block size-5 rounded-full border-2 border-surface"
                  style={{
                    background: categoryColor(s.naqi_category),
                    opacity: s.is_stale ? 0.5 : 1,
                  }}
                />
              </AdvancedMarker>
            ))}
        </Map>
      </APIProvider>
      {failed && (
        <p role="alert">Map failed to load. Use the station directory below.</p>
      )}
      <p className="caption mt-4" aria-live="polite">
        {picked
          ? `${picked.name}: ${picked.naqi_24h ?? "Missing"} · IN_NAQI_CPCB · OpenAQ · ${observed(picked.last_observed_at)}`
          : "Select a station. Faded markers indicate stale readings. Full observations are in the directory below."}
      </p>
    </section>
  );
}
