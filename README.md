# Image Merger & Auto-Splitter

Aplikasi desktop ringan berbasis Python dan Tkinter untuk menggabungkan banyak gambar secara vertikal sekaligus memecahnya otomatis berdasarkan batas tinggi maksimal (*max height*). Sangat cocok untuk menyusun *webtoon*, komik strip, katalog produk, atau *moodboard*.

## Fitur Utama
* **Antarmuka Visual (GUI):** Atur folder, dimensi, format, dan kualitas langsung tanpa perlu menyentuh kode.
* **Natural Sorting:** Mengurutkan nama file secara cerdas (`1.jpg`, `2.jpg`, `10.jpg`) sehingga urutan panel tidak berantakan.
* **Auto-Resize Proporsional:** Menyamakan lebar seluruh gambar secara otomatis tanpa merusak rasio aspek (*aspect ratio*).
* **Auto-Splitting:** Memecah hasil gabungan menjadi beberapa file secara otomatis jika tinggi kanvas melebihi batas yang ditentukan.
* **Dukungan Multi-Format:** Mendukung input `.jpg`, `.jpeg`, `.webp`, dan `.png`, dengan opsi output `WEBP`, `JPEG`, atau `PNG`.

## Prasyarat & Instalasi

Pastikan Python 3.x sudah terinstal di komputer Anda.

1. **Clone repository ini:**
   ```bash
   git clone [https://github.com/username-kamu/nama-repo-kamu.git](https://github.com/username-kamu/nama-repo-kamu.git)
   cd nama-repo-kamu