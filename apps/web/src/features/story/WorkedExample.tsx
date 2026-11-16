import type { Day } from "@/shared/lib/api";
import { number } from "@/shared/lib/format";
export function WorkedExample({ day }: { day: Day }) {
  const c = day.pm25_avg;
  return (
    <div className="notice">
      <strong>Real example · Delhi · {day.date_ist}</strong>
      <span>
        PM2.5 averaged {number(c, 2)} µg/m³. Across {day.pollutants_used}{" "}
        pollutants and {day.stations_count} stations, the published NAQI is{" "}
        {day.naqi}, dominated by {day.dominant_pollutant}. {day.index_standard}{" "}
        · {day.source}.
      </span>
      {c != null && c >= 121 && c <= 250 && (
        <span>
          PM2.5 falls in the 121–250 band: 301 + ({number(c, 2)} − 121) × (400 −
          301) / (250 − 121) ≈ {Math.round(301 + ((c - 121) * 99) / 129)}. This
          is the PM2.5 sub-index; the final NAQI is the maximum of all eligible
          sub-indices.
        </span>
      )}
      <span>
        Concentration measures particle mass; NAQI is a unitless index. They are
        not interchangeable.
      </span>
    </div>
  );
}
