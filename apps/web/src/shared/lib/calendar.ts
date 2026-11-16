export function calendar<T extends { date_ist: string }>(
  rows: T[],
): (T | { date_ist: string; naqi: null })[] {
  if (!rows.length) return [];
  const ordered = [...rows].sort((a, b) =>
    a.date_ist.localeCompare(b.date_ist),
  );
  const byDate = new Map(ordered.map((r) => [r.date_ist, r]));
  const result = [];
  for (
    let t = Date.parse(ordered[0].date_ist);
    t <= Date.parse(ordered.at(-1)!.date_ist);
    t += 86400000
  ) {
    const date_ist = new Date(t).toISOString().slice(0, 10);
    result.push(byDate.get(date_ist) ?? { date_ist, naqi: null });
  }
  return result;
}
