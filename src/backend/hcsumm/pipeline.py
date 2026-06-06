"""Pipeline orchestrator.

``run_full_pipeline`` ties together every stage and returns the complete, stateless
ArtifactBundle (both call graphs, summary graphs, membership, all NPD metrics, per-stage
data, and Ward linkage matrices). Basis: ``run_full_pipeline`` (cell 63) +
``evaluate_npd_over_k`` (cell 79) from ``hcsumm_star_NPD_final.ipynb``.

This function is CPU-bound and is invoked inside a ProcessPoolExecutor by the API layer.
"""

from __future__ import annotations

from dataclasses import asdict
from typing import Any

from .config import EmbeddingMode, PipelineConfig


def _run_one_side(source: str, config: PipelineConfig) -> dict[str, Any]:
    """Run the per-graph half of the pipeline for a single .py source.

    Stages: call graph -> execution paths (guarded) -> behaviour features -> node2vec
    embedding -> fusion (per embedding_mode) -> Ward clustering -> summary graph.
    Returns the raw (pre-serialization) artifacts for one time point.
    """
    raise NotImplementedError("Compose callgraph/paths/features/embedding/fusion/clustering/summary")


def run_full_pipeline(
    source_t0: str,
    source_t1: str,
    config: PipelineConfig | None = None,
) -> dict[str, Any]:
    """Run the full t0 vs t1 pipeline and return the serializable ArtifactBundle.

    See ``doc/Desain Teknis Web HCSumm.md`` §4 for the bundle shape.
    """
    config = config or PipelineConfig()
    # 1. run each side (_run_one_side)
    # 2. align cluster indices across t0/t1 (cluster_indexing.align_cluster_indices)
    # 3. compute all NPD metrics (npd.compute_all_npd)
    # 4. serialize graphs (serialization.graph_to_cytoscape) and assemble bundle
    raise NotImplementedError("Assemble bundle per design doc §4")
