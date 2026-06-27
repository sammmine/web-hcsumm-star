"""Ward clustering and per-iteration reconstruction.

Source: ``hcsumm_star_NPD_final.ipynb`` cell 19 (``ward_clustering``).

``ward_iteration_steps`` is NEW: the notebook does not emit intermediate Ward states. We
reconstruct each merge from the scipy linkage matrix Z so the (deferred) Cluster Iteration
Visualization can replay the agglomeration without backend changes later.
"""

from __future__ import annotations

import numpy as np
from scipy.cluster.hierarchy import fcluster, linkage


def ward_clustering(
    x: dict[str, np.ndarray], k: int = 2
) -> tuple[dict[int, list[str]], np.ndarray | None]:
    """Ward linkage + fcluster to k clusters.

    Returns ``(clusters, Z)`` where ``clusters = {cluster_id: [nodes]}`` and ``Z`` is the
    scipy linkage matrix (``None`` when there are 0 or 1 nodes).
    """
    nodes = sorted(x.keys())
    X = np.array([x[n] for n in nodes])

    if len(nodes) == 0:
        return {}, None

    if not np.isfinite(X).all():
        raise ValueError("Feature matrix contains NaN or inf.")

    if len(nodes) == 1:
        return {1: [nodes[0]]}, None

    k = min(k, len(nodes))
    Z = linkage(X, method="ward")
    labels = fcluster(Z, k, criterion="maxclust")

    clusters: dict[int, list[str]] = {}
    for i, n in enumerate(nodes):
        clusters.setdefault(int(labels[i]), []).append(n)

    return clusters, Z


def ward_iteration_steps(Z: np.ndarray | None, nodes: list[str]) -> list[dict]:
    """Reconstruct cluster membership after each merge in the linkage matrix.

    Returns a list of steps (init + one per merge), each like::

        {"step": int, "merged": [a, b], "distance": float, "clusters": {cid: [nodes]}}

    Cluster ids follow scipy's convention: leaves are ``0..n-1`` (mapped to ``nodes``),
    each merge creates a new id ``n, n+1, ...``. Used by the deferred Cluster Iteration view.
    """
    n = len(nodes)
    if n == 0:
        return []

    members: dict[int, list[str]] = {i: [nodes[i]] for i in range(n)}
    steps: list[dict] = [
        {
            "step": 0,
            "merged": [],
            "distance": 0.0,
            "clusters": {cid: list(m) for cid, m in members.items()},
        }
    ]

    if Z is None:
        return steps

    next_id = n
    for s, row in enumerate(Z, start=1):
        a, b = int(row[0]), int(row[1])
        dist = float(row[2])
        merged_a = list(members[a])
        merged_b = list(members[b])
        members[next_id] = members.pop(a) + members.pop(b)
        steps.append(
            {
                "step": s,
                "merged": [a, b],
                "merged_names": [merged_a, merged_b],
                "distance": dist,
                "clusters": {cid: list(m) for cid, m in members.items()},
            }
        )
        next_id += 1

    return steps
