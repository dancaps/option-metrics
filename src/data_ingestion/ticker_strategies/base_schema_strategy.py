# src/data_ingestion/ticker_strategies/base_schema_strategy.py
class BaseSchemaStrategy:
    type_map = {}

    @classmethod
    def get_type_map(cls):
        return cls.type_map