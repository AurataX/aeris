const steps = [
  ["ingest_batch", "Collect station metadata and weather"],
  ["load_bronze", "Auto Loader reads landed files"],
  ["silver_stations", "Clean station identities"],
  ["silver_pollution", "Depends on stations; MERGE observations"],
  ["silver_weather", "Parallel Silver branch: clean weather"],
  ["gold_daily", "Compute daily pollutant indices"],
  ["gold_latest", "Join daily indices and Silver weather"],
  ["validate_gold", "Check keys, ranges and counts"],
  ["sync_supabase", "Publish only after validation"],
];
export function JobFlow() {
  return (
    <section>
      <h2 className="section-heading">The nine-task job</h2>
      <p className="caption mb-4">
        ingest · Bronze · [stations · pollution · daily | weather] · latest ·
        validate · sync
      </p>
      <ol className="grid gap-3 md:grid-cols-3">
        {steps.map(([name, text], i) => (
          <li className="surface p-5" key={name}>
            <span className="eyebrow">{String(i + 1).padStart(2, "0")}</span>
            <h3 className="text-sm break-all mt-2">{name}</h3>
            <p className="caption mt-2">{text}</p>
          </li>
        ))}
      </ol>
    </section>
  );
}
