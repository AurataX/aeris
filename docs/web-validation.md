# Web handoff verification — 16 Nov 2026

Local production preview: http://localhost:3002. Development preview: http://localhost:3001.

## Observed API facts

- `/cities/latest`: Delhi NAQI 400, observation `2026-11-12T00:00:00+00:00`; source `openaq`, standard `IN_NAQI_CPCB`. This is not a current live reading.
- `/pipeline/tables`: Bronze archive 27,673,721; Silver pollutant observations 4,421,174; Gold city-day AQI 2,863. Snapshot computed 16 Nov 2026, 13:55 UTC.
- Last serving sync finished 16 Nov 2026, 13:56 UTC. Publication time differs from observation time.
- `/pipeline/runs`: HTTP 503. The UI labels telemetry unavailable, preserving the documented nine-task DAG separately.

## Checks

- Production vinext build passed (`apps/web/output/build.log`). Only framework sourcemap/classification warnings.
- Next route type generation and TypeScript passed.
- `node --experimental-strip-types --test tests/data.test.mjs`: three checks passed. Test fixtures are synthetic boundary cases, never displayed as project measurements.
- Browser assertions passed for 36 viewport/theme/route combinations and theme, plain sky, station filtering, range selection, table expansion, Power BI configuration. All six routes tested at 375, 768 and 1280 px in light/dark, with reduced motion enabled for repeatable screenshots.
- Supabase subscription connected. No database mutation was made to manufacture a refresh event.
- Lighthouse production Overview: performance 99, accessibility 100. Other routes were browser checked, not Lighthouse scored.
- Every source file under `apps/web/src` is below the 350-word hard cap.

## Review artifacts

- [Overview, desktop light](../apps/web/output/playwright/overview-1280-light.png)
- [Overview, mobile dark](../apps/web/output/playwright/overview-375-dark.png)
- [Architecture and evidence](../apps/web/output/playwright/how-it-works-1280-light.png)
- [Trends, mobile](../apps/web/output/playwright/trends-375-light.png)
- [Interaction and viewport check](../apps/web/output/browser-check.log)
- [Lighthouse report](../apps/web/output/lighthouse.json)

## Limits and remaining work

Deployed with user approval to https://aeris.inerate.com on 16 Nov 2026. Worker version: `81d5cfcd-9dce-4187-bb00-cc2799ae4ed1`. Production Lighthouse: performance 95, accessibility 100. All 36 production viewport/theme/route checks passed.

Production Google Maps loaded with 60 station marker controls; the directory also works independently. The local preview does not have the Maps secret. Dashboard sign-in/report access is controlled by Databricks and Microsoft; unauthenticated iframe 401 responses are expected and the page offers direct links.

Run-now and authenticated Jobs telemetry remain API-side dependencies. A live SSE task event and a new sync refresh have not been triggered. Source-specific collector timestamps, before/after rerun counts and quarantine counts are not exposed by the API; none are invented.

The existing illustrated skyline remains; a licensed photographic backdrop and the additional social/apple/legacy icon exports in design.md are still outstanding design assets. Historical insights are on Trends. No new cloud resource, pipeline run or Git push was performed.

The dependency audit reports six existing/transitive advisories (five moderate, one high, including Vite development-server paths). No forced toolchain downgrade was applied. See apps/web/output/audit.json. The preview remains local.


Generated screenshots and reports under `apps/web/output/` are retained locally and gitignored. Artifact links above require the local verification outputs; these files are not part of a fresh clone.
