import requests
import pandas as pd
from io import StringIO
from bs4 import BeautifulSoup
import logging

# Logger ayarı
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Kaynak URL'ler
URL_ALL_STOCKS = "https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/Temel-Degerler-Ve-Oranlar.aspx#page-1"
URL_KATILIM_STOCKS = "https://finans.mynet.com/borsa/endeks/xktum-bist-katilim-tum/endekshisseleri/"

def get_table_from_url(url, table_index=0):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    tables = soup.find_all("table")
    if not tables or len(tables) <= table_index:
        raise ValueError(f"Tablo bulunamadı veya index hatası: {url}")
    table_html = str(tables[table_index])
    return pd.read_html(StringIO(table_html))[0]

def get_stock_code(name):
    if isinstance(name, str) and name.strip():
        return name.split()[0].strip()
    return ""

def fetch_and_process_difference_data():
    # Tabloları çek
    all_stocks_df = get_table_from_url(URL_ALL_STOCKS, table_index=2)
    katilim_df = get_table_from_url(URL_KATILIM_STOCKS, table_index=0)

    # Kodları ayıkla
    all_stocks_df["stock"] = all_stocks_df["Kod"].apply(get_stock_code)
    katilim_df["stock"] = katilim_df["Hisseler"].apply(get_stock_code)

    katilim_stocks_set = set(katilim_df["stock"])

    # Onay sütunu
    all_stocks_df["Onay"] = all_stocks_df["stock"].apply(
        lambda x: "Katılım Endeksine Uygundur" if x in katilim_stocks_set else "Katılım Endeksine Uygun Değildir"
    )

    # Gerekli sütunlar varsa yoksa ekle
    for col in ["Hisse Adı", "Sektör"]:
        if col not in all_stocks_df.columns:
            all_stocks_df[col] = ""

    final_cols = ["Kod", "Onay", "Hisse Adı", "Sektör"]
    final_df = all_stocks_df[final_cols].copy()

    # Katılım hissesi sayısı
    katilim_sayisi = final_df[final_df["Onay"] == "Katılım Endeksine Uygundur"].shape[0]
    olmayanlar_sayisi = final_df.shape[0] - katilim_sayisi

    logger.info(f"Katılım endeksindeki hisse sayısı: {katilim_sayisi}")
    logger.info(f"Katılım endeksinde olmayan hisse sayısı: {olmayanlar_sayisi}")

    # Dosyaları kaydet
    csv_path = "data/Katilim_Endeksi_Onay_Tablosu.csv"
    html_path = "data/Katilim_Endeksi_Onay_Tablosu.html"
    final_df.to_csv(csv_path, index=False, encoding="utf-8-sig")
    final_df.to_html(html_path, index=False, encoding="utf-8")

    logger.info(f"✅ CSV dosyası kaydedildi: {csv_path}")
    logger.info(f"✅ HTML dosyası kaydedildi: {html_path}")

    return final_df

if __name__ == "__main__":
    df = fetch_and_process_difference_data()
    print(df.head())
