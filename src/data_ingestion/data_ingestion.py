import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime

from .datasource_strategies.datasource_enum import get_datasource_strategy

def ingest_data(logger, DB_URL, FILE_PATH, DATASOURCE):
    # Load CSV into a DataFrame
    df = pd.read_csv(FILE_PATH, delimiter='\t', dtype=str)
    df.columns = [col.strip() for col in df.columns]

    # Get current datetime string
    timestamp = datetime.now().strftime('%Y%m%d')

    # Database connection
    engine = create_engine(DB_URL)

    # Get datasource strategy
    datasource_strategy = get_datasource_strategy(DATASOURCE)
    type_map = datasource_strategy.get_data_schema()

    # Convert column types as per the strategy
    for col, typ in type_map.items():
        if col in df.columns:
            df[col] = df[col].astype(typ, errors='ignore')

    # Table name includes datasource and timestamp
    table_name = f"options_raw_{DATASOURCE.lower()}_{timestamp}"
    df.to_sql(table_name, engine, if_exists='replace', index=False)

    # Close the database connection
    engine.dispose()

    logger.info(f"Data ingested from provider [{DATASOURCE}] into table [{table_name}] completed successfully.")

if __name__ == "__main__":
    ingest_data()