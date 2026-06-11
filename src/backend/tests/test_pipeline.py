"""Golden / structural tests for the HCSumm* pipeline.

Phase 0 goal: assert the lifted package reproduces the notebook's structural outputs for the
bundled test cases (tc1-tc4) under ``research/testing/t2-12-20-mei/``.

Note: the full-pipeline tests need gensim (node2vec). gensim has no wheels for very new
CPython yet, so those tests ``importorskip`` gensim and run on a supported interpreter
(3.11/3.12). The call-graph / path / feature tests are pure-Python and always run.
"""

from __future__ import annotations

from pathlib import Path

import pytest

TESTCASES = Path(__file__).resolve().parents[3] / "research" / "testing" / "t2-12-20-mei"

CASES = ["tc1", "tc2", "tc3", "tc4"]


def _read(name: str) -> str:
    return (TESTCASES / name).read_text()


@pytest.mark.parametrize("case", CASES)
def test_callgraph_nonempty(case: str) -> None:
    from hcsumm.callgraph import extract_call_graph_from_py

    for tp in ("t0", "t1"):
        g = extract_call_graph_from_py(_read(f"{case}_{tp}.py"))
        assert g.number_of_nodes() > 0, f"{case}_{tp}: expected at least one function node"


def test_execution_paths_guard_capped_flag() -> None:
    """The path-explosion guard must trip and flag when max_paths is tiny."""
    from hcsumm.callgraph import extract_call_graph_from_py
    from hcsumm.paths import extract_execution_paths

    g = extract_call_graph_from_py(_read("tc1_t0.py"))
    paths, capped = extract_execution_paths(g, max_paths=3)
    assert len(paths) <= 3
    assert capped is True

    paths, capped = extract_execution_paths(g, max_paths=50_000)
    assert capped is False


def test_behaviour_features_shape() -> None:
    from hcsumm.callgraph import extract_call_graph_from_py
    from hcsumm.features import build_compact_behavior_feature_epl
    from hcsumm.paths import extract_execution_paths

    g = extract_call_graph_from_py(_read("tc1_t0.py"))
    paths, _ = extract_execution_paths(g)
    f_star = build_compact_behavior_feature_epl(g, paths)
    assert set(f_star.keys()) == set(g.nodes())
    assert all(len(v) == 5 for v in f_star.values())  # EPL, indeg, outdeg, depth, pagerank


@pytest.mark.parametrize("case", CASES)
def test_full_pipeline_bundle_shape(case: str) -> None:
    pytest.importorskip("gensim", reason="node2vec embedding needs gensim")
    from hcsumm.config import PipelineConfig
    from hcsumm.pipeline import run_full_pipeline

    bundle = run_full_pipeline(_read(f"{case}_t0.py"), _read(f"{case}_t1.py"), PipelineConfig())

    assert {"config", "t0", "t1", "npd", "warnings"} <= bundle.keys()
    for side in ("t0", "t1"):
        s = bundle[side]
        assert {"callgraph", "summary", "membership", "linkage", "stages"} <= s.keys()
        assert {"features", "embedding", "fusion", "distance_matrix"} <= s["stages"].keys()

    # Six NPD variants, each a finite number.
    assert len(bundle["npd"]) == 6
    assert all(isinstance(r["value"], float) for r in bundle["npd"])

    # Consistent cluster indexing: t0 and t1 share the same cluster-id namespace.
    t0_ids = set(bundle["t0"]["membership"].values())
    t1_ids = set(bundle["t1"]["membership"].values())
    assert t0_ids & t1_ids, "expected at least one cluster id shared across t0/t1"
