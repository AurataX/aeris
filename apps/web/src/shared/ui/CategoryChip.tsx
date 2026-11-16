import { categoryColor, categoryInk } from "@/shared/lib/aqi";

// The category name is always written out; color is never the only signal.
export function CategoryChip({ category }: { category: string | null }) {
  return (
    <span
      className="inline-flex items-center rounded-full px-2.5 py-1 text-xs font-semibold"
      style={{
        background: categoryColor(category),
        color: categoryInk(category),
      }}
    >
      {category ?? "No data"}
    </span>
  );
}
