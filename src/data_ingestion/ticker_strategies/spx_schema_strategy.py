# src/data_ingestion/ticker_strategies/spx_schema_strategy.py
from .base_schema_strategy import BaseSchemaStrategy

class SPXSchemaStrategy(BaseSchemaStrategy):
    type_map = {
        'Ticker': str,
        'Date': str,
        'Expiration': str,
        'T': float,
        'Strike': float,
        'CallPut': str,
        'symbol': str,
        'BestBid': float,
        'BestOffer': float,
        'Midpoint': float,
        'Volume': int,
        'OpenInterest': int,
        'ImpliedVolatility': float,
        'Delta': float,
        'Gamma': float,
        'Vega': float,
        'Theta': float,
        'OptionID': str
    }