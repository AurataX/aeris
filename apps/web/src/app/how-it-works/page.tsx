const STEPS = [
  ["Sources", "OpenAQ archive on AWS S3, live OpenAQ and CPCB readings, Open-Meteo weather."],
  ["Landing", "Raw files land in a Unity Catalog volume on Azure. Nothing is changed or thrown away."],
  ["Bronze", "Spark Structured Streaming (Auto Loader) reads only new files. 27.7 million raw readings."],
  ["Silver", "Bad rows dropped by expectations, gases converted to µg/m³, 15-minute readings made hourly: 4.4 million rows."],
  ["Gold", "Indian NAQI (CPCB method), trends, latest status and weather joins. Small and fast."],
  ["Serving", "A validated sync upserts Gold into Supabase Postgres. This site never queries the warehouse."],
  ["You", "This site, a Databricks dashboard and a Power BI report all read the same Gold data."],
] as const;

export default function HowItWorks() {
  return (
    <>
      <h1 className="text-4xl font-semibold tracking-tight sm:text-5xl">How it works</h1>
      <p className="mb-8 mt-3 max-w-2xl text-ink-2">From a sensor reading to the number on the Overview page.</p>
      <ol className="space-y-3">
        {STEPS.map(([title, text], i) => (
          <li key={title} className="surface flex gap-5 p-5">
            <span className="text-3xl font-semibold text-primary/40">{i + 1}</span>
            <div>
              <h2 className="font-semibold">{title}</h2>
              <p className="text-sm text-ink-2">{text}</p>
            </div>
          </li>
        ))}
      </ol>
    </>
  );
}
