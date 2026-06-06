import type { ArtifactBundle, JobStatus, PipelineConfig } from "../types";

const BASE = "/api";

export async function createRun(
  source_t0: string,
  source_t1: string,
  config: PipelineConfig,
): Promise<string> {
  const res = await fetch(`${BASE}/runs`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ source_t0, source_t1, config }),
  });
  if (!res.ok) throw new Error(`createRun failed: ${res.status} ${await res.text()}`);
  const data = (await res.json()) as { job_id: string };
  return data.job_id;
}

export async function getStatus(
  jobId: string,
): Promise<{ status: JobStatus; error: string | null }> {
  const res = await fetch(`${BASE}/runs/${jobId}`);
  if (!res.ok) throw new Error(`getStatus failed: ${res.status}`);
  return (await res.json()) as { status: JobStatus; error: string | null };
}

export async function getResult(jobId: string): Promise<ArtifactBundle> {
  const res = await fetch(`${BASE}/runs/${jobId}/result`);
  if (!res.ok) throw new Error(`getResult failed: ${res.status}`);
  const data = (await res.json()) as { bundle: ArtifactBundle };
  return data.bundle;
}

/** Poll a job until done/error. */
export async function pollRun(
  jobId: string,
  { intervalMs = 1000, onStatus }: { intervalMs?: number; onStatus?: (s: JobStatus) => void } = {},
): Promise<ArtifactBundle> {
  for (;;) {
    const { status, error } = await getStatus(jobId);
    onStatus?.(status);
    if (status === "done") return getResult(jobId);
    if (status === "error") throw new Error(error ?? "pipeline error");
    await new Promise((r) => setTimeout(r, intervalMs));
  }
}
