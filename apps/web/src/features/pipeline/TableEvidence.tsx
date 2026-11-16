import { getTables } from "@/shared/lib/api";
import { observed } from "@/shared/lib/format";
import { Medallion } from "./Medallion";
export async function TableEvidence() {
  const res = await getTables();
  return (
    <section>
      <h2 className="section-heading">Real rows. Traceable layers.</h2>
      {res ? (
        <>
          <Medallion tables={res.data} />
          <p className="caption mt-4">
            Source: validated ops.table_stats · Last serving sync:{" "}
            {observed(res.meta.last_sync?.finished_at)}. Counts are snapshots,
            not streaming counters.
          </p>
        </>
      ) : (
        <p className="surface p-6">
          Table statistics unavailable from the API.
        </p>
      )}
    </section>
  );
}
