import { calendar } from "@/shared/lib/calendar";
import { getDaily } from "@/shared/lib/api";
import { TrendChart, type Row } from "./TrendChart";
export async function TrendData({
  city,
  days,
}: {
  city: string;
  days: number;
}) {
  const cities =
    city === "All"
      ? ["Delhi", "Gurugram", "Noida", "Ghaziabad", "Faridabad"]
      : [city];
  const all = await Promise.all(cities.map((c) => getDaily(c, days)));
  const dates = new Map<string, Row>();
  all.forEach((res, i) =>
    res?.data.forEach((d) => {
      const row = dates.get(d.date_ist) ?? { date: d.date_ist };
      row[cities[i]] = d.naqi;
      dates.set(d.date_ist, row);
    }),
  );
  const rows: Row[] = calendar(
    [...dates.values()].map((r) => ({ ...r, date_ist: r.date })),
  ).map((r) => ({ ...r, date: r.date_ist }));
  return (
    <section className="surface p-6">
      {rows.length ? (
        <>
          <TrendChart rows={rows} />
          <details className="mt-4">
            <summary>Show observations as a table</summary>
            <div className="overflow-auto max-h-80">
              <table className="w-full text-sm">
                <caption>Daily IN_NAQI_CPCB · OpenAQ</caption>
                <thead>
                  <tr>
                    <th>Date</th>
                    {cities.map((c) => (
                      <th key={c}>{c}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {rows.map((r) => (
                    <tr key={r.date}>
                      <th>{r.date}</th>
                      {cities.map((c) => (
                        <td className="text-center p-2" key={c}>
                          {r[c] ?? "Missing"}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </details>
        </>
      ) : (
        <p>No observations returned for this range.</p>
      )}
      <p className="caption mt-4">
        IN_NAQI_CPCB · OpenAQ. {all.filter((r) => !r).length} city requests
        unavailable. Higher lines indicate higher indices, not higher
        concentrations. Missing values remain gaps.
      </p>
    </section>
  );
}
