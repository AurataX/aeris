-- AERIS serving schema: copies of Gold tables, written only by Databricks (aeris_sync), read by FastAPI (aeris_api).
-- Spec: docs/data-model.md §6

create table public.dim_city (
  city text primary key,
  state text not null,
  lat double precision not null,
  lon double precision not null
);

create table public.dim_pollutant (
  pollutant text primary key,
  display_name text not null,
  unit text not null,
  naaqs_limit double precision,
  averaging text not null
);

create table public.station_status (
  station_id text primary key,
  source text not null,
  name text not null,
  city text not null references public.dim_city(city),
  lat double precision not null,
  lon double precision not null,
  last_observed_at timestamptz,
  pm25_latest double precision,
  pm10_latest double precision,
  no2_latest double precision,
  o3_latest double precision,
  naqi_24h integer,
  naqi_category text,
  is_stale boolean not null default false
);
create index station_status_city_idx on public.station_status (city);

create table public.latest_city_status (
  city text primary key references public.dim_city(city),
  as_of timestamptz not null,
  naqi integer,
  naqi_category text,
  dominant_pollutant text,
  pm25_avg_24h double precision,
  pm10_avg_24h double precision,
  stations_reporting integer not null,
  temperature_c double precision,
  humidity_pct double precision,
  wind_speed_kmh double precision,
  index_standard text not null
);

create table public.city_daily_aqi (
  city text not null references public.dim_city(city),
  date_ist date not null,
  index_standard text not null,
  source text not null,
  naqi integer,
  naqi_category text,
  dominant_pollutant text,
  pollutants_used integer,
  pm25_avg double precision,
  pm10_avg double precision,
  no2_avg double precision,
  so2_avg double precision,
  o3_max8h double precision,
  co_max8h double precision,
  stations_count integer,
  primary key (city, date_ist, index_standard, source)
);

create table public.pollutant_trends (
  city text not null references public.dim_city(city),
  date_ist date not null,
  pollutant text not null references public.dim_pollutant(pollutant),
  source text not null,
  avg_value double precision,
  min_value double precision,
  max_value double precision,
  p95_value double precision,
  unit text not null,
  hours_covered integer,
  exceeds_naaqs boolean,
  primary key (city, date_ist, pollutant, source)
);

create table public.weather_pollution_daily (
  city text not null references public.dim_city(city),
  date_ist date not null,
  pm25_avg double precision,
  pm10_avg double precision,
  temp_avg_c double precision,
  humidity_avg_pct double precision,
  wind_avg_kmh double precision,
  precip_sum_mm double precision,
  pressure_avg_hpa double precision,
  weather_is_modeled boolean not null default true,
  primary key (city, date_ist)
);

create table public.table_stats (
  run_id text not null,
  table_name text not null,
  layer text not null,
  row_count bigint not null,
  max_event_ts timestamptz,
  computed_at timestamptz not null,
  primary key (run_id, table_name)
);

create table public.sync_runs (
  run_id text primary key,
  job_run_id text,
  started_at timestamptz not null,
  finished_at timestamptz,
  status text not null,
  rows_upserted jsonb
);

-- RLS on everything; only sync_runs is readable by anon (Realtime "data updated" signal)
alter table public.dim_city enable row level security;
alter table public.dim_pollutant enable row level security;
alter table public.station_status enable row level security;
alter table public.latest_city_status enable row level security;
alter table public.city_daily_aqi enable row level security;
alter table public.pollutant_trends enable row level security;
alter table public.weather_pollution_daily enable row level security;
alter table public.table_stats enable row level security;
alter table public.sync_runs enable row level security;

create policy "anon reads sync_runs" on public.sync_runs for select to anon using (true);
alter publication supabase_realtime add table public.sync_runs;

-- Least-privilege login roles; passwords are set by the owner in the SQL editor, never in git
create role aeris_sync nologin;
create role aeris_api nologin;

grant usage on schema public to aeris_sync, aeris_api;
grant select, insert, update on all tables in schema public to aeris_sync;
grant select on all tables in schema public to aeris_api;

create policy "sync writes" on public.dim_city for all to aeris_sync using (true) with check (true);
create policy "sync writes" on public.dim_pollutant for all to aeris_sync using (true) with check (true);
create policy "sync writes" on public.station_status for all to aeris_sync using (true) with check (true);
create policy "sync writes" on public.latest_city_status for all to aeris_sync using (true) with check (true);
create policy "sync writes" on public.city_daily_aqi for all to aeris_sync using (true) with check (true);
create policy "sync writes" on public.pollutant_trends for all to aeris_sync using (true) with check (true);
create policy "sync writes" on public.weather_pollution_daily for all to aeris_sync using (true) with check (true);
create policy "sync writes" on public.table_stats for all to aeris_sync using (true) with check (true);
create policy "sync writes" on public.sync_runs for all to aeris_sync using (true) with check (true);

create policy "api reads" on public.dim_city for select to aeris_api using (true);
create policy "api reads" on public.dim_pollutant for select to aeris_api using (true);
create policy "api reads" on public.station_status for select to aeris_api using (true);
create policy "api reads" on public.latest_city_status for select to aeris_api using (true);
create policy "api reads" on public.city_daily_aqi for select to aeris_api using (true);
create policy "api reads" on public.pollutant_trends for select to aeris_api using (true);
create policy "api reads" on public.weather_pollution_daily for select to aeris_api using (true);
create policy "api reads" on public.table_stats for select to aeris_api using (true);
create policy "api reads" on public.sync_runs for select to aeris_api using (true);
