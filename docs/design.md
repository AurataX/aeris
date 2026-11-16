# Design system — AERIS web

Sources: **ui-ux-pro-max** (style: Liquid Glass; palette: blue data + amber highlights; type: Premium Sans), the user's references `prompt/fluid_ui.jpeg` (light, airy bento, soft tinted cards) and `prompt/fluid-interface-library/reference.png` (smoked glass, floating dock, photoreal environment), and the motion/material contract in `prompt/fluid-interface-library/master-brief.md`. **We take their feel, never their layout or content.**

## 1. Thesis — "the sky is the interface"

The background is a photoreal Delhi skyline, and its **haze follows the real air**. When Delhi is Good, the sky is clear and blue. When it is Severe, the sky turns a heavy amber smog. Before reading a number, a viewer *feels* the air quality. Everything else is quiet: crisp reading surfaces, a floating glass dock, and data as the hero.

Three qualities: **clean** (no clutter, no decoration without data), **hyper-real** (a real photo, real numbers, real timestamps), **fluid** (every change is continuous and interruptible).

## 2. Shell composition (decided)

Two options were compared (master-brief rule):

| | A. Bottom-centre floating dock ✅ | B. Left sidebar (like fluid_ui.jpeg) |
|---|---|---|
| Map page | Full-bleed map, nothing steals width | Map loses ~240 px |
| Atmosphere | Backdrop stays visible edge to edge | Sidebar blocks the sky |
| Pointer travel | 6 destinations, centred | Shorter on desktop |
| Mobile | Becomes the bottom tab bar (same order) | Needs a drawer (an extra tap) |

**Chosen: A.** The dock carries the 6 destinations. The top-right utility cluster holds the city picker, the data-freshness pill and the theme toggle. Content reserves 120 px at the bottom so the dock never covers the last row.

## 3. Materials (a small, fixed set)

| Material | Use | Recipe (light) |
|---|---|---|
| **Atmosphere** | page background | photo (AVIF/WebP ≤ 300 KB, blur placeholder) + haze gradient layer, `--haze-opacity` 0 → 0.65 and hue from Delhi's category |
| **Reading surface** | data cards, panels, chart frames | `rgba(255,255,255,.86)`, `backdrop-filter: blur(12px)`, 1 px border `rgba(15,23,42,.06)`, radius 24, inset top-light `inset 0 1px 0 rgba(255,255,255,.9)` |
| **Navigation glass** (liquid) | dock, top utilities | `rgba(255,255,255,.55)`, `blur(24px) saturate(180%)`, border `rgba(255,255,255,.6)`, specular highlight pseudo-element (top-left radial, opacity .5), shadow `0 8px 32px rgba(15,23,42,.12)` |
| **Transient overlay** | sheets, menus, tooltips | navigation glass at .72 opacity + scrim `rgba(15,23,42,.25)` behind sheets |
| **Metallic active** | active dock item, primary button | subtle vertical gradient (`#F8FAFC → #E2E8F0`) + 1 px inner highlight; never chrome-rainbow, never a perpetual shimmer |
| **Solid fallback** | `prefers-reduced-transparency`, low-end devices, "plain background" toggle | opaque `--bg-raised`, no blur |

Glass is **chrome only**. Data surfaces are ≥ 80% opaque so text passes 4.5:1 over the brightest crop of the photo. Full-screen blur layers are never nested.

## 4. Tokens (`apps/web/src/shared/styles/tokens.css` — the only place colors live)

```css
:root[data-theme="light"] {
  --bg: #F8FAFC;            --bg-raised: #FFFFFF;
  --ink: #0F172A;           --ink-2: #475569;   --ink-3: #64748B;
  --hairline: rgba(15,23,42,.08);
  --primary: #1E40AF;       --primary-2: #3B82F6;     /* brand: data blue */
  --highlight: #F59E0B;     /* amber: ONLY for forecast/estimated/stale labels */
}
:root[data-theme="dark"] {
  --bg: #0B1020;            --bg-raised: rgba(15,23,42,.78);
  --ink: #F1F5F9;           --ink-2: #CBD5E1;   --ink-3: #94A3B8;
  --hairline: rgba(255,255,255,.08);
  --primary: #60A5FA;       --primary-2: #93C5FD;     --highlight: #FBBF24;
}
```

