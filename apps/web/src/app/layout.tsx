import type { Metadata } from "next";
import { DM_Sans, Fira_Code } from "next/font/google";
import { Suspense } from "react";
import { Backdrop } from "@/shared/ui/Backdrop";
import { Dock } from "@/shared/ui/Dock";
import "./globals.css";

const sans = DM_Sans({ variable: "--font-dm-sans", subsets: ["latin"] });
const mono = Fira_Code({ variable: "--font-fira-code", subsets: ["latin"] });

export const metadata: Metadata = {
  title: "AERIS · Delhi NCR air quality",
  description: "Real air-quality data for Delhi NCR, processed with Spark on Azure Databricks.",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="en" data-theme="light" className={`${sans.variable} ${mono.variable} antialiased`}>
      <body className="min-h-screen">
        <Suspense fallback={null}>
          <Backdrop />
        </Suspense>
        <main className="mx-auto w-full max-w-6xl px-4 pb-32 pt-10 sm:px-6">{children}</main>
        <Dock />
        <footer className="mx-auto max-w-6xl px-6 pb-28 text-xs text-ink-3">
          Air quality: OpenAQ and its data providers · Central Pollution Control Board via data.gov.in · Weather:
          Open-Meteo.com (CC BY 4.0, model data) · AQI shown is the Indian NAQI computed by AERIS from observations.
        </footer>
      </body>
    </html>
  );
}
