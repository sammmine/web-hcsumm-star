"""Golden tests for the HCSumm* pipeline.

Phase 0 goal: assert the lifted package reproduces the notebook outputs for the bundled
test cases (tc1-tc4) under ``research/testing/t2-12-20-mei/``.

These are skipped until the pipeline stubs are implemented.
"""

from __future__ import annotations

from pathlib import Path

import pytest

TESTCASES = Path(__file__).resolve().parents[3] / "research" / "testing" / "t2-12-20-mei"


@pytest.mark.skip(reason="pipeline stubs not yet implemented (Phase 0)")
def test_callgraph_tc1() -> None:
    from hcsumm.callgraph import extract_call_graph_from_py

    src = (TESTCASES / "tc1_t0.py").read_text()
    g = extract_call_graph_from_py(src)
    assert g.number_of_nodes() > 0


@pytest.mark.skip(reason="pipeline stubs not yet implemented (Phase 0)")
def test_full_pipeline_tc1() -> None:
    from hcsumm.config import PipelineConfig
    from hcsumm.pipeline import run_full_pipeline

    src0 = (TESTCASES / "tc1_t0.py").read_text()
    src1 = (TESTCASES / "tc1_t1.py").read_text()
    bundle = run_full_pipeline(src0, src1, PipelineConfig())
    assert {"config", "t0", "t1", "npd"} <= bundle.keys()
