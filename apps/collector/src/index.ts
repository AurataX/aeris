import { CITIES } from "./config";
import { Env, land, token } from "./databricks";
import { cpcbState, cpcbStates, openaqLatest, weatherCity } from "./sources";

// Each run stays under the free plan's 50 subrequests:
//   cron "*/30"   -> OpenAQ half 0 + CPCB (3 states)       = 38 calls
//   cron "15,45"  -> OpenAQ half 1 + weather (5 cities)    = 43 calls
// A failed source is skipped and logged; the next run tries again.
async function collect(env: Env, minute: number) {
  const group = minute % 30 < 15 ? 0 : 1;
  const bearer = await token(env);
  const jobs: Promise<unknown>[] = [
    openaqLatest(env.OPENAQ_API_KEY, group).then((p) => land(env, bearer, "openaq", p, `,"group":${group}`)),
  ];
  if (group === 0) {
    for (const state of cpcbStates) {
      jobs.push(cpcbState(env.DATA_GOV_IN_API_KEY, state).then((p) => land(env, bearer, "cpcb", p, `,"state":"${state}"`)));
    }
  } else {
    for (const city of Object.keys(CITIES)) {
      jobs.push(weatherCity(city).then((p) => land(env, bearer, "weather", p, `,"city":"${city}","api":"forecast"`)));
    }
  }
  const results = await Promise.allSettled(jobs);
  results.forEach((r, i) => r.status === "rejected" && console.error("source", i, String(r.reason)));
}

export default {
  scheduled: (event: ScheduledEvent, env: Env, ctx: ExecutionContext) =>
    ctx.waitUntil(collect(env, new Date(event.scheduledTime).getUTCMinutes())),
};
