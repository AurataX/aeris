import { runtime } from "@/shared/lib/runtime";
import { DashboardViewer } from "@/features/dashboards/DashboardViewer";
export default function Dashboards() {
  const embeds = [
    {
      name: "Databricks AI/BI",
      url: runtime("NEXT_PUBLIC_DATABRICKS_DASHBOARD_EMBED_URL") ?? "",
      note: "Gold tables on a serverless SQL warehouse. Sign in with your authorised Databricks account.",
    },
    {
      name: "Power BI",
      url: runtime("NEXT_PUBLIC_POWERBI_EMBED_URL") ?? "",
      note: "Star schema and DAX measures over the same Gold data. Your Microsoft account needs report access.",
    },
  ];
  return (
    <>
      <p className="eyebrow">ONE DATA FOUNDATION · TWO BI LENSES</p>
      <h1>Explore the BI side.</h1>
      <p className="intro">
        Inspect the Gold analytics through Databricks AI/BI or Power BI. Access
        permissions and refresh times belong to each reporting platform.
      </p>
      <DashboardViewer embeds={embeds} />
    </>
  );
}
