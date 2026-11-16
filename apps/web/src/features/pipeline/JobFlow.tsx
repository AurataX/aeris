import { Icon } from "@/shared/icons/Icon";

const STEPS = [
  ["ingest_batch", "Calls the APIs, saves raw JSON"],
  ["etl_bronze_silver_gold", "Spark pipeline: Bronze → Silver → Gold"],
  ["validate_gold", "Checks keys, ranges, counts"],
  ["sync_supabase", "Publishes Gold to the website database"],
] as const;

export function JobFlow() {
  return (
    <ol className="grid gap-3 md:grid-cols-4">
      {STEPS.map(([name, text], i) => (
        <li key={name} className="surface relative p-5">
          <span className="flex size-8 items-center justify-center rounded-full bg-primary/10 text-primary">
            <Icon name={i === STEPS.length - 1 ? "check" : "pipeline"} size={18} />
          </span>
          <p className="mt-3 font-mono text-sm">{name}</p>
          <p className="mt-1 text-xs text-ink-3">{text}</p>
        </li>
      ))}
    </ol>
  );
}
