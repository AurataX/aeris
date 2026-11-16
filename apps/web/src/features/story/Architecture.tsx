"use client";
import { motion, useReducedMotion } from "motion/react";
import { flow } from "./flow";
export function Architecture() {
  const reduced = useReducedMotion();
  return (
    <section>
      <div className="section-heading">
        <h2>A reading's journey</h2>
        <span className="caption">INGEST · TRANSFORM · SERVE</span>
      </div>
      <ol className="grid gap-4 md:grid-cols-2">
        {flow.map(([n, title, detail]) => (
          <motion.li
            key={n}
            initial={reduced ? false : { opacity: 1, y: 12 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="surface p-6"
          >
            <span className="eyebrow">{n} ·</span>
            <h3 className="mt-2 mb-2">{title}</h3>
            <p className="text-ink-2 leading-relaxed">{detail}</p>
          </motion.li>
        ))}
      </ol>
    </section>
  );
}
