"""Directed node2vec embedding.

Source: ``hcsumm_star_NPD_final.ipynb`` cell 17
(``directed_node2vec_walk``, ``generate_directed_node2vec_walks``,
``compute_directed_node2vec_embedding``, ``normalize_e_l2``).

CPU-bound (gensim Word2Vec + random walks) — this is the main runtime cost and the reason
the API runs the pipeline in a ProcessPoolExecutor.
"""

from __future__ import annotations

import networkx as nx
import numpy as np


def directed_node2vec_walk(
    G: nx.DiGraph, start_node: str, walk_length: int, p: float = 1.0, q: float = 1.0
) -> list[str]:
    raise NotImplementedError("Lift from notebook cell 17")


def generate_directed_node2vec_walks(
    G: nx.DiGraph,
    num_walks: int = 200,
    walk_length: int = 10,
    p: float = 1.0,
    q: float = 1.0,
    seed: int = 42,
) -> list[list[str]]:
    raise NotImplementedError("Lift from notebook cell 17")


def compute_directed_node2vec_embedding(
    G: nx.DiGraph,
    dimensions: int = 4,
    walk_length: int = 10,
    num_walks: int = 200,
    p: float = 1.0,
    q: float = 1.0,
    seed: int = 42,
    window: int = 5,
    epochs: int = 100,
) -> dict[str, np.ndarray]:
    """Generate walks -> train Word2Vec skip-gram -> per-node embedding ``e[v]``."""
    raise NotImplementedError("Lift from notebook cell 17")


def normalize_e_l2(e: dict[str, np.ndarray]) -> dict[str, np.ndarray]:
    """Per-node L2 normalization."""
    raise NotImplementedError("Lift from notebook cell 17")
