"""Consistent cluster labeling across t0 and t1 (NEW).

So that side-by-side summary graphs use the same color for "the same" cluster, we match
cluster ids between t0 and t1 by membership overlap (Jaccard).

Reuse the Jaccard cluster-matching logic from
``research/testing/t2-12-20-mei/hcsumm_with_npd_testcases_v5.ipynb``.
"""

from __future__ import annotations


def align_cluster_indices(
    membership_t0: dict[str, str],
    membership_t1: dict[str, str],
) -> dict[str, str]:
    """Return a remap ``{t1_cluster_id: aligned_id}`` so matched clusters share an index.

    Greedy max-Jaccard matching between t0 and t1 clusters; unmatched t1 clusters get fresh ids.
    """
    raise NotImplementedError("Adapt Jaccard cluster matching from testcases_v5 notebook")
