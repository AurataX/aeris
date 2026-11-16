const VOLUME = "/Volumes/aeris_brick/default/aeris/landing/live";

export interface Env {
  DATABRICKS_HOST: string;
  DATABRICKS_CLIENT_ID: string;
  DATABRICKS_CLIENT_SECRET: string;
  OPENAQ_API_KEY: string;
  DATA_GOV_IN_API_KEY: string;
}

// OAuth machine-to-machine token for the collector service principal
export async function token(env: Env): Promise<string> {
  const r = await fetch(`${env.DATABRICKS_HOST}/oidc/v1/token`, {
    method: "POST",
    headers: {
      Authorization: "Basic " + btoa(`${env.DATABRICKS_CLIENT_ID}:${env.DATABRICKS_CLIENT_SECRET}`),
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: "grant_type=client_credentials&scope=all-apis",
  });
  if (!r.ok) throw new Error(`token ${r.status}`);
  return ((await r.json()) as { access_token: string }).access_token;
}

// One new file per call. Unique names, so the file-arrival trigger sees every file.
export async function land(env: Env, bearer: string, source: string, payload: unknown, meta = {}) {
  const now = new Date();
  const day = now.toISOString().slice(0, 10).replaceAll("-", "/");
  const stamp = now.toISOString().replace(/[-:.]/g, "");
  const path = `${VOLUME}/${source}/${day}/${source}_${stamp}.json`;
  const body = JSON.stringify({ source, fetched_at: now.toISOString(), ...meta, payload });
  const r = await fetch(`${env.DATABRICKS_HOST}/api/2.0/fs/files${path}?overwrite=false`, {
    method: "PUT",
    headers: { Authorization: `Bearer ${bearer}` },
    body,
  });
  if (!r.ok) throw new Error(`land ${source} ${r.status}`);
  return path;
}
