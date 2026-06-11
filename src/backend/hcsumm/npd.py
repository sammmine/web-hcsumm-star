"""Network Portrait Divergence metrics.

Source: ``hcsumm_star_NPD_final.ipynb`` cells 68-79
(``compute_jsd``, ``align_distributions``, ``compute_network_portrait_npd``,
``compute_original_npd``, ``compute_execution_path_portrait_npd``, ``compute_ep_npd``,
``compute_cluster_ep_npd``, ``compute_dual_length_cluster_ep_portrait``).

All six metric variants are computed in one run (see :func:`compute_all_npd`, basis cell 79).
"""

from __future__ import annotations

from collections import Counter, defaultdict

import networkx as nx
import numpy as np

from .paths import extract_execution_paths, get_exit_nodes


# ============================================================
# Jensen-Shannon divergence
# ============================================================

def align_distributions(p1: dict, p2: dict) -> tuple[np.ndarray, np.ndarray, list]:
    keys = sorted(set(p1) | set(p2))
    P = np.array([p1.get(k, 0.0) for k in keys])
    Q = np.array([p2.get(k, 0.0) for k in keys])
    return P, Q, keys


def compute_jsd(P: np.ndarray, Q: np.ndarray) -> float:
    P = np.asarray(P, dtype=float)
    Q = np.asarray(Q, dtype=float)

    if P.sum() == 0 and Q.sum() == 0:
        return 0.0
    if P.sum() > 0:
        P = P / P.sum()
    if Q.sum() > 0:
        Q = Q / Q.sum()

    M = 0.5 * (P + Q)

    def kl_div(A: np.ndarray, B: np.ndarray) -> float:
        mask = A > 0
        return float(np.sum(A[mask] * np.log2(A[mask] / B[mask])))

    return 0.5 * kl_div(P, M) + 0.5 * kl_div(Q, M)


# ============================================================
# 1. Original NPD: neighbourhood portrait
# ============================================================

def compute_network_portrait_npd(G: nx.DiGraph) -> dict:
    """Neighbourhood portrait ``{(l, k): probability}`` (l = shortest-path distance)."""
    portrait: dict[int, dict[int, int]] = defaultdict(lambda: defaultdict(int))

    for node in G.nodes:
        lengths = nx.single_source_shortest_path_length(G, node)
        count_by_distance: dict[int, int] = defaultdict(int)
        for target, dist in lengths.items():
            if target != node:
                count_by_distance[dist] += 1
        for l, k in count_by_distance.items():
            portrait[l][k] += 1

    flat: dict[tuple[int, int], int] = defaultdict(int)
    total = 0
    for l in portrait:
        for k in portrait[l]:
            flat[(l, k)] += portrait[l][k]
            total += portrait[l][k]

    if total == 0:
        return {}
    return {key: val / total for key, val in flat.items()}


def compute_original_npd(G1: nx.DiGraph, G2: nx.DiGraph) -> float:
    """Shortest-path-neighbourhood portrait divergence."""
    P, Q, _ = align_distributions(
        compute_network_portrait_npd(G1), compute_network_portrait_npd(G2)
    )
    return compute_jsd(P, Q)


# ============================================================
# 2. EP-NPD before clustering (function-level execution paths)
# ============================================================

def compute_execution_path_portrait_from_paths(
    paths: list[list[str]], graph_nodes: list[str]
) -> dict:
    """Portrait ``P(l, k)``: number of nodes with k outgoing paths of length l."""
    graph_nodes = sorted(graph_nodes)
    valid_paths = [p for p in paths if len(p) > 1]
    if not valid_paths:
        return {}

    L = max(len(p) - 1 for p in valid_paths)
    if L == 0:
        return {}

    node_length_counts = {v: Counter() for v in graph_nodes}
    for p in valid_paths:
        start_node = p[0]
        l = len(p) - 1
        if start_node in node_length_counts:
            node_length_counts[start_node][l] += 1

    portrait_counts: Counter = Counter()
    for l in range(1, L + 1):
        for v in graph_nodes:
            portrait_counts[(l, node_length_counts[v].get(l, 0))] += 1

    total = sum(portrait_counts.values())
    if total == 0:
        return {}
    return {key: count / total for key, count in sorted(portrait_counts.items())}


