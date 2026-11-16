import { get } from "@/shared/lib/api";
import { WeatherChart, type WeatherPoint } from "./WeatherChart";
export async function WeatherEvidence({ city }: { city: string }) {
  const res = await get<{ data: WeatherPoint[] }>(
    `/weather/correlation?city=${city}`,
  );
  return (
    <section className="surface p-6 mt-6">
      <h2>{city} · does wind coincide with cleaner air?</h2>
      <p className="caption my-3">
        Past 365 days · OpenAQ PM2.5 × Open-Meteo modelled wind
      </p>
      <WeatherChart data={res?.data ?? []} />
      <p className="text-sm text-ink-2">
        Each point pairs a day’s wind speed and PM2.5 concentration. Seasonal
        changes and other factors can influence both; the chart does not
        establish causation.
      </p>
      <details className="mt-4">
        <summary>Show weather pairs</summary>
        <div className="max-h-64 overflow-auto">
          <table className="w-full text-sm">
            <thead>
              <tr>
                <th>Date</th>
                <th>Wind km/h</th>
                <th>PM2.5 µg/m³</th>
              </tr>
            </thead>
            <tbody>
              {res?.data.map((d) => (
                <tr key={d.date_ist}>
                  <th>{d.date_ist}</th>
                  <td>{d.wind_avg_kmh?.toFixed(2) ?? "Missing"}</td>
                  <td>{d.pm25_avg?.toFixed(2) ?? "Missing"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </details>
    </section>
  );
}
