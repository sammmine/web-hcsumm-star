"""In-memory job store + ProcessPoolExecutor runner.

Stateless by design: results live only in memory and are evicted after ``RESULT_TTL``.
The pipeline is CPU-bound (gensim/node2vec) so it runs in a separate process to keep the
FastAPI event loop responsive.
"""

from __future__ import annotations

import time
import uuid
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass, field
from typing import Any

from hcsumm.config import PipelineConfig
from hcsumm.pipeline import run_full_pipeline

from .schemas import JobStatus

RESULT_TTL = 60 * 30  # seconds


@dataclass
class Job:
    job_id: str
    status: JobStatus = JobStatus.PENDING
    bundle: dict[str, Any] | None = None
    error: str | None = None
    created_at: float = field(default_factory=time.monotonic)


# Module-level worker so it is picklable for ProcessPoolExecutor.
def _worker(source_t0: str, source_t1: str, config: PipelineConfig) -> dict[str, Any]:
    return run_full_pipeline(source_t0, source_t1, config)


class JobManager:
    def __init__(self, max_workers: int = 2) -> None:
        self._jobs: dict[str, Job] = {}
        self._executor = ProcessPoolExecutor(max_workers=max_workers)

    def submit(self, source_t0: str, source_t1: str, config: PipelineConfig) -> str:
        self._sweep()
        job_id = uuid.uuid4().hex
        job = Job(job_id=job_id, status=JobStatus.RUNNING)
        self._jobs[job_id] = job
        future = self._executor.submit(_worker, source_t0, source_t1, config)

        def _done(fut, jid=job_id) -> None:
            j = self._jobs.get(jid)
            if j is None:
                return
            try:
                j.bundle = fut.result()
                j.status = JobStatus.DONE
            except Exception as exc:  # noqa: BLE001 - surface any pipeline failure to client
                j.error = f"{type(exc).__name__}: {exc}"
                j.status = JobStatus.ERROR

        future.add_done_callback(_done)
        return job_id

    def get(self, job_id: str) -> Job | None:
        return self._jobs.get(job_id)

    def _sweep(self) -> None:
        now = time.monotonic()
        stale = [k for k, j in self._jobs.items() if now - j.created_at > RESULT_TTL]
        for k in stale:
            self._jobs.pop(k, None)

    def shutdown(self) -> None:
        self._executor.shutdown(wait=False, cancel_futures=True)


job_manager = JobManager()
