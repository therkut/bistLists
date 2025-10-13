import time
import logging
from typing import List, Dict
import requests
from bs4 import BeautifulSoup
from src.update_csv import update_csv

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

STOCK_URLS = {
    "XU030": "https://oyakyatirim.com.tr/piyasa-verileri/XU030",
    "XU050": "https://oyakyatirim.com.tr/piyasa-verileri/XU050",
    "XU100": "https://oyakyatirim.com.tr/piyasa-verileri/XU100"
}

CSV_PATHS = {
    "XU030": "data/stock_xu030_data.csv",
    "XU050": "data/stock_xu050_data.csv",
    "XU100": "data/stock_xu100_data.csv"
}

SLEEP_SECONDS = 2

def fetch_stock_data_from_url(url: str) -> List[Dict[str, str]]:
    """Belirtilen URL'den hisse verisini çeker ve dict listesi döner."""
    response = requests.get(url)
    response.raise_for_status()  # HTTP hatalarını yakalar

    soup = BeautifulSoup(response.content, 'html.parser')
    portlet_box = soup.find('div', class_='portlet box green')
    if not portlet_box:
        raise ValueError("HTML içinde 'portlet box green' bulunamadı.")

    table = portlet_box.find('table')
    if not table:
        raise ValueError("'portlet box green' içinde tablo bulunamadı.")

    rows = table.find_all('tr')
    stock_data = []

    for row in rows[1:]:
        cols = row.find_all('td')
        if len(cols) < 10:
            continue
        stock_data.append({
            "symbol": cols[0].text.strip(),
            "name": cols[1].text.strip(),
            "last": cols[2].text.strip(),
            "high": cols[3].text.strip(),
            "low": cols[4].text.strip(),
            "volume": cols[5].text.strip(),
            "daily_change": cols[6].text.strip(),
            "weekly_change": cols[7].text.strip(),
            "monthly_change": cols[8].text.strip(),
            "annual_change": cols[9].text.strip(),
        })

    return stock_data

def fetch_and_save_stock_data():
    for key, url in STOCK_URLS.items():
        csv_file_path = CSV_PATHS[key]
        try:
            logging.info(f"{key} verisi çekiliyor: {url}")
            data = fetch_stock_data_from_url(url)
            update_csv(data, csv_file_path)
            logging.info(f"{key} verisi '{csv_file_path}' dosyasına kaydedildi.")
            time.sleep(SLEEP_SECONDS)
        except Exception as e:
            logging.error(f"{key} verisi işlenirken hata oluştu: {e}")

if __name__ == "__main__":
    fetch_and_save_stock_data()
