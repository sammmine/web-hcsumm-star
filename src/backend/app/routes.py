"""API routes: create run, poll status, fetch result."""

from __future__ import annotations

import ast

from fastapi import APIRouter, HTTPException, UploadFile

from hcsumm.config import PipelineConfig

from .jobs import job_manager
from .schemas import (
    ConfigModel,
    JobStatus,
    ResultResponse,
    RunCreated,
    RunRequest,
    StatusResponse,
)

router = APIRouter(prefix="/api")

MAX_SOURCE_BYTES = 2_000_000


def _validate_py(name: str, source: str) -> None:
    if len(source.encode("utf-8")) > MAX_SOURCE_BYTES:
        raise HTTPException(413, f"{name} exceeds size limit")
    try:
        ast.parse(source)
    except SyntaxError as exc:
        raise HTTPException(422, f"{name} is not valid Python: {exc}") from exc


def _to_pipeline_config(cfg: ConfigModel) -> PipelineConfig:
    return PipelineConfig(
        embedding_mode=cfg.embedding_mode,
        behaviour_features=tuple(cfg.behaviour_features),
        k_clusters=cfg.k_clusters,
        embed_dim=cfg.embed_dim,
        walk_length=cfg.walk_length,
        num_walks=cfg.num_walks,
        p_return=cfg.p_return,
        q_inout=cfg.q_inout,
        seed=cfg.seed,
        window=cfg.window,
        epochs=cfg.epochs,
        alpha=cfg.alpha,
        beta=cfg.beta,
        max_paths=cfg.max_paths,
        path_cutoff=cfg.path_cutoff,
    )


@router.post("/runs", response_model=RunCreated)
async def create_run(req: RunRequest) -> RunCreated:
    """JSON entry point: inline source for t0 and t1."""
    _validate_py("source_t0", req.source_t0)
    _validate_py("source_t1", req.source_t1)
    job_id = job_manager.submit(req.source_t0, req.source_t1, _to_pipeline_config(req.config))
    return RunCreated(job_id=job_id)


@router.post("/runs/upload", response_model=RunCreated)
async def create_run_upload(file_t0: UploadFile, file_t1: UploadFile) -> RunCreated:
    """Multipart entry point: upload two .py files (uses default config)."""
    for f in (file_t0, file_t1):
        if not (f.filename or "").endswith(".py"):
            raise HTTPException(422, f"{f.filename!r} is not a .py file")
    source_t0 = (await file_t0.read()).decode("utf-8", errors="replace")
    source_t1 = (await file_t1.read()).decode("utf-8", errors="replace")
    _validate_py("file_t0", source_t0)
    _validate_py("file_t1", source_t1)
    job_id = job_manager.submit(source_t0, source_t1, _to_pipeline_config(ConfigModel()))
    return RunCreated(job_id=job_id)


@router.get("/runs/{job_id}", response_model=StatusResponse)
async def get_status(job_id: str) -> StatusResponse:
    job = job_manager.get(job_id)
    if job is None:
        raise HTTPException(404, "job not found (may have expired)")
    return StatusResponse(job_id=job.job_id, status=job.status, error=job.error)


@router.get("/runs/{job_id}/result", response_model=ResultResponse)
async def get_result(job_id: str) -> ResultResponse:
    job = job_manager.get(job_id)
    if job is None:
        raise HTTPException(404, "job not found (may have expired)")
    if job.status != JobStatus.DONE:
        raise HTTPException(409, f"job not done (status={job.status.value})")
    return ResultResponse(job_id=job.job_id, status=job.status, bundle=job.bundle)
