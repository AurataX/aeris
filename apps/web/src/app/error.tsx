"use client";
export default function ErrorPage({ reset }: { reset: () => void }) {
  return (
    <section className="surface p-8">
      <h1>This view could not load</h1>
      <p className="intro">
        The page encountered an error. Your data has not been changed.
      </p>
      <button onClick={reset}>Try again</button>
    </section>
  );
}
