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
      API_URL: bindings.text("https://aeris-api-70530354318.asia-south1.run.app"),
      NEXT_PUBLIC_DATABRICKS_DASHBOARD_EMBED_URL: bindings.text("https://adb-7405619537081466.6.azuredatabricks.net/embed/dashboardsv3/01f1e1c15f7e1996bd3a30ca268ed58c"),
      VINEXT_KV_CACHE: bindings.kv({ id: "350fbe8ddb924866bd2bf3e80c2cd540" }),
      REVALIDATE_SECRET: bindings.secret(),
    },
  }),
});
