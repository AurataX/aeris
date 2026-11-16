import { Suspense } from "react";
import { CityCard } from "@/features/overview/CityCard";
import { getCities, getDaily } from "@/shared/lib/api";

async function Cards() {
  const res = await getCities();
  if (!res) return <Unavailable />;
  const cities = res.data;
  const series = await Promise.all(cities.map((c) => getDaily(c.city, 30)));

  return (
    <div className="grid gap-4 md:grid-cols-4 md:auto-rows-fr">
      {cities.map((c, i) => (
        <CityCard key={c.city} city={c} days={series[i]?.data ?? []} large={c.city === "Delhi"} />
      ))}
    </div>
  );
}

const Unavailable = () => (
  <div className="surface p-8 text-ink-2">
    Air-quality data is unavailable right now. The pipeline publishes it to the database; please try again shortly.
  </div>
);

export default function Overview() {
  return (
    <>
      <h1 className="text-4xl font-semibold tracking-tight sm:text-5xl">Delhi NCR air, right now</h1>
      <p className="mb-8 mt-3 max-w-2xl text-ink-2">
        Indian NAQI per city, computed with the CPCB method from 62 ground monitors. Updated whenever the data
        pipeline finishes a run.
      </p>
      <Suspense fallback={<div className="surface h-96 animate-pulse" />}>
        <Cards />
      </Suspense>
    </>
  );
}
