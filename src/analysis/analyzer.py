import pandas as pd
from sqlalchemy import create_engine
import numpy as np

class Analyzer:

    @staticmethod
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


    @staticmethod
    def analyze_volume_open_interest(DB_URL, source_table, output_table, logger):
        engine = create_engine(DB_URL)
        try:
            df = pd.read_sql_table(source_table, engine)
        except ValueError as e:
            logger.info(f"Error reading from source table [{source_table}]: {e}")
            exit()

        # Ensure correct types
        df['Volume'] = pd.to_numeric(df['Volume'], errors='coerce')
        df['OpenInterest'] = pd.to_numeric(df['OpenInterest'], errors='coerce')
        df['Date'] = pd.to_datetime(df['Date'])
        df['Expiration'] = pd.to_datetime(df['Expiration'])
        df['Strike'] = pd.to_numeric(df['Strike'], errors='coerce')

        # Strike buckets (e.g., $50 increments)
        df['StrikeBucket'] = (df['Strike'] // 50) * 50

        # Expiration buckets (days to expiration)
        df['T'] = pd.to_numeric(df['T'], errors='coerce')
        bins = [0, 7, 30, 60, 180, np.inf]
        labels = ['0-7', '8-30', '31-60', '61-180', '180+']
        df['ExpirationBucket'] = pd.cut(df['T'], bins=bins, labels=labels, right=True)

        # Volume outlier: volume > 2x average for that option
        avg_volume = df.groupby('OptionID')['Volume'].transform('mean')
        df['VolumeOutlier'] = df['Volume'] > 2 * avg_volume

        # Open Interest change: compare to previous day for each option
        df = df.sort_values(['OptionID', 'Date'])
        df['PrevOpenInterest'] = df.groupby('OptionID')['OpenInterest'].shift(1)
        df['OIChangePct'] = (df['OpenInterest'] - df['PrevOpenInterest']) / df['PrevOpenInterest']
        df['OIOutlier'] = df['OIChangePct'].abs() > 0.5

        # Save results
        df.to_sql(output_table, engine, if_exists='replace', index=False)
        logger.info(f"Volume/Open Interest analysis saved to table [{output_table}]")

        engine.dispose()