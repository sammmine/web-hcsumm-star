"""Feature fusion and distance matrix.

Source: ``hcsumm_star_NPD_final.ipynb`` cell 19
(``fuse_features``, ``compute_distance_matrix``).
"""

from __future__ import annotations

import numpy as np


def fuse_features(
    e_norm: dict[str, np.ndarray],
    f_norm: dict[str, np.ndarray],
    alpha: float = 1.0,
    beta: float = 1.0,
) -> dict[str, np.ndarray]:
    """``x[v] = concat([alpha * e_norm[v], beta * f_norm[v]])``."""
    raise NotImplementedError("Lift from notebook cell 19")


def compute_distance_matrix(x: dict[str, np.ndarray]) -> tuple[list[str], np.ndarray]:
    """Return ``(sorted_nodes, euclidean_distance_matrix)``."""
    raise NotImplementedError("Lift from notebook cell 19")
