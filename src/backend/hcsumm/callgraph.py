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
        self.graph = nx.DiGraph()
        self.current_function: str | None = None
        self.defined_functions: set[str] = set()

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self.defined_functions.add(node.name)
        self.graph.add_node(node.name)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self.defined_functions.add(node.name)
        self.graph.add_node(node.name)
        self.generic_visit(node)


def _get_callee_name(call_node: ast.Call) -> str | None:
    if isinstance(call_node.func, ast.Name):
        return call_node.func.id
    if isinstance(call_node.func, ast.Attribute):
        return call_node.func.attr
    return None


class CallEdgeExtractor(ast.NodeVisitor):
    """Second pass: add edges for in-file function calls."""

    def __init__(self, graph: nx.DiGraph, defined_functions: set[str]) -> None:
        self.graph = graph
        self.defined_functions = defined_functions
        self.current_function: str | None = None

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        prev = self.current_function
        self.current_function = node.name
        self.generic_visit(node)
        self.current_function = prev

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        prev = self.current_function
        self.current_function = node.name
        self.generic_visit(node)
        self.current_function = prev

    def visit_Call(self, node: ast.Call) -> None:
        callee = _get_callee_name(node)
        if self.current_function and callee in self.defined_functions:
            self.graph.add_edge(self.current_function, callee)
        self.generic_visit(node)


def extract_call_graph_from_py(source: str) -> nx.DiGraph:
    """Parse Python *source* text into a directed call graph.

    Note: the notebook version takes a file path; this web version takes source text
    so we never touch the filesystem in the pipeline.
    """
    tree = ast.parse(source)

    node_extractor = CallGraphExtractor()
    node_extractor.visit(tree)

    edge_extractor = CallEdgeExtractor(
        node_extractor.graph, node_extractor.defined_functions
    )
    edge_extractor.visit(tree)

    return node_extractor.graph