**AQI category colors (CPCB scale, tuned; data only, never decoration):**

| Category | Fill | Text on fill |
|---|---|---|
| Good (0–50) | `#3BA55C` | white |
| Satisfactory (51–100) | `#A3C853` | `#0F172A` |
| Moderate (101–200) | `#F2C94C` | `#0F172A` |
| Poor (201–300) | `#F2994A` | `#0F172A` |
| Very Poor (301–400) | `#EB5757` | white |
| Severe (401–500) | `#9B2C2C` | white |

Each also has a 12% tint for card backgrounds. Color is never the only signal: the category name is always written too.

**City series (charts):** five blues and teals, kept apart from the AQI colors: `#1E40AF #3B82F6 #0EA5E9 #14B8A6 #6366F1`.

Scales: radius 12 (inputs) · 16 (chips/menus) · 24 (cards) · full (dock, pills). Spacing on a 4-px scale; 24 px card padding (16 on mobile). Z-index: base 0 · sticky 10 · dock 30 · overlay 40 · sheet 50 · toast 60.

## 5. Typography

- **Satoshi** (display, numbers) + **General Sans** (UI/body), both from Fontshare (free licence, self-hosted via `next/font/local`); **Fira Code** only for SQL/code on the Pipeline page.
- Scale: display 56/60 (−2% tracking) · h1 36 · h2 24 · h3 18 · body 16 / 1.6 · small 14 · micro label 12 uppercase +0.08em.
- All data numbers use `font-variant-numeric: tabular-nums`. The big NAQI number is Satoshi 600.
- Body text ≥ 16 px on mobile; lines ≤ 70 characters.

## 6. Icons — custom SVG family (no Lucide, no emoji)

Spec: 24 px grid, 2 px padding, **1.75 stroke** (1.5 at 16 px), round caps and joins, 2 px corner radius, `currentColor`, no fills (except small dots). One React component per file in `src/shared/icons/`, `aria-hidden` by default; icon-only buttons carry an `aria-label`.

Set (20): `overview` (wind swirl) · `map` (folded map + pin) · `trends` (rising line) · `pipeline` (three linked nodes) · `dashboards` (2×2 grid with a bar) · `layers` (stacked planes, How it works) · `city` (skyline) · `station` (sensor mast) · `particle` (PM dot cluster) · `wind` · `humidity` · `temperature` · `clock` (freshness) · `refresh` · `run` (play in a ring) · `check` · `alert` · `close` · `chevron` · `external`.

Animate only on state: `check` stroke-draws on success, `refresh` turns once, `run` ring sweeps while running, theme sun↔moon morphs, `close` rotates from `+`. Motion's `pathLength` drives the drawing; there are no idle loops.

## 7. Motion contract

Engine: **Motion** (framer-motion) for UI, plus the **View Transitions API** for the theme switch only (with a fallback). Defaults: UI spring `{ stiffness: 380, damping: 34, mass: 0.9 }` (no visible bounce); small hover changes 80–140 ms; menus 120–200 ms; dock indicator 160–240 ms; object expansion 200–320 ms. Input is acknowledged instantly; settling may continue while the UI stays usable.

| Interaction | Immediate | Settling | Stable anchors | Interrupt / reverse | Reduced motion |
|---|---|---|---|---|---|
| Dock navigation | pressed scale .97 | active pill slides (spring); content crossfades 180 ms | dock, top utilities | A→B→C converges to C | instant swap |
| City card → detail sheet | card lifts 2 px | `layoutId` shared-element expand, 280 ms; backdrop dims | dock, page scroll | Esc/back closes and reverses into the card; focus returns to the card | fade only |
| Map marker → station panel | marker scales 1.15 | panel slides in from the right, 240 ms | map camera | a new marker retargets the panel | instant |
| City picker | trigger pressed | anchored menu grows from the trigger, 160 ms | trigger position | reopenable at once | fade |
| New data (Realtime) | "Updated just now" pill appears | changed numbers count to the new value, 600 ms, once | layout (no shift: reserved widths) | — | numbers swap |
| Pipeline task state | node outline changes | running = stroke sweep loop (the only allowed loop); success = check draws in 300 ms; failure = one 2 px shake + red | DAG layout | — | static state icons |
| Chart first view | — | line draws in 500 ms | axes | — | drawn |
| Theme toggle | — | circular reveal from the toggle (View Transitions) | everything | — | instant |

