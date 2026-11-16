import { Suspense } from "react";
import Link from "next/link";
import { OverviewData } from "@/features/overview/OverviewData";
import { WorstStations } from "@/features/overview/WorstStations";
export default function Overview() {
  return (
    <>
      <p className="eyebrow">THE AIR WE SHARE</p>
      <h1>Five cities. One atmosphere.</h1>
      <p className="intro">
        Delhi NCR air quality, with the evidence behind every number. Ground
        measurements, processed with Apache Spark into Indian NAQI.
      </p>
      <Suspense
        fallback={
          <div className="surface p-8" role="status">
            Loading city observations...
          </div>
        }
      >
        <OverviewData />
      </Suspense>
      <section className="section-heading">
        <h2>Behind the numbers</h2>
        <Link href="/how-it-works">
          Follow a reading through the pipeline ·
        </Link>
      </section>
      <div className="surface p-6">
        <p>
          PM2.5 is a concentration in µg/m³. NAQI is a unitless index combining
          pollutant sub-indices. A missing index can mean there were too few
          pollutants to calculate it.
        </p>
      </div>
      <Suspense fallback={<p>Loading stations·</p>}>
        <WorstStations />
      </Suspense>
    </>
  );
}
