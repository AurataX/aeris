import { getDaily, get } from "@/shared/lib/api";
import { number } from "@/shared/lib/format";
import { insights } from "./insights";
export async function CityInsights({ city }: { city: string }) {
  const [daily, weather] = await Promise.all([
    getDaily(city, 365),
    get<{ data: unknown[]; meta: { pearson_pm25: { wind: number | null } } }>(
      `/weather/correlation?city=${city}`,
    ),
  ]);
  if (!daily?.data.length)
    return (
      <section className="surface p-6">
        No historical observations available for {city}.
      </section>
    );
  const s = insights(daily.data);
  return (
    <section className="surface p-6">
      <h3>{city} · beneath the average</h3>
      <dl className="grid grid-cols-2 gap-5 my-5">
        <div>
          <dt>Very Poor or Severe</dt>
          <dd>
            {s.poor} / {s.valid} valid days
          </dd>
        </div>
        <div>
          <dt>Highest monthly mean NAQI</dt>
          <dd>{s.worst}</dd>
        </div>
        <div>
          <dt>Most frequent dominant pollutant</dt>
          <dd>{s.dominant}</dd>
        </div>
        <div>
          <dt>Days PM2.5 exceeded 60 µg/m³</dt>
          <dd>
            {number(s.exceed, 1)}% of {s.pmDays} measured days
          </dd>
        </div>
        <div>
          <dt>PM2.5 vs wind · Pearson r</dt>
          <dd>{number(weather?.meta.pearson_pm25.wind, 3)}</dd>
        </div>
      </dl>
      <p className="caption">
        Requested window: past 365 days · available dates{" "}
        {daily.data[0].date_ist}·{daily.data.at(-1)?.date_ist}. IN_NAQI_CPCB ·
        OpenAQ; weather: Open-Meteo model.
      </p>
      <p className="text-sm text-ink-2 mt-3">
        Only observed days enter these percentages. Months with different
        coverage are not equally representative. A negative r means higher wind
        coincided with lower PM2.5; it does not prove a cause.
      </p>
    </section>
  );
}
