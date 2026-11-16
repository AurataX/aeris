import assert from "node:assert/strict";
import { test } from "node:test";
import { insights } from "../src/features/trends/insights.ts";
import { calendar } from "../src/shared/lib/calendar.ts";
import { observed, number } from "../src/shared/lib/format.ts";
test("missing days are retained as chart gaps", () => {
  const rows = calendar([
    { date_ist: "2026-01-01", naqi: 0 },
    { date_ist: "2026-01-03", naqi: 100 },
  ]);
  assert.equal(rows.length, 3);
  assert.equal(rows[1].naqi, null);
  assert.equal(rows[0].naqi, 0);
  assert.deepEqual(calendar([]), []);
});
test("insights exclude missing values and retain zero", () => {
  const rows = [
    { date_ist: "2026-01-01", naqi: null, pm25_avg: null },
    { date_ist: "2026-01-02", naqi: 0, pm25_avg: 0 },
    {
      date_ist: "2026-02-01",
      naqi: 301,
      pm25_avg: 61,
      dominant_pollutant: "pm25",
    },
  ];
  const s = insights(rows);
  assert.equal(s.valid, 2);
  assert.equal(s.poor, 1);
  assert.equal(s.exceed, 50);
  assert.equal(s.worst, "2026-02");
  assert.equal(s.dominant, "pm25");
  assert.equal(insights([]).exceed, null);
});
test("formatters distinguish unknown from zero and label IST", () => {
  assert.equal(number(null), "Unavailable");
  assert.equal(number(0), "0");
  assert.match(observed("2026-11-12T00:00:00Z"), /IST$/);
});
