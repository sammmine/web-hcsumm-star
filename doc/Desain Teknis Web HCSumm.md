# Desain Teknis — Web HCSumm\*

> Status: disetujui untuk implementasi · Tanggal: 2026-06-06 · Deadline proyek: akhir Juli 2026
> Dokumen ini melengkapi `Spesifikasi Proyek Web HCSumm.md` (spesifikasi fungsional) dengan
> keputusan teknis & arsitektur konkret.

## 1. Konteks & Tujuan

HCSumm\* adalah pipeline riset (saat ini berupa notebook di `research/notebooks/`) yang
merangkum evolusi *directed call graph* antara dua titik waktu (t0 → t1). Pipeline:
parse dua file `.py` → call graph berarah → fitur behaviour (EPL, in-degree, out-degree,
depth, PageRank) + embedding directed node2vec → fusion → Ward clustering → summary graph →
metrik NPD (Network Portrait Divergence) untuk membandingkan t0 vs t1.

Tujuan proyek: membungkus pipeline tersebut menjadi **web app interaktif lokal** sehingga
peneliti (pengguna + dosen) dapat mengunggah kode, mengatur parameter, menjalankan pipeline,
dan mengeksplorasi hasil secara visual tanpa membuka notebook.

Fungsi-fungsi inti pipeline **sudah ada** dan terstruktur rapi di
`research/notebooks/hcsumm_star_NPD_final.ipynb`. Inti pekerjaan: (a) mengangkat fungsi-fungsi
itu dari notebook menjadi package Python yang bersih, dan (b) membangun backend FastAPI +
frontend React di sekitarnya.

## 2. Keputusan Arsitektur

| Topik | Keputusan |
| --- | --- |
| Konteks pakai | Tool riset lokal (pengguna + dosen). Tanpa auth, tanpa multi-tenant. |
| Skala graph | Harus tahan graph sedang–besar (ratusan fungsi) → butuh *guard* enumerasi path + eksekusi async. |
| Persistence | **Stateless** — tanpa database. Satu run menghitung **seluruh** artifact; hasil ditahan di memori sementara (TTL). |
| Frontend | **React + Vite (TypeScript)**, SPA. |
| Visualisasi graph | **Cytoscape.js** (compound node untuk cluster, layout dagre untuk graph berarah). |
| Eksekusi | FastAPI background task + `ProcessPoolExecutor` (pipeline CPU-bound gensim/node2vec) + job store in-memory + polling dari frontend. |
| UX parameter | Mode simpel (toggle fitur behaviour, mode embedding, K) + panel **Advanced / OFAT** (collapsible) untuk parameter node2vec (EMBED_DIM, WALK_LENGTH, NUM_WALKS, P_RETURN, Q_INOUT, SEED, α, β). |
| Lingkup MVP | Upload + run + **Direct View** + tabel NPD + tabel keanggotaan cluster; **Side-by-side compare** dengan cluster indexing konsisten; **Step-by-Step view**. |
| Ditunda (post-MVP) | **Cluster Iteration Visualization** (animasi merge Ward); **OFAT batch runner** UI. |

### Prinsip inti: run stateless tapi lengkap

Satu run pipeline menghitung **semua** artifact sekaligus (dua call graph, dua summary graph,
keanggotaan cluster, semua metrik NPD, semua tahap pipeline, dan linkage matrix Ward). Frontend
berpindah antar view (Direct / Step-by-Step / Side-by-side) sepenuhnya di sisi klien **tanpa
recompute**. Linkage matrix disertakan di bundle sejak awal agar fitur Cluster Iteration yang
ditunda tidak memerlukan perubahan backend di kemudian hari.

> **Catatan kontradiksi spec:** Bagian 2 spesifikasi fungsional menyebut user hanya mengatur
> parameter behavioural + K, namun tujuan OFAT & tabel parameter node2vec mengharuskan parameter
> node2vec dapat diubah. Diselesaikan dengan **panel Advanced/OFAT**: mode default sederhana,
> parameter node2vec tersedia saat dibutuhkan.

## 3. Struktur Repository

