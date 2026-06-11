"""Directed node2vec embedding.

Source: ``hcsumm_star_NPD_final.ipynb`` cell 17
(``directed_node2vec_walk``, ``generate_directed_node2vec_walks``,
``compute_directed_node2vec_embedding``, ``normalize_e_l2``).

CPU-bound (gensim Word2Vec + random walks) — this is the main runtime cost and the reason
the API runs the pipeline in a ProcessPoolExecutor.
"""

from __future__ import annotations

import random

import networkx as nx
import numpy as np


def directed_node2vec_walk(
    G: nx.DiGraph, start_node: str, walk_length: int, p: float = 1.0, q: float = 1.0
) -> list[str]:
    walk = [start_node]

    while len(walk) < walk_length:
        curr = walk[-1]
        neighbors = list(G.successors(curr))  # outgoing neighbours only

        if len(neighbors) == 0:
            break  # exit node

        if len(walk) == 1:
            next_node = random.choice(neighbors)
        else:
            prev = walk[-2]
            weights = []
            for nbr in neighbors:
                if nbr == prev:
                    weight = 1.0 / p
                elif G.has_edge(prev, nbr) or G.has_edge(nbr, prev):
                    weight = 1.0
                else:
                    weight = 1.0 / q
                weights.append(weight)

            probs = np.array(weights, dtype=float)
            probs = probs / probs.sum()
            next_node = np.random.choice(neighbors, p=probs)

        walk.append(next_node)

    return walk


def generate_directed_node2vec_walks(
    G: nx.DiGraph,
    num_walks: int = 200,
    walk_length: int = 10,
    p: float = 1.0,
    q: float = 1.0,
    seed: int = 42,
) -> list[list[str]]:
    random.seed(seed)
    np.random.seed(seed)

    nodes = list(G.nodes())
    walks: list[list[str]] = []

    for _ in range(num_walks):
        random.shuffle(nodes)
        for n in nodes:
            walk = directed_node2vec_walk(G, n, walk_length, p=p, q=q)
            walks.append([str(x) for x in walk])

    return walks


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
    from gensim.models import Word2Vec  # lazy: heavy dep, only needed at run time

    walks = generate_directed_node2vec_walks(
        G, num_walks=num_walks, walk_length=walk_length, p=p, q=q, seed=seed
    )

    model = Word2Vec(
        sentences=walks,
        vector_size=dimensions,
        window=window,
        min_count=1,
        sg=1,  # skip-gram
        workers=1,
        seed=seed,
        epochs=epochs,
    )

    e: dict[str, np.ndarray] = {}
    for n in G.nodes():
        key = str(n)
        e[n] = model.wv[key] if key in model.wv else np.zeros(dimensions)

    return e


def normalize_e_l2(e: dict[str, np.ndarray]) -> dict[str, np.ndarray]:
    """Per-node L2 normalization."""
    e_norm: dict[str, np.ndarray] = {}
    for v, vec in e.items():
        norm = np.linalg.norm(vec)
        e_norm[v] = vec / norm if norm > 0 else vec.copy()
    return e_norm
