export const number = (n: number | null | undefined, digits = 0) =>
  n == null
    ? "Unavailable"
    : n.toLocaleString("en-IN", { maximumFractionDigits: digits });
export const observed = (value?: string | null) =>
  value
    ? new Date(value).toLocaleString("en-IN", {
        dateStyle: "medium",
        timeStyle: "short",
        timeZone: "Asia/Kolkata",
      }) + " IST"
    : "Time unavailable";
