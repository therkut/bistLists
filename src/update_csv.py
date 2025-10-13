import os
import logging
import pandas as pd
from typing import List, Dict, Any

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

def update_csv(fetched_data: List[Dict[str, Any]], csv_file_path: str) -> None:
    """
    CSV dosyasını günceller. Eğer veri değişmemişse dosya güncellenmez.
    """
    # Gerekirse dizini oluştur
    os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)

    # Mevcut veriyi yükle
    if os.path.exists(csv_file_path):
        try:
            existing_data = pd.read_csv(csv_file_path)
        except Exception as e:
            logging.warning(f"CSV dosyası okunamadı: {e}")
            existing_data = pd.DataFrame()
    else:
        existing_data = pd.DataFrame()

    # Yeni veriyi DataFrame olarak oluştur
    new_data = pd.DataFrame(fetched_data)

    # Değişiklik kontrolü
    if existing_data.empty or not existing_data.equals(new_data):
        try:
            new_data.to_csv(csv_file_path, index=False)
            logging.info(f"CSV dosyası '{csv_file_path}' başarıyla güncellendi.")
        except Exception as e:
            logging.error(f"CSV dosyasına yazılamadı '{csv_file_path}': {e}")
    else:
        logging.info(f"Değişiklik yok. CSV dosyası '{csv_file_path}' aynı kaldı.")
