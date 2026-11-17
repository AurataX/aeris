# Codex handoff: AERIS website (design + in-depth pages)

Paste the "Prompt" block below into Codex. Everything else in this file is context it can read.

## Prompt

You are finishing the website for AERIS, a university Big Data project (deadline 20 Nov 2026) that shows real Delhi NCR air-quality data processed with Apache Spark on Azure Databricks. Read `AGENTS.md`, `docs/design.md`, `docs/data-model.md`, `docs/pipelines.md`, `docs/api.md` and `docs/architecture.md` first.

The data engineering, API and deployment are done. Your job is the **front end only**, in `apps/web`. Make it enterprise-grade and make the project understandable. The instructor should see not just numbers but **what we built, how, and what is hidden behind each number**.

### 1. Do not break these rules
- Real data only. Never invent a number, station, date or chart value. Missing data stays missing and is labelled.
- PM2.5 is not AQI. Always show `index_standard` and `source` next to an index value. Say "live" only where data is really live (the latest Gold data may be days old; show its `as_of`).
- Design follows `docs/design.md`: "the sky is the interface", Liquid Glass on chrome only (dock, utility cluster, sheets), data cards high-opacity, light first with a dark theme, all colours from tokens on `:root[data-theme]`, CPCB category colours reserved for data. Fonts Satoshi + General Sans (self-hosted). **Custom SVG icons only, no Lucide.** Respect `prefers-reduced-motion`. Use `motion` layoutId/spring for shared-element moves, count-ups once.
- Code laws: **max 250 words per source file (hard cap 350)**, one responsibility per file, Server Components fetch the API with `next: { revalidate: 3600, tags: ['gold'] }`, **no browser polling** (Supabase Realtime on `sync_runs` then `router.refresh()`; SSE for the pipeline page). Ponytail style: least code that fully works, no speculative abstractions.
- Comments short and human. No AI attribution in commits or PRs (commits are authored by the student).

### 2. Deployment facts (so you do not break it)
- Site: https://aeris.inerate.com on **Cloudflare Workers** via `vinext` (Next.js API on Vite). Config: `apps/web/cloudflare.config.ts`, `vite.config.ts`. Cache: KV namespace `aeris-web-cache` (`VINEXT_KV_CACHE`).
- Build and deploy from `apps/web`: `npm run build:vinext`, then `env -u CLOUDFLARE_API_TOKEN npx cf deploy --prebuilt`. Login once with `env -u CLOUDFLARE_API_TOKEN npx cf auth login`. First-time or changed secrets: `--secrets-file <file>` with `REVALIDATE_SECRET=...` (never commit it).
- Runtime values live as Worker bindings in `cloudflare.config.ts` (`API_URL`, `NEXT_PUBLIC_DATABRICKS_DASHBOARD_EMBED_URL`). Add `NEXT_PUBLIC_POWERBI_EMBED_URL` and the Google Maps key/Map ID there when they exist. Server code reads them from `process.env`.
- Workers limits: no Node-only APIs, no native modules, no `next/image` optimisation (use plain images/SVG). Local check: `npm run dev:vinext`. `npm run dev` still runs plain Next.js.
- API: https://aeris-api-70530354318.asia-south1.run.app (FastAPI, Cloud Run). CORS allows `https://aeris.inerate.com` and `http://localhost:3000`. Endpoints: `/health`, `/api/v1/cities/latest`, `/stations`, `/cities/{city}/daily`, `/trends/pollutants`, `/weather/correlation`, `/pipeline/tables`, `/pipeline/runs` (+ `/runs/{id}/events` SSE, `POST /runs` admin only, needs Databricks credentials which are not set). Check `docs/api.md` for response shapes before using a field.
- Existing pages: `/` Overview, `/map`, `/trends`, `/pipeline`, `/dashboards`, `/how-it-works`. Shared bits in `src/shared/{ui,icons,lib}`, features in `src/features/*`.

