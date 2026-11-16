export function Evidence() {
  return (
    <section>
      <h2 className="section-heading">Engineering evidence & guardrails</h2>
      <div className="surface p-6 space-y-4">
        <p>
          <strong>Replay without duplicates.</strong> Auto Loader stores file
          progress under checkpoints/, outside landing/live/. Silver MERGE and
          serving upserts preserve business keys.
        </p>
        <p>
          <strong>Proof boundary.</strong> The API exposes one table-count
          snapshot. It does not expose before/after rerun counts or quarantine
          counts, so this page cannot claim a verified idempotency test or zero
          rejected rows.
        </p>
        <p>
          <strong>Cost control.</strong> availableNow stops after processing new
          files. The SQL warehouse has a five-minute auto-stop. The web reads
          Supabase through FastAPI; visitors do not each start a warehouse.
        </p>
        <p>
          <strong>Orchestration.</strong> Nine tasks, one concurrent run,
          validation before sync. The documented file-arrival trigger is paused
          by default; its current enabled state is not exposed here.
        </p>
      </div>
    </section>
  );
}
