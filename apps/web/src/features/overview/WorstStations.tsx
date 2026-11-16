import Link from "next/link";
import { getStations } from "@/shared/lib/api";
import { observed } from "@/shared/lib/format";
import { CategoryChip } from "@/shared/ui/CategoryChip";
export async function WorstStations() {
  const res = await getStations();
  const stations = res?.data
    .filter((s) => s.naqi_24h != null)
    .sort((a, b) => b.naqi_24h! - a.naqi_24h!)
    .slice(0, 3);
  return (
    <section>
      <div className="section-heading">
        <h2>Highest station indices</h2>
        <Link href="/map">All stations ·</Link>
      </div>
      <p className="caption mb-4">
        Latest available per station; observation times may differ. IN_NAQI_CPCB
        · OpenAQ
      </p>
      <div className="grid gap-4 md:grid-cols-3">
        {stations?.length ? (
          stations.map((s) => (
            <article className="surface p-5" key={s.station_id}>
              <h3>{s.name}</h3>
              <p className="text-3xl my-3">{s.naqi_24h}</p>
              <CategoryChip category={s.naqi_category} />
              <p className="caption mt-3">
                {s.is_stale ? "Stale observation" : "Recent observation"} ·{" "}
                {observed(s.last_observed_at)}
              </p>
            </article>
          ))
        ) : (
          <p>Station indices unavailable.</p>
        )}
      </div>
    </section>
  );
}
