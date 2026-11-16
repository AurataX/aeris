import { Architecture } from "@/features/story/Architecture";
import { NumberStory } from "@/features/story/NumberStory";
import { Honesty } from "@/features/story/Honesty";
import { TableEvidence } from "@/features/pipeline/TableEvidence";
import { LayerNotes } from "@/features/pipeline/LayerNotes";
import { Evidence } from "@/features/pipeline/Evidence";
export default function HowItWorks() {
  return (
    <>
      <p className="eyebrow">FROM SENSOR TO SCREEN</p>
      <h1>
        There's a system
        <br />
        behind this number.
      </h1>
      <p className="intro">
        AERIS turns raw air-quality records into explainable city intelligence.
        Follow the data, inspect the transformations, and see where uncertainty
        remains.
      </p>
      <Architecture />
      <TableEvidence />
      <LayerNotes />
      <NumberStory />
      <Honesty />
      <Evidence />
    </>
  );
}
