import os
import logging
from io import StringIO
from typing import List
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Logger configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

# Source URLs
URL_ALL_STOCKS = "https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/Temel-Degerler-Ve-Oranlar.aspx#page-1"
URL_KATILIM_STOCKS = "https://finans.mynet.com/borsa/endeks/xktum-bist-katilim-tum/endekshisseleri/"

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

def get_table_from_url(url: str, table_index: int = 0) -> pd.DataFrame:
    """Belirtilen URL'den tabloyu çekip DataFrame olarak döner."""
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    tables = soup.find_all("table")
    if not tables or len(tables) <= table_index:
        raise ValueError(f"Table not found or index error: {url}")
    return pd.read_html(StringIO(str(tables[table_index])))[0]

def extract_stock_code(name: str) -> str:
    """Hisse adından kodu çıkarır."""
    return name.split()[0].strip() if isinstance(name, str) and name.strip() else ""

def save_csv(df: pd.DataFrame, path: str, index: bool = False) -> None:
    """CSV dosyasını kaydeder ve log mesajı verir."""
    df.to_csv(path, index=index, encoding="utf-8-sig")
    logger.info(f"{path} başarıyla güncellendi.")

def save_html(df: pd.DataFrame, path: str) -> None:
    """HTML dosyasını kaydeder."""
    df.to_html(path, index=False, encoding="utf-8")
    logger.info(f"{path} başarıyla kaydedildi.")

def fetch_and_process_difference_data() -> pd.DataFrame:
    # Verileri çek
    all_stocks_df = get_table_from_url(URL_ALL_STOCKS, table_index=2)
    katilim_df = get_table_from_url(URL_KATILIM_STOCKS, table_index=0)

    # Kodları ekle
    all_stocks_df["stock"] = all_stocks_df["Kod"].apply(extract_stock_code)
    katilim_df["stock"] = katilim_df["Hisseler"].apply(extract_stock_code)

    # stockall.txt oluştur
    stock_list = sorted(all_stocks_df["stock"].dropna().unique().tolist())
    with open(f"{DATA_DIR}/stockall.txt", "w", encoding="utf-8") as f:
        f.write(",\n".join(stock_list) + ",")
    logger.info(f"✅ {len(stock_list)} tekil hisse adı {DATA_DIR}/stockall.txt dosyasına kaydedildi.")

    # Katılım onayı
    katilim_stocks_set = set(katilim_df["stock"])
    all_stocks_df["Onay"] = all_stocks_df["stock"].apply(
        lambda x: "Katılım Endeksine Uygundur" if x in katilim_stocks_set else "Katılım Endeksine Uygun Değildir"
    )

    # Eksik kolonlar
    for col in ["Hisse Adı", "Sektör"]:
        if col not in all_stocks_df.columns:
            all_stocks_df[col] = ""

    # all_data.csv ile birleştir
    all_data_path = f"{DATA_DIR}/all_data.csv"
    if os.path.exists(all_data_path):
        all_data = pd.read_csv(all_data_path, dtype=str)
        merged_df = pd.merge(
            all_stocks_df,
            all_data[["stock", "id", "ipoDate", "firstTradeDate"]],
            on="stock",
            how="left"
        )
    else:
        logger.warning("⚠️ data/all_data.csv bulunamadı, id ve tarih bilgileri eklenemedi.")
        merged_df = all_stocks_df.copy()
        merged_df["id"] = ""
        merged_df["ipoDate"] = ""
        merged_df["firstTradeDate"] = ""

    # Tekrar edenleri logla
    duplicates = merged_df[merged_df.duplicated(subset=["stock"], keep=False)].sort_values("stock")
    if not duplicates.empty:
        logger.info("⚠️ Tekrar eden kayıtlar bulundu ve tekilleştirilecek:")
        logger.info(duplicates[["stock", "id", "ipoDate", "firstTradeDate"]])
    else:
        logger.info("✅ Tekrar eden kayıt yok.")

    merged_unique = merged_df.drop_duplicates(subset=["stock"])

    # Son tabloyu oluştur
    final_df = merged_unique[[
        "stock", "Onay", "Hisse Adı", "Sektör", "id", "ipoDate", "firstTradeDate"
    ]].copy()
    final_df.rename(columns={"ipoDate": "Halka Arz Tarihi", "firstTradeDate": "İlk İşlem Tarihi"}, inplace=True)

    # CSV ve HTML kaydet
    save_csv(final_df, f"{DATA_DIR}/Katilim_Endeksi_Onay_Tablosu.csv")
    save_html(final_df, f"{DATA_DIR}/Katilim_Endeksi_Onay_Tablosu.html")

    # Farklı CSV'ler: tüm, onaylı, onaysız
    stock_cols = ["stock", "id", "ipoDate", "firstTradeDate"]
    save_csv(merged_unique[stock_cols], f"{DATA_DIR}/stock_xutum_data.csv")
    save_csv(merged_unique.loc[merged_unique["Onay"] == "Katılım Endeksine Uygundur", stock_cols],
             f"{DATA_DIR}/stock_xktum_data.csv")
    save_csv(merged_unique.loc[merged_unique["Onay"] == "Katılım Endeksine Uygun Değildir", stock_cols],
             f"{DATA_DIR}/stock_xktumext_data.csv")

    return final_df

if __name__ == "__main__":
    df = fetch_and_process_difference_data()
    logger.info(df.head())
