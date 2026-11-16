import { JobFlow } from "@/features/pipeline/JobFlow";
import { TableEvidence } from "@/features/pipeline/TableEvidence";
import { LayerNotes } from "@/features/pipeline/LayerNotes";
import { Evidence } from "@/features/pipeline/Evidence";
import { Runs } from "@/features/pipeline/Runs";
export default function Pipeline() {
  return (
    <>
      <p className="eyebrow">THE ENGINEERING, EXPOSED</p>
      <h1>
        From raw files
        <br />
        to trusted tables.
      </h1>
      <p className="intro">
        Apache Spark on Azure Databricks. Incremental ingestion, explicit
        quality checks, and a serving layer that keeps the website independent
        of compute.
      </p>
      <Runs />
      <JobFlow />
      <TableEvidence />
      <LayerNotes />
      <Evidence />
    </>
  );
}
