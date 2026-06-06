<!-- Slide number: 1 -->
Testing 3: Isolation

### Notes:

<!-- Slide number: 2 -->
Baseline Parameters
EMBED_DIM = 4
WALK_LENGTH = 10
NUM_WALKS = 200
P_RETURN = 1.0
Q_INOUT = 1.0

### Notes:

<!-- Slide number: 3 -->
Parameter Variations
| No | EMBED\_DIM | WALK\_LENGTH | NUM\_WALKS | P\_RETURN | Q\_INOUT | KETERANGAN |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 4 | 10 | 200 | 1.0 | 1.0 | Baseline |
| 2 | 2 | 10 | 200 | 1.0 | 1.0 | Isolasi EMBED\_DIM |
| 3 | 8 | 10 | 200 | 1.0 | 1.0 | Isolasi EMBED\_DIM |
| 4 | 16 | 10 | 200 | 1.0 | 1.0 | Isolasi EMBED\_DIM |
| 5 | 4 | 5 | 200 | 1.0 | 1.0 | Isolasi WALK\_LENGTH |

### Notes:

<!-- Slide number: 4 -->
| No | EMBED\_DIM | WALK\_LENGTH | NUM\_WALKS | P\_RETURN | Q\_INOUT | KETERANGAN |
| --- | --- | --- | --- | --- | --- | --- |
| 6 | 4 | 20 | 200 | 1.0 | 1.0 | Isolasi WALK\_LENGTH |
| 7 | 4 | 40 | 200 | 1.0 | 1.0 | Isolasi WALK\_LENGTH |
| 8 | 4 | 10 | 10 | 1.0 | 1.0 | Isolasi NUM\_WALKS |
| 9 | 4 | 10 | 50 | 1.0 | 1.0 | Isolasi NUM\_WALKS |
| 10 | 4 | 10 | 100 | 1.0 | 1.0 | Isolasi NUM\_WALKS |
| 11 | 4 | 10 | 500 | 1.0 | 1.0 | Isolasi NUM\_WALKS |
| 12 | 4 | 10 | 200 | 0.25 | 1.0 | Isolasi P\_RETURN |

### Notes:

<!-- Slide number: 5 -->
| No | EMBED\_DIM | WALK\_LENGTH | NUM\_WALKS | P\_RETURN | Q\_INOUT | KETERANGAN |
| --- | --- | --- | --- | --- | --- | --- |
| 13 | 4 | 10 | 200 | 0.5 | 1.0 | Isolasi P\_RETURN |
| 14 | 4 | 10 | 200 | 2.0 | 1.0 | Isolasi P\_RETURN |
| 15 | 4 | 10 | 200 | 4.0 | 1.0 | Isolasi P\_RETURN |
| 16 | 4 | 10 | 200 | 1.0 | 0.25 | Isolasi Q\_INOUT |
| 17 | 4 | 10 | 200 | 1.0 | 0.5 | Isolasi Q\_INOUT |
| 18 | 4 | 10 | 200 | 1.0 | 2.0 | Isolasi Q\_INOUT |
| 19 | 4 | 10 | 200 | 1.0 | 4.0 | Isolasi Q\_INOUT |

### Notes:

<!-- Slide number: 6 -->
Metrik Evaluasi Cluster
IntraDist → rata-rata jarak Euclidean antar node dalam cluster yang sama.

### Notes:

<!-- Slide number: 7 -->
Test Case 1 (TC1)
“Branch Expansion”
Test case ini akan merepresentasikan ketika terdapat cabang baru karena fungsi yang lama memanggil fungsi baru. Akibatnya, jumlah jalur eksekusi (EPL) yang melewati node tertentu akan meningkat. Perubahan ini umum terjadi saat penambahan fitur baru dalam perangkat lunak.

### Notes:

<!-- Slide number: 8 -->
TC1
(±15 Nodes, K=2)

![](GoogleShape97p3.jpg)

![](GoogleShape93p3.jpg)
t0
t1

### Notes:

<!-- Slide number: 9 -->
Isolation Summary TC1
Untuk test case ini, param WALK_LENGTH, P_RETURN, dan Q_INOUT tidak berefek sama sekali (sama persis dengan baseline).
Param EMBED_DIM berpengaruh terhadap kerapatan
Semakin kecil dimensi (EMBED_DIM = 2), klaster semakin rapat (IntraDist t0 mengecil dari 0.84 ke 0.61).
Semakin besar dimensi (EMBED_DIM = 16), jarak penyebaran membesar (IntraDist t0 membesar ke 0.97).
Param NUM_WALKS fluktuatif → mungkin karena graf kecil.

### Notes:

<!-- Slide number: 10 -->
Test Case 2 (TC2)
“Deepen Call Chain”
Test case ini merepresentasikan penambahan panjang jalur pemanggilan fungsi, misalnya akibat refactoring atau penambahan layer abstraks sehingga alur eksekusi sebetulnya juga akan bertambah karena adanya node maupun edge baru. Agar dapat mengisolasi kasus penambahan panjang ini, contoh yang dibangkitkan tidak akan terdapat percabangan.

### Notes:

<!-- Slide number: 11 -->
TC2
(±15 Nodes, K=2)
t0

![](GoogleShape118p7.jpg)
t1

![](GoogleShape119p7.jpg)

### Notes:

