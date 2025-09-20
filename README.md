# Scraper Leaderboard HackerRank (khusus F2)
MADE BY: ASPRAK DASPROO F2 UNDIP - ANNIS

Ini adalah skrip Python yang berfungsi untuk melakukan *scraping* data dari leaderboard sebuah kontes di HackerRank dan menyimpannya ke dalam file CSV. Skrip ini dirancang untuk menargetkan dan mengambil data pengguna yang namanya diawali dengan prefix tertentu (contoh: "F2"). 

## Fitur Utama
- **Scraping Cerdas**: Menggunakan logika "Ctrl+F" untuk memeriksa setiap halaman leaderboard. Skrip hanya akan memproses halaman yang mengandung username yang dicari, membuatnya sangat efisien.
- **Navigasi Otomatis**: Secara otomatis berpindah dari satu halaman leaderboard ke halaman berikutnya sampai selesai.
- **Penanganan Cookie**: Mampu menutup banner persetujuan cookie yang terkadang menghalangi konten.
- **Output Terformat**: Menyimpan hasil (username, skor, dan waktu) ke dalam file `.csv` dengan format yang rapi dan kolom yang terpisah.

## Kebutuhan (Dependencies)
- Python 3.x
- Selenium
- Pandas
- BeautifulSoup4
- Webdriver Manager

## Cara Instalasi
1.  Clone repository ini ke komputer Anda.
    ```bash
    git clone [https://github.com/anniszkk/hackerrank-scraper.git](https://github.com/anniszkk/hackerrank-scraper.git)
    ```
2.  Masuk ke direktori proyek.
    ```bash
    cd hackerrank-scraper
    ```
3.  (Sangat direkomendasikan) Buat dan aktifkan *virtual environment*.
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```
4.  Install semua *library* yang dibutuhkan dengan satu perintah:
    ```bash
    pip install -r requirements.txt
    ```

## Cara Menjalankan
1.  Buka file skrip `.py` (contoh: `scrape_hackerrank_final_lengkap.py`).
2.  Sesuaikan variabel di bagian **KONFIGURASI** di bagian atas file, seperti `CONTEST_URL`, `USERNAME_PREFIX`, dan `OUTPUT_CSV`.
3.  Jalankan skrip dari terminal:
    ```bash
    python nama_file_skrip_anda.py
    ```
