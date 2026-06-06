"""Execution path enumeration and path-length profile.

Source: ``hcsumm_star_NPD_final.ipynb`` cell 15
(``get_exit_nodes``, ``extract_execution_paths``, ``build_path_length_profile``).

GUARD: ``extract_execution_paths`` must respect ``max_paths`` and ``path_cutoff`` from
``PipelineConfig`` and return a warning flag when capped — ``nx.all_simple_paths`` can blow
up exponentially on large/cyclic call graphs. Handle cycles (recursion) gracefully.
"""

from __future__ import annotations

import networkx as nx


def get_exit_nodes(G: nx.DiGraph) -> list[str]:
    """Nodes with out_degree == 0."""
    raise NotImplementedError("Lift from notebook cell 15")


def extract_execution_paths(
    G: nx.DiGraph,
    *,
    max_paths: int = 50_000,
    cutoff: int | None = None,
) -> tuple[list[list[str]], bool]:
    """All simple paths to exit nodes, with explosion guard.

    Returns ``(paths, capped)`` where ``capped`` is True if enumeration hit ``max_paths``.
    """
    raise NotImplementedError("Lift from notebook cell 15 + add max_paths/cutoff guard")


def build_path_length_profile(
    G: nx.DiGraph, paths: list[list[str]]
) -> tuple[dict[str, list[int]], int]:
    """``f[v][i]`` = count of paths of length ``i+1`` containing ``v``. Returns ``(f, L)``."""
    raise NotImplementedError("Lift from notebook cell 15")
