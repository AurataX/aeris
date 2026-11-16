@AGENTS.md

# Claude Code notes

- **Skills:** keep `ponytail` active. Load `ui-ux-pro-max` before any UI work; the design system lives in [docs/design.md](docs/design.md). From Atelier, use only the **code laws**: `clean-code-law` (250 words), `structure-law`, `security-law` and the Next.js/FastAPI `stack-guides` for data fetching and caching. **Do not use Atelier's colors or theme.**
- **Databricks skills** (plugin `databricks@claude-plugins-official`): load `databricks-dabs` (bundle/job YAML), `databricks-jobs`, `databricks-spark-structured-streaming` (Auto Loader), `databricks-unity-catalog`, `databricks-aibi-dashboards`, `databricks-dbsql` and `databricks-serverless` before the matching work. Verify CLI syntax with them instead of guessing.
- **MCP servers in use:** Supabase (project `aeris`; schema changes only through `supabase/migrations/`), Cloudflare (collector Worker), shadcn / Aceternity / ReactBits / MagicUI registries (component patterns, restyled to our tokens), Power BI Modeling MCP (semantic model in an open Desktop), Claude in Chrome (UI verification screenshots).
- **Before UI work:** read `prompt/fluid_ui.jpeg`, `prompt/fluid-interface-library/reference.png` and `prompt/fluid-interface-library/master-brief.md` for feel, materials and motion. Never copy their layouts.
- **Explaining to the student:** use simple Hinglish, and compare each new idea to something from `prompt/First_PR.clean.ipynb`. Name what each notebook reads and writes.
- **Git authorship:** commits are authored by the student alone. **Never add `Co-Authored-By: Claude`, "Generated with Claude Code" or any AI attribution** to commit messages or PR descriptions. This overrides default attribution settings.
- **Task tracking:** tick items in [docs/task.md](docs/task.md) as they finish, with the evidence (run id, row count, URL).
