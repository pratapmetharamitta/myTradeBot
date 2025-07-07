# Configuration for TradeBot
FUNDS = 25000
DAILY_TARGET = 150  # Updated target: $150/day = $39,000/year (156% annual return)
BROKER = 'Fidelity'
MARKET_OPEN = '09:30'
MARKET_CLOSE = '16:00'

# Fidelity API credentials (replace with your actual credentials, or load from env vars)
FIDELITY_CLIENT_ID = ''
FIDELITY_CLIENT_SECRET = ''
FIDELITY_REDIRECT_URI = 'http://localhost/callback'  # Set this in your Fidelity app settings
