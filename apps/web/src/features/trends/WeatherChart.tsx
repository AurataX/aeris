"use client";
import {
  ScatterChart,
  Scatter,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";
export type WeatherPoint = {
  date_ist: string;
  pm25_avg: number | null;
  wind_avg_kmh: number | null;
};
export function WeatherChart({ data }: { data: WeatherPoint[] }) {
  const points = data.filter(
    (d) => d.pm25_avg != null && d.wind_avg_kmh != null,
  );
  if (!points.length) return <p>No paired weather and PM2.5 observations.</p>;
  return (
    <div
      className="h-72"
      role="img"
      aria-label="Wind speed versus PM2.5 concentration"
    >
      <ResponsiveContainer>
        <ScatterChart margin={{ bottom: 25, right: 15, left: 5 }}>
          <CartesianGrid stroke="var(--hairline)" />
          <XAxis
            type="number"
            dataKey="wind_avg_kmh"
            name="Wind"
            unit=" km/h"
            tick={{ fontSize: 11, fill: "var(--ink-2)" }}
          />
          <YAxis
            type="number"
            dataKey="pm25_avg"
            name="PM2.5"
            unit=" µg/m³"
            tick={{ fontSize: 11, fill: "var(--ink-2)" }}
          />
          <Tooltip
            contentStyle={{
              background: "var(--surface-solid)",
              color: "var(--ink)",
            }}
          />
          <Scatter
            data={points}
            fill="var(--primary)"
            isAnimationActive={false}
          />
        </ScatterChart>
      </ResponsiveContainer>
    </div>
  );
}
