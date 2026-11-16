const layers = [
  [
    "Bronze → original records",
    "Source records plus ingested_at, batch_id and _source_file. Auto Loader checkpoints track files; rescued fields preserve schema surprises.",
  ],
  [
    "Silver → hourly observations",
    "Grain: station → pollutant → observed_at → source. Units are standardised; invalid rows are quarantined; latest ingestion wins duplicates. Delta MERGE updates the business key.",
  ],
  [
    "Gold → city-day analytics",
    "Grain: city → date_ist → index_standard → source. NAQI, trends and weather joins turn observations into comparable metrics. Small Gold tables are recomputed each run.",
  ],
  [
    "Serving → published snapshots",
    "Supabase keeps the Gold business keys. INSERT ON CONFLICT DO UPDATE makes a repeated sync safe. Validation gates publication.",
  ],
];
export function LayerNotes() {
  return (
    <div className="grid gap-4 md:grid-cols-2 mt-5">
      {layers.map(([title, text]) => (
        <article className="surface p-6" key={title}>
          <h3>{title}</h3>
          <p className="text-ink-2 mt-2 leading-relaxed">{text}</p>
        </article>
      ))}
    </div>
  );
}
