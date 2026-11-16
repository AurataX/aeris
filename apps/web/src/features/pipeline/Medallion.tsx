import type { TableStat } from "@/shared/lib/api";
import { number, observed } from "@/shared/lib/format";
export function Medallion({ tables }: { tables: TableStat[] }) {
  return (
    <div className="grid gap-4 lg:grid-cols-3">
      {["bronze", "silver", "gold"].map((layer) => (
        <section className="surface p-5 min-w-0" key={layer}>
          <h3 className="capitalize mb-4">{layer}</h3>
          <ul className="space-y-4">
            {tables
              .filter((t) => t.layer === layer)
              .map((t) => (
                <li key={t.table_name}>
                  <p className="text-sm break-all text-ink-2">{t.table_name}</p>
                  <p className="text-2xl font-semibold">
                    {number(t.row_count)} <span className="caption">rows</span>
                  </p>
                  <p className="caption">Counted {observed(t.computed_at)}</p>
                </li>
              ))}
          </ul>
          {!tables.some((t) => t.layer === layer) && <p>Counts unavailable.</p>}
        </section>
      ))}
    </div>
  );
}
