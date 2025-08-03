import pandas as pd
from sqlalchemy import create_engine

def calculate_put_call_ratio(DB_URL, source_table, output_table, logger):
    engine = create_engine(DB_URL)
    try:
        df = pd.read_sql_table(source_table, engine)
    except ValueError as e:
        logger.info(f"Error reading from source table [{source_table}]: {e}")
        exit()

    # Ensure correct types
    df['Volume'] = pd.to_numeric(df['Volume'], errors='coerce')
    df['Date'] = pd.to_datetime(df['Date'])
    df['Expiration'] = pd.to_datetime(df['Expiration'])

    # Group by Date and Expiration (for breakdowns)
    grouped = df.groupby(['Date', 'Expiration', 'CallPut'])['Volume'].sum().unstack(fill_value=0).reset_index()

    # Calculate Put-Call Ratio
    grouped['PutCallRatio'] = grouped.get('P', 0) / grouped.get('C', 1)  # Avoid division by zero

    # Identify significant day-over-day changes
    grouped = grouped.sort_values(['Expiration', 'Date'])
    grouped['PrevRatio'] = grouped.groupby('Expiration')['PutCallRatio'].shift(1)
    grouped['RatioChange'] = grouped['PutCallRatio'] - grouped['PrevRatio']
    grouped['SignificantChange'] = grouped['RatioChange'].abs() > 0.5  # Threshold can be adjusted

    # Store results
    grouped.to_sql(output_table, engine, if_exists='replace', index=False)
    logger.info(f"Put-Call Ratio analysis saved to table [{output_table}]")

    engine.dispose()