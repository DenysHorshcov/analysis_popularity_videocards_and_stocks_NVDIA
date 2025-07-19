import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# PostgreSQL connection config
load_dotenv()

db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

# Create connection string
engine = create_engine(f'postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}')

# Load CSV files
stock_prices_df = pd.read_csv("tables/stock_prices.csv")
rtx_4070_df = pd.read_csv("tables/rtx4070.csv")
rtx_4080_df = pd.read_csv("tables/rtx4080.csv")
rtx_4090_df = pd.read_csv("tables/rtx4090.csv")

# Upload to PostgreSQL 
stock_prices_df.to_sql("stock_prices", engine, if_exists="replace", index=False)
rtx_4070_df.to_sql("rtx_4070", engine, if_exists="replace", index=False)
rtx_4080_df.to_sql("rtx_4080", engine, if_exists="replace", index=False)
rtx_4090_df.to_sql("rtx_4090", engine, if_exists="replace", index=False)

print("Data successfully uploaded to PostgreSQL.")
