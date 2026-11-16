"use client";
import { useEffect, useState } from "react";
export function RunEvents({ runId, base }: { runId: number; base: string }) {
  const [tasks, setTasks] = useState<{ task: string; state: string }[]>([]);
  const [status, setStatus] = useState("Connecting to task events...");
  useEffect(() => {
    const stream = new EventSource(
      `${base}/api/v1/pipeline/runs/${runId}/events`,
    );
    stream.onmessage = (event) => {
      try {
        const rows = JSON.parse(event.data);
        if (!Array.isArray(rows)) return;
        setTasks(rows);
        setStatus("Latest task snapshot");
      } catch {
        setStatus("Invalid task event received");
      }
    };
    stream.onerror = () => {
      stream.close();
      setStatus(
        "Event stream ended or disconnected. Last received snapshot retained.",
      );
    };
    return () => stream.close();
  }, [runId, base]);
  return (
    <div>
      <p className="caption" role="status">
        {status}
      </p>
      <ul>
        {tasks.map((t) => (
          <li className="caption" key={t.task}>
            {t.task} · {t.state}
          </li>
        ))}
      </ul>
    </div>
  );
}
