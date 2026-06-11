"""Consistent cluster labeling across t0 and t1 (NEW).

So that side-by-side summary graphs use the same color for "the same" cluster, we match
cluster ids between t0 and t1 by membership overlap (Jaccard). Greedy: repeatedly take the
highest-Jaccard (t0, t1) pair, lock it in, and continue. Unmatched t1 clusters get fresh ids
that do not collide with any t0 id.

Reuses the Jaccard cluster-matching idea from
``research/testing/t2-12-20-mei/hcsumm_with_npd_testcases_v5.ipynb``.
"""

from __future__ import annotations

from collections import defaultdict


def _members_by_cluster(membership: dict[str, int]) -> dict[int, set[str]]:
    groups: dict[int, set[str]] = defaultdict(set)
    for node, cid in membership.items():
        groups[cid].add(node)
    return groups


def align_cluster_indices(
    membership_t0: dict[str, int],
    membership_t1: dict[str, int],
) -> dict[int, int]:
    """Return a remap ``{t1_cluster_id: aligned_id}`` so matched clusters share an index.

    Greedy max-Jaccard matching between t0 and t1 clusters; unmatched t1 clusters get fresh ids.
    """
    c0 = _members_by_cluster(membership_t0)
    c1 = _members_by_cluster(membership_t1)

    candidates: list[tuple[float, int, int]] = []
    for a, sa in c0.items():
        for b, sb in c1.items():
            inter = len(sa & sb)
            if inter == 0:
                continue
            union = len(sa | sb)
            candidates.append((inter / union, a, b))

    # Highest Jaccard first; break ties deterministically by cluster ids.
    candidates.sort(key=lambda t: (t[0], -t[1], -t[2]), reverse=True)

    remap: dict[int, int] = {}
    used_t0: set[int] = set()
    for _jacc, a, b in candidates:
        if b in remap or a in used_t0:
            continue
        remap[b] = a
        used_t0.add(a)

    # Fresh ids for unmatched t1 clusters, avoiding any existing aligned id.
    existing = set(c0.keys()) | set(remap.values())
    next_free = (max(existing) + 1) if existing else 0
    for b in c1:
        if b not in remap:
            remap[b] = next_free
            existing.add(next_free)
            next_free += 1

    return remap
