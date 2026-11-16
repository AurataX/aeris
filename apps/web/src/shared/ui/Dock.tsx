"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { motion } from "motion/react";
import { Icon, type IconName } from "@/shared/icons/Icon";

const items: { href: string; label: string; icon: IconName }[] = [
  { href: "/", label: "Overview", icon: "overview" },
  { href: "/map", label: "Map", icon: "map" },
  { href: "/trends", label: "Trends", icon: "trends" },
  { href: "/pipeline", label: "Pipeline", icon: "pipeline" },
  { href: "/dashboards", label: "Dashboards", icon: "dashboards" },
  { href: "/how-it-works", label: "How it works", icon: "layers" },
];

export function Dock() {
  const path = usePathname();
  return (
    <nav aria-label="Main" className="glass fixed bottom-4 left-1/2 z-30 flex -translate-x-1/2 gap-1 rounded-full p-1.5">
      {items.map(({ href, label, icon }) => {
        const active = href === "/" ? path === "/" : path.startsWith(href);
        return (
          <Link key={href} href={href} aria-current={active ? "page" : undefined}
                className="relative flex min-h-11 items-center gap-2 rounded-full px-3.5 text-sm font-medium text-ink-2 transition-colors hover:text-ink sm:px-4">
            {active && (
              <motion.span layoutId="dock-pill" className="absolute inset-0 rounded-full"
                           style={{ background: "linear-gradient(180deg, #ffffff, #e8eef6)", boxShadow: "0 1px 0 #fff inset, 0 2px 8px rgba(15,23,42,.12)" }}
                           transition={{ type: "spring", stiffness: 380, damping: 34, mass: 0.9 }} />
            )}
            <Icon name={icon} className={`relative ${active ? "text-primary" : ""}`} />
            <span className={`relative hidden md:inline ${active ? "text-[#0f172a]" : ""}`}>{label}</span>
          </Link>
        );
      })}
    </nav>
  );
}
