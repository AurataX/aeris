import { getDaily } from "@/shared/lib/api";
import { WorkedExample } from "./WorkedExample";
export async function NumberStory() {
  const res = await getDaily("Delhi", 30);
  const day = res?.data.filter((d) => d.naqi != null).at(-1);
  return (
    <section>
      <h2 className="section-heading">How the number is made</h2>
      <div className="surface p-6 space-y-4">
        <p>
          1. Average PM2.5, PM10, NO₂ and SO₂ over 24 hours. O₃ and CO use the
          day's maximum rolling 8-hour mean. Coverage checks leave insufficient
          days missing.
        </p>
        <p>
          2. Convert each concentration into a unitless sub-index using its CPCB
          breakpoint band.
        </p>
        <p className="font-mono text-sm">
          I = I_low + (C · BP_low) · (I_high · I_low) / (BP_high · BP_low)
        </p>
        <p>
          3. Require at least three pollutants, including PM2.5 or PM10. Take
          the highest sub-index: its pollutant is dominant. The implementation
          caps NAQI at 500.
        </p>
        {day ? (
          <WorkedExample day={day} />
        ) : (
          <p>
            Worked example unavailable: the daily API returned no valid index.
          </p>
        )}
      </div>
    </section>
  );
}
