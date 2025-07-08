# Configuration for TradeBot
FUNDS = 25000
DAILY_TARGET = 150  # Updated target: $150/day = $39,000/year (156% annual return)
BROKER = 'Fidelity'
MARKET_OPEN = '09:30'
MARKET_CLOSE = '16:00'

# Custom Trading Configuration
# You can modify these settings to customize your trading preferences

# Custom Ticker List - Add/remove tickers as needed
CUSTOM_TICKERS = [
    'AAPL', 'MSFT', 'NVDA', 'TSLA', 'GOOG', 'AMZN', 'META', 'NFLX',
    'CRM', 'ADBE', 'AMD', 'ORCL', 'PYPL', 'INTC', 'QCOM', 'TXN', 'AVGO', 'CSCO'
]

# Position Sizing Configuration
POSITION_SIZING = {
    'method': 'adaptive',  # Options: 'adaptive', 'equal', 'custom'
    'min_position_value': 500,   # Minimum dollar amount per position (lower for more trades)
    'max_position_value': 4000,  # Maximum dollar amount per position (higher for bigger profits)
    'max_positions': 18,  # Maximum number of positions per day (use all available stocks)
    'risk_per_trade': 0.03,  # Risk 3% of portfolio per trade (more aggressive)
}

# Custom Position Sizes (only used if method='custom')
CUSTOM_POSITION_SIZES = {
    'AAPL': 2500,   # $2500 position size for AAPL
    'MSFT': 2000,   # $2000 position size for MSFT
    'NVDA': 1500,   # $1500 position size for NVDA
    'TSLA': 1000,   # $1000 position size for TSLA
    # Add more custom sizes as needed
    # If ticker not listed here, will use default from POSITION_SIZING
}

# Trading Strategy Settings
STRATEGY_CONFIG = {
    'profit_threshold': 0.004,  # 0.4% profit target (was too high at 3%)
    'stop_loss_pct': 0.025,     # 2.5% stop loss
    'trailing_stop_pct': 0.02,  # 2% trailing stop
    'volume_threshold': 1000000,  # Minimum daily volume
    'volatility_threshold': 0.02, # Minimum volatility for entry
}

# Fidelity API credentials (replace with your actual credentials, or load from env vars)
FIDELITY_CLIENT_ID = ''
FIDELITY_CLIENT_SECRET = ''
FIDELITY_REDIRECT_URI = 'http://localhost/callback'  # Set this in your Fidelity app settings
