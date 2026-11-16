import { getCities } from "@/shared/lib/api";
import { hazeFor } from "@/shared/lib/aqi";

// A real photo can replace this later (public/backdrop.webp). Until then: sky + skyline drawn in SVG.
export async function Backdrop() {
  const delhi = (await getCities())?.data.find((c) => c.city === "Delhi");
  const haze = hazeFor(delhi?.naqi ?? null); // the sky turns smoggy when the real air is bad

  return (
    <div
      aria-hidden
      className="atmosphere fixed inset-0 -z-10 overflow-hidden"
      style={{
        background:
          "linear-gradient(180deg, var(--sky-top), var(--sky-bottom) 70%)",
      }}
    >
      <div
        className="absolute inset-0 transition-opacity duration-1000"
        style={{ opacity: haze * 0.75, background: "var(--haze-gradient)" }}
      />
      <svg
        viewBox="0 0 1440 220"
        preserveAspectRatio="none"
        className="absolute bottom-0 h-[26vh] w-full"
        style={{ fill: "var(--ink)", opacity: 0.07 + haze * 0.05 }}
      >
        <path d="M0 220V150h60v-30h40v30h50V90h30v60h60v-45h45v45h70V60h26v90h64v-35h50v35h80V80h34v70h56v-25h60v25h90v-55h40v55h70V40h22v110h80v-40h50v40h70v-70h30v70h90v-30h55v30h60V100h35v50h70v-35h50v35h86v70Z" />
      </svg>
    </div>
  );
}
