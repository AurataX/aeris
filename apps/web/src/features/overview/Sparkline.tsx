// Tiny trend line for a city card. Gaps (null) break the line instead of being invented.
export function Sparkline({ values, color }: { values: (number | null)[]; color: string }) {
  const nums = values.filter((v): v is number => v != null);
  if (nums.length < 2) return <div className="h-10 text-xs text-ink-3">not enough data</div>;
  const [lo, hi] = [Math.min(...nums), Math.max(...nums)];
  const x = (i: number) => (i / (values.length - 1)) * 100;
  const y = (v: number) => 36 - ((v - lo) / (hi - lo || 1)) * 32;

  let d = "";
  values.forEach((v, i) => {
    if (v == null) return;
    d += `${d && values[i - 1] != null ? "L" : "M"}${x(i).toFixed(1)} ${y(v).toFixed(1)} `;
  });

  return (
    <svg viewBox="0 0 100 40" preserveAspectRatio="none" className="h-10 w-full" role="img"
         aria-label={`trend from ${nums[0]} to ${nums[nums.length - 1]}`}>
      <path d={d} fill="none" stroke={color} strokeWidth={1.8} strokeLinecap="round" strokeLinejoin="round"
            vectorEffect="non-scaling-stroke" />
    </svg>
  );
}
