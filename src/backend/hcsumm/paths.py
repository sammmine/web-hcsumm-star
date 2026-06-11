"""Execution path enumeration and path-length profile.

Source: ``hcsumm_star_NPD_final.ipynb`` cell 15
(``get_exit_nodes``, ``extract_execution_paths``, ``build_path_length_profile``).

GUARD: ``extract_execution_paths`` respects ``max_paths`` and ``cutoff`` from
``PipelineConfig`` and returns a warning flag when capped — ``nx.all_simple_paths`` can blow
up exponentially on large/cyclic call graphs. ``nx.all_simple_paths`` only enumerates simple
paths, so recursion/cycles do not cause infinite loops; the cutoff bounds path length too.
"""

from __future__ import annotations

import networkx as nx
import numpy as np


def get_exit_nodes(G: nx.DiGraph) -> list[str]:
    """Nodes with out_degree == 0."""
    return [n for n in G.nodes() if G.out_degree(n) == 0]


def extract_execution_paths(
    G: nx.DiGraph,
    *,
    max_paths: int = 50_000,
    cutoff: int | None = None,
) -> tuple[list[list[str]], bool]:
    """All simple paths to exit nodes, with explosion guard.

    Returns ``(paths, capped)`` where ``capped`` is True if enumeration hit ``max_paths``.
    Duplicates are removed while preserving first-seen order (matching the notebook).
    """
    exit_nodes = get_exit_nodes(G)
    seen: set[tuple[str, ...]] = set()
    paths: list[list[str]] = []
    capped = False

    for start in G.nodes():
        if capped:
            break
        for end in exit_nodes:
            if start == end:
                continue
            try:
                for path in nx.all_simple_paths(G, start, end, cutoff=cutoff):
                    if len(path) <= 1:
                        continue
                    key = tuple(path)
                    if key in seen:
                        continue
                    seen.add(key)
                    paths.append(path)
                    if len(paths) >= max_paths:
                        capped = True
                        break
            except nx.NetworkXNoPath:
                pass
            if capped:
                break

    return paths, capped


def build_path_length_profile(
    G: nx.DiGraph, paths: list[list[str]]
) -> tuple[dict[str, np.ndarray], int]:
    """``f[v][i]`` = count of paths of length ``i+1`` containing ``v``. Returns ``(f, L)``."""
    if not paths:
        return {n: np.array([], dtype=float) for n in G.nodes()}, 0

    L = max(len(p) - 1 for p in paths)
    f = {n: np.zeros(L, dtype=float) for n in G.nodes()}

    for p in paths:
        idx = (len(p) - 1) - 1
        for v in p:
            f[v][idx] += 1

    return f, L
