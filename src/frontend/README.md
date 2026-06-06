# HCSumm\* Web — Frontend

React + Vite + TypeScript SPA. Graph visualization via Cytoscape.js (+ dagre).

See `../../doc/Desain Teknis Web HCSumm.md` for the full design.

## Setup & run

```bash
cd src/frontend
npm install
npm run dev          # http://localhost:5173 (proxies /api -> http://localhost:8000)
```

Start the backend (`uvicorn app.main:app --port 8000`) in parallel.

## Layout

- `src/api/client.ts` — typed API client + polling.
- `src/state/runStore.ts` — zustand store (config, sources, current bundle, selected view).
- `src/components/ParamForm.tsx` — simple controls + Advanced/OFAT panel.
- `src/components/GraphView.tsx` — Cytoscape wrapper (dagre, cluster coloring).
- `src/components/views/` — DirectView, SideBySideView, StepByStepView (MVP).

## Status

Boilerplate scaffold. Views render once the backend returns a real ArtifactBundle (the
pipeline stubs must be filled first — see backend Phase 0). Deferred: Cluster Iteration
Visualization, OFAT batch runner.
