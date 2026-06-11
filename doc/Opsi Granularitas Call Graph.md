# Opsi Granularitas Input Call Graph — Web HCSumm\*

Dokumen ini memetakan tiga opsi untuk **sumber** call graph yang dibandingkan HCSumm\*:
file tunggal, multi-file (namespace digabung), atau project penuh (resolusi import). Tujuannya
membantu memutuskan arah scope sebelum nambah kerjaan implementasi.

> Ringkas: metode HCSumm\* hanya butuh **satu `nx.DiGraph` per titik waktu (t0, t1)**. NPD
> membandingkan dua graf itu. Dari mana graf itu berasal — satu file atau satu project —
> *bukan bagian dari metode*. Jadi naik ke level project itu sah; yang berubah cuma cara
> membangun grafnya di `hcsumm/callgraph.py`.

---

## 0. Kondisi sekarang (baseline)

`hcsumm/callgraph.py` → `extract_call_graph_from_py(source: str) -> nx.DiGraph`:

- Input: **satu** string source `.py`, di-parse dengan `ast.parse`.
- **Node** = setiap fungsi yang didefinisikan di file itu (`def` / `async def`), termasuk
  nested function.
- **Edge** `(caller, callee)` = pemanggilan di mana `caller` adalah fungsi yang sedang
  dikunjungi **dan** nama `callee` ada di himpunan fungsi yang didefinisikan di file itu.
- Nama callee diambil dari `ast.Name` (`foo()`) atau `ast.Attribute` (`obj.foo()` → `foo`).
- Panggilan ke library / fungsi dari file lain → **diabaikan**.

Konsekuensi: graf = relasi antar-fungsi **dalam satu file**. Ini lift apa adanya dari
`research/notebooks/hcsumm_star_NPD_final.ipynb`, yang memang dievaluasi pada file tunggal
(`app_2.0.0.py` vs `app_2.2.0.py`, dan `tc1_t0.py`/`tc1_t1.py`).

Lapisan yang menyentuh granularitas ini:

- `app/routes.py` — `POST /api/runs` (JSON `source_t0`/`source_t1`) & `POST /api/runs/upload`
  (dua file `file_t0`/`file_t1`).
- `app/schemas.py` — `RunRequest { source_t0, source_t1, config }`.
- `hcsumm/pipeline.py` — `run_full_pipeline(source_t0, source_t1, config)` (string, bukan list).
- Frontend `UploadPanel.tsx` — dua input file tunggal.

---

## Opsi A — Tetap single-file

**Apa yang dibangun:** tidak ada. Seperti sekarang.

**Perubahan kode:** —

**Effort:** nol.

**Kelebihan:**
- Persis dengan notebook & evaluasi tesis — tidak ada risiko menyimpang dari metode yang
  sudah divalidasi.
- Graf kecil, eksekusi cepat, path-enumeration jarang meledak.

**Kekurangan / batasan:**
- Hanya melihat satu file. Codebase nyata yang tersebar di banyak modul tidak terwakili.
- Cocok kalau unit analisisnya memang satu modul (mis. `app.py` sebuah service kecil).

**Dampak API/frontend:** —

---

## Opsi B — Multi-file, namespace digabung

**Ide:** terima **banyak file** per titik waktu (multi-upload / folder / zip). Parse semua,
kumpulkan **satu tabel nama fungsi global**, lalu bangun edge untuk panggilan ke nama fungsi
mana pun yang terdaftar — tanpa peduli file asalnya. Ini "project-ish" tanpa harus
menyelesaikan resolusi import.

**Perubahan kode:**

- `hcsumm/callgraph.py`
  - Tambah `extract_call_graph_from_sources(sources: list[str]) -> nx.DiGraph` (atau
    `dict[str, str]` nama→source).
  - Pass 1: jalankan `CallGraphExtractor` pada **semua** file → union `defined_functions`
    dan semua node.
  - Pass 2: jalankan `CallEdgeExtractor` pada **semua** file memakai `defined_functions`
    gabungan. Logika `visit_Call` tetap sama; sekarang callee bisa lintas-file.
  - `extract_call_graph_from_py(source)` jadi pembungkus tipis `[source]`.
- `hcsumm/pipeline.py` — `_run_one_side`/`run_full_pipeline` menerima `list[str]` (atau dict)
  alih-alih satu string. Sisanya (paths, fitur, node2vec, NPD) **tidak berubah** karena tetap
  bekerja pada satu `DiGraph`.
- `app/schemas.py` — `RunRequest.sources_t0: list[str]`, `sources_t1: list[str]` (atau
  pertahankan field lama sebagai single dan tambah field baru untuk kompatibilitas).
- `app/routes.py` — `POST /api/runs/upload` terima banyak file per sisi; tambah dukungan
  upload **zip/folder** (unzip in-memory, ambil semua `*.py`). Validasi `ast.parse` per file
  + batas ukuran total.
