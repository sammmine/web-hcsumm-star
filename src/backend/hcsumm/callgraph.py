"""Call graph extraction from Python source.

Source: ``hcsumm_star_NPD_final.ipynb`` cell 7
(``CallGraphExtractor``, ``CallEdgeExtractor``, ``extract_call_graph_from_py``).

Nodes = function names defined in the file. Edges = (caller, callee) for calls to
functions defined in the same file (library/external calls ignored).
"""

from __future__ import annotations

import ast

import networkx as nx


class CallGraphExtractor(ast.NodeVisitor):
    """First pass: collect defined function names as graph nodes."""

    def __init__(self) -> None:
        raise NotImplementedError("Lift from notebook cell 7")


class CallEdgeExtractor(ast.NodeVisitor):
    """Second pass: add edges for in-file function calls."""

    def __init__(self, graph: nx.DiGraph, defined_functions: set[str]) -> None:
        raise NotImplementedError("Lift from notebook cell 7")


def extract_call_graph_from_py(source: str) -> nx.DiGraph:
    """Parse Python *source* text into a directed call graph.

    Note: the notebook version takes a file path; this web version takes source text
    so we never touch the filesystem in the pipeline.
    """
    raise NotImplementedError("Lift from notebook cell 7 (adapt file_path -> source str)")
