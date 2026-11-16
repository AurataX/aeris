export const CATEGORIES = [
  "Good",
  "Satisfactory",
  "Moderate",
  "Poor",
  "Very Poor",
  "Severe",
] as const;
export type Category = (typeof CATEGORIES)[number];

const token: Record<Category, string> = {
  Good: "--aqi-good",
  Satisfactory: "--aqi-satisfactory",
  Moderate: "--aqi-moderate",
  Poor: "--aqi-poor",
  "Very Poor": "--aqi-very-poor",
  Severe: "--aqi-severe",
};

// text on the colored chip: dark on the light colors, white on the dark ones
const darkText = new Set<string>(["Satisfactory", "Moderate", "Poor"]);

export const categoryColor = (c: string | null) =>
  c && c in token ? `var(${token[c as Category]})` : "var(--ink-3)";
export const categoryInk = (c: string | null) =>
  c && darkText.has(c) ? "var(--chip-dark)" : "var(--chip-light)";

// 0 = clear sky, 1 = heavy smog. NAQI 500 is the top of the scale.
export const hazeFor = (naqi: number | null) =>
  naqi == null ? 0 : Math.min(1, Math.max(0, (naqi - 50) / 400));
