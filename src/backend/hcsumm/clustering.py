"""Ward clustering and per-iteration reconstruction.

Source: ``hcsumm_star_NPD_final.ipynb`` cell 19 (``ward_clustering``).

``ward_iteration_steps`` is NEW: the notebook does not emit intermediate Ward states. We
reconstruct each merge from the scipy linkage matrix Z so the (deferred) Cluster Iteration
Visualization can replay the agglomeration without backend changes later.
"""

from __future__ import annotations

import numpy as np


def ward_clustering(
    x: dict[str, np.ndarray], k: int = 2
) -> tuple[dict[int, list[str]], np.ndarray]:
    """Ward linkage + fcluster to k clusters.

    Returns ``(clusters, Z)`` where ``clusters = {cluster_id: [nodes]}`` and ``Z`` is the
    scipy linkage matrix.
    """
    raise NotImplementedError("Lift from notebook cell 19")


def ward_iteration_steps(Z: np.ndarray, nodes: list[str]) -> list[dict]:
    """Reconstruct cluster membership after each merge in the linkage matrix.

    Returns a list of steps (init + one per merge), each like::

        {"step": int, "merged": [a, b], "distance": float, "clusters": {cid: [nodes]}}

    Used by the deferred Cluster Iteration Visualization.
    """
    raise NotImplementedError("NEW — derive from scipy linkage matrix Z")
