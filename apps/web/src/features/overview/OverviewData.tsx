import { getCities, getDaily } from "@/shared/lib/api";
import { observed } from "@/shared/lib/format";
import { CityCard } from "./CityCard";
export async function OverviewData() {
  const res = await getCities();
  if (!res?.data.length)
    return (
      <div className="surface p-8">
        City observations could not be loaded from the API. Try refreshing this
        page.
      </div>
    );
  const series = await Promise.all(res.data.map((c) => getDaily(c.city, 30)));
  const latest = res.data
    .map((c) => c.as_of)
    .filter(Boolean)
    .sort()
    .at(-1);
  return (
    <>
      <div className="notice">
        <strong>Latest available observations</strong>
        <span>
          {observed(latest)} · Daily aggregates, not a live feed. A recent sync
          does not mean recent measurements.
        </span>
      </div>
      <div className="city-grid">
        {res.data.map((c, i) => (
          <CityCard
            key={c.city}
            city={c}
            source={res.meta.source}
            days={series[i]?.data ?? []}
          />
        ))}
      </div>
    </>
  );
}
