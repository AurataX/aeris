"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
export function Utilities() {
  const [dark, setDark] = useState(false);
  const [plain, setPlain] = useState(false);
  useEffect(() => {
    const saved = localStorage.getItem("aeris-theme");
    const value = saved
      ? saved === "dark"
      : matchMedia("(prefers-color-scheme: dark)").matches;
    setDark(value);
    document.documentElement.dataset.theme = value ? "dark" : "light";
  }, []);
  function theme() {
    const next = !dark;
    setDark(next);
    document.documentElement.dataset.theme = next ? "dark" : "light";
    localStorage.setItem("aeris-theme", next ? "dark" : "light");
  }
  return (
    <header className="shell-header">
      <Link href="/" className="brand">
        <img src="/icon.svg" alt="" width="36" height="36" />
        <span>
          AERIS<small>DELHI NCR · AIR INTELLIGENCE</small>
        </span>
      </Link>
      <div className="glass utilities">
        <button onClick={theme} aria-pressed={dark}>
          {dark ? "Light theme" : "Dark theme"}
        </button>
        <button
          aria-pressed={plain}
          onClick={() => {
            setPlain(!plain);
            document.documentElement.dataset.plain = String(!plain);
          }}
        >
          Plain sky
        </button>
      </div>
    </header>
  );
}