```
web-hcsumm-star/
  src/backend/
    pyproject.toml                  # fastapi, uvicorn, pydantic, networkx, numpy, scipy, pandas, gensim
    hcsumm/                         # pipeline murni (di-lift dari notebook)
      config.py                     # PipelineConfig + default semua parameter
      callgraph.py                  # extract_call_graph_from_py + extractor AST
      paths.py                      # execution paths + path-length profile (+ GUARD cap/timeout)
      features.py                   # fitur behaviour (EPL, indeg, outdeg, depth, pagerank) + seleksi
      embedding.py                  # directed node2vec walk + Word2Vec embedding + normalisasi L2
      fusion.py                     # fuse_features + distance matrix
      clustering.py                 # ward_clustering + ward_iteration_steps (BARU)
      summary.py                    # build_summary_graph
      cluster_indexing.py           # BARU: pencocokan cluster t0↔t1 via Jaccard (warna konsisten)
      npd.py                        # JSD, portrait, original NPD, EP-NPD, cluster-EP, dual-length
      pipeline.py                   # run_full_pipeline(src_t0, src_t1, config) -> ArtifactBundle
      serialization.py              # nx.DiGraph -> Cytoscape JSON; bundle -> dict
    app/
      main.py                       # FastAPI app + CORS
      schemas.py                    # model pydantic request/response
      jobs.py                       # job store in-memory + ProcessPoolExecutor + sweep TTL
      routes.py                     # POST /api/runs, GET status, GET result
    tests/                          # golden test vs output notebook (tc1–tc4)
  src/frontend/                     # React + Vite + TS
    src/
      api/client.ts                 # fetch client typed + helper polling
      types.ts                      # mirror ArtifactBundle
      state/runStore.ts             # bundle aktif, view terpilih, parameter
      components/
        UploadPanel.tsx             # upload dua .py (t0, t1) + loader sample
        ParamForm.tsx               # kontrol simpel + AdvancedPanel collapsible
        GraphView.tsx               # wrapper Cytoscape (dagre, pewarnaan cluster)
        NpdTable.tsx
        ClusterMembershipTable.tsx
        views/{DirectView,SideBySideView,StepByStepView}.tsx
      App.tsx
  doc/        (spec, papers, slides, artifact testing — sudah ada)
  research/   (notebook sumber — referensi saja)
```

## 4. Kontrak API

- `POST /api/runs` — multipart (dua file `.py`) **atau** JSON `{ source_t0, source_t1, config }`.
  Mengembalikan `{ job_id }`. Validasi: ekstensi `.py`, dapat di-`ast.parse`, batas ukuran.
- `GET /api/runs/{job_id}` — `{ status: pending|running|done|error, progress?, error? }`.
- `GET /api/runs/{job_id}/result` — `ArtifactBundle` penuh saat `status == done`.

### Bentuk ArtifactBundle (satu run = satu bundle)

```jsonc
{
  "config": { /* echo parameter */ },
  "t0": {
    "callgraph": { /* Cytoscape JSON, node membawa fitur */ },
    "summary":   { /* Cytoscape JSON, cluster id konsisten */ },
    "membership": { "<node>": "<cluster_id>" },
    "linkage":    [[i, j, dist, size]],          // scipy Z, untuk iteration view (ditunda)
    "stages": { "features": {}, "embedding": {}, "fusion": {}, "distance_matrix": [] }
  },
  "t1": { /* sama */ },
  "npd": [ { "metric": "...", "when": "before|after", "value": 0.0 } ],  // 6 varian
  "warnings": [ "path enumeration capped at N", "..." ]
}
```

### Mode embedding → parameter aktif (mengatur enable/disable form)

- **Node2Vec Only** `x = e'(v)` → parameter node2vec aktif, toggle behaviour nonaktif.
- **Behaviour Only** `x = f'(v)` → toggle behaviour aktif, parameter node2vec nonaktif.
- **Combined/Fused** `x = fuse(e', f', α, β)` → keduanya + α/β aktif.

## 5. Parameter (default)

| Parameter | Default | Kelompok |
| --- | --- | --- |
| EMBED_DIM | 4 | node2vec (Advanced) |
| WALK_LENGTH | 10 | node2vec (Advanced) |
| NUM_WALKS | 200 | node2vec (Advanced) |
| P_RETURN | 1.0 | node2vec (Advanced) |
| Q_INOUT | 1.0 | node2vec (Advanced) |
| SEED | 42 | node2vec (Advanced) |
| alpha (α) | 1.0 | fusion (Advanced) |
| beta (β) | 1.0 | fusion (Advanced) |
| K_CLUSTERS | 2 | simpel |
| behaviour features | EPL, indeg, outdeg, depth (pagerank opsional) | simpel (toggle) |
| embedding_mode | fused | simpel |

## 6. Metrik NPD

| Metrik | Kapan | Deskripsi |
| --- | --- | --- |
| Original NPD | sebelum & sesudah clustering | Portrait berbasis shortest-path neighbourhood |
| EP-NPD | sebelum clustering | Portrait berbasis execution path function-level |
| Cluster-EP-NPD (compressed) | sesudah clustering | Path diproyeksikan ke cluster, duplikat berurutan dihapus |
| Cluster-EP-NPD (uncompressed) | sesudah clustering | Sama tapi duplikat dipertahankan (diagnostik) |
| Dual-Length Cluster-EP-NPD | sesudah clustering | Portrait gabungan panjang original + panjang cluster |

