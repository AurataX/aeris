import { Suspense } from "react";
import { JobFlow } from "@/features/pipeline/JobFlow";
import { Medallion } from "@/features/pipeline/Medallion";
import { getTables } from "@/shared/lib/api";

async function Tables() {
  const res = await getTables();
  if (!res) return <div className="surface p-8 text-ink-2">Pipeline statistics are unavailable right now.</div>;
  const sync = res.meta.last_sync?.finished_at;
  return (
    <>
      <Medallion tables={res.data} />
      <p className="mt-3 text-xs text-ink-3">Row counts from the last validated run{sync ? ` · last sync ${sync}` : ""}.</p>
    </>
  );
}

export default function Pipeline() {
  return (
    <>
      <h1 className="text-4xl font-semibold tracking-tight sm:text-5xl">The data engineering</h1>
      <p className="mb-8 mt-3 max-w-2xl text-ink-2">
        A Databricks Job runs these four steps every day at 07:00 IST. If validation fails, nothing is published.
      </p>
      <JobFlow />
      <h2 className="mb-3 mt-10 text-lg font-semibold">What is in each layer</h2>
      <Suspense fallback={<div className="surface h-64 animate-pulse" />}>
        <Tables />
      </Suspense>
    </>
  );
}
