# HCSumm\* Web — Backend

FastAPI backend wrapping the HCSumm\* call-graph summarization pipeline.

See `../../doc/Desain Teknis Web HCSumm.md` for the full design.

## Setup

```bash
cd src/backend
python -m venv .venv && source .venv/bin/activate   # fish: source .venv/bin/activate.fish
pip install -e ".[dev]"
```

## Run

```bash
uvicorn app.main:app --reload --port 8000
```

## Test

```bash
pytest
```

## Layout

- `hcsumm/` — pure pipeline package (lifted from `research/notebooks/hcsumm_star_NPD_final.ipynb`).
- `app/` — FastAPI app: routes, schemas, in-memory job runner.
- `tests/` — golden tests vs notebook outputs (tc1–tc4).

## Status

Phase 0 done: the `hcsumm/` pipeline is fully lifted from the notebook (call graph → paths →
behaviour features → node2vec → fusion → Ward → summary → NPD), plus `run_full_pipeline`
assembling the JSON ArtifactBundle. Pure-Python tests pass; the full-pipeline tests need
`gensim` (use Python 3.11/3.12 — gensim 4.x has no wheels for 3.14 yet) and auto-skip otherwise.
