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

Boilerplate scaffold. Pipeline functions are stubs (`raise NotImplementedError`) — to be filled
from the notebook in Phase 0. See module docstrings for the source cell references.
