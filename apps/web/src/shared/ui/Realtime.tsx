"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { createClient } from "@supabase/supabase-js";
export function Realtime({
  url,
  publicKey,
}: {
  url: string;
  publicKey: string;
}) {
  const router = useRouter();
  const [status, setStatus] = useState("Updates connect when configured");
  useEffect(() => {
    if (!url || !publicKey) return;
    const client = createClient(url, publicKey, {
      auth: { persistSession: false, autoRefreshToken: false },
    });
    const channel = client
      .channel("aeris-sync")
      .on(
        "postgres_changes",
        { event: "*", schema: "public", table: "sync_runs" },
        (payload) => {
          if ("status" in payload.new && payload.new.status === "success") {
            setStatus("New publication received");
            router.refresh();
          }
        },
      )
      .subscribe((state) =>
        setStatus(
          state === "SUBSCRIBED"
            ? "Publication updates connected"
            : "Updates reconnecting; published data retained",
        ),
      );
    return () => {
      void client.removeChannel(channel);
    };
  }, [url, publicKey, router]);
  return (
    <p className="caption" role="status">
      {status}
    </p>
  );
}
