"use client";

import {
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

const SERIES = [
  ["Delhi", "var(--series-1)"],
  ["Gurugram", "var(--series-2)"],
  ["Noida", "var(--series-3)"],
  ["Ghaziabad", "var(--series-4)"],
  ["Faridabad", "var(--series-5)"],
] as const;

export type Row = { date: string } & Record<string, number | string | null>;

// Days without a NAQI stay null, so the line breaks (connectNulls is off): gaps are never interpolated.
export function TrendChart({ rows }: { rows: Row[] }) {
  return (
    <div
      className="h-[360px] w-full"
      role="img"
      aria-label="Daily NAQI per city"
    >
      <ResponsiveContainer>
        <LineChart data={rows} margin={{ left: -12, right: 8, top: 8 }}>
          <CartesianGrid stroke="var(--hairline)" vertical={false} />
          <XAxis
            dataKey="date"
            tick={{ fontSize: 11, fill: "var(--ink-3)" }}
            tickLine={false}
            minTickGap={48}
          />
          <YAxis
            domain={[0, 500]}
            tick={{ fontSize: 11, fill: "var(--ink-3)" }}
            tickLine={false}
            axisLine={false}
          />
          <Legend />
          <Tooltip
            contentStyle={{
              borderRadius: 12,
              border: "1px solid var(--hairline)",
              background: "var(--surface-solid)",
            }}
          />
          {SERIES.map(([city, color]) => (
            <Line
              key={city}
              dataKey={city}
              stroke={color}
              dot={false}
              strokeWidth={2}
              isAnimationActive={false}
            />
          ))}
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
