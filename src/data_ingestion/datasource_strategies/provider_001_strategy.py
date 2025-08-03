
from .base_datasource_strategy import BaseDatasourceStrategy

class Provider001Strategy(BaseDatasourceStrategy):
    schema = {
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