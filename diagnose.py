import pandas as pd
import yfinance as yf
from strategy import detect_market_regime, select_tickers_adaptive, decide_entry_exit_adaptive
import numpy as np

def diagnose_strategy():
    """Diagnose why the strategy fails after February"""
    
    # Test a few days in different months
    tickers = ['AAPL', 'MSFT', 'NVDA', 'TSLA', 'GOOG', 'AMZN', 'META', 'NFLX', 'CRM', 'ADBE']
    
    test_dates = [
        '2024-01-15',  # January (working)
        '2024-03-15',  # March (not working)
        '2024-05-15',  # May (not working)
        '2024-07-15',  # July (not working)
        '2024-11-15',  # November (not working)
    ]
    
    print("=== STRATEGY DIAGNOSTIC ===")
    
    for test_date in test_dates:
        print(f"\n--- Testing {test_date} ---")
        
        # Download data for that specific day
        day_data = {}
        for ticker in tickers:
            try:
                df = yf.download(ticker, start=test_date, end=test_date, progress=False)
                if not df.empty:
                    row = df.iloc[0]
                    day_data[ticker] = {
                        'open': float(row['Open']),
                        'high': float(row['High']),
                        'low': float(row['Low']),
                        'close': float(row['Close']),
                        'volume': float(row['Volume']),
                        'sector': 'Unknown'
                    }
            except Exception as e:
                print(f"Error downloading {ticker}: {e}")
                continue
        
        if not day_data:
            print("No data available for this date")
            continue
        
        # Detect market regime
        market_regime = detect_market_regime(day_data)
        print(f"Market regime: {market_regime}")
        
        # Calculate market statistics
        gains = []
        volatilities = []
        for ticker, d in day_data.items():
            gain = (d['close'] - d['open']) / d['open']
            vol = (d['high'] - d['low']) / d['open']
            gains.append(gain)
            volatilities.append(vol)
        
        avg_gain = np.mean(gains)
        avg_vol = np.mean(volatilities)
        
        print(f"Average gain: {avg_gain:.4f} ({avg_gain*100:.2f}%)")
        print(f"Average volatility: {avg_vol:.4f} ({avg_vol*100:.2f}%)")
        
        # Test ticker selection
        selected_tickers = select_tickers_adaptive(day_data, market_regime=market_regime)
        print(f"Selected tickers: {selected_tickers}")
        
        # Test individual ticker decisions
        profitable_trades = 0
        total_profit = 0
        
        for ticker in selected_tickers:
            if ticker in day_data:
                trade_plan = decide_entry_exit_adaptive(day_data[ticker], 25000, len(selected_tickers), market_regime)
                if trade_plan.get('expected_profit', 0) > 0:
                    profitable_trades += 1
                    total_profit += trade_plan['expected_profit']
                    print(f"  {ticker}: ${trade_plan['expected_profit']:.2f} profit")
                else:
                    print(f"  {ticker}: {trade_plan.get('exit_type', 'no trade')}")
        
        print(f"Profitable trades: {profitable_trades}/{len(selected_tickers)}")
        print(f"Total profit: ${total_profit:.2f}")
        
        # Show raw data for top 3 tickers
        print("\nRaw data for analysis:")
        sorted_tickers = sorted(day_data.items(), key=lambda x: (x[1]['close'] - x[1]['open'])/x[1]['open'], reverse=True)
        for ticker, data in sorted_tickers[:3]:
            gain = (data['close'] - data['open']) / data['open']
            vol = (data['high'] - data['low']) / data['open']
            print(f"  {ticker}: gain={gain:.4f}, vol={vol:.4f}, volume={data['volume']:,.0f}")

if __name__ == "__main__":
    diagnose_strategy()
