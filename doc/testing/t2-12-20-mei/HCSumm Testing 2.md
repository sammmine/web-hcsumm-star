<!-- Slide number: 1 -->
Testing 2

### Notes:

<!-- Slide number: 2 -->
Test Case 1 (TC1)
“Branch Expansion”
Test case ini akan merepresentasikan ketika terdapat cabang baru karena fungsi yang lama memanggil fungsi baru. Akibatnya, jumlah jalur eksekusi (EPL) yang melewati node tertentu akan meningkat. Perubahan ini umum terjadi saat penambahan fitur baru dalam perangkat lunak.

### Notes:

<!-- Slide number: 3 -->
TC1
(±15 Nodes, K=2)

![](GoogleShape69p15.jpg)

![](GoogleShape65p15.jpg)
t0
t1

### Notes:

<!-- Slide number: 4 -->
TC1 Result
t0 Summary Graph
t1 Summary Graph

![](GoogleShape78p16.jpg)

![](GoogleShape79p16.jpg)

### Notes:

<!-- Slide number: 5 -->
TC1 NPD Result

![](GoogleShape85p17.jpg)

### Notes:

<!-- Slide number: 6 -->
Test Case 2 (TC2)
“Deepen Call Chain”
Test case ini merepresentasikan penambahan panjang jalur pemanggilan fungsi, misalnya akibat refactoring atau penambahan layer abstraks sehingga alur eksekusi sebetulnya juga akan bertambah karena adanya node maupun edge baru. Agar dapat mengisolasi kasus penambahan panjang ini, contoh yang dibangkitkan tidak akan terdapat percabangan.

### Notes:

<!-- Slide number: 7 -->
TC2
(±15 Nodes, K=2)
t0

![](GoogleShape99p19.jpg)
t1

![](GoogleShape100p19.jpg)

### Notes:

<!-- Slide number: 8 -->

![](GoogleShape114p20.jpg)

![](GoogleShape115p20.jpg)
     TC2 Result
t0 Summary Graph
t1 Summary Graph

### Notes:

<!-- Slide number: 9 -->
TC2 NPD Result

![](GoogleShape121p21.jpg)

### Notes:

<!-- Slide number: 10 -->
Test Case 3 (TC3)
“Add New Exit Node”
Test case ini menggambarkan penambahan titik akhir baru dalam alur eksekusi, yang menyebabkan distribusi jalur menuju exit node menjadi lebih beragam. Ilustrasinya adalah dengan melakukan percabangan/branching dari TC-02, sehingga variasi kasus untuk TC-01 dan TC-02 sudah lengkap dengan adanya test case ini.

### Notes:

<!-- Slide number: 11 -->
TC3
(±15 Nodes, K=2)
t0

![](GoogleShape132p23.jpg)

![](GoogleShape136p23.jpg)
t1

### Notes:

<!-- Slide number: 12 -->

![](GoogleShape144p24.jpg)

![](GoogleShape145p24.jpg)
     TC3 Result
t0 Summary Graph
t1 Summary Graph

### Notes:

<!-- Slide number: 13 -->
TC3 NPD Result

![](GoogleShape152p25.jpg)

### Notes:

<!-- Slide number: 14 -->
Test Case 4 (TC4)
“Insertion”
Test case ini merepresentasikan penyisipan fungsi (node) baru di tengah jalur yang sudah ada, tanpa mengubah struktur global secara signifikan. Perbedaan test case ini dengan TC-02 adalah jika pada TC-02 penambahan node dan edge dilakukan setelah exit node paling ujung. Sementara pada test case ini, penambahan terjadi di tengah node atau di antara entry node dengan exit node. Walaupun dampaknya mungkin akan sama, karena panjang jalur eksekusi akan bertambah, namun disini akan coba dilihat perilakunya seperti apa.

### Notes:

<!-- Slide number: 15 -->
TC4
(±20 Nodes,
K=2)

![](GoogleShape164p27.jpg)

![](GoogleShape165p27.jpg)
t0
t1

### Notes:

<!-- Slide number: 16 -->
TC4 Result
t0 Summary Graph
t1 Summary Graph

![](GoogleShape177p28.jpg)

![](GoogleShape176p28.jpg)

### Notes:

<!-- Slide number: 17 -->
TC4 NPD Result

![](GoogleShape183p29.jpg)

### Notes:

<!-- Slide number: 18 -->
Flask
app.py
Version 2.0.0 vs Version 3.1.0

### Notes:

<!-- Slide number: 19 -->

![](GoogleShape197p31.jpg)
Flask
Result
(K=2)

![](GoogleShape196p31.jpg)
t0
t1

### Notes:

<!-- Slide number: 20 -->
Flask
Result

![](GoogleShape203p32.jpg)
t0
t1

![](GoogleShape202p32.jpg)

### Notes:

<!-- Slide number: 21 -->
Flask NPD Result

![](GoogleShape212p33.jpg)

### Notes: