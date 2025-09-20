# scrape_hackerrank_final_lengkap.py
# Versi final dengan output CSV yang sempurna (kolom terpisah + ada waktu).

import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ---------- KONFIGURASI ----------
CONTEST_URL = "https://www.hackerrank.com/contests/praktikum-daspro-2025-minggu-3/leaderboard"
USERNAME_PREFIX = "F2" 
OUTPUT_CSV = "hasil_F2_lengkap.csv"
# -----------------------------------

def start_driver(headless=True):
    """Mempersiapkan dan memulai browser Selenium."""
    opts = Options()
    if headless:
        opts.add_argument("--headless")
        opts.add_argument("--disable-gpu")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--window-size=1200,900")
    opts.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=opts)
    return driver

def scrape_leaderboard_with_find(driver):
    """
    Fungsi utama untuk scrape leaderboard dengan logika "Ctrl+F" di setiap halaman.
    """
    base_url = CONTEST_URL.rstrip('/')
    wait = WebDriverWait(driver, 15)
    filtered_results = []
    page_num = 1
    
    print(f"Mengunjungi halaman utama untuk menangani cookie...")
    driver.get(base_url)
    try:
        ok_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.cookie-accept-btn")))
        ok_button.click()
        print("✅ Banner cookie ditutup.")
    except TimeoutException:
        print("Banner cookie tidak ditemukan, lanjut.")

    while True:
        current_url = base_url if page_num == 1 else f"{base_url}/{page_num}"
        if page_num > 1:
            driver.get(current_url)

        print(f"Menganalisis Halaman {page_num}...")

        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.leaderboard-row")))
        except TimeoutException:
            print("\n>> Konten leaderboard tidak ditemukan. Kemungkinan sudah mencapai halaman terakhir.")
            break

        page_content = driver.page_source
        if USERNAME_PREFIX not in page_content:
            print(f"   Prefix '{USERNAME_PREFIX}' tidak ditemukan di halaman ini. Lanjut ke halaman berikutnya.")
            page_num += 1
            time.sleep(0.5)
            continue

        print(f"   ✅ Prefix '{USERNAME_PREFIX}' DITEMUKAN! Memproses data di halaman ini...")
        soup = BeautifulSoup(page_content, "html.parser")
        leaderboard_rows = soup.select("div.leaderboard-row")

        if not leaderboard_rows:
            print(">> Baris leaderboard kosong. Proses scraping selesai.")
            break

        found_on_page = 0
        for row in leaderboard_rows:
            cols = row.select("div[class*='span-flex-']")
            # Pastikan ada cukup kolom untuk mengambil waktu (minimal 5 div)
            if len(cols) >= 5:
                username = cols[1].get_text(strip=True)
                if username.startswith(USERNAME_PREFIX):
                    score = cols[3].get_text(strip=True)
                    # --- PENAMBAHAN: Ambil data waktu dari kolom ke-5 (indeks 4) ---
                    time_taken = cols[4].get_text(strip=True)
                    
                    filtered_results.append({
                        "username": username,
                        "score": score,
                        "time": time_taken  # Tambahkan waktu ke hasil
                    })
                    found_on_page += 1
        
        print(f"   -> Selesai, ditemukan {found_on_page} data yang cocok di halaman ini.")
        page_num += 1
        time.sleep(0.5)

    return filtered_results

def main():
    """Fungsi utama untuk menjalankan seluruh proses."""
    print(f"=== Scraper Cerdas dengan Filter '{USERNAME_PREFIX}' ===")
    driver = None
    try:
        driver = start_driver(headless=False)
        final_results = scrape_leaderboard_with_find(driver)
        
        if final_results:
            print(f"\nProses selesai. Total ditemukan {len(final_results)} peserta dengan prefix '{USERNAME_PREFIX}'.")
            df = pd.DataFrame(final_results)
            
            # --- PERUBAHAN: Gunakan titik koma (;) sebagai pemisah agar kolom di Excel benar ---
            df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8", sep=';')
            
            print(f"✅ Data berhasil disimpan ke file: {OUTPUT_CSV}")
        else:
            print(f"\nTidak ada data yang cocok dengan prefix '{USERNAME_PREFIX}' yang ditemukan di seluruh leaderboard.")
            
    except Exception as e:
        print(f"\n❌ Terjadi error tak terduga: {e}")
    finally:
        if driver:
            driver.quit()
            print("Browser telah ditutup.")

if __name__ == "__main__":
    main()