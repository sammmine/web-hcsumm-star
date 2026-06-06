"""Behaviour feature extraction.

Source: ``hcsumm_star_NPD_final.ipynb`` cell 15
(``compute_node_depth``, ``build_compact_behavior_feature_epl``, ``normalize_f_l1``,
``select_behavior_features``).

Features per node: EPL, in-degree, out-degree, depth, PageRank (each normalized to [0,1]).
"""

from __future__ import annotations

import networkx as nx
import numpy as np

from .config import BehaviourFeature


def compute_node_depth(G: nx.DiGraph) -> dict[str, int]:
    """BFS depth from root nodes (in_degree == 0)."""
    raise NotImplementedError("Lift from notebook cell 15")


def build_compact_behavior_feature_epl(
    G: nx.DiGraph, paths: list[list[str]]
) -> dict[str, np.ndarray]:
    """Return ``f_star[v] = [epl', indeg', outdeg', depth', pagerank']`` (all normalized).

    The notebook returns 11 values; for the web pipeline we only need ``f_star`` (and ``L``
    via :func:`paths.build_path_length_profile`). Keep the normalized 5-dim vector.
    """
    raise NotImplementedError("Lift from notebook cell 15")


def normalize_f_l1(f: dict[str, np.ndarray]) -> dict[str, np.ndarray]:
    """Per-node L1 normalization."""
    raise NotImplementedError("Lift from notebook cell 15")


def select_behavior_features(
    f_star: dict[str, np.ndarray],
    selected: tuple[BehaviourFeature, ...],
) -> dict[str, np.ndarray]:
    """Slice ``f_star`` to the selected feature dimensions (via ``config.FEATURE_INDEX``)."""
    raise NotImplementedError("Lift from notebook cell 15 (use FEATURE_INDEX mapping)")
