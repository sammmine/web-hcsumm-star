"""Feature fusion and distance matrix.

Source: ``hcsumm_star_NPD_final.ipynb`` cell 19
(``align_feature_dimensions``, ``fuse_features``, ``compute_distance_matrix``).
"""

from __future__ import annotations

import numpy as np
from scipy.spatial.distance import pdist, squareform


def align_feature_dimensions(
    feat_dict: dict[str, np.ndarray], target_len: int
) -> dict[str, np.ndarray]:
    """Right-pad each feature vector with zeros up to ``target_len``."""
    aligned: dict[str, np.ndarray] = {}
    for n, vec in feat_dict.items():
        vec = np.asarray(vec, dtype=float)
        if len(vec) < target_len:
            vec = np.concatenate([vec, np.zeros(target_len - len(vec))])
        aligned[n] = vec
    return aligned


def fuse_features(
    e_norm: dict[str, np.ndarray],
    f_norm: dict[str, np.ndarray],
    alpha: float = 1.0,
    beta: float = 1.0,
) -> dict[str, np.ndarray]:
    """``x[v] = concat([alpha * e_norm[v], beta * f_norm[v]])``."""
    nodes_e = set(e_norm.keys())
    nodes_f = set(f_norm.keys())
    if nodes_e != nodes_f:
        raise ValueError(
            "Node mismatch between embedding features and behavior features. "
            f"Missing in e_norm: {nodes_f - nodes_e}. "
            f"Missing in f_norm: {nodes_e - nodes_f}."
        )

    x: dict[str, np.ndarray] = {}
    for n in e_norm:
        e_vec = np.asarray(e_norm[n], dtype=float)
        f_vec = np.asarray(f_norm[n], dtype=float)
        x[n] = np.concatenate([alpha * e_vec, beta * f_vec])
    return x


def compute_distance_matrix(x: dict[str, np.ndarray]) -> tuple[list[str], np.ndarray]:
    """Return ``(sorted_nodes, euclidean_distance_matrix)``."""
    nodes = sorted(x.keys())
    X = np.array([x[n] for n in nodes])

    if len(nodes) <= 1:
        return nodes, np.zeros((len(nodes), len(nodes)))

    if not np.isfinite(X).all():
        raise ValueError("Feature matrix contains NaN or inf.")

    dist = squareform(pdist(X, metric="euclidean"))
    return nodes, dist
