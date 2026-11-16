import { runtime } from "@/shared/lib/runtime";
import type { Metadata } from "next";

import { Suspense } from "react";
import { Backdrop } from "@/shared/ui/Backdrop";
import { Dock } from "@/shared/ui/Dock";
import { Realtime } from "@/shared/ui/Realtime";
import { Utilities } from "@/shared/ui/Utilities";
import "./globals.css";

export const metadata: Metadata = {
  title: "AERIS · Delhi NCR air quality",
  description:
    "Real air-quality data for Delhi NCR, processed with Spark on Azure Databricks.",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="en" data-theme="light" className="antialiased">
      <body className="min-h-screen">
        <Suspense fallback={null}>
          <Backdrop />
        </Suspense>
        <a className="skip-link" href="#content">
          Skip to content
        </a>
        <Utilities />
        <main
          id="content"
          className="mx-auto w-full max-w-6xl px-4 pb-20 pt-8 sm:px-6"
        >
          {children}
        </main>
        <Dock />
        <footer className="mx-auto max-w-6xl px-6 pb-28 text-xs text-ink-3">
          <Realtime
            url={runtime("NEXT_PUBLIC_SUPABASE_URL") ?? ""}
            publicKey={runtime("NEXT_PUBLIC_SUPABASE_ANON_KEY") ?? ""}
          />
          Air quality: OpenAQ and its data providers · Central Pollution Control
          Board via data.gov.in · Weather: Open-Meteo.com (CC BY 4.0, model
          data) · AQI shown is the Indian NAQI computed by AERIS from
          observations.
        </footer>
      </body>
    </html>
  );
}
