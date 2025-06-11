import yfinance as yf
import pandas as pd

tickers = ['AAPL', 'MSFT', 'TSLA', 'JNJ']

# ---------- 1. Download 1-year historical stock prices ----------
stock_prices_list = []

for ticker in tickers:
    print(f"📥 Downloading historical prices for {ticker}...")
    data = yf.download(ticker, start="2024-06-01", end="2025-06-01", auto_adjust=False, group_by='column')
    # ✅ Flatten multi-index columns
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)
    print(data.columns)  # before fix: MultiIndex with AAPL
    data = data.reset_index()
    data['ticker'] = ticker
    stock_prices_list.append(data)

stock_prices_df = pd.concat(stock_prices_list, ignore_index=True)
stock_prices_df = stock_prices_df.rename(columns={
    "Date": "date",
    "Open": "open",
    "High": "high",
    "Low": "low",
    "Close": "close",
    "Adj Close": "adj_close",
    "Volume": "volume"
})[['ticker', 'date', 'open', 'high', 'low', 'close', 'adj_close', 'volume']]

# ---------- 2. Extract company metrics using yfinance.Ticker().info ----------
company_metrics_list = []

for ticker in tickers:
    print(f"🔍 Getting metrics for {ticker}...")
    try:
        company = yf.Ticker(ticker)
        info = company.info

        company_metrics_list.append({
            "ticker": ticker,
            "company_name": info.get("longName"),
            "sector": info.get("sector"),
            "market_cap": info.get("marketCap"),
            "pe_ratio": info.get("trailingPE"),
            "eps": info.get("trailingEps"),
            "dividend_yield": info.get("dividendYield"),
            "beta": info.get("beta"),
            "1y_target_price": info.get("targetMeanPrice"),
            "52_week_high": info.get("fiftyTwoWeekHigh"),
            "52_week_low": info.get("fiftyTwoWeekLow"),
            "revenue": info.get("totalRevenue"),
            "net_income": info.get("netIncomeToCommon"),
            "ebitda": info.get("ebitda"),
            "free_cash_flow": info.get("freeCashflow"),
            "profit_margin": info.get("profitMargins"),
            "return_on_equity": info.get("returnOnEquity")
        })

    except Exception as e:
        print(f"❌ Error fetching metrics for {ticker}: {e}")

company_metrics_df = pd.DataFrame(company_metrics_list)

# ---------- 3. Export CSVs ----------
stock_prices_df.to_csv("stock_prices.csv", index=False)
company_metrics_df.to_csv("company_metrics.csv", index=False)

print("\n✅ Data successfully exported.")