Semua menggunakan Jensen-Shannon Divergence (`compute_jsd`).

## 7. Rencana Implementasi (Bertahap)

**Fase 0 — Ekstraksi package pipeline (prioritas tertinggi, mengurangi risiko)**
- Angkat fungsi dari `hcsumm_star_NPD_final.ipynb` (cell 7/15/17/19/63/68–79) ke modul `hcsumm/`.
  Hapus efek samping `display`/graphviz/Jupyter; fungsi mengembalikan data biasa.
- `run_full_pipeline(src_t0, src_t1, config)` → bundle in-memory. Basis: `run_full_pipeline`
  (cell 63) + `evaluate_npd_over_k` (cell 79).
- **Guard enumerasi path** di `paths.py`: `nx.all_simple_paths(..., cutoff)` + batas jumlah path,
  catat warning saat ter-cap. Tangani graph siklik (rekursi).
- `ward_iteration_steps(Z, nodes)`: rekonstruksi tiap merge Ward dari linkage matrix.
- `cluster_indexing.py`: cocokkan id cluster t0↔t1 via overlap Jaccard (reuse logika di
  `hcsumm_with_npd_testcases_v5.ipynb`).
- Golden test: jalankan tc1–tc4, assert output cocok dengan notebook (toleransi float).

**Fase 1 — Backend FastAPI + job runner**
- `serialization.py`: `nx.DiGraph` → Cytoscape JSON.
- `jobs.py`: dict in-memory `{job_id: {status, result, ts}}` + `ProcessPoolExecutor` + sweep TTL.
- `routes.py` + `schemas.py`: tiga endpoint + validasi input.

**Fase 2 — Frontend scaffold + run loop**
- Vite + React + TS, API client typed + polling, UploadPanel (+ "load sample"), ParamForm
  (simpel + Advanced/OFAT collapsible), enable/disable berdasar mode embedding, run → progress → store.

**Fase 3 — Direct View (MVP):** GraphView (dagre + pewarnaan cluster), summary t0 & t1, NpdTable,
ClusterMembershipTable.

**Fase 4 — Side-by-side compare (MVP):** dua GraphView berdampingan, warna cluster konsisten via
cluster indexing Fase 0.

**Fase 5 — Step-by-Step view (MVP):** render tiap tahap dari `bundle.t*.stages`.

**Fase 6 — Ditunda (post-MVP):** Cluster Iteration Visualization (slider/play atas linkage);
OFAT batch runner.

## 8. Verifikasi

- **Fase 0:** `pytest src/backend/tests` — golden test membandingkan node/edge call graph, keanggotaan
  cluster, dan 6 nilai NPD dengan output notebook untuk tc1–tc4. Uji guard path pada sampel Flask
  v2/v3 (besar) — harus memberi warning, bukan hang.
- **Fase 1:** `uvicorn app.main:app` → `curl` POST sampel → poll status → GET result; pastikan bundle
  valid & event loop tidak ter-blok untuk graph besar.
- **Fase 2–5:** `npm run dev`; upload tc1, run, verifikasi Direct View merender dua summary graph,
  tabel NPD cocok dengan backend, warna side-by-side konsisten, Step-by-Step menampilkan semua tahap,
  dan ganti mode embedding men-disable parameter yang benar.
- **End-to-end:** jalankan tc1–tc4 lewat UI, sanity-check terhadap hasil notebook.

## 9. Risiko

- **Ledakan enumerasi path** pada graph besar/siklik — dimitigasi guard cutoff; call graph siklik
  (rekursi) perlu penanganan karena `all_simple_paths` mengasumsikan struktur acyclic.
- **Runtime node2vec** ∝ NUM_WALKS × WALK_LENGTH × jumlah node — tampilkan perkiraan biaya kasar di
  panel Advanced; andalkan runner async + polling agar UI tidak ter-blok.

## 10. Sumber yang Di-reuse

- `research/notebooks/hcsumm_star_NPD_final.ipynb` — semua fungsi inti (cell 7/15/17/19/63/68–79).
- `research/testing/t3-21-mei/hcsumm_param_isolation_v7.ipynb` — wrapper OFAT (Fase 6).
- `research/testing/t2-12-20-mei/hcsumm_with_npd_testcases_v5.ipynb` — pencocokan cluster Jaccard.
- `research/testing/t2-12-20-mei/tc1..tc4_t{0,1}.py` — input sampel untuk test & fitur "load sample".
