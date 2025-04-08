def fetch_and_save_stock_data():
    import requests
    from bs4 import BeautifulSoup
    from src.update_csv import update_csv
    import time  # Gecikme için gerekli modül

    # URL ve CSV dosyası eşleştirmeleri
    url_csv_map = {
        "https://oyakyatirim.com.tr/piyasa-verileri/XU030": "data/stock_xu030_data.csv",
        "https://oyakyatirim.com.tr/piyasa-verileri/XU050": "data/stock_xu050_data.csv",
        "https://oyakyatirim.com.tr/piyasa-verileri/XU100": "data/stock_xu100_data.csv",
    }

    for url, csv_file_path in url_csv_map.items():
        try:
            print(f"Fetching stock data from {url}...")
            response = requests.get(url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')

                # Doğru div'i seçin
                portlet_box = soup.find('div', class_='portlet box green')
                if not portlet_box:
                    raise Exception("Failed to find 'portlet box green' in the HTML.")

                # Div içerisindeki tabloyu bulun
                table = portlet_box.find('table')
                if not table:
                    raise Exception("Failed to find 'table' in the 'portlet box green'.")

                stock_data = []
                rows = table.find_all('tr')
                print(f"Number of rows found: {len(rows)}")

                if len(rows) <= 1:  # Ensure there are rows beyond the header
                    raise Exception("No data rows found in the table.")

                for row in rows[1:]:  # Skip the header row
                    columns = row.find_all('td')
                    if len(columns) < 10:  # Ensure there are enough columns
                        continue  # Skip rows with insufficient data

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

                # CSV'ye yaz
                update_csv(stock_data, csv_file_path)
                print(f"Stock data from {url} saved to {csv_file_path}.")
            else:
                raise Exception(f"Failed to fetch data: HTTP {response.status_code}")

            # İstekler arasında 1-2 saniye bekle
            time.sleep(2)

        except Exception as e:
            print(f"An error occurred while processing {url}: {e}")