Rules: animate only `transform`/`opacity`; no application logic in animation callbacks; no invisible overlays left behind; test the app with motion disabled.

## 8. Screens

| Route | Purpose | Content | Key states |
|---|---|---|---|
| `/` Overview | "Delhi NCR air, right now" | headline + as-of time + freshness pill; 5 city cards as a bento (Delhi large): NAQI, category chip, dominant pollutant, 7-day sparkline, weather row; "worst stations right now" strip (from data); attribution footer | skeleton per card; stale (amber pill); a city with no stations |
| `/map` | where it's bad | full-bleed Google Map (muted Map ID), category-colored station dots + clustering, pollutant chips, legend, **Google UAQI heatmap toggle** (labelled "model, Google"), station panel with a 48 h chart | no key → station list fallback; stale stations dimmed |
| `/trends` | how it changes | filters (cities, pollutant, 7d/30d/90d/1y); multi-city NAQI line; pollutant small multiples with the NAAQS reference line; **calendar heatmap** of daily category; weather-vs-PM2.5 scatter with Pearson r | empty range; partial coverage note |
| `/pipeline` | **data engineering made visible** | live 6-task DAG (SSE); medallion stack with row counts per layer (Bronze → Silver → Gold → Supabase); quarantine count; recent runs (trigger type, duration); **Run pipeline** (passcode → server action → API; cooldown shown) | idle / running / failed / cooldown |
| `/dashboards` | the BI side | segmented control Databricks / Power BI → iframe in a glass frame with a skeleton; "open in new tab" | embed blocked → screenshot gallery + link |
| `/how-it-works` | viva walkthrough | scroll-stepped animated architecture SVG: Sources → Landing → Bronze → Silver → Gold → Serving → Apps, each step with a 2-line explanation + the live count | — |

Every data view shows the **source label, index standard and last-updated time**. Data gaps are shown as gaps in charts, never interpolated.

## 9. Components

Primitives: shadcn/ui (Radix) restyled to our tokens: Dialog/Sheet, Popover, Select, Tabs/Segmented, Tooltip, Toggle, Skeleton, Sonner toasts. Patterns may be studied from the Aceternity, ReactBits and MagicUI registries (via MCP), then rewritten to our tokens with demo delays and loops removed. Charts: **Recharts**, themed with tokens (hairline grid, tabular ticks, a "show as table" toggle for accessibility). Map: `@vis.gl/react-google-maps`.

## 10. Quality bar (checked before any UI ships)

- [ ] Contrast ≥ 4.5:1 on the brightest backdrop crop, in light and dark
- [ ] Glass only on chrome; reading surfaces ≥ 80% opaque
- [ ] Only custom icons; no emoji; icon buttons labelled
- [ ] Amber used only for forecast/estimated/stale; AQI colors only for data
- [ ] Every number has a unit + source + time; no fabricated values
- [ ] Focus rings visible; tab order follows the visual order; Esc closes sheets and menus; focus is restored
- [ ] Touch targets ≥ 44 px; responsive at 375 / 768 / 1024 / 1440; no horizontal scroll
- [ ] `prefers-reduced-motion` and reduced transparency respected; the app works with motion off
- [ ] Skeletons match the final layout; no full-page spinners; no layout shift on data refresh
- [ ] Lighthouse: performance ≥ 85, accessibility ≥ 95

**Banned:** purple/pink gradient heroes, glass on every card, colored icon circles in many hues, heavy drop shadows, bounce-in, perpetual shimmer, fake dashboard numbers, Lucide/emoji icons.
