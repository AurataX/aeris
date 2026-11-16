import { runtime } from "@/shared/lib/runtime";
import { GoogleMap } from "@/features/map/GoogleMap";
import { Suspense } from "react";
import { StationMap } from "@/features/map/StationMap";
import { getStations } from "@/shared/lib/api";

async function Stations() {
  const res = await getStations();
  if (!res)
    return (
      <div className="surface p-8 text-ink-2">
        Station data is unavailable right now.
      </div>
    );
  return (
    <>
      <GoogleMap
        stations={res.data}
        apiKey={runtime("NEXT_PUBLIC_GOOGLE_MAPS_API_KEY") ?? ""}
        mapId={runtime("NEXT_PUBLIC_GOOGLE_MAP_ID") ?? ""}
      />
      <StationMap stations={res.data} />
    </>
  );
}

export default function MapPage() {
  return (
    <>
      <h1 className="text-4xl font-semibold tracking-tight sm:text-5xl">
        Find a monitoring station
      </h1>
      <p className="mb-8 mt-3 max-w-2xl text-ink-2">
        Browse available station measurements, categories and observation times.
        Stale readings are labelled.
      </p>
      <Suspense
        fallback={<div className="surface aspect-[4/3] animate-pulse" />}
      >
        <Stations />
      </Suspense>
    </>
  );
}
