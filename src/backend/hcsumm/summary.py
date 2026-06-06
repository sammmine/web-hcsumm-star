"""Summary graph construction.

Source: ``hcsumm_star_NPD_final.ipynb`` cell 19 (``build_summary_graph``).

Collapses function nodes into cluster nodes ("C1", "C2", ...) and projects cross-cluster edges.
"""

from __future__ import annotations

import networkx as nx


def build_summary_graph(
    G: nx.DiGraph, clusters: dict[int, list[str]]
) -> tuple[nx.DiGraph, dict[str, str]]:
    """Return ``(summary_graph, node_to_cluster)``."""
    raise NotImplementedError("Lift from notebook cell 19")
