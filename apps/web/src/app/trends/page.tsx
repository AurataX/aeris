import { Suspense } from "react";
import { TrendChart, type Row } from "@/features/trends/TrendChart";
import { getDaily } from "@/shared/lib/api";

const CITIES = ["Delhi", "Gurugram", "Noida", "Ghaziabad", "Faridabad"];

async function Chart() {
  const all = await Promise.all(CITIES.map((c) => getDaily(c, 180)));
  if (all.every((r) => !r)) return <div className="surface p-8 text-ink-2">Trend data is unavailable right now.</div>;

  const byDate = new Map<string, Row>();
  all.forEach((res, i) =>
    res?.data.forEach((d) => {
      const row = byDate.get(d.date_ist) ?? { date: d.date_ist };
      row[CITIES[i]] = d.naqi;
      byDate.set(d.date_ist, row);
    }),
  );
  const rows = [...byDate.values()].sort((a, b) => a.date.localeCompare(b.date));

  return (
    <div className="surface p-6">
      <TrendChart rows={rows} />
      <p className="mt-3 text-xs text-ink-3">
        Daily Indian NAQI (0 to 500) from OpenAQ ground monitors, computed by AERIS. A day needs at least 16 hours of
        data; days without enough data are left as gaps.
      </p>
    </div>
  );
}

export default function Trends() {
  return (
    <>
      <h1 className="text-4xl font-semibold tracking-tight sm:text-5xl">How the air changes</h1>
      <p className="mb-8 mt-3 max-w-2xl text-ink-2">Last 180 days, all five cities. Winter smog shows up every year.</p>
      <Suspense fallback={<div className="surface h-[430px] animate-pulse" />}>
        <Chart />
      </Suspense>
    </>
  );
}
