import { getCities, getTables } from "@/shared/lib/api";
import { observed } from "@/shared/lib/format";
export async function Honesty() {
  const [cities, tables] = await Promise.all([getCities(), getTables()]);
  return (
    <section>
      <h2 className="section-heading">What the data can · and cannot · say</h2>
      <div className="surface p-6 space-y-4">
        <p>
          Air pollution comes from ground monitors. Open-Meteo weather is
          modelled, not a co-located station measurement. Correlation describes
          association, not causation.
        </p>
        <div className="grid gap-3 sm:grid-cols-2">
          {cities?.data.map((c) => (
            <p key={c.city}>
              <strong>{c.city}</strong>
              <br />
              <span className="caption">
                Latest city observation: {observed(c.as_of)}
              </span>
            </p>
          ))}
        </div>
        <p className="caption">
          Serving sync: {observed(tables?.meta.last_sync?.finished_at)}. This is
          a publication timestamp, not an observation timestamp.
        </p>
        <p>
          CPCB and collector source-level observation times are not exposed by
          the current API. Their freshness cannot be verified here. Missing
          pollutants, gaps and stale stations remain visible; no readings are
          filled in.
        </p>
        <p className="caption">
          Attribution: OpenAQ and its original providers (provider-specific
          licences); CPCB via data.gov.in (Government Open Data Licence ·
          India); Open-Meteo (CC BY 4.0). The computed IN_NAQI_CPCB is an AERIS
          index, not an official CPCB publication.
        </p>
      </div>
    </section>
  );
}