<!-- Slide number: 12 -->
Isolation Summary TC2
Param WALK_LENGTH kini terlihat berpengaruh.
Untuk program t0: Saat WALK_LENGTH=5, skor IntraDist berubah menjadi 1.185. Tapi saat diset 10 (Baseline), 20, dan 40, hasilnya terkunci di 1.191.
Untuk program t1: Saat WALK_LENGTH=5, skornya 0.951. Saat diset 10, skornya 0.833. Saat diset 20 dan 40, skornya terkunci di 0.814.
Param P_RETURN dan Q_INOUT masih konsisten (hasilnya sama dengan baseline).
Sifat param EMBED_DIM sama dengan TC1.
Param NUM_WALKS terlihat berbanding terbalik dengan kerapatan kluster. Namun saat menyentuh NUM_WALKS ratusan (nilai 200 dan 500), nilainya melandai.

### Notes:

<!-- Slide number: 13 -->
Test Case 3 (TC3)
“Add New Exit Node”
Test case ini menggambarkan penambahan titik akhir baru dalam alur eksekusi, yang menyebabkan distribusi jalur menuju exit node menjadi lebih beragam. Ilustrasinya adalah dengan melakukan percabangan/branching dari TC-02, sehingga variasi kasus untuk TC-01 dan TC-02 sudah lengkap dengan adanya test case ini.

### Notes:

<!-- Slide number: 14 -->
TC3
(±15 Nodes, K=2)
t0

![](GoogleShape142p11.jpg)

![](GoogleShape146p11.jpg)
t1

### Notes:

<!-- Slide number: 15 -->
Isolation Summary TC3
WALK_LENGTH = 5, 10, dan 20 menghasilkan nilai yang berbeda-beda untuk t0 maupun t1
t0: (L=5: 0.955) ➔ (L=10: 0.856) ➔ (L=20: 0.998) ➔ (L=40: 0.998)
t1: (L=5: 0.956) ➔ (L=10: 0.894) ➔ (L=20: 0.920) ➔ (L=40: 0.920)
Kode pada TC3 (t0 maupun t1) memiliki rantai pemanggilan fungsi yang sangat dalam (lebih dari 10 langkah, tetapi kurang dari 20). Menaikkan limit hingga 20 merubah hasil (karena random walk akhirnya bisa menembus sampai ke ujung rantai), tetapi ketika dinaikkan ke 40, hasilnya terkunci (konsisten).
NUM_WALKS berosilasi.
0: 0.679 (W=10) ➔ melompat ke 0.979 (W=50) ➔ perlahan turun dan stabil di 0.878, 0.856, 0.845 (W=100, 200, 500).
t1: 0.673 (W=10) ➔ 0.860 (W=50) ➔ stabil di sekitar 0.923, 0.894, 0.933 (W=100, 200, 500).
Param P_RETURN dan Q_INOUT masih konsisten (hasilnya sama dengan baseline).
Di beberapa eksperimen t1 (tidak ada pola yang clear), pemisahan klusternya sangat baik.

### Notes:

<!-- Slide number: 16 -->
Test Case 4 (TC4)
“Insertion”
Test case ini merepresentasikan penyisipan fungsi (node) baru di tengah jalur yang sudah ada, tanpa mengubah struktur global secara signifikan. Perbedaan test case ini dengan TC-02 adalah jika pada TC-02 penambahan node dan edge dilakukan setelah exit node paling ujung. Sementara pada test case ini, penambahan terjadi di tengah node atau di antara entry node dengan exit node. Walaupun dampaknya mungkin akan sama, karena panjang jalur eksekusi akan bertambah, namun disini akan coba dilihat perilakunya seperti apa.

### Notes:

<!-- Slide number: 17 -->
TC4
(±20 Nodes,
K=2)

![](GoogleShape165p15.jpg)

![](GoogleShape166p15.jpg)
t0
t1

### Notes:

<!-- Slide number: 18 -->
Isolation Summary TC4
Param P_RETURN dan Q_INOUT masih konsisten (hasilnya sama dengan baseline).
NUM_WALKS dan EMBED_DIM idem TC3.
Untuk WALK_LENGTH:
Pada t0: nilai 5, 10, 20, dan 40 menghasilkan nilai yang sama (1.043931). Artinya arsitektur scraper dasar pada t0 sangat dangkal. Fungsi-fungsinya memanggil fungsi lain maksimal tidak lebih dari 5 lapis sebelum eksekusi berakhir.
Pada t1: Tambahan fitur baru memperdalam struktur graf. Terlihat saat WALK_LENGTH=5, skornya 1.046, namun saat dinaikkan ke 10, 20, 40, skornya berubah menjadi 1.057.

### Notes:

<!-- Slide number: 19 -->
Flask
app.py
Version 2.0.0 vs Version 3.1.0

### Notes:

<!-- Slide number: 20 -->

![](GoogleShape189p19.jpg)
Flask
Result
(K=2)

![](GoogleShape188p19.jpg)
t0
t1

### Notes:

<!-- Slide number: 21 -->
Isolation Summary Flask
Param P_RETURN tiba-tiba ada pengaruhnya, namun terlihat fluktuatif.
Param Q_INOUT masih konsisten, tetap sama dengan baseline (obsolete).
WALK_LENGTH cukup fluktuatif.
Note: beberapa fungsi di Flask itu tunggal (tidak terhubung ke node lain, sehingga terlepas dari graf).

### Notes:

<!-- Slide number: 22 -->
(Python) Datasets
Django (github.com/django/django)
FastAPI (github.com/fastapi/fastapi)
Tornado (github.com/tornadoweb/tornado)
Requests (github.com/psf/requests)
Celery (github.com/celery/celery)
Scikit-Learn (github.com/scikit-learn/scikit-learn)
Pandas (github.com/pandas-dev/pandas)

### Notes: