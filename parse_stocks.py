import yfinance as yf
import pandas as pd
import os

ticker = 'NVDA'
start_date = '2022-01-01'  
end_date = '2025-06-01'    

output_path = "tables"
os.makedirs(output_path, exist_ok=True)

# Завантаження  цін акцій NVIDIA

print(f"Завантаження цін акцій для {ticker}...")
data = yf.download(ticker, start=start_date, end=end_date, auto_adjust=False, group_by='column')

if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.get_level_values(0)

data = data.reset_index()
data['ticker'] = ticker

stock_prices_df = data.rename(columns={
    "Date": "date",
    "Open": "open",
    "High": "high",
    "Low": "low",
    "Close": "close",
    "Adj Close": "adj_close",
    "Volume": "volume"
})[['ticker', 'date', 'open', 'high', 'low', 'close', 'adj_close', 'volume']]

# Збереження у CSV

stock_prices_df.to_csv(os.path.join(output_path, "stock_prices.csv"), index=False)

print("\nДані успішно збережено у 'tables/stock_prices.csv'.")


