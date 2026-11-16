import { Calendar } from "@/features/trends/Calendar";
import { WeatherEvidence } from "@/features/trends/WeatherEvidence";
import { TrendData } from "@/features/trends/TrendData";
import { CityInsights } from "@/features/trends/CityInsights";
const cities = ["Delhi", "Gurugram", "Noida", "Ghaziabad", "Faridabad"];
export default async function Trends({
  searchParams,
}: {
  searchParams: Promise<{ city?: string; days?: string }>;
}) {
  const q = await searchParams;
  const city = cities.includes(q.city ?? "") ? q.city! : "All";
  const days = [7, 30, 90, 365].includes(Number(q.days)) ? Number(q.days) : 90;
  return (
    <>
      <p className="eyebrow">PATTERNS, NOT JUST SNAPSHOTS</p>
      <h1>See beyond today.</h1>
      <p className="intro">
        Explore observed city-day indices, historical exceedances and the
        relationship between pollution and weather.
      </p>
      <form className="surface flex flex-wrap gap-4 items-end p-4 mb-6">
        <label>
          City
          <select
            name="city"
            defaultValue={city}
            className="block p-3 bg-bg rounded-xl"
          >
            <option>All</option>
            {cities.map((c) => (
              <option key={c}>{c}</option>
            ))}
          </select>
        </label>
        <label>
          Range
          <select
            name="days"
            defaultValue={days}
            className="block p-3 bg-bg rounded-xl"
          >
            {[7, 30, 90, 365].map((d) => (
              <option key={d} value={d}>
                {d} days
              </option>
            ))}
          </select>
        </label>
        <button className="text-primary" type="submit">
          Apply filters ·
        </button>
      </form>
      <TrendData city={city} days={days} />
      <Calendar city={city === "All" ? "Delhi" : city} />
      <WeatherEvidence city={city === "All" ? "Delhi" : city} />
      <h2 className="section-heading">A year of hidden insights</h2>
      <div className="grid gap-4 md:grid-cols-2">
        {(city === "All" ? cities : [city]).map((c) => (
          <CityInsights key={c} city={c} />
        ))}
      </div>
    </>
  );
}
