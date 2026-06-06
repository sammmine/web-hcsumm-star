"""Serialize pipeline artifacts to JSON-friendly structures (Cytoscape.js shape).

Cytoscape element format::

    {"nodes": [{"data": {"id": "foo", "label": "foo", "epl": .., "cluster": "C1", ...}}],
     "edges": [{"data": {"id": "foo->bar", "source": "foo", "target": "bar"}}]}
"""

from __future__ import annotations

import networkx as nx


def graph_to_cytoscape(
    G: nx.DiGraph,
    *,
    node_attrs: dict[str, dict] | None = None,
    membership: dict[str, str] | None = None,
) -> dict:
    """Convert a directed graph to Cytoscape elements, attaching per-node attrs/cluster id."""
    raise NotImplementedError("Implement in Phase 1")