def compute_ep_npd_from_paths(
    paths_1: list[list[str]],
    paths_2: list[list[str]],
    graph_nodes_1: list[str],
    graph_nodes_2: list[str],
) -> float:
    """EP-NPD before clustering, using already-validated execution paths."""
    P, Q, _ = align_distributions(
        compute_execution_path_portrait_from_paths(paths_1, graph_nodes_1),
        compute_execution_path_portrait_from_paths(paths_2, graph_nodes_2),
    )
    return compute_jsd(P, Q)


def compute_ep_npd(G1: nx.DiGraph, G2: nx.DiGraph) -> float:
    """Execution-path portrait divergence (function level, before clustering).

    Convenience wrapper that enumerates paths from each graph; for pipeline use prefer
    :func:`compute_ep_npd_from_paths` with the already-validated path lists.
    """
    paths_1, _ = extract_execution_paths(G1)
    paths_2, _ = extract_execution_paths(G2)
    return compute_ep_npd_from_paths(
        paths_1, paths_2, list(G1.nodes()), list(G2.nodes())
    )


# ============================================================
# 3. Cluster-EP-NPD after clustering (compressed / uncompressed)
# ============================================================

def compress_consecutive_duplicates(seq: list) -> list:
    """``[C1, C2, C2, C3] -> [C1, C2, C3]``."""
    if not seq:
        return []
    compressed = [seq[0]]
    for item in seq[1:]:
        if item != compressed[-1]:
            compressed.append(item)
    return compressed


def _cluster_ep_portrait_from_paths(
    paths: list[list[str]],
    graph_nodes: list[str],
    node_to_cluster: dict[str, int],
    compressed: bool,
) -> dict:
    """Portrait ``P(lc, k)`` of cluster-projected execution-path lengths."""
    graph_nodes = sorted(graph_nodes)
    node_cluster_length_counts = {v: Counter() for v in graph_nodes}
    max_lc = 0
    any_projected = False

    for p in paths:
        if len(p) <= 1:
            continue
        start_node = p[0]
        projected = [node_to_cluster[v] for v in p if v in node_to_cluster]
        if compressed:
            projected = compress_consecutive_duplicates(projected)
        if len(projected) == 0:
            continue
        lc = len(projected) - 1
        max_lc = max(max_lc, lc)
        any_projected = True
        if start_node in node_cluster_length_counts:
            node_cluster_length_counts[start_node][lc] += 1

    if not any_projected:
        return {}

    portrait_counts: Counter = Counter()
    min_lc = 0 if compressed else 1
    for lc in range(min_lc, max_lc + 1):
        for v in graph_nodes:
            portrait_counts[(lc, node_cluster_length_counts[v].get(lc, 0))] += 1

    total = sum(portrait_counts.values())
    if total == 0:
        return {}
    return {key: count / total for key, count in sorted(portrait_counts.items())}


def compute_cluster_ep_npd(
    paths1: list[list[str]],
    paths2: list[list[str]],
    node_to_cluster_1: dict[str, int],
    node_to_cluster_2: dict[str, int],
    compressed: bool = True,
    graph_nodes_1: list[str] | None = None,
    graph_nodes_2: list[str] | None = None,
) -> float:
    """Cluster-projected execution-path divergence (compressed/uncompressed)."""
    gn1 = graph_nodes_1 if graph_nodes_1 is not None else list(node_to_cluster_1.keys())
    gn2 = graph_nodes_2 if graph_nodes_2 is not None else list(node_to_cluster_2.keys())
    P, Q, _ = align_distributions(
        _cluster_ep_portrait_from_paths(paths1, gn1, node_to_cluster_1, compressed),
        _cluster_ep_portrait_from_paths(paths2, gn2, node_to_cluster_2, compressed),
    )
    return compute_jsd(P, Q)


# ============================================================
# 4. Dual-Length Cluster-EP-NPD: P(lo, lc, k)
# ============================================================

