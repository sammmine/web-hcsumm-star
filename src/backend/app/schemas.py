"""Pydantic request/response models for the API."""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field

from hcsumm.config import BehaviourFeature, EmbeddingMode


class ConfigModel(BaseModel):
    """Mirror of hcsumm.config.PipelineConfig for JSON I/O."""

    embedding_mode: EmbeddingMode = EmbeddingMode.FUSED
    behaviour_features: list[BehaviourFeature] = Field(
        default_factory=lambda: [
            BehaviourFeature.EPL,
            BehaviourFeature.INDEG,
            BehaviourFeature.OUTDEG,
            BehaviourFeature.DEPTH,
        ]
    )
    k_clusters: int = Field(default=2, ge=1)

    embed_dim: int = Field(default=4, ge=1)
    walk_length: int = Field(default=10, ge=1)
    num_walks: int = Field(default=200, ge=1)
    p_return: float = 1.0
    q_inout: float = 1.0
    seed: int = 42
    window: int = 5
    epochs: int = 100

    alpha: float = 1.0
    beta: float = 1.0

    max_paths: int = 50_000
    path_cutoff: int | None = None


class RunRequest(BaseModel):
    """JSON variant of POST /api/runs (source code inline)."""

    source_t0: str
    source_t1: str
    config: ConfigModel = Field(default_factory=ConfigModel)


class RunCreated(BaseModel):
    job_id: str


class JobStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    DONE = "done"
    ERROR = "error"


class StatusResponse(BaseModel):
    job_id: str
    status: JobStatus
    error: str | None = None


class ResultResponse(BaseModel):
    job_id: str
    status: JobStatus
    bundle: dict[str, Any] | None = None
