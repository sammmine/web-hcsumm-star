"""Pipeline orchestrator.

``run_full_pipeline`` ties together every stage and returns the complete, stateless
ArtifactBundle (both call graphs, summary graphs, membership, all NPD metrics, per-stage
data, and Ward linkage matrices). Basis: ``run_full_pipeline`` (cell 63) +
``evaluate_npd_over_k`` (cell 79) from ``hcsumm_star_NPD_final.ipynb``.

Design note: the notebook's canonical cell-63 pipeline fuses node2vec with the raw
path-length-profile distribution. This web pipeline instead fuses node2vec with the
*selectable* compact behaviour features (EPL / indeg / outdeg / depth / pagerank), which is
what the parameter form exposes. ``embedding_mode`` decides what goes into the cluster vector:

    node2vec_only  -> x = e'(v)
    behaviour_only -> x = f'(v)            (L1-normalized selected behaviour features)
    fused          -> x = [alpha*e'(v), beta*f'(v)]

This function is CPU-bound and is invoked inside a ProcessPoolExecutor by the API layer.
"""

from __future__ import annotations

from typing import Any

import numpy as np

from .callgraph import extract_call_graph_from_py
from .cluster_indexing import align_cluster_indices
from .clustering import ward_clustering
from .config import EmbeddingMode, PipelineConfig
from .embedding import compute_directed_node2vec_embedding, normalize_e_l2
from .features import (
    build_compact_behavior_feature_epl,
    normalize_f_l1,
    select_behavior_features,
)
from .fusion import compute_distance_matrix, fuse_features
from .npd import compute_all_npd
from .paths import extract_execution_paths
from .serialization import graph_to_cytoscape, vectors_to_dict
from .summary import build_summary_graph

# Display order of the compact behaviour feature vector (see build_compact_behavior_feature_epl).
FEATURE_NAMES = ("epl", "indeg", "outdeg", "depth", "pagerank")


def _config_to_dict(config: PipelineConfig) -> dict[str, Any]:
    """JSON-friendly echo of the config (enums -> str, tuple -> list)."""
    return {
        "embedding_mode": config.embedding_mode.value,
        "behaviour_features": [f.value for f in config.behaviour_features],
        "k_clusters": config.k_clusters,
        "embed_dim": config.embed_dim,
        "walk_length": config.walk_length,
        "num_walks": config.num_walks,
        "p_return": config.p_return,
        "q_inout": config.q_inout,
        "seed": config.seed,
        "window": config.window,
        "epochs": config.epochs,
        "alpha": config.alpha,
        "beta": config.beta,
        "max_paths": config.max_paths,
        "path_cutoff": config.path_cutoff,
    }


def _run_one_side(source: str, config: PipelineConfig) -> dict[str, Any]:
    """Run the per-graph half of the pipeline for a single .py source.

    Returns the raw (pre-serialization) artifacts for one time point.
    """
    mode = config.embedding_mode

    G = extract_call_graph_from_py(source)
    paths, capped = extract_execution_paths(
        G, max_paths=config.max_paths, cutoff=config.path_cutoff
    )

    # Always compute the full behaviour vector for display (cheap, no gensim).
    f_star = build_compact_behavior_feature_epl(G, paths)

    # Behaviour component of the cluster vector (selected + L1-normalized).
    if mode != EmbeddingMode.NODE2VEC_ONLY:
        f_sel = select_behavior_features(f_star, config.behaviour_features)
        f_norm = normalize_f_l1(f_sel)
    else:
        f_norm = {}

    # Embedding component (the expensive node2vec step).
    if mode != EmbeddingMode.BEHAVIOUR_ONLY:
        e = compute_directed_node2vec_embedding(
            G,
            dimensions=config.embed_dim,
            walk_length=config.walk_length,
            num_walks=config.num_walks,
            p=config.p_return,
            q=config.q_inout,
            seed=config.seed,
            window=config.window,
            epochs=config.epochs,
        )
        e_norm = normalize_e_l2(e)
    else:
        e_norm = {}

    # Assemble the cluster vector x(v) per embedding mode.
    if mode == EmbeddingMode.NODE2VEC_ONLY:
        x = {n: np.asarray(e_norm[n], dtype=float) for n in G.nodes()}
    elif mode == EmbeddingMode.BEHAVIOUR_ONLY:
        x = {n: np.asarray(f_norm[n], dtype=float) for n in G.nodes()}
    else:
        x = fuse_features(e_norm, f_norm, config.alpha, config.beta)

    dist_nodes, dist = compute_distance_matrix(x)
    clusters, Z = ward_clustering(x, k=config.k_clusters)
    summary, node_to_cluster = build_summary_graph(G, clusters)

    return {
        "G": G,
        "paths": paths,
        "capped": capped,
        "f_star": f_star,
        "e_norm": e_norm,
        "x": x,
        "dist_nodes": dist_nodes,
        "dist": dist,
        "clusters": clusters,
        "Z": Z,
        "summary": summary,
        "node_to_cluster": node_to_cluster,
    }


