import { getDaily } from "@/shared/lib/api";
import { categoryColor, CATEGORIES } from "@/shared/lib/aqi";
import { calendar } from "@/shared/lib/calendar";
export async function Calendar({ city }: { city: string }) {
  const res = await getDaily(city, 365);
  return (
    <section className="surface p-6 mt-6">
      <h2>{city} · daily category calendar</h2>
      <p className="caption my-3">
        IN_NAQI_CPCB · OpenAQ · one square per day, ordered oldest to newest.
      </p>
      <div className="flex flex-wrap gap-1">
        {calendar(res?.data ?? []).map((d) => (
          <span
            key={d.date_ist}
            className="size-3 rounded-sm"
            style={{
              background: categoryColor(
                "naqi_category" in d ? d.naqi_category : null,
              ),
            }}
            title={`${d.date_ist}: ${d.naqi ?? "Missing"}`}
          />
        ))}
      </div>
      <p className="caption mt-4">{CATEGORIES.join(" · ")} · grey = missing</p>
      <p className="text-sm mt-3 text-ink-2">
        Runs of the same category reveal sustained periods. Grey cells are gaps,
        not clean-air days. Exact values are available in the observations table
        above.
      </p>
    </section>
  );
}
