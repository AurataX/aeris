import type { TableStat } from "@/shared/lib/api";

const LAYERS = [
  { key: "bronze", title: "Bronze", note: "raw, exactly as received", tint: "#b7791f" },
  { key: "silver", title: "Silver", note: "clean, hourly, in µg/m³", tint: "#64748b" },
  { key: "gold", title: "Gold", note: "analytics-ready", tint: "#d4a72c" },
] as const;

const short = (n: number) => (n >= 1e6 ? `${(n / 1e6).toFixed(1)}M` : n >= 1e3 ? `${(n / 1e3).toFixed(1)}k` : String(n));

export function Medallion({ tables }: { tables: TableStat[] }) {
  return (
    <div className="grid gap-4 md:grid-cols-3">
      {LAYERS.map((l) => {
        const rows = tables.filter((t) => t.layer === l.key);
        return (
          <section key={l.key} className="surface p-5" aria-label={l.title}>
            <h2 className="flex items-center gap-2 font-semibold">
              <span className="size-2.5 rounded-full" style={{ background: l.tint }} /> {l.title}
            </h2>
            <p className="mb-4 text-xs text-ink-3">{l.note}</p>
            <ul className="space-y-2 text-sm">
              {rows.map((t) => (
                <li key={t.table_name} className="flex justify-between gap-3">
                  <span className="truncate text-ink-2">{t.table_name.split(".")[1]}</span>
                  <span className="font-medium">{short(t.row_count)}</span>
                </li>
              ))}
            </ul>
          </section>
        );
      })}
    </div>
  );
}
