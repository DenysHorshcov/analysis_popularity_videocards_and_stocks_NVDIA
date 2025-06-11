import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# --------- 1. PostgreSQL connection config ---------
load_dotenv()

for key in ['DB_USER', 'DB_PASSWORD', 'DB_HOST', 'DB_PORT', 'DB_NAME']:
    val = os.getenv(key)
    print(f"{key}: {repr(val)}")

db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

# Create connection string
engine = create_engine(f'postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}')

# --------- 2. Load CSV files ---------
stock_prices_df = pd.read_csv("stock_prices.csv")
company_metrics_df = pd.read_csv("company_metrics.csv")

# --------- 3. Upload to PostgreSQL ---------
# Replace old table if exists
stock_prices_df.to_sql("stock_prices", engine, if_exists="replace", index=False)
company_metrics_df.to_sql("company_metrics", engine, if_exists="replace", index=False)

print("✅ Data successfully uploaded to PostgreSQL.")
