import { revalidateTag } from "next/cache";
import { timingSafeEqual } from "node:crypto";

// Called by the Databricks sync task after every successful Gold -> Supabase sync.
export async function POST(request: Request) {
  const sent = Buffer.from(request.headers.get("x-revalidate-secret") ?? "");
  const wanted = Buffer.from(process.env.REVALIDATE_SECRET ?? "");
  if (!wanted.length || sent.length !== wanted.length || !timingSafeEqual(sent, wanted)) {
    return Response.json({ error: "unauthorized" }, { status: 401 });
  }
  revalidateTag("gold", "max"); // stale-while-revalidate: visitors never wait
  return Response.json({ revalidated: true });
}
