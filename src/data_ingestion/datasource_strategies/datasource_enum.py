
from enum import Enum
from .base_datasource_strategy import BaseDatasourceStrategy
from .provider_001_strategy import Provider001Strategy


class DatasourceEnum(Enum):
    PROVIDER001 = 'PROVIDER001'
    # Add more tickers as needed

    @property
    def datasource_strategy(self):
        if self is DatasourceEnum.PROVIDER001:
            return Provider001Strategy
        # Add more mappings as needed
        return BaseDatasourceStrategy

def get_datasource_strategy(datasource):
    try:
        datasource_enum = DatasourceEnum(datasource)
        return datasource_enum.datasource_strategy
    except ValueError:
        return BaseDatasourceStrategy