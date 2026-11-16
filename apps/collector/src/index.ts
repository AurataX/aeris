import { Env, land, token } from "./databricks";
import { cpcbSnapshot, openaqLatest, weatherNow } from "./sources";

// cron "*/30" -> half 0 + CPCB + weather · cron "15,45" -> half 1.   A failed source is skipped; the next run retries.
async function collect(env: Env, minute: number) {
  const group = minute % 30 < 15 ? 0 : 1;
  const bearer = await token(env);
  const jobs: Promise<unknown>[] = [
    openaqLatest(env.OPENAQ_API_KEY, group).then((p) => land(env, bearer, "openaq", p, { group })),
  ];
  if (group === 0) {
    jobs.push(cpcbSnapshot(env.DATA_GOV_IN_API_KEY).then((p) => land(env, bearer, "cpcb", p)));
    jobs.push(
      weatherNow().then((byCity) =>
        Promise.all(Object.entries(byCity).map(([city, p]) => land(env, bearer, "weather", p, { city, api: "forecast" }))),
      ),
    );
  }
  const results = await Promise.allSettled(jobs);
  results.forEach((r, i) => r.status === "rejected" && console.error("source", i, String(r.reason)));
}

export default {
  scheduled: (event: ScheduledEvent, env: Env, ctx: ExecutionContext) =>
    ctx.waitUntil(collect(env, new Date(event.scheduledTime).getUTCMinutes())),
};
