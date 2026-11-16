import { bindings, defineConfig, defineWorker } from "cf/config";

export default defineConfig({
  accountId: "09fc9d2f5f1796915f66c4cd4302d111",
  worker: defineWorker({
    name: "aeris-web",
    entrypoint: "vinext/server/fetch-handler",
    compatibilityDate: "2026-11-16",
    domains: ["aeris.inerate.com"],
    assets: {
      htmlHandling: "none",
      notFoundHandling: "none",
      runWorkerFirst: ["/*", "!/_next/static/*", "!/*/_next/static/*"],
    },
    env: {
      ASSETS: bindings.assets(),
      NEXT_PUBLIC_SUPABASE_URL: bindings.text("https://ttdduchixyhuzpnkodyj.supabase.co"),
      NEXT_PUBLIC_SUPABASE_ANON_KEY: bindings.text("sb_publishable_8M6Fejsm-VlUnb3sdQPvvQ_t4s1axm_"),
      API_URL: bindings.text("https://aeris-api-70530354318.asia-south1.run.app"),
      NEXT_PUBLIC_DATABRICKS_DASHBOARD_EMBED_URL: bindings.text("https://adb-7405619537081466.6.azuredatabricks.net/embed/dashboardsv3/01f1e1c15f7e1996bd3a30ca268ed58c"),
      VINEXT_KV_CACHE: bindings.kv({ id: "350fbe8ddb924866bd2bf3e80c2cd540" }),
      NEXT_PUBLIC_POWERBI_EMBED_URL: bindings.text("https://app.powerbi.com/reportEmbed?reportId=a91e5d4c-2f3e-4f85-b4d4-60cc0a710a4e      NEXT_PUBLIC_GOOGLE_MAP_ID: bindings.text("1a16bea3e9521acf82834bdd"),
      NEXT_PUBLIC_GOOGLE_MAPS_API_KEY: bindings.secret(),
      REVALIDATE_SECRET: bindings.secret(),autoAuth=true      NEXT_PUBLIC_GOOGLE_MAP_ID: bindings.text("1a16bea3e9521acf82834bdd"),
      NEXT_PUBLIC_GOOGLE_MAPS_API_KEY: bindings.secret(),
      REVALIDATE_SECRET: bindings.secret(),ctid=e81b2e5d-de73-4804-96ee-eacf89a7a5e8"),
      NEXT_PUBLIC_GOOGLE_MAP_ID: bindings.text("1a16bea3e9521acf82834bdd"),
      NEXT_PUBLIC_GOOGLE_MAPS_API_KEY: bindings.secret(),
      REVALIDATE_SECRET: bindings.secret(),
    },
  }),
});
