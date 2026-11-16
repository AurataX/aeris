import { get } from "@/shared/lib/api";
import { RunEvents } from "./RunEvents";
export async function Runs() {
  const res = await get<{
    data: { run_id: number; state: string; started: number }[];
  }>("/pipeline/runs");
  if (!res)
    return (
      <div className="notice">
        <strong>Run telemetry unavailable</strong>
        <span>
          The Jobs API is unavailable or not configured. Task cards below
          describe the DAG; they do not report live execution. Run controls
          require API-side Databricks credentials.
        </span>
      </div>
    );
  return (
    <section className="surface p-6">
      <h2>Recent runs</h2>
      {res.data.length ? (
        res.data.map((r) => (
          <div className="mt-4" key={r.run_id}>
            <p>
              Run {r.run_id} · {r.state} · {new Date(r.started).toISOString()}
            </p>
            <RunEvents runId={r.run_id} base={process.env.API_URL ?? ""} />
          </div>
        ))
      ) : (
        <p>No runs returned.</p>
      )}
      <p className="caption">
        Duration and trigger type are not exposed by this API.
      </p>
    </section>
  );
}
