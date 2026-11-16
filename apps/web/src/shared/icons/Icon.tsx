import type { SVGProps } from "react";

// AERIS icon family: 24px grid, 1.75 stroke, round caps. Drawn for this project (no icon library).
const paths = {
  overview: "M3 9c3-2.4 5.4-2.4 8.4 0S17 11.4 21 9M3 14c3-2.4 5.4-2.4 8.4 0S17 16.4 21 14M3 19c3-2.4 5.4-2.4 8.4 0",
  map: "M4 6.5 9 4.5l6 2 5-2v13l-5 2-6-2-5 2v-13ZM9 4.5v13M15 6.5v13",
  trends: "M3.5 17.5 9 11.5l3.5 3L20.5 6M15 6h5.5v5.5",
  pipeline: "M5 6.5h4M15 6.5h4M12 17.5V11M7 6.5a2 2 0 1 0-.01 0M17 6.5a2 2 0 1 0-.01 0M12 19.5a2 2 0 1 0-.01 0M9 8.5l3 2.5 3-2.5",
  dashboards: "M4 4.5h7v7H4zM13 4.5h7v4h-7zM13 11.5h7v8h-7zM4 14.5h7v5H4z",
  layers: "m12 4 8.5 4.5L12 13 3.5 8.5 12 4ZM3.5 12.5 12 17l8.5-4.5M3.5 16 12 20.5 20.5 16",
  clock: "M12 20.5a8.5 8.5 0 1 0 0-17 8.5 8.5 0 0 0 0 17ZM12 7.5V12l3 2",
  refresh: "M19.5 12a7.5 7.5 0 1 1-2.2-5.3M19.5 4.5v4h-4",
  check: "m5 12.5 4.5 4.5L19 7.5",
  station: "M12 3.5v9M8 7.5a5.5 5.5 0 0 1 8 0M5.5 5a9 9 0 0 1 13 0M12 12.5 8.5 20.5M12 12.5l3.5 8M9.5 17.5h5",
  wind: "M3.5 9.5h10a2.5 2.5 0 1 0-2.5-2.5M3.5 14h14a2.5 2.5 0 1 1-2.5 2.5M3.5 18.5h7",
  external: "M14 4.5h5.5V10M19.5 4.5 11 13M17 14v4.5a1 1 0 0 1-1 1H5.5a1 1 0 0 1-1-1V8a1 1 0 0 1 1-1H10",
} as const;

export type IconName = keyof typeof paths;

export function Icon({ name, size = 20, ...rest }: { name: IconName; size?: number } & SVGProps<SVGSVGElement>) {
  return (
    <svg viewBox="0 0 24 24" width={size} height={size} fill="none" stroke="currentColor" strokeWidth={1.75}
         strokeLinecap="round" strokeLinejoin="round" aria-hidden="true" {...rest}>
      <path d={paths[name]} />
    </svg>
  );
}
