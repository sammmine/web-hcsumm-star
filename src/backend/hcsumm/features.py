"""Behaviour feature extraction.

Source: ``hcsumm_star_NPD_final.ipynb`` cell 15
(``compute_node_depth``, ``build_compact_behavior_feature_epl``, ``normalize_f_l1``,
``select_behavior_features``).

Features per node: EPL, in-degree, out-degree, depth, PageRank (each normalized to [0,1]).
"""

from __future__ import annotations

from collections import deque

import networkx as nx
import numpy as np

from .config import FEATURE_INDEX, BehaviourFeature
from .paths import build_path_length_profile


def compute_node_depth(G: nx.DiGraph) -> dict[str, float]:
    """BFS depth from root nodes (in_degree == 0). Unreachable nodes keep ``inf``."""
    roots = [n for n, d in G.in_degree() if d == 0]
    depth: dict[str, float] = {v: float("inf") for v in G.nodes()}

    queue: deque[str] = deque()
    for r in roots:
        depth[r] = 0
        queue.append(r)

    while queue:
        u = queue.popleft()
        for v in G.successors(u):
            if depth[v] > depth[u] + 1:
                depth[v] = depth[u] + 1
                queue.append(v)

    return depth


def build_compact_behavior_feature_epl(
    G: nx.DiGraph, paths: list[list[str]]
) -> dict[str, np.ndarray]:
    """Return ``f_star[v] = [epl', indeg', outdeg', depth', pagerank']`` (all normalized).

    The notebook returns 11 values; the web pipeline only needs the normalized 5-dim
    ``f_star`` vector here (``L`` is obtained separately via ``build_path_length_profile``).
    """
    # 1. Path-length profile
    f_path, L = build_path_length_profile(G, paths)

    # 2. EPL (expected path length), normalized by L
    epl_norm: dict[str, float] = {}
    for v, vec in f_path.items():
        total = vec.sum()
        if total > 0 and L > 0:
            lengths = np.arange(1, L + 1)
            epl_norm[v] = (np.sum(lengths * vec) / total) / L
        else:
            epl_norm[v] = 0.0

    # 3. Degree
    indeg = dict(G.in_degree())
    outdeg = dict(G.out_degree())
    max_indeg = max(indeg.values()) if indeg else 0
    max_outdeg = max(outdeg.values()) if outdeg else 0
    max_indeg = max_indeg if max_indeg > 0 else 1
    max_outdeg = max_outdeg if max_outdeg > 0 else 1

    # 4. Depth
    depth = compute_node_depth(G)
    finite_depths = [d for d in depth.values() if d < float("inf")]
    max_depth = max(finite_depths) if finite_depths else 1
    depth_norm: dict[str, float] = {}
    for v in G.nodes():
        if depth[v] == float("inf"):
            depth_norm[v] = 1.0
        else:
            depth_norm[v] = depth[v] / max_depth if max_depth > 0 else 0.0

    # 5. PageRank
    pagerank = nx.pagerank(G, alpha=0.85) if G.number_of_nodes() else {}
    max_pr = max(pagerank.values()) if pagerank else 0
    max_pr = max_pr if max_pr > 0 else 1
    pagerank_norm = {v: pagerank.get(v, 0.0) / max_pr for v in G.nodes()}

    # 6. Final f*(v)
    f_star: dict[str, np.ndarray] = {}
    for v in G.nodes():
        f_star[v] = np.array([
            epl_norm[v],
            indeg[v] / max_indeg,
            outdeg[v] / max_outdeg,
            depth_norm[v],
            pagerank_norm[v],
        ])

    return f_star


def normalize_f_l1(f: dict[str, np.ndarray]) -> dict[str, np.ndarray]:
    """Per-node L1 normalization."""
    f_norm: dict[str, np.ndarray] = {}
    for v, vec in f.items():
        s = vec.sum()
        f_norm[v] = vec / s if s > 0 else vec.copy()
    return f_norm


def select_behavior_features(
    f_star: dict[str, np.ndarray],
    selected: tuple[BehaviourFeature, ...],
) -> dict[str, np.ndarray]:
    """Slice ``f_star`` to the selected feature dimensions (via ``config.FEATURE_INDEX``)."""
    idx = [FEATURE_INDEX[name] for name in selected]
    return {v: np.asarray(f_star[v])[idx] for v in f_star}
