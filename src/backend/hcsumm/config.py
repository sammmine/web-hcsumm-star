"""Pipeline configuration: all tunable parameters with defaults.

Mirrors the parameter block in ``hcsumm_star_NPD_final.ipynb`` (cell 5) plus the
embedding-mode selection and behaviour-feature toggles from the spec.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class EmbeddingMode(str, Enum):
    NODE2VEC_ONLY = "node2vec_only"   # x = e'(v)
    BEHAVIOUR_ONLY = "behaviour_only"  # x = f'(v)
    FUSED = "fused"                    # x = fuse(e'(v), f'(v), alpha, beta)


class BehaviourFeature(str, Enum):
    EPL = "EPL"
    INDEG = "indeg"
    OUTDEG = "outdeg"
    DEPTH = "depth"
    PAGERANK = "pagerank"


# Order used to build the behaviour feature vector (see select_behavior_features).
FEATURE_INDEX: dict[BehaviourFeature, int] = {
    BehaviourFeature.EPL: 0,
    BehaviourFeature.INDEG: 1,
    BehaviourFeature.OUTDEG: 2,
    BehaviourFeature.DEPTH: 3,
    BehaviourFeature.PAGERANK: 4,
}

DEFAULT_FEATURES: tuple[BehaviourFeature, ...] = (
    BehaviourFeature.EPL,
    BehaviourFeature.INDEG,
    BehaviourFeature.OUTDEG,
    BehaviourFeature.DEPTH,
)


@dataclass(frozen=True)
class PipelineConfig:
    # --- simple controls ---
    embedding_mode: EmbeddingMode = EmbeddingMode.FUSED
    behaviour_features: tuple[BehaviourFeature, ...] = DEFAULT_FEATURES
    k_clusters: int = 2

    # --- node2vec (Advanced / OFAT panel) ---
    embed_dim: int = 4
    walk_length: int = 10
    num_walks: int = 200
    p_return: float = 1.0
    q_inout: float = 1.0
    seed: int = 42
    window: int = 5
    epochs: int = 100

    # --- fusion (Advanced) ---
    alpha: float = 1.0
    beta: float = 1.0

    # --- safety guards for large/cyclic graphs ---
    max_paths: int = 50_000          # cap total enumerated execution paths
    path_cutoff: int | None = None    # max edges per simple path (None = unbounded)

    def __post_init__(self) -> None:
        if self.k_clusters < 1:
            raise ValueError("k_clusters must be >= 1")
        if self.embedding_mode != EmbeddingMode.NODE2VEC_ONLY and not self.behaviour_features:
            raise ValueError("behaviour_features must be non-empty unless mode is node2vec_only")
