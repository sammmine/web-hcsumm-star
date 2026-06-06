Deskripsi

*Test case* yang disusun untuk melakukan pengujian perilaku sebagai berikut:

1. *Branch expansion* (TC-01)

*Test case* ini akan merepresentasikan ketika terdapat cabang baru karena fungsi yang lama memanggil fungsi baru. Akibatnya, jumlah jalur eksekusi yang melewati node tertentu akan meningkat. Perubahan ini umum terjadi saat penambahan fitur baru dalam perangkat lunak.

2. *Deepen call chain* (TC-02)

*Test case* ini merepresentasikan penambahan panjang jalur pemanggilan fungsi, misalnya akibat refactoring atau penambahan layer abstraks sehingga alur eksekusi sebetulnya juga akan bertambah karena adanya node maupun edge baru. Agar dapat mengisolasi kasus penambahan panjang ini, contoh yang dibangkitkan tidak akan terdapat percabangan.

3. *Add new exit node* (TC-03)

*Test case* ini menggambarkan penambahan titik akhir baru dalam alur eksekusi, yang menyebabkan distribusi jalur menuju exit node menjadi lebih beragam. Ilustrasinya adalah dengan melakukan percabangan/*branching* dari TC-02, sehingga variasi kasus untuk TC-01 dan TC-02 sudah lengkap dengan adanya *test case* ini.

4. *Insertion* (TC-04)

*Test case* ini merepresentasikan penyisipan fungsi baru di tengah jalur yang sudah ada, tanpa mengubah struktur global secara signifikan. Perbedaan *test case* ini dengan TC-02 adalah jika pada TC-02 penambahan node dan edge dilakukan setelah exit node paling ujung. Sementara pada *test case* ini, penambahan terjadi di tengah node atau di antara *entry* node dengan *exit* node. Walaupun dampaknya mungkin akan sama, karena panjang jalur eksekusi akan bertambah, namun disini akan coba dilihat perilakunya seperti apa.

5. *Pruning* (TC-05)

*Test case* ini menggambarkan penghapusan node atau edge, misalnya akibat optimasi atau penghapusan fitur yang sangat sering terjadi dalam pengembangan perangkat lunak. Kondisi yang akan disimulasikan adalah penghapusan *branching* yang menyebabkan hilangnya node dan juga edge.