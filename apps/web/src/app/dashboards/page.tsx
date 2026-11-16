import { Icon } from "@/shared/icons/Icon";

const EMBEDS = [
  { name: "Databricks AI/BI", url: process.env.NEXT_PUBLIC_DATABRICKS_DASHBOARD_EMBED_URL, note: "Gold tables on a serverless SQL warehouse. Sign in to Databricks to view." },
  { name: "Power BI", url: process.env.NEXT_PUBLIC_POWERBI_EMBED_URL, note: "Star schema with DAX measures over the same Gold tables." },
];

export default function Dashboards() {
  return (
    <>
      <h1 className="text-4xl font-semibold tracking-tight sm:text-5xl">The BI side</h1>
      <p className="mb-8 mt-3 max-w-2xl text-ink-2">Two dashboards read the same Gold tables as this website.</p>
      <div className="grid gap-4 md:grid-cols-2">
        {EMBEDS.map((e) => (
          <section key={e.name} className="surface flex min-h-72 flex-col p-5">
            <h2 className="font-semibold">{e.name}</h2>
            <p className="mb-4 text-sm text-ink-3">{e.note}</p>
            {e.url ? (
              <iframe src={e.url} title={e.name} className="min-h-96 w-full flex-1 rounded-2xl border border-hairline" />
            ) : (
              <p className="my-auto text-sm text-ink-2">Not connected yet.</p>
            )}
            {e.url && (
              <a href={e.url} target="_blank" rel="noreferrer" className="mt-3 inline-flex items-center gap-1.5 text-sm text-primary">
                Open in a new tab <Icon name="external" size={14} />
              </a>
            )}
          </section>
        ))}
      </div>
    </>
  );
}
