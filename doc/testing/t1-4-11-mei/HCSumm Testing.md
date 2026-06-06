<!-- Slide number: 1 -->
Testing

### Notes:

<!-- Slide number: 2 -->
Test Case 1 (TC1)
“Branch Expansion”

### Notes:

<!-- Slide number: 3 -->
Scenario TC1
Test case ini akan merepresentasikan ketika terdapat cabang baru karena fungsi yang lama memanggil fungsi baru. Akibatnya, jumlah jalur eksekusi (EPL) yang melewati node tertentu akan meningkat. Perubahan ini umum terjadi saat penambahan fitur baru dalam perangkat lunak.

### Notes:

<!-- Slide number: 4 -->
First Test (TC1)
(±15 Nodes, K=3)

![](GoogleShape74p16.jpg)

![](GoogleShape70p16.jpg)
t0
t1

### Notes:

<!-- Slide number: 5 -->
Result (TC1)
t0 Summary Graph
t1 Summary Graph

![](GoogleShape83p17.jpg)

![](GoogleShape84p17.jpg)

### Notes:

<!-- Slide number: 6 -->
Test Case 2 (TC2)
“Deepen Call Chain”

### Notes:

<!-- Slide number: 7 -->
Scenario TC2
Test case ini merepresentasikan penambahan panjang jalur pemanggilan fungsi, misalnya akibat refactoring atau penambahan layer abstraks sehingga alur eksekusi sebetulnya juga akan bertambah karena adanya node maupun edge baru. Agar dapat mengisolasi kasus penambahan panjang ini, contoh yang dibangkitkan tidak akan terdapat percabangan.

### Notes:

<!-- Slide number: 8 -->
First Test (TC2-1)
(±15 Nodes, K=2)
t0

![](GoogleShape103p20.jpg)
t1

![](GoogleShape104p20.jpg)

### Notes:

<!-- Slide number: 9 -->

![](GoogleShape118p21.jpg)

![](GoogleShape119p21.jpg)
      Result (TC2-1)
t0 Summary Graph
t1 Summary Graph

### Notes:

<!-- Slide number: 10 -->
Second Test (TC2-2)
(Same test file, but K=3)
t0

![](GoogleShape127p22.jpg)
t1

![](GoogleShape128p22.jpg)

### Notes:

<!-- Slide number: 11 -->

![](GoogleShape143p23.jpg)
      Result (TC2-2)

![](GoogleShape142p23.jpg)
t0 Summary Graph
t1 Summary Graph

### Notes:

<!-- Slide number: 12 -->
Test Case 3 (TC3)
“Add New Exit Node”

### Notes:

<!-- Slide number: 13 -->
Scenario TC3
Test case ini menggambarkan penambahan titik akhir baru dalam alur eksekusi, yang menyebabkan distribusi jalur menuju exit node menjadi lebih beragam. Ilustrasinya adalah dengan melakukan percabangan/branching dari TC-02, sehingga variasi kasus untuk TC-01 dan TC-02 sudah lengkap dengan adanya test case ini.

### Notes:

<!-- Slide number: 14 -->
First Test (TC3)
(±15 Nodes, K=3)
t0

![](GoogleShape159p26.jpg)

![](GoogleShape163p26.jpg)
t1

### Notes:

<!-- Slide number: 15 -->

![](GoogleShape171p27.jpg)

![](GoogleShape172p27.jpg)
      Result (TC3)
t0 Summary Graph
t1 Summary Graph

### Notes:

<!-- Slide number: 16 -->
Test Case 4 (TC4)
“Insertion”

### Notes:

<!-- Slide number: 17 -->
Scenario TC4
Test case ini merepresentasikan penyisipan fungsi (node) baru di tengah jalur yang sudah ada, tanpa mengubah struktur global secara signifikan. Perbedaan test case ini dengan TC-02 adalah jika pada TC-02 penambahan node dan edge dilakukan setelah exit node paling ujung. Sementara pada test case ini, penambahan terjadi di tengah node atau di antara entry node dengan exit node. Walaupun dampaknya mungkin akan sama, karena panjang jalur eksekusi akan bertambah, namun disini akan coba dilihat perilakunya seperti apa.

### Notes:

<!-- Slide number: 18 -->
First Test (TC4-1)
(±20 Nodes,
Medium Complexity,
K=3)

![](GoogleShape190p30.jpg)

![](GoogleShape191p30.jpg)
t0
t1

### Notes:

<!-- Slide number: 19 -->
Result (TC4-1)
t0 Summary Graph
t1 Summary Graph

![](GoogleShape203p31.jpg)

![](GoogleShape202p31.jpg)

### Notes:

<!-- Slide number: 20 -->

![](GoogleShape211p32.jpg)

![](GoogleShape212p32.jpg)
Second (TC4-2)
(±100 Nodes,
Medium Complexity,
K=5,
EMBED_DIM=16)
t0
t1

### Notes:

<!-- Slide number: 21 -->
Result (TC4-2)
t0 Summary Graph

![](GoogleShape223p33.jpg)
t1 Summary Graph

![](GoogleShape219p33.jpg)

### Notes:

<!-- Slide number: 22 -->
Test Case 5 (TC5)
“Pruning”

### Notes:

<!-- Slide number: 23 -->
Scenario TC5
Test case ini menggambarkan penghapusan node atau edge, misalnya akibat optimasi atau penghapusan fitur yang sangat sering terjadi dalam pengembangan perangkat lunak. Kondisi yang akan disimulasikan adalah penghapusan branching yang menyebabkan hilangnya node dan juga edge.

### Notes:

<!-- Slide number: 24 -->
First Test (TC5)
(Kebalikan dari TC1, ±15 Nodes, K=3)

![](GoogleShape239p36.jpg)

![](GoogleShape242p36.jpg)
t0
t1

### Notes:

<!-- Slide number: 25 -->
Result (TC5)
t1 Summary Graph

![](GoogleShape252p37.jpg)
t0 Summary Graph

![](GoogleShape255p37.jpg)

### Notes: