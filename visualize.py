import pandas as pd
import matplotlib.pyplot as plt
import os

def load_trades(log_file):
    # Parse log file into DataFrame
    rows = []
    with open(log_file) as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) < 5:
                continue
            ts, ticker, entry, exit_, exit_type = [p.strip() for p in parts]
            entry_val = float(entry.split(':')[1].strip())
            exit_val = exit_.split(':')[1].strip()
            exit_val = float(exit_val) if exit_val != 'None' else None
            rows.append({
                'timestamp': ts,
                'ticker': ticker,
                'entry': entry_val,
                'exit': exit_val,
                'exit_type': exit_type.split(':')[1].strip()
            })
    return pd.DataFrame(rows)

def plot_trades(df):
    if df.empty:
        print("No trades to plot.")
        return
    df = df[df['exit'].notnull()]
    df['pnl'] = df['exit'] - df['entry']
    df['pnl_pct'] = df['pnl'] / df['entry'] * 100
    plt.figure(figsize=(8, 5))
    for ticker in df['ticker'].unique():
        tdf = df[df['ticker'] == ticker]
        plt.plot(tdf['timestamp'], tdf['pnl_pct'], marker='o', label=ticker)
    plt.xlabel('Timestamp')
    plt.ylabel('PnL (%)')
    plt.title('Trade PnL by Ticker')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    log_file = os.path.join("logs", "trades_20250703.log")
    df = load_trades(log_file)
    plot_trades(df)
