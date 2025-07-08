import pandas as pd
import yfinance as yf
from strategy import select_custom_tickers, decide_entry_exit_adaptive, detect_market_regime
from config import CUSTOM_TICKERS, FUNDS

def download_data(tickers, start, end):
    data = {}
    for ticker in tickers:
        df = yf.download(ticker, start=start, end=end, progress=False, auto_adjust=True)
        if not df.empty:
            data[ticker] = df
    return data

def run_backtest(tickers, start, end, initial_funds=25000):
    data = download_data(tickers, start, end)
    all_trades = []
    funds = initial_funds
    total_profit = 0
    dates = pd.date_range(start, end, freq='B')
    
    for i, date in enumerate(dates):
        day_data = {}
        for ticker, df in data.items():
            if date.strftime('%Y-%m-%d') in df.index:
                row = df.loc[date.strftime('%Y-%m-%d')]
                # If multiple rows, take the first
                if hasattr(row, 'shape') and len(row.shape) > 1 and row.shape[0] > 1:
                    row = row.iloc[0]
                day_data[ticker] = {
                    'open': float(row['Open'].iloc[0]) if hasattr(row['Open'], 'iloc') else float(row['Open']),
                    'high': float(row['High'].iloc[0]) if hasattr(row['High'], 'iloc') else float(row['High']),
                    'low': float(row['Low'].iloc[0]) if hasattr(row['Low'], 'iloc') else float(row['Low']),
                    'close': float(row['Close'].iloc[0]) if hasattr(row['Close'], 'iloc') else float(row['Close']),
                    'volume': float(row['Volume'].iloc[0]) if hasattr(row['Volume'], 'iloc') else float(row['Volume']),
                    'sector': 'Unknown',  # Optional: add sector info if available
                }
        if not day_data:
            continue
        
        # REALISTIC DAY TRADING: Use previous day's data for selection, current day for execution
        if i > 0:  # Need at least one previous day
            prev_date = dates[i-1]
            prev_day_data = {}
            for ticker, df in data.items():
                if prev_date.strftime('%Y-%m-%d') in df.index:
                    prev_row = df.loc[prev_date.strftime('%Y-%m-%d')]
                    if hasattr(prev_row, 'shape') and len(prev_row.shape) > 1 and prev_row.shape[0] > 1:
                        prev_row = prev_row.iloc[0]
                    prev_day_data[ticker] = {
                        'open': float(prev_row['Open'].iloc[0]) if hasattr(prev_row['Open'], 'iloc') else float(prev_row['Open']),
                        'high': float(prev_row['High'].iloc[0]) if hasattr(prev_row['High'], 'iloc') else float(prev_row['High']),
                        'low': float(prev_row['Low'].iloc[0]) if hasattr(prev_row['Low'], 'iloc') else float(prev_row['Low']),
                        'close': float(prev_row['Close'].iloc[0]) if hasattr(prev_row['Close'], 'iloc') else float(prev_row['Close']),
                        'volume': float(prev_row['Volume'].iloc[0]) if hasattr(prev_row['Volume'], 'iloc') else float(prev_row['Volume']),
                        'sector': 'Unknown',
                    }
            
            # Detect market regime for adaptive strategy
            market_regime = detect_market_regime(prev_day_data)
            
            # Use custom tickers from configuration
            available_custom_tickers = [t for t in CUSTOM_TICKERS if t in prev_day_data]
            tickers_today = available_custom_tickers[:12]  # Limit to max positions
            min_tickers = max(5, len(tickers_today))
            
            # DAY TRADING FIX: Use current total funds for each day (funds reset daily)
            daily_funds = funds + total_profit  # Available funds = starting funds + accumulated profit
            
            for ticker in tickers_today:
                if ticker in day_data:  # Ensure ticker is available today
                    # Use current day's opening price for entry
                    current_data = day_data[ticker].copy()
                    current_data['open'] = day_data[ticker]['open']  # Buy at today's open
                    current_data['symbol'] = ticker  # Add ticker symbol for position sizing
                    
                    # Simulate realistic exit: can achieve high/low/close during the day
                    trade_plan = decide_entry_exit_adaptive(current_data, daily_funds, min_tickers, market_regime)
                    
                    # For day trading, we close the position at the end of the day
                    if trade_plan.get('expected_profit') and trade_plan['expected_profit'] != 0:
                        total_profit += trade_plan['expected_profit']
                    
                    trade_plan['date'] = date.strftime('%Y-%m-%d')
                    trade_plan['ticker'] = ticker
                    all_trades.append(trade_plan)
    
    return pd.DataFrame(all_trades)

if __name__ == "__main__":
    import sys
    
    # Use custom tickers from configuration
    tickers = CUSTOM_TICKERS
    
    # Get year from command line argument, default to 2024
    year = int(sys.argv[1]) if len(sys.argv) > 1 else 2024
    start = f'{year}-01-01'
    end = f'{year}-12-31'
    
    print(f"Running ENHANCED backtest for 1 year of data: {start} to {end}")
    print(f"Testing {len(tickers)} custom stocks: {', '.join(tickers)}")
    print("Using CUSTOM CONFIGURATION: Custom tickers, adaptive position sizing, configurable strategy")
    df = run_backtest(tickers, start, end, FUNDS)
    print(df.head())
    print(f"Total trades: {len(df)}")
    print(f"Total expected profit: {df['expected_profit'].sum():.2f}")
    
    # Save results to CSV with year in filename
    filename = f'backtest_results_{year}.csv'
    df.to_csv(filename, index=False)
    print(f"Results saved to {filename}")
