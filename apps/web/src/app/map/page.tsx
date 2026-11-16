import { Suspense } from "react";
import { StationMap } from "@/features/map/StationMap";
import { getStations } from "@/shared/lib/api";

async function Stations() {
  const res = await getStations();
  if (!res) return <div className="surface p-8 text-ink-2">Station data is unavailable right now.</div>;
  return <StationMap stations={res.data} />;
}

export default function MapPage() {
  return (
    <>
      <h1 className="text-4xl font-semibold tracking-tight sm:text-5xl">Where it is bad</h1>
      <p className="mb-8 mt-3 max-w-2xl text-ink-2">
        Every monitoring station, colored by its latest 24-hour NAQI category.
      </p>
      <Suspense fallback={<div className="surface aspect-[4/3] animate-pulse" />}>
        <Stations />
      </Suspense>
    </>
  );
}
