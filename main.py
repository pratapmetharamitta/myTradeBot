# Entry point for TradeBot
# 
# Demo Mode: Set DEMO_MODE=true (default) to run without real API authentication
# Live Mode: Set DEMO_MODE=false to enable real Fidelity API authentication

import os
from datetime import datetime
from config import FUNDS, DAILY_TARGET, BROKER, FIDELITY_CLIENT_ID, FIDELITY_CLIENT_SECRET, FIDELITY_REDIRECT_URI, CUSTOM_TICKERS, POSITION_SIZING
from fidelity_api import FidelityAPI
from strategy import select_custom_tickers, decide_entry_exit, detect_market_regime
from data import get_mock_market_data



def log_trade(ticker, trade_plan):
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"trades_{datetime.now().strftime('%Y%m%d')}.log")
    with open(log_file, "a") as f:
        f.write(f"{datetime.now().isoformat()} | {ticker} | Entry: {trade_plan['entry']} | Exit: {trade_plan['exit']} | ExitType: {trade_plan.get('exit_type', 'n/a')}\n")

def risk_report(trades):
    total_invested = sum(t.get('invested', 0) for t in trades)
    max_loss = sum((t['entry'] - t['stop_loss']) * t['shares'] for t in trades if t.get('stop_loss') and t.get('shares'))
    expected_profit = sum(t.get('expected_profit', 0) for t in trades)
    print("\n--- Risk Report ---")
    print(f"Total Invested: ${total_invested:.2f}")
    print(f"Maximum Possible Loss (if all stop-losses hit): ${max_loss:.2f}")
    print(f"Expected Profit (if all targets hit): ${expected_profit:.2f}")
    print(f"Number of trades: {len(trades)}")

def main():
    print(f"Starting TradeBot with ${FUNDS} aiming for ${DAILY_TARGET} daily using {BROKER}")
    
    # Check if we're in demo mode (no real API authentication)
    demo_mode = os.environ.get('DEMO_MODE', 'true').lower() == 'true'
    
    if demo_mode:
        print("Running in DEMO MODE - No actual API authentication required")
        api = None  # Skip API initialization in demo mode
    else:
        api = FidelityAPI()
        # --- Fidelity OAuth2 Authentication ---
        # 1. Set your credentials in config.py or as environment variables
        # 2. First run: get auth_code by visiting the printed URL and pasting the code
        auth_code = os.environ.get('FIDELITY_AUTH_CODE', None)  # Or prompt user for input
        if not auth_code:
            api.authenticate(FIDELITY_CLIENT_ID, FIDELITY_CLIENT_SECRET, FIDELITY_REDIRECT_URI)
            auth_code = input("Paste the 'code' from the Fidelity redirect URL: ").strip()
        api.authenticate(FIDELITY_CLIENT_ID, FIDELITY_CLIENT_SECRET, FIDELITY_REDIRECT_URI, auth_code)
        # --- End Fidelity OAuth2 Authentication ---

    market_data = get_mock_market_data()  # Replace with api.get_market_data(symbol) for live
    
    # Use custom ticker configuration
    print(f"Using custom ticker list: {CUSTOM_TICKERS}")
    print(f"Position sizing method: {POSITION_SIZING['method']}")
    print(f"Max positions: {POSITION_SIZING['max_positions']}")
    
    # Get custom tickers and detect market regime
    tickers = select_custom_tickers(market_data)
    market_regime = detect_market_regime(market_data)
    print(f"Market regime detected: {market_regime}")
    print(f"Selected tickers: {tickers}")
    
    available_funds = FUNDS
    trades = []
    
    for ticker in tickers:
        ticker_data = market_data.get(ticker, {})
        if ticker_data:
            # Add ticker symbol to the data for position sizing
            ticker_data['symbol'] = ticker
            trade_plan = decide_entry_exit(ticker_data, available_funds, len(tickers))
            
            # Deduct invested amount from available funds for next trade
            if trade_plan.get('invested'):
                available_funds -= trade_plan['invested']
            
            # Example: Place a real order (uncomment for live trading)
            # api.place_order(ticker, trade_plan['shares'], 'buy', 'market')
            print(f"Planned trade for {ticker}: {trade_plan}")
            log_trade(ticker, trade_plan)
            trades.append(trade_plan)
        trades.append(trade_plan)
    risk_report(trades)

if __name__ == "__main__":
    main()
