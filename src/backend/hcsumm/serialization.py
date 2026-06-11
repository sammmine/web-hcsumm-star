"""Serialize pipeline artifacts to JSON-friendly structures (Cytoscape.js shape).

Cytoscape element format::

    {"nodes": [{"data": {"id": "foo", "label": "foo", "epl": .., "cluster": "C1", ...}}],
     "edges": [{"data": {"id": "foo->bar", "source": "foo", "target": "bar"}}]}
"""

from __future__ import annotations

import networkx as nx
import numpy as np


def _jsonable(value):
    """Coerce numpy scalars/arrays to plain Python for JSON serialization."""
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, np.ndarray):
        return [_jsonable(v) for v in value.tolist()]
    if isinstance(value, (list, tuple)):
        return [_jsonable(v) for v in value]
    return value


def graph_to_cytoscape(
    G: nx.DiGraph,
    *,
    node_attrs: dict[str, dict] | None = None,
    membership: dict[str, str] | None = None,
) -> dict:
    """Convert a directed graph to Cytoscape elements, attaching per-node attrs/cluster id."""
    nodes = []
    for n in G.nodes():
        data: dict = {"id": str(n), "label": str(n)}
        if membership and n in membership:
            data["cluster"] = membership[n]
        if node_attrs and n in node_attrs:
            for key, val in node_attrs[n].items():
                data[key] = _jsonable(val)
        nodes.append({"data": data})

    edges = []
    for u, v in G.edges():
        edges.append(
            {"data": {"id": f"{u}->{v}", "source": str(u), "target": str(v)}}
        )

    return {"nodes": nodes, "edges": edges}


def vectors_to_dict(vecs: dict[str, np.ndarray]) -> dict[str, list[float]]:
    """``{node: ndarray}`` -> ``{node: [float, ...]}`` for the Step-by-Step stage views."""
    return {str(n): [float(x) for x in np.asarray(v)] for n, v in vecs.items()}
