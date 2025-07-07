import yfinance as yf
import pandas as pd
import numpy as np

def analyze_market_conditions():
    # Download recent data for key stocks
    tickers = ['AAPL', 'MSFT', 'NVDA', 'TSLA', 'GOOG']
    data = {}
    for ticker in tickers:
        df = yf.download(ticker, start='2024-01-01', end='2024-12-31', progress=False)
        data[ticker] = df

    # Analyze monthly volatility and performance
    print('Monthly Market Analysis:')
    monthly_stats = []
    
    for month in range(1, 13):
        month_data = {}
        for ticker, df in data.items():
            month_df = df[df.index.month == month]
            if not month_df.empty:
                daily_returns = (month_df['Close'] - month_df['Open']) / month_df['Open']
                volatility = (month_df['High'] - month_df['Low']) / month_df['Open']
                month_data[ticker] = {
                    'avg_daily_return': float(daily_returns.mean()),
                    'avg_volatility': float(volatility.mean()),
                    'profitable_days': int((daily_returns > 0.002).sum()),
                    'total_days': len(daily_returns)
                }
        
        if month_data:
            avg_return = np.mean([d['avg_daily_return'] for d in month_data.values()])
            avg_vol = np.mean([d['avg_volatility'] for d in month_data.values()])
            total_profitable = sum(d['profitable_days'] for d in month_data.values())
            total_days = sum(d['total_days'] for d in month_data.values())
            
            profitable_rate = total_profitable/total_days*100 if total_days > 0 else 0
            monthly_stats.append({
                'month': month,
                'avg_return': avg_return,
                'avg_volatility': avg_vol,
                'profitable_rate': profitable_rate,
                'total_profitable': total_profitable,
                'total_days': total_days
            })
            
            print(f'Month {month:02d}: Avg Return={avg_return:.4f}, Avg Volatility={avg_vol:.4f}, Profitable Days={total_profitable}/{total_days} ({profitable_rate:.1f}%)')
    
    # Analyze why trades are being skipped
    print('\n--- Strategy Analysis ---')
    
    # Check May 2024 specifically
    may_data = {}
    for ticker, df in data.items():
        may_df = df[df.index.month == 5]  # May
        if not may_df.empty:
            for date, row in may_df.iterrows():
                day_key = date.strftime('%Y-%m-%d')
                if day_key not in may_data:
                    may_data[day_key] = {}
                may_data[day_key][ticker] = {
                    'open': float(row['Open']),
                    'high': float(row['High']),
                    'low': float(row['Low']),
                    'close': float(row['Close']),
                    'volume': float(row['Volume']),
                    'sector': 'Unknown'
                }
    
    print(f'\nMay 2024 sample analysis:')
    sample_days = list(may_data.keys())[:5]
    for day in sample_days:
        day_data = may_data[day]
        print(f'\n{day}:')
        for ticker, data_point in day_data.items():
            gain_pct = (data_point['close'] - data_point['open']) / data_point['open']
            volatility = (data_point['high'] - data_point['low']) / data_point['open']
            print(f'  {ticker}: Gain={gain_pct:.4f}, Volatility={volatility:.4f}, Volume={data_point["volume"]:,.0f}')

if __name__ == "__main__":
    analyze_market_conditions()
