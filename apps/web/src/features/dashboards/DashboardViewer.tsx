"use client";
import { useState } from "react";
export function DashboardViewer({
  embeds,
}: {
  embeds: { name: string; url: string; note: string }[];
}) {
  const [selected, setSelected] = useState(0);
  const [loaded, setLoaded] = useState(false);
  const e = embeds[selected];
  return (
    <section className="surface p-5">
      <div
        className="flex gap-2 mb-5"
        role="group"
        aria-label="Dashboard provider"
      >
        {embeds.map((item, i) => (
          <button
            key={item.name}
            aria-pressed={i === selected}
            className={i === selected ? "text-primary underline" : "text-ink-2"}
            onClick={() => {
              setSelected(i);
              setLoaded(false);
            }}
          >
            {item.name}
          </button>
        ))}
      </div>
      <h2>{e.name}</h2>
      <p className="text-ink-2 my-3">{e.note}</p>
      {e.url ? (
        <>
          <p className="caption mb-3">
            Sign-in or embedding restrictions may prevent display.{" "}
            <a
              className="text-primary underline"
              href={e.url}
              target="_blank"
              rel="noreferrer"
            >
              Open in a new tab
            </a>
          </p>
          {!loaded && <p role="status">Loading dashboard frame…</p>}
          <iframe
            key={e.url}
            src={e.url}
            title={e.name}
            onLoad={() => setLoaded(true)}
            className="w-full min-h-[600px] rounded-xl border border-hairline"
          />
        </>
      ) : (
        <p className="py-16 text-ink-2">
          The report is awaiting its embed link. Explore the other dashboard or
          the Trends page meanwhile.
        </p>
      )}
    </section>
  );
}
