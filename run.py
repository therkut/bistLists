import logging
from src.fetch_stock_data import fetch_and_save_stock_data
from src.fetch_difference_data import fetch_and_process_difference_data

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    logging.info("Starting the stock data fetch process...")
    fetch_and_save_stock_data()
    logging.info("Stock data fetch process completed.")

    logging.info("Starting the difference data fetch process...")
    fetch_and_process_difference_data()
    logging.info("Difference data fetch process completed.")

if __name__ == "__main__":
    main()
