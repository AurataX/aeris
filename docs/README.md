# AERIS docs

This folder is the clean, final source of truth. Original chat briefs live in `../prompt/` for history only.

| Doc | Read it when you need… |
|---|---|
| [system.md](system.md) | the mission, scope and the data rules nobody may break |
| [architecture.md](architecture.md) | how all services connect, batch vs streaming, caching, secrets |
| [data-sources.md](data-sources.md) | which API/dataset gives what, endpoints, limits, licenses |
| [data-model.md](data-model.md) | every Bronze/Silver/Gold/Supabase table, its columns, grain, keys; the AQI method |
| [pipelines.md](pipelines.md) | ingestion, Auto Loader, the Job DAG, triggers, reruns, data quality |
| [api.md](api.md) | the FastAPI endpoints the web app uses |
| [design.md](design.md) | the UI design system: tokens, glass materials, motion, icons, screens |
| [dashboards.md](dashboards.md) | the Databricks AI/BI dashboard and the Power BI report |
| [setup.md](setup.md) | step-by-step installs, logins and secrets on Windows |
| [cost.md](cost.md) | what costs money, how much, and the guardrails |
| [decisions.md](decisions.md) | why each technology was chosen (and what was rejected) |
| [task.md](task.md) | the build checklist, day by day |
| [demo-script.md](demo-script.md) | the presentation flow + viva questions |
| [learning.md](learning.md) | Hinglish notes connecting new concepts to the practice notebook |

**Reading order for a newcomer:** system → architecture → data-model → pipelines → task.
