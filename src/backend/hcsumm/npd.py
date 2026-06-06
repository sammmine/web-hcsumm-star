"""Network Portrait Divergence metrics.

Source: ``hcsumm_star_NPD_final.ipynb`` cells 68-79
(``compute_jsd``, ``align_distributions``, ``compute_network_portrait_npd``,
``compute_original_npd``, ``compute_execution_path_portrait_npd``, ``compute_ep_npd``,
``compute_cluster_ep_npd``, ``compute_dual_length_cluster_ep_portrait``).

All six metric variants are computed in one run (see :func:`compute_all_npd`).
"""

from __future__ import annotations

import networkx as nx
import numpy as np


def compute_jsd(P: np.ndarray, Q: np.ndarray) -> float:
    """Jensen-Shannon divergence (sqrt form)."""
    raise NotImplementedError("Lift from notebook cell 68")


def align_distributions(
    p1: dict, p2: dict
) -> tuple[np.ndarray, np.ndarray, list]:
    raise NotImplementedError("Lift from notebook cell 68")


def compute_original_npd(G1: nx.DiGraph, G2: nx.DiGraph) -> float:
    """Shortest-path-neighbourhood portrait divergence."""
    raise NotImplementedError("Lift from notebook cells 68-74")


def compute_ep_npd(G1: nx.DiGraph, G2: nx.DiGraph) -> float:
    """Execution-path portrait divergence (function level, before clustering)."""
    raise NotImplementedError("Lift from notebook cells 68-74")


def compute_cluster_ep_npd(
    paths1: list[list[str]],
    paths2: list[list[str]],
    node_to_cluster_1: dict[str, str],
    node_to_cluster_2: dict[str, str],
    compressed: bool = True,
) -> float:
    """Cluster-projected execution-path divergence (compressed/uncompressed)."""
    raise NotImplementedError("Lift from notebook cells 68-74")


def compute_dual_length_cluster_ep_npd(
    paths1: list[list[str]],
    paths2: list[list[str]],
    node_to_cluster_1: dict[str, str],
    node_to_cluster_2: dict[str, str],
) -> float:
    """Dual-length portrait P(lo, lc, k) divergence."""
    raise NotImplementedError("Lift from notebook cell 74")


def compute_all_npd(*args, **kwargs) -> list[dict]:
    """Compute all six NPD variants and return rows ``{metric, when, value}``.

    Orchestrate the calls above; basis = ``evaluate_npd_over_k`` (cell 79) restricted to the
    chosen k. Returns the table consumed by the frontend NPD view.
    """
    raise NotImplementedError("Orchestrate the six NPD variants (basis: cell 79)")
