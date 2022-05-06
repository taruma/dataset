# DATASET BMKG

Penyimpanan [Data Online Pusat Database - BMKG](https://dataonline.bmkg.go.id/) berbentuk [HDF5] dan [pandas].

## Metode Kompilasi Data

Metode pengambilan data dilakukan dengan manual (melalui website). Proses yang dilakukan berupa:

- Membuka halaman ketersediaan data, periksa kelengkapan data dari tahun berapa. Tanggal awal selalu diambil dari 1 Januari dengan tahun dimana data mulai tersedia. Ketersediaan data mengacu pada data hujan (RR). Proses ini memakan waktu karena dilakukan secara manual dan tidak menggunakan _script_. 
- Pembacaan data dan kompilasi menggunakan python dengan bantuan paket [hidrokit] untuk mengekstrak tabel dari berkas excel bmkg.
- Verifikasi dan Validasi metadata database dengan metadata berkas. Produk tahapan ini yaitu `/metadata/database` dan `/metadata/files`.
- Tabel setiap stasiun kemudian digabungkan jika terpisah dan disimpan dalam bentuk koleksi _dictionary_ yang kemudian akan disimpan sebagai masing-masing _key_ di grup `/stations/`. Produk tahapan ini yaitu `/info/compile_files`.
- Setelah itu semua data diperiksa kelengkapannya, untuk memeriksa kesesuaian rentang tanggal awal dan akhir. Produk tahapan ini yaitu `/info/data`.
- Setelah informasi metadata dan berkas terkumpul, disimpan dalam bentuk format [HDF5] dengan [struktur file](#struktur-file) yang telah ditetapkan. 


## Mengapa dalam bentuk format HDF5?

Alasan untuk mengubah data dalam bentuk HDF5 dibandingkan dalam bentuk Excel atau CSV dikarenakan kemudahan distribusi dan kemudahan untuk memulai analisis. Format HDF5 memudahkan untuk mendistribusikan banyaknya tabel/data dalam bentuk satu berkas. 

Meski saat ini, data bmkg yang diperoleh masih tergolong kecil (sekitar 50 MB (compressed=1) atau 200 MB (uncompressed)), format HDF5 bisa memberikan ide atau gambaran kemudahan distribusi data untuk analisis.  

Berikut artikel mengenai HDF5: [Hierarchical Data Formats - What is HDF5?](https://www.neonscience.org/resources/learning-hub/tutorials/about-hdf5#:~:text=Supports%20Large%2C%20Complex%20Data%3A%20HDF5,the%20computers%20memory%20or%20RAM.).


## Penggunaan

Untuk mengekstrak data di `.h5`, gunakan paket `pandas` untuk membaca berkas dengan keterangan `*_pandas.h5`. Untuk kemudahan pembacaan, akan saya tambahkan fungsi di modul `hidrokit.contrib.taruma.hk73` untuk membaca berkas ini di versi >= 0.4.1.

Mengingatkan untuk melakukan **VERIFIKASI DAN VALIDASI DATA DI SETIAP STASIUN**.

## Struktur File

Pada berkas `data_bmkg_2021_pandas.h5` memiliki 3 grup utama yaitu:

- `/metadata/` (group): Berisikan informasi metadata seperti informasi nomor stasiun, nama stasiun, dll. Terdapat __dua__ _key_ pada grup ini yaitu:

    - `/metadata/database`: berisikan informasi metadata yang diperoleh dari database BMKG. Proses ini dilakukan secara manual. 

        - `id_stat` (index): ID Stasiun
        - `name_stat`: Nama Stasiun
        - `type_stat`: Tipe Stasiun
        - `region`: Wilayah Administrasi
        - `provinsi`: Provinsi
        - `kabupaten`: Kabupaten Lokasi Stasiun
        - `lintang_derajat`: Lintang Derajat
        - `bujur_derajat`: Bujur Derajat

    - `/metadata/files`: berisikan informasi metadata yang diperoleh dari berkas `laporan_iklam_harian.xlsx`. Informasi tersebut ada di 5 baris pertama setiap berkas.

        - `ID WMO` (index): ID Stasiun
        - `Nama Stasiun`: Nama Stasiun
        - `Lintang`: Lintang Derajat
        - `Bujur`: Bujur Derajat
        - `Elevasi`: Elevasi

- `/info/` (group): Berisikan informasi mengenai isian berkas. Terdapat __dua__ _key_ pada grup ini yaitu:

    - `/info/compile_files`: informasi saat proses kompilasi berbagai berkas dalam satu berkas tunggal HDF5.

        - `stat_id` (index): ID Stasiun
        - `stat_name`: Nama Stasiun
        - `prov`: Provinsi
        - `year_start`: Tahun dimulainya data di berkas
        - `year_end`: Tahun akhirnya data di berkas
        - `file_name`: Nama berkas

    - `/info/data`: informasi umum mengenai baris data yang tersedia.

        - `stat_id` (index): ID Stasiun
        - `name_stat`: Nama Stasiun
        - `prov`: Provinsi
        - `year_start`: Tanggal dimulainya data di berkas
        - `year_end`: Tanggal akhirnya data di berkas
        - `days`: Jumlah hari
        - `months`: Jumlah bulan
        - `years`: Jumlah Tahun
        - `path_h5`: _Key_ pada berkas `.h5`

- `/stations/` (group): Berisikan data meteorologi dan klimatologi untuk setiap stasiun. Berikut penamaan _key_ di dalam grup ini:

    - `/stations/sta{id_stasiun}`: berisikan `pandas.DataFrame` dengan kolom:
        
        - (index): Tanggal
        - `Tn`: Temperatur minimum (°C)
        - `Tx`: Temperatur maksimum (°C)
        - `Tavg`: Temperatur rata-rata (°C)
        - `RH_avg`: Kelembapan rata-rata (%)
        - `RR`: Curah hujan (mm)
        - `ss`: Lamanya penyinaran matahari (jam)
        - `ff_x`: Kecepatan angin maksimum (m/s)
        - `ddd_x`: Arah angin saat kecepatan maksimum (°)
        - `ff_avg`: Kecepatan angin rata-rata (m/s)
        - `ddd_car`: Arah angin terbanyak (°)

    - Contoh penggunaannya untuk stasiun "Pos Pengamatan Kahang-Kahang" itu memiliki `id_stasiun = 97234`, maka key yang digunakan `/stations/sta97234`. Informasi id stasiun bisa diperoleh melalui tabel di `/metadata/`. 

    - Berikut keterangan tambahan mengenai nilai di dalam tabel (tersedia di setiap berkas excel):

        - `8888`: data tidak terukur.
        - `9999`: Tidak ada data (tidak dilakukan pengukuran).

Berikut lokasi stasiun yang tersedia di dalam dataset (180 stasiun dari total 191 stasiun):

![image](https://user-images.githubusercontent.com/1007910/164337266-aca7b6ac-87b7-4877-8b89-69d8edd9b64b.png)


<!-- LINK -->
[hidrokit]: https://github.com/hidrokit/hidrokit
[pandas]: https://github.com/pandas-dev/pandas
[HDF5]: https://www.hdfgroup.org/