def _serialize_side(side: dict[str, Any], node_to_cluster: dict[str, int]) -> dict[str, Any]:
    """Build the JSON SideBundle from one side's raw artifacts + (possibly aligned) membership."""
    G = side["G"]
    f_star = side["f_star"]

    membership = {n: f"C{cid}" for n, cid in node_to_cluster.items()}

    # Per-node behaviour attributes for call-graph hover/inspection.
    node_attrs = {
        n: {name: float(f_star[n][i]) for i, name in enumerate(FEATURE_NAMES)}
        for n in G.nodes()
    }

    # Summary-node attributes: member list + size + its own cluster id (for coloring).
    summary_attrs: dict[str, dict] = {}
    cluster_members: dict[int, list[str]] = {}
    for n, cid in node_to_cluster.items():
        cluster_members.setdefault(cid, []).append(n)
    for cid, members in cluster_members.items():
        summary_attrs[f"C{cid}"] = {
            "cluster": f"C{cid}",
            "size": len(members),
            "members": sorted(members),
        }

    Z = side["Z"]
    return {
        "callgraph": graph_to_cytoscape(G, node_attrs=node_attrs, membership=membership),
        "summary": graph_to_cytoscape(side["summary"], node_attrs=summary_attrs),
        "membership": membership,
        "linkage": Z.tolist() if Z is not None else [],
        "stages": {
            "features": vectors_to_dict({n: f_star[n] for n in G.nodes()}),
            "embedding": vectors_to_dict(side["e_norm"]),
            "fusion": vectors_to_dict(side["x"]),
            "distance_matrix": [[float(v) for v in row] for row in side["dist"]],
        },
    }


def run_full_pipeline(
    source_t0: str,
    source_t1: str,
    config: PipelineConfig | None = None,
) -> dict[str, Any]:
    """Run the full t0 vs t1 pipeline and return the serializable ArtifactBundle.

    See ``doc/Desain Teknis Web HCSumm.md`` §4 for the bundle shape.
    """
    config = config or PipelineConfig()

    # 1. Run each side.
    s0 = _run_one_side(source_t0, config)
    s1 = _run_one_side(source_t1, config)

    n2c0 = s0["node_to_cluster"]
    n2c1 = s1["node_to_cluster"]

    # 2. Align t1 cluster indices to t0 (Jaccard) so colors are consistent side-by-side.
    remap = align_cluster_indices(n2c0, n2c1)
    n2c1_aligned = {n: remap.get(cid, cid) for n, cid in n2c1.items()}
    clusters1_aligned: dict[int, list[str]] = {}
    for n, cid in n2c1_aligned.items():
        clusters1_aligned.setdefault(cid, []).append(n)
    s1["summary"], _ = build_summary_graph(s1["G"], clusters1_aligned)

    # 3. NPD metrics (relabeling-invariant; use the aligned memberships).
    npd = compute_all_npd(
        s0["G"], s1["G"], s0["summary"], s1["summary"],
        s0["paths"], s1["paths"], n2c0, n2c1_aligned,
    )

    # 4. Serialize + assemble bundle.
    warnings: list[str] = []
    if s0["capped"]:
        warnings.append(
            f"t0 execution-path enumeration capped at max_paths={config.max_paths}; "
            "EPL/NPD are computed on a truncated path set."
        )
    if s1["capped"]:
        warnings.append(
            f"t1 execution-path enumeration capped at max_paths={config.max_paths}; "
            "EPL/NPD are computed on a truncated path set."
        )

    return {
        "config": _config_to_dict(config),
        "t0": _serialize_side(s0, n2c0),
        "t1": _serialize_side(s1, n2c1_aligned),
        "npd": npd,
        "warnings": warnings,
    }
