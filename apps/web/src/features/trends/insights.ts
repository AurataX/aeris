import type { Day } from "../../shared/lib/api";
export function insights(days: Day[]) {
  const valid = days.filter((d) => d.naqi != null);
  const pm = days.filter((d) => d.pm25_avg != null);
  const months = new Map<string, number[]>();
  const pollutants = new Map<string, number>();
  for (const d of valid) {
    const month = d.date_ist.slice(0, 7);
    months.set(month, [...(months.get(month) ?? []), d.naqi!]);
    if (d.dominant_pollutant)
      pollutants.set(
        d.dominant_pollutant,
        (pollutants.get(d.dominant_pollutant) ?? 0) + 1,
      );
  }
  const mean = (v: number[]) => v.reduce((a, b) => a + b, 0) / v.length;
  return {
    valid: valid.length,
    poor: valid.filter((d) => d.naqi! > 300).length,
    worst:
      [...months].sort((a, b) => mean(b[1]) - mean(a[1]))[0]?.[0] ??
      "Unavailable",
    dominant:
      [...pollutants].sort((a, b) => b[1] - a[1])[0]?.[0] ?? "Unavailable",
    exceed: pm.length
      ? (100 * pm.filter((d) => d.pm25_avg! > 60).length) / pm.length
      : null,
    pmDays: pm.length,
  };
}
