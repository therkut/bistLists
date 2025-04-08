import logging
from src.fetch_stock_data import fetch_and_save_stock_data

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    logging.info("Starting the stock data fetch process...")
    fetch_and_save_stock_data()
    logging.info("Process completed successfully.")

if __name__ == "__main__":
    main()