- Frontend `UploadPanel.tsx` — `<input type="file" multiple>` atau drop folder/zip per sisi.

**Effort:** sedang (~setengah hari). Inti pipeline aman; yang nambah adalah penggabungan
multi-source + jalur upload.

**Kelebihan:**
- Graf selevel project tanpa parser kompleks.
- Perubahan terlokalisasi; metode NPD tidak tersentuh.

**Kekurangan / tradeoff:**
- **Tabrakan nama:** dua fungsi berbeda bernama sama di file berbeda (mis. dua `run`) ke-merge
  jadi **satu node** → bisa menambah edge palsu. Untuk banyak codebase masih dapat diterima,
  tapi harus disebut eksplisit sebagai asumsi.
- Method/atribut yang kebetulan senama dengan fungsi top-level tetap ke-match by name
  (warisan perilaku `ast.Attribute.attr` sekarang).
- Graf lebih besar → **execution-path bisa meledak**; guard `max_paths`/`cutoff` (sudah ada)
  jadi makin penting, dan EPL/NPD dihitung atas path yang mungkin terpotong.

**Dampak ke metode:** netral selama tabrakan nama dianggap asumsi yang dilaporkan. Hasil NPD
tetap valid sebagai perbandingan dua graf.

---

## Opsi C — Project penuh (resolusi import + class/method)

**Ide:** bangun call graph yang benar-benar sadar modul: ikuti `import` / `from x import y`,
pakai **qualified name** (`paket.modul.fungsi`), resolusi method (`self.x()`, `obj.x()`) ke
kelas yang tepat, tangani alias dan re-export.

**Perubahan kode:**

- `hcsumm/callgraph.py` — pada dasarnya ditulis ulang jadi **static analyzer**:
  - Bangun tabel simbol per modul (fungsi, kelas, method, nama yang di-import + alias-nya).
  - Resolusi pemanggilan: `ast.Name` dicocokkan ke binding lokal/impor; `ast.Attribute`
    butuh inferensi tipe receiver (mis. instance kelas mana) — ini bagian tersulit.
  - Node = qualified name; edge lintas modul ter-resolve dengan benar.
  - Pertimbangkan pakai pustaka yang sudah ada (`code2flow`, `pyan3`, atau membungkus
    `jedi`/`rope` untuk resolusi nama) ketimbang menulis dari nol.
- `pipeline.py`, `schemas.py`, `routes.py`, frontend — sama seperti Opsi B (terima banyak
  file / zip), plus label node sekarang qualified.

**Effort:** besar (beberapa hari, dan rawan kasus tepi). Resolusi tipe untuk method call di
Python yang dinamis tidak pernah 100% akurat tanpa menjalankan kode.

**Kelebihan:**
- Paling akurat & representatif untuk codebase nyata.
- Tidak ada tabrakan nama; edge lintas-modul benar.

**Kekurangan / tradeoff:**
- Kompleksitas & maintenance tinggi; banyak heuristik.
- **Menyimpang paling jauh dari pipeline yang divalidasi di tesis** — perlu re-justifikasi
  bahwa graf hasil analyzer ini setara/lebih baik untuk klaim HCSumm\*.
- Graf besar → tekanan path-enumeration & runtime node2vec paling tinggi.

---

## Ringkasan perbandingan

| Aspek | A. Single-file | B. Multi-file (gabung) | C. Project penuh |
| --- | --- | --- | --- |
| Effort | nol | sedang (~½ hari) | besar (beberapa hari) |
| Perubahan inti pipeline | — | minimal (list of sources) | minimal (label qualified) |
| Perubahan callgraph.py | — | kecil (2-pass multi-file) | tulis ulang (analyzer) |
| Upload (API/FE) | 2 file | banyak file / zip | banyak file / zip |
| Akurasi lintas-file | tidak ada | "by name" (bisa tabrakan) | akurat |
| Risiko path-explosion | rendah | naik | paling tinggi |
| Kesesuaian dgn tesis | persis | netral (asumsi dilaporkan) | perlu re-justifikasi |

---

## Catatan & rekomendasi

- Metode HCSumm\* tidak mengunci granularitas; pilihan ini soal **seberapa "project" unit
  analisis yang kamu mau klaim** di tesis.
- **Jalur paling aman & murah** kalau ingin naik ke level project: **Opsi B**, dengan asumsi
  "fungsi senama lintas-file diperlakukan sebagai satu node" dicatat eksplisit di metodologi,
  dan andalkan guard `max_paths`/`cutoff` untuk graf besar.
- **Opsi C** hanya sepadan kalau memang dituntut akurasi call graph selevel tools static
  analysis — dan siap me-rejustifikasi kesetaraannya dengan pipeline notebook.
- Apa pun yang dipilih, **lapisan setelah call graph (paths → fitur → node2vec → fusion →
  Ward → NPD) tidak perlu berubah** — semuanya sudah bekerja pada `nx.DiGraph` generik.
