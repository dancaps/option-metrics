import pandas as pd
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
from datetime import datetime

from ticker_strategies.ticker_enum import get_schema_strategy_for_ticker

def main():
    # Load environment variables from .env
    load_dotenv()

    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        raise ValueError("DATABASE_URL not set in .env file")

    csv_path = os.getenv('FILE_PATH')
    if not csv_path:
        raise ValueError("FILE_PATH not set in .env file")

    # Load CSV into a DataFrame
    df = pd.read_csv(csv_path, delimiter='\t', dtype=str)
    df.columns = [col.strip() for col in df.columns]

    if 'Ticker' not in df.columns:
        raise ValueError("Ticker column not found in input file.")

    # Get current datetime string
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    # Database connection
    engine = create_engine(db_url)

    # Group the data by ticker, process each group using the appropriate schema strategy and save each group to a
    # separate table.
    for ticker, group in df.groupby('Ticker'):
        schema_strategy = get_schema_strategy_for_ticker(ticker)
        type_map = schema_strategy.get_type_map()
        for col, typ in type_map.items():
            if col in group.columns:
                group[col] = group[col].astype(typ, errors='ignore')
        table_name = f"options_raw_{ticker.lower()}_{timestamp}"
        group.to_sql(table_name, engine, if_exists='replace', index=False)
        print(f"Data for ticker {ticker} ingested into table: {table_name}")

    # Close the database connection
    engine.dispose()

    print("Data ingested completed successfully.")

if __name__ == "__main__":
    main()