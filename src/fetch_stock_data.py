import requests
from bs4 import BeautifulSoup
from src.update_csv import update_csv
import time
import csv
import os

def fetch_and_save_stock_data():
    # URL to CSV file mapping
    url_csv_map = {
        "https://oyakyatirim.com.tr/piyasa-verileri/XU030": "data/stock_xu030_data.csv",
        "https://oyakyatirim.com.tr/piyasa-verileri/XU050": "data/stock_xu050_data.csv",
        "https://oyakyatirim.com.tr/piyasa-verileri/XU100": "data/stock_xu100_data.csv",
        "https://oyakyatirim.com.tr/piyasa-verileri/XUTUM": "data/stock_xutum_data.csv",
        "https://oyakyatirim.com.tr/piyasa-verileri/XKTUM": "data/stock_xktum_data.csv",
    }

    for url, csv_file_path in url_csv_map.items():
        try:
            print(f"Fetching stock data from {url}...")
            response = requests.get(url)
            if response.status_code != 200:
                raise Exception(f"Failed to fetch data: HTTP {response.status_code}")

            soup = BeautifulSoup(response.content, 'html.parser')
            portlet_box = soup.find('div', class_='portlet box green')
            if not portlet_box:
                raise Exception("Could not find 'portlet box green' in the HTML.")

            table = portlet_box.find('table')
            if not table:
                raise Exception("Could not find 'table' in the 'portlet box green'.")

            rows = table.find_all('tr')

            # For files that require a different CSV format (just stock names)
            if csv_file_path in ["data/stock_xutum_data.csv", "data/stock_xktum_data.csv"]:
                new_stocks = [
                    row.find_all('td')[0].text.strip()
                    for row in rows[1:]
                    if row.find_all('td') and row.find_all('td')[0].text.strip()
                ]

                # Read old data if exists
                old_data = {}
                if os.path.exists(csv_file_path):
                    with open(csv_file_path, "r", encoding="utf-8") as f:
                        reader = csv.DictReader(f)
                        for row in reader:
                            old_data[row["stock"]] = {
                                "id": row.get("id", ""),
                                "ipoDate": row.get("ipoDate", ""),
                                "firstTradeDate": row.get("firstTradeDate", "")
                            }

                # Merge new stocks with old data
                merged_rows = [
                    {
                        "stock": stock,
                        "id": old_data.get(stock, {}).get("id", ""),
                        "ipoDate": old_data.get(stock, {}).get("ipoDate", ""),
                        "firstTradeDate": old_data.get(stock, {}).get("firstTradeDate", "")
                    }
                    for stock in new_stocks
                ]

                # Write merged data to CSV
                with open(csv_file_path, "w", newline="", encoding="utf-8") as f:
                    writer = csv.DictWriter(f, fieldnames=["stock", "id", "ipoDate", "firstTradeDate"])
                    writer.writeheader()
                    writer.writerows(merged_rows)
                print(f"Stock list from {url} saved to {csv_file_path}.")
            else:
                # For regular stock data tables
                stock_data = []
                for row in rows[1:]:
                    columns = row.find_all('td')
                    if len(columns) < 10:
                        continue
                    stock_info = {
                        "symbol": columns[0].text.strip(),
                        "name": columns[1].text.strip(),
                        "last": columns[2].text.strip(),
                        "high": columns[3].text.strip(),
                        "low": columns[4].text.strip(),
                        "volume": columns[5].text.strip(),
                        "daily_change": columns[6].text.strip(),
                        "weekly_change": columns[7].text.strip(),
                        "monthly_change": columns[8].text.strip(),
                        "annual_change": columns[9].text.strip(),
                    }
                    stock_data.append(stock_info)
                update_csv(stock_data, csv_file_path)
                print(f"Stock data from {url} saved to {csv_file_path}.")

            # Wait 2 seconds between requests to avoid overloading the server
            time.sleep(2)

        except Exception as e:
            print(f"An error occurred while processing {url}: {e}")

    # After the loop: calculate the difference between xutum and xktum and write to file
    xutum_path = "data/stock_xutum_data.csv"
    xktum_path = "data/stock_xktum_data.csv"
    xktumext_path = "data/stock_xktumext_data.csv"
    stockall_path = "data/stockall.txt"

    # Write all stock names from xutum to stockall.txt
    if os.path.exists(xutum_path):
        with open(xutum_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            stocks = [row["stock"] for row in reader if row["stock"]]
        with open(stockall_path, "w", encoding="utf-8") as f:
            for stock in stocks:
                f.write(f"{stock},\n")

    # Write the difference between xutum and xktum to xktumext
    if os.path.exists(xutum_path) and os.path.exists(xktum_path):
        with open(xutum_path, "r", encoding="utf-8") as f:
            xutum_reader = csv.DictReader(f)
            xutum_stocks = {row["stock"]: row for row in xutum_reader if row["stock"]}

        with open(xktum_path, "r", encoding="utf-8") as f:
            xktum_reader = csv.DictReader(f)
            xktum_stocks = {row["stock"] for row in xktum_reader if row["stock"]}

        # Find stocks in xutum but not in xktum
        diff_stocks = [xutum_stocks[stock] for stock in xutum_stocks if stock not in xktum_stocks]
        diff_stocks_sorted = sorted(diff_stocks, key=lambda x: x["stock"])

        with open(xktumext_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["stock", "id", "ipoDate", "firstTradeDate"])
            writer.writeheader()
            writer.writerows(diff_stocks_sorted)
        print(f"Difference written to {xktumext_path}")