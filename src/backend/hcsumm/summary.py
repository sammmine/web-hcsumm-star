"""Summary graph construction.

Source: ``hcsumm_star_NPD_final.ipynb`` cell 19 (``build_summary_graph``).

Collapses function nodes into cluster nodes ("C1", "C2", ...) and projects cross-cluster edges.
"""

from __future__ import annotations

import networkx as nx


def build_summary_graph(
    G: nx.DiGraph, clusters: dict[int, list[str]]
) -> tuple[nx.DiGraph, dict[str, int]]:
    """Return ``(summary_graph, node_to_cluster)``.

    ``node_to_cluster`` maps each function node to its integer cluster id; the summary graph
    has one node ``"C{cid}"`` per cluster and an edge for every cross-cluster call.
    """
    node_to_cluster: dict[str, int] = {}
    for cid, members in clusters.items():
        for n in members:
            node_to_cluster[n] = cid

    S = nx.DiGraph()
    for cid in clusters:
        S.add_node(f"C{cid}")

    for u, v in G.edges():
        cu = node_to_cluster.get(u)
        cv = node_to_cluster.get(v)
        if cu is not None and cv is not None and cu != cv:
            S.add_edge(f"C{cu}", f"C{cv}")

    return S, node_to_cluster
