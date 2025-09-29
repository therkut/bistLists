# BIST Stock Data Fetcher

This project is designed to fetch and update stock data from specific URLs and save the data into CSV files. It includes functionality to process, validate, and update stock data efficiently.

## Features

- Fetches stock data from XU030, XU050, and XU100 indices
- Saves data in CSV format
- Avoids unnecessary updates by checking for changes
- Includes error handling and logging

## Project Structure

```
bistLists/
├── data/                    # Directory for CSV files
├── src/                     # Source code directory
│   ├── fetch_stock_data.py  # Data fetching operations
│   ├── update_csv.py        # CSV file operations
│   └── utils.py            # Helper functions
└── run.py                  # Main execution file
```

## Installation

1. Python 3.7 or higher is required
2. Create and activate virtual environment:

```bash
python -m venv venv
venv\Scripts\activate  # For Windows
```

3. Install required packages:

```bash
pip install -r requirements.txt
```

## Usage

To run the program:

```bash
python run.py
```

## Output Files

The program creates the following CSV files in the `data` directory:

- `stock_xu030_data.csv` - XU030 index stock data
- `stock_xu050_data.csv` - XU050 index stock data
- `stock_xu100_data.csv` - XU100 index stock data

## CSV File Format

Each CSV file contains the following columns:

- symbol: Stock code
- name: Company name
- last: Last price
- high: Daily high
- low: Daily low
- volume: Trading volume
- daily_change: Daily change
- weekly_change: Weekly change
- monthly_change: Monthly change
- annual_change: Annual change

## Requirements

- Python 3.7+
- pandas
- requests
- beautifulsoup4

## Error Handling

- Error catching for network connection issues
- HTML structure validation
- CSV file operation error checks
- Detailed logging
