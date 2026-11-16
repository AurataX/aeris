"use client";

import { useEffect, useRef } from "react";
import type { Station } from "@/shared/lib/api";
import { categoryColor } from "@/shared/lib/aqi";

/* eslint-disable @typescript-eslint/no-explicit-any */
const G = () => (window as any).google;

function loadMaps(key: string) {
  return new Promise<void>((done, fail) => {
    if (G()?.maps) return done();
    const s = document.createElement("script");
    s.src = `https://maps.googleapis.com/maps/api/js?key=${key}&v=weekly&loading=async`;
    s.onload = () => done();
    s.onerror = () => fail();
    document.head.append(s);
  });
}

type Props = { stations: Station[]; mapsKey: string; mapId: string; onPick: (s: Station) => void };

export function GoogleLayer({ stations, mapsKey, mapId, onPick }: Props) {
  const box = useRef<HTMLDivElement>(null);
  useEffect(() => {
    let alive = true;
    (async () => {
      try {
        await loadMaps(mapsKey);
        const { Map } = await G().maps.importLibrary("maps");
        const { AdvancedMarkerElement } = await G().maps.importLibrary("marker");
        if (!alive || !box.current) return;
        const map = new Map(box.current, { center: { lat: 28.6139, lng: 77.209 }, zoom: 9, mapId, disableDefaultUI: true, zoomControl: true });
        stations.forEach((s) => {
          const dot = document.createElement("div");
          dot.style.cssText = `width:16px;height:16px;border-radius:50%;border:2px solid #fff;background:${categoryColor(s.naqi_category)};opacity:${s.is_stale ? 0.45 : 0.95}`;
          new AdvancedMarkerElement({ map, position: { lat: s.lat, lng: s.lon }, content: dot, title: s.name }).addListener("click", () => onPick(s));
        });
      } catch {
        if (box.current) box.current.textContent = "The map could not load. Check the Maps key.";
      }
    })();
    return () => { alive = false; };
  }, [stations, mapsKey, mapId, onPick]);
  return <div ref={box} className="h-full w-full" />;
}