### 3. Work to do (in this order)
1. **Story pages ("what we actually did")**, the main ask. Make `/how-it-works` and `/pipeline` deep and visual:
   - End-to-end flow diagram, animated: sources (OpenAQ API + S3 archive, CPCB data.gov.in, Open-Meteo) → Cloudflare collector → Databricks Volume → Auto Loader → Bronze → Silver → Gold → Supabase → API → site, plus Databricks dashboard and Power BI. One line each on what that step does and why that tool.
   - Per-layer cards with **real row counts** from `/api/v1/pipeline/tables` (bronze ~27.7M archive rows, Silver ~4.4M hourly rows, Gold `city_daily_aqi` ~2.9k rows), table names, grain, keys, and "what changed between layers" (dedupe, unit standardisation, quarantine, MERGE idempotency).
   - **How the number is made**: explain NAQI step by step (sub-index per pollutant from CPCB breakpoints, take the max, dominant pollutant, 24h averaging rules), with a worked example using a real city/day from the API. Explain why PM2.5 is not the AQI.
   - **Hidden insights** panel per city: days Very Poor+, worst month, dominant pollutant, PM2.5 vs wind correlation (from `/weather/correlation`), % days over the NAAQS limit. Add a plain-language "what this means" under every chart.
   - **Data honesty** section: where data is modelled vs measured, last observed time per source, known gaps (e.g. live collector lag), and licences/attribution for OpenAQ, CPCB, Open-Meteo.
   - **Engineering evidence** section: idempotent reruns (counts unchanged), Auto Loader checkpoints, job DAG with task states, cost guardrails (serverless warehouse auto-stop 1 min, Supabase serves the web so no warehouse per visitor).
2. **Overview, Map, Trends polish** to the design system: skeleton/empty/error states with the real reason, source + timestamp labels, tabular numerals, responsive 375/768/1280, light + dark.
3. **Map page**: the Google Maps key and Map ID now exist. Key is in the gitignored `.env` (`NEXT_PUBLIC_GOOGLE_MAPS_API_KEY`, referrer-restricted to aeris.inerate.com and localhost:3000, Maps JavaScript API only). Map ID `1a16bea3e9521acf82834bdd` (vector) is bound as `NEXT_PUBLIC_GOOGLE_MAP_ID` in `cloudflare.config.ts`; the key is declared there as `bindings.secret()`. `src/features/map/GoogleLayer.tsx` is a ready client component (`stations`, `mapsKey`, `mapId`, `onPick`): load it from the map page, passing the two env values from the Server Component, and keep your station list as the fallback when the key is missing. Deploy with `--secrets-file` containing `REVALIDATE_SECRET=` and `NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=` copied from `.env` (delete the file afterwards, never commit it).
4. **Dashboards page**: Databricks embed (needs sign-in, say so) and Power BI embed via `NEXT_PUBLIC_POWERBI_EMBED_URL` (link will be provided; show a friendly placeholder until then).
5. **Realtime**: subscribe to Supabase Realtime `sync_runs` (publishable key is public by design) and call `router.refresh()`; no polling.
6. **Accessibility and checks**: visible focus, contrast AA, keyboard order, reduced-motion fallbacks. Capture screenshots at 375/768/1280 (light+dark), run Lighthouse, then deploy and verify the live URL.

### 4. Done means
`npm run build:vinext` passes, the live site at https://aeris.inerate.com shows the new pages with real API data, every file is under the word cap, and `docs/task.md` is ticked with evidence (URL, screenshots).

## What is not finished (not Codex's job)
- Power BI embed URL (student will supply), Google Maps key/Map ID (student), "Run pipeline" button needs a Databricks service-principal secret on the API, optional.

## Cache note (Cloudflare KV free limit)
KV on the free plan allows about 1,000 writes a day. The data changes once a day and the pipeline calls `/api/revalidate`, so the TTL in `src/shared/lib/api.ts` is now 3600 s (`cacheLife` revalidate 3600, expire 86400). Keep it long; do not go back to 300 s and do not add polling.