def _dual_length_portrait(
    paths: list[list[str]],
    node_to_cluster: dict[str, int],
    graph_nodes: list[str],
) -> dict:
    graph_nodes = sorted(graph_nodes)
    node_pair_counts = {v: Counter() for v in graph_nodes}
    observed_pairs: set[tuple[int, int]] = set()

    for p in paths:
        if len(p) <= 1:
            continue
        start_node = p[0]
        lo = len(p) - 1
        cluster_path = [node_to_cluster[v] for v in p if v in node_to_cluster]
        if len(cluster_path) != len(p):
            continue
        lc = len(compress_consecutive_duplicates(cluster_path)) - 1
        pair = (lo, lc)
        observed_pairs.add(pair)
        if start_node in node_pair_counts:
            node_pair_counts[start_node][pair] += 1

    if not observed_pairs:
        return {}

    portrait_counts: Counter = Counter()
    for pair in sorted(observed_pairs):
        lo, lc = pair
        for v in graph_nodes:
            portrait_counts[(lo, lc, node_pair_counts[v].get(pair, 0))] += 1

    total = sum(portrait_counts.values())
    if total == 0:
        return {}
    return {key: count / total for key, count in sorted(portrait_counts.items())}


def compute_dual_length_cluster_ep_npd(
    paths1: list[list[str]],
    paths2: list[list[str]],
    node_to_cluster_1: dict[str, int],
    node_to_cluster_2: dict[str, int],
    graph_nodes_1: list[str] | None = None,
    graph_nodes_2: list[str] | None = None,
) -> float:
    """Dual-length portrait ``P(lo, lc, k)`` divergence."""
    gn1 = graph_nodes_1 if graph_nodes_1 is not None else list(node_to_cluster_1.keys())
    gn2 = graph_nodes_2 if graph_nodes_2 is not None else list(node_to_cluster_2.keys())
    P, Q, _ = align_distributions(
        _dual_length_portrait(paths1, node_to_cluster_1, gn1),
        _dual_length_portrait(paths2, node_to_cluster_2, gn2),
    )
    return compute_jsd(P, Q)


# ============================================================
# Orchestrator: all six variants at the chosen k
# ============================================================

def compute_all_npd(
    G0: nx.DiGraph,
    G1: nx.DiGraph,
    S0: nx.DiGraph,
    S1: nx.DiGraph,
    paths0: list[list[str]],
    paths1: list[list[str]],
    node_to_cluster0: dict[str, int],
    node_to_cluster1: dict[str, int],
) -> list[dict]:
    """Compute all six NPD variants and return rows ``{metric, when, value}``.

    Basis = ``evaluate_npd_over_k`` (cell 79) restricted to the single chosen k. EP-NPD and
    the cluster variants reuse the validated path lists rather than re-enumerating.
    """
    gn0 = list(G0.nodes())
    gn1 = list(G1.nodes())
    return [
        {
            "metric": "Original NPD",
            "when": "before",
            "value": compute_original_npd(G0, G1),
        },
        {
            "metric": "EP-NPD",
            "when": "before",
            "value": compute_ep_npd_from_paths(paths0, paths1, gn0, gn1),
        },
        {
            "metric": "Original NPD",
            "when": "after",
            "value": compute_original_npd(S0, S1),
        },
        {
            "metric": "Cluster-EP-NPD compressed",
            "when": "after",
            "value": compute_cluster_ep_npd(
                paths0, paths1, node_to_cluster0, node_to_cluster1,
                compressed=True, graph_nodes_1=gn0, graph_nodes_2=gn1,
            ),
        },
        {
            "metric": "Cluster-EP-NPD uncompressed",
            "when": "after",
            "value": compute_cluster_ep_npd(
                paths0, paths1, node_to_cluster0, node_to_cluster1,
                compressed=False, graph_nodes_1=gn0, graph_nodes_2=gn1,
            ),
        },
        {
            "metric": "Dual-Length Cluster-EP-NPD",
            "when": "after",
            "value": compute_dual_length_cluster_ep_npd(
                paths0, paths1, node_to_cluster0, node_to_cluster1,
                graph_nodes_1=gn0, graph_nodes_2=gn1,
            ),
        },
    ]
