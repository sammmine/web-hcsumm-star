Spesifikasi Proyek Web HCSumm*
Latar Belakang
Proyek ini merupakan lanjutan dari implementasi algoritma HCSumm* yang
*
menggunakan directed node2vec (𝑒(𝑣)) dan fitur behaviour (𝑓 (𝑣)) berbasis call path untuk
merangkum evolusi call graph antara dua titik waktu (t0 → t1). Kualitas summarization diukur
menggunakan beberapa varian NPD (Network Portrait Divergence) berbasis Jensen-Shannon
Divergence. Saat ini pipeline dijalankan melalui file notebook (ipynb). Tujuan proyek ini adalah
mengemas pipeline tersebut menjadi aplikasi web interaktif yang memungkinkan eksplorasi
parameter dan visualisasi hasil secara langsung.
Tujuan
● Membuat antarmuka berbasis web untuk menjalankan pipeline HCSumm* tanpa perlu
membuka notebook
● Memungkinkan pengguna mengupload call graph t0 dan t1, mengatur parameter, dan
melihat hasil clustering beserta visualisasinya
● Mendukung eksperimen isolasi parameter (OFAT) melalui UI
● Menyediakan mode perbandingan t0 vs t1 dengan indexing cluster yang konsisten
Tenggat Proyek
Proyek diharapkan selesai di akhir bulan Juli 2026.
Fitur
1. Upload File
● Web dapat mendukung pengunggahan dua versi kode program (t0 dan t1).
● Format file yang didukung hanya file python (.py).

2. Konfigurasi Kluster dan Parameter
●  Pengguna dapat mengatur semua parameter pipeline.
○  Parameter Node2Vec:
| Parameter    | Default  | Keterangan                    |
| ------------ | -------- | ----------------------------- |
| EMBED_DIM    | 4        | Dimensi embedding vektor      |
| WALK_LENGTH  | 10       | Panjang random walk           |
| NUM_WALKS    | 200      | Jumlah walk per node          |
| P_RETURN     | 1.0      | Probabilitas kembali ke node  |
sebelumnya
| Q_INOUT  | 1.0  | Kontrol eksplorasi lokal vs global  |
| -------- | ---- | ----------------------------------- |
| SEED     | 42   | Seed untuk reproduktifitas          |

○  Parameter Behaviour:
| Pilihan Preset      |     | Fitur Aktif                 |
| ------------------- | --- | --------------------------- |
| baseline_current    |     | EPL, indeg, outdeg, depth   |
| full_with_pagerank  |     | EPL, indeg, outdeg, depth,  |
PageRank
| without_EPL     |     | indeg, outdeg, depth, PageRank  |
| --------------- | --- | ------------------------------- |
| without_indeg   |     | EPL, outdeg, depth, PageRank    |
| without_outdeg  |     | EPL, indeg, depth, PageRank     |
| without_depth   |     | EPL, indeg, outdeg, PageRank    |
| pagerank_only   |     | PageRank                        |
| EPL_only        |     | EPL                             |

Deskripsi masing-masing parameter behaviour:

| Parameter  | Deskripsi                              |     |     |
| ---------- | -------------------------------------- | --- | --- |
| EPL        | Rata-rata panjang execution path yang  |     |     |
melewati node tersebut, diukur dari entry
node sampai exit node.
indeg (In-degree)  Jumlah fungsi lain yang memanggil node ini.
outdeg (Out-degree)  Jumlah fungsi lain yang dipanggil oleh node
ini.
| Depth  | Jarak terpendek dari entry node ke node ini  |     |     |
| ------ | -------------------------------------------- | --- | --- |
di dalam call graph.
| PageRank  | Skor "kepentingan" node berdasarkan  |     |     |
| --------- | ------------------------------------ | --- | --- |
struktur graph secara global.

○  Parameter Clustering:
| Parameter   |     | Keterangan             |     |
| ----------- | --- | ---------------------- | --- |
| K_CLUSTERS  |     | Jumlah cluster target  |     |

3. Mode Embedding
●  Pengguna dapat memilih satu dari tiga mode sebelum menjalankan pipeline.
| Mode           | 𝑥(𝑣) yang digunakan  |     | Deskripsi             |
| -------------- | -------------------- | --- | --------------------- |
| Node2Vec Only  | 𝑥 = 𝑒'(𝑣)            |     | Embedding hanya dari  |
node2vec, tanpa fitur
behaviour
*
| Behaviour Only  | 𝑥 = 𝑓 (𝑣)  |     | Embedding hanya dari fitur  |
| --------------- | ---------- | --- | --------------------------- |
behaviour
| Combined/Fused  |                  | *         | Fusion kedua fitur  |
| --------------- | ---------------- | --------- | ------------------- |
|                 | 𝑥 = 𝑓𝑢𝑠𝑒(𝑒'(𝑣),𝑓 | (𝑣),α,β)  |                     |

●  Pilihan mode tersebut mempengaruhi parameter mana saja yang aktif di form
konfigurasi (parameter yang tidak relevan akan di-disable otomatis).

4. Mode Visualisasi Hasil
●
Pengguna dapat memilih mode tampilan hasil.
| Mode View    | Deskripsi                                  |     |
| ------------ | ------------------------------------------ | --- |
| Direct View  | Hanya menampilkan summary graph t0 dan t1  |     |
langsung setelah pipeline selesai, disertai tabel
keanggotaan cluster.
| Step-by-Step  | Menampilkan hasil dari tiap tahap pipeline.  |     |
| ------------- | -------------------------------------------- | --- |
Cluster Iteration  Menampilkan visualisasi* proses Ward Clustering
| Visualization  | pada tiap iterasi.  |     |
| -------------- | ------------------- | --- |

*Perlu dilakukannya cluster indexing untuk mempermudah visualisasi kluster.

5. Evaluasi NPD
●  Berikut merupakan metrik NPD yang tersedia.
| Metrik  | Kapan Dihitung  | Deskripsi Singkat  |
| ------- | --------------- | ------------------ |
Original NPD  Sebelum & sesudah  Portrait berbasis shortest-path
|     | clustering  | neighbourhood  |
| --- | ----------- | -------------- |
EP-NPD  Sebelum clustering  Portrait berbasis execution path
function-level 𝑃(𝑙, 𝑘)
Cluster-EP-NPD  Setelah clustering  Path diproyeksikan ke cluster,
| (compressed)    |                     | duplikat berurutan dihapus  |
| --------------- | ------------------- | --------------------------- |
| Cluster-EP-NPD  | Setelah clustering  | Sama tapi duplikat          |
| (uncompressed)  |                     | dipertahankan (diagnostic)  |
Dual-Length  Setelah clustering  Portrait gabungan 𝑃(𝑙𝑜, 𝑙𝑐, 𝑘) —
| Cluster-EP-NPD  |     | panjang original + panjang  |
| --------------- | --- | --------------------------- |
cluster

●
Tabel ringkasan NPD ditampilkan setelah pipeline selesai.

6. Side-by-Side Comparison t0 vs t1
● Menampilkan summary graph t0 dan t1 berdampingan. Perlu dilakukannya
cluster indexing untuk mempermudah visualisasi kluster.
Spesifikasi Lainnya
1. Tech Stack (Rekomendasi Kakas)
Layer Pilihan
Frontend React + Vite atau Next.js
Graph Visualization Cytoscape.js atau react-force-graph
Backend FastAPI (Python) — pipeline notebook dapat langsung
dipakai
Deploy Ditentukan kemudian
2. Github Repository
hps://github.com/sammmine/web-hcsumm-star