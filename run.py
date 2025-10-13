import logging
from src.fetch_stock_data import fetch_and_save_stock_data
from src.fetch_difference_data import fetch_and_process_difference_data

# Logging yapılandırması
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

def main():
    try:
        logging.info("Başlatılıyor: Hisse verisi çekme süreci...")
        fetch_and_save_stock_data()
        logging.info("Hisse verisi çekme tamamlandı.")

        logging.info("Başlatılıyor: Fark verisi işleme süreci...")
        fetch_and_process_difference_data()
        logging.info("Fark verisi işleme tamamlandı.")
        
    except Exception as e:
        logging.exception(f"Bir hata oluştu: {e}")

if __name__ == "__main__":
    main()
