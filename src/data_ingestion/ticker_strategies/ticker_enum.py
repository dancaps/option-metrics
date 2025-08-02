# src/data_ingestion/ticker_strategies/ticker_enum.py
from enum import Enum
from .base_schema_strategy import BaseSchemaStrategy
from .spx_schema_strategy import SPXSchemaStrategy


class TickerEnum(Enum):
    SPX = 'SPX'
    # Add more tickers as needed

    @property
    def schema_strategy(self):
        if self is TickerEnum.SPX:
            return SPXSchemaStrategy
        # Add more mappings as needed
        return BaseSchemaStrategy

def get_schema_strategy_for_ticker(ticker_value):
    try:
        ticker_enum = TickerEnum(ticker_value)
        return ticker_enum.schema_strategy
    except ValueError:
        return BaseSchemaStrategy