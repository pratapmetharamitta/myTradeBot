# Data retrieval (mock or public API for prototyping)
import pandas as pd

def get_mock_market_data():
    # Enhanced mock data with leveraged ETFs and additional tickers
    data = {
        'SOXL': {'open': 26, 'high': 28, 'low': 25.5, 'close': 27.2, 'volume': 25000000, 'sector': 'Tech'},
        'SOXS': {'open': 64, 'high': 66, 'low': 62, 'close': 63.5, 'volume': 20000000, 'sector': 'Tech'},
        'AAPL': {'open': 190, 'high': 210, 'low': 189, 'close': 194, 'volume': 12000000, 'sector': 'Tech'},
        'TSLA': {'open': 700, 'high': 750, 'low': 695, 'close': 715, 'volume': 9000000, 'sector': 'Auto'},
        'AMD': {'open': 110, 'high': 120, 'low': 109, 'close': 119, 'volume': 8500000, 'sector': 'Tech'},
        'NVDA': {'open': 130, 'high': 160, 'low': 129, 'close': 158, 'volume': 15000000, 'sector': 'Tech'},
        'MSFT': {'open': 300, 'high': 320, 'low': 299, 'close': 319, 'volume': 11000000, 'sector': 'Tech'},
        'GOOG': {'open': 2500, 'high': 2600, 'low': 2490, 'close': 2590, 'volume': 9500000, 'sector': 'Tech'},
        'META': {'open': 350, 'high': 370, 'low': 349, 'close': 369, 'volume': 10500000, 'sector': 'Tech'},
        'NFLX': {'open': 400, 'high': 440, 'low': 399, 'close': 439, 'volume': 9000000, 'sector': 'Media'},
        'BABA': {'open': 80, 'high': 90, 'low': 79, 'close': 89, 'volume': 8700000, 'sector': 'E-Commerce'},
        'ORCL': {'open': 120, 'high': 130, 'low': 119, 'close': 129, 'volume': 8200000, 'sector': 'Tech'},
    }
    return data
