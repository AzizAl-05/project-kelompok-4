## Jejak Buku - Sistem Manajemen Perpustakaan Digital - Oleh Kelompok 4
Aplikasi Manajemen Perpustakaan berbasis Web yang dibangun menggunakan Django Framework dan RWD Bootstrap. Project ini dirancang untuk mendigitalisasi proses reservasi buku, pengelolaan stok inventaris, dan pelaporan administrasi secara otomatis.

## Anggota Kelompok
Abdul Aziz Al Palembani (NIM : 0110225118)

M Giza Reifan J (NIM : 0110225149)

Ghifana Adzkia Ahmad (NIM : 0110225044)

Abdul Aziz Alfarizi (NIM : 0110225057)

Sahru Ramadoan (NIM : 0110225046)

--


## 🌟 Fitur Utama

👤 Fitur Member (User)

  Koleksi Buku Dinamis: Menampilkan daftar buku dengan status ketersediaan stok secara real-time.

  Sistem Reservasi: Member dapat melakukan reservasi buku secara online sebelum mengambil fisik buku di perpustakaan.

  Profil Personal: Riwayat peminjaman yang rapi beserta status (Dipinjam/Dikembalikan).

  Cetak Struk Digital: Fitur cetak struk peminjaman instan menggunakan JavaScript Print.

  Fitur Favorit: Simpan buku pilihan ke dalam daftar favorit.


## 🔑 Fitur Admin

  Inventory Management: Stok buku berkurang otomatis saat dipinjam dan bertambah saat dikembalikan.

  Master Reporting (PDF): Export laporan seluruh transaksi peminjaman ke format PDF profesional menggunakan xhtml2pdf.

  Dashboard Admin: Pengelolaan data buku, user, dan transaksi melalui Django Admin.


## 🛠️ Teknologi yang Digunakan

  Backend: Python 3.x & Django Framework

  Frontend: HTML5, CSS3 (Custom), Bootstrap 5

  Database: Default Django

  Library PDF: xhtml2pdf & ReportLab

  Version Control: Git & GitHub

---

**Note!** (Akun Admin)

Username : admin

Password : perpus123

---

## 🚀 Cara Instalasi & Menjalankan Project
1. Download keseluruhan project dengan format zip,

2. Ekstract File, kemudian buka di vs code

   Jalankan terminal dan masukkan perintah ini

   python -m venv venv (Buat Venv dulu)

   Windows:

   venv\Scripts\activate (kemudian aktifkan venv)

   Mac/Linux:

   source venv/bin/activate

   setelah venv aktif cd dulu ke folder project

   cd project-kelompok-4-main (dengan perintah ini)

3. Install Dependencies dengan perintah

   pip install -r requirements.txt

4. Migrasi Database dengan perintah

   python manage.py makemigrations (ini pertama)

   python manage.py migrate (ini kedua)

5. Jalankan Server

   python manage.py runserver

6. Selesai
