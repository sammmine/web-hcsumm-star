# web-hcsumm-star

Web app interaktif untuk pipeline **HCSumm\*** — merangkum evolusi *directed call graph*
antara dua titik waktu (t0 → t1): call graph → fitur behaviour + node2vec → fusion →
Ward clustering → summary graph → metrik NPD.

## Dokumen

- `doc/Spesifikasi Proyek Web HCSumm.md` — spesifikasi fungsional (sumber).
- `doc/Desain Teknis Web HCSumm.md` — desain teknis & arsitektur (keputusan + rencana bertahap).

## Struktur

```
src/backend/   FastAPI + pipeline package `hcsumm/` (lift dari research/notebooks)
src/frontend/  React + Vite + TS, visualisasi Cytoscape.js
research/      notebook sumber & test case (referensi)
doc/           spesifikasi, paper, slide, artifact testing
```

## Menjalankan (dev)

```bash
# backend
cd src/backend && python -m venv .venv && source .venv/bin/activate.fish
pip install -e ".[dev]" && uvicorn app.main:app --reload --port 8000

# frontend (terminal lain)
cd src/frontend && npm install && npm run dev   # http://localhost:5173
```

## Status

**Fase 0 selesai.** Pipeline `src/backend/hcsumm/` sudah terisi penuh (lift dari
`research/notebooks/hcsumm_star_NPD_final.ipynb`): call graph → execution path (dengan guard) →
fitur behaviour → node2vec → fusion → Ward clustering → summary graph → metrik NPD, plus
`run_full_pipeline` yang merakit ArtifactBundle JSON. Lapisan API (FastAPI, job runner, schema)
& frontend (store, views, Cytoscape) sudah scaffolded. Catatan: node2vec butuh `gensim`
(pakai Python 3.11/3.12 — gensim 4.x belum punya wheel untuk 3.14).
