import requests
from bs4 import BeautifulSoup
import json

# List of stock symbols for the companies
mystocks = [
    'AAPL',        # Apple Inc.
    'MSFT',        # Microsoft Corporation
    'AMZN',        # Amazon.com, Inc.
    'INFY.NS',     # Infosys Limited (Indian market - .NS for NSE)
    'TCS.NS',      # Tata Consultancy Services
    'WIPRO.NS',    # Wipro Limited
    'HCLTECH.NS',  # HCL Technologies Limited
    'ITC.NS',      # ITC Limited
    'ICICIBANK.NS',# ICICI Bank Limited
    'RELIANCE.NS'  # Reliance Industries Limited
]

stockdata = []

# Function to fetch stock data
def getData(symbol):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }
    url = f'https://finance.yahoo.com/quote/{symbol}'
    
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()  # Check for HTTP request errors
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # Updated selectors (Inspect Yahoo Finance to confirm latest HTML structure)
        price = soup.find('fin-streamer', {'data-field': 'regularMarketPrice'}).text
        change = soup.find('fin-streamer', {'data-field': 'regularMarketChangePercent'}).text
        
        stock = {
            'symbol': symbol,
            'price': price,
            'change': change
        }
        return stock
    
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None

# Main script to gather data
for item in mystocks:
    print(f"Fetching data for: {item}")
    stock_info = getData(item)
    if stock_info:
        stockdata.append(stock_info)

# Save data to a JSON file
with open('stockdata.json', 'w') as f:
    json.dump(stockdata, f, indent=4)

print("Stock data saved to stockdata.json")
