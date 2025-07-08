import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

def plot_equity_curve(df, title_prefix="Trading Strategy"):
    df = df.copy()
    df = df[df['expected_profit'].notnull()]
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    df['cum_profit'] = df['expected_profit'].cumsum()
    plt.figure(figsize=(10, 5))
    plt.plot(df['date'], df['cum_profit'], label='Cumulative Profit')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Profit ($)')
    plt.title(f'{title_prefix} - Equity Curve')
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_win_loss(df, title_prefix="Trading Strategy"):
    df = df.copy()
    df = df[df['expected_profit'].notnull()]
    wins = (df['expected_profit'] > 0).sum()
    losses = (df['expected_profit'] < 0).sum()
    plt.figure(figsize=(5, 5))
    plt.bar(['Wins', 'Losses'], [wins, losses], color=['green', 'red'])
    plt.title(f'{title_prefix} - Win/Loss Count')
    plt.show()

def plot_monthly_returns(df, title_prefix="Trading Strategy"):
    df = df.copy()
    df = df[df['expected_profit'].notnull()]
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    df['month'] = df['date'].dt.to_period('M')
    monthly = df.groupby('month')['expected_profit'].sum()
    plt.figure(figsize=(10, 5))
    monthly.plot(kind='bar', color=['green' if x > 0 else 'red' for x in monthly])
    plt.xlabel('Month')
    plt.ylabel('Profit ($)')
    plt.title(f'{title_prefix} - Monthly Returns')
    plt.tight_layout()
    plt.show()

def print_performance_metrics(df, title_prefix="Trading Strategy"):
    df = df.copy()
    df = df[df['expected_profit'].notnull()]
    total_profit = df['expected_profit'].sum()
    num_trades = len(df)
    win_trades = (df['expected_profit'] > 0).sum()
    loss_trades = (df['expected_profit'] < 0).sum()
    win_rate = win_trades / num_trades * 100 if num_trades else 0
    avg_win = df[df['expected_profit'] > 0]['expected_profit'].mean() if win_trades else 0
    avg_loss = df[df['expected_profit'] < 0]['expected_profit'].mean() if loss_trades else 0
    max_drawdown = (df['cum_profit'].cummax() - df['cum_profit']).max() if 'cum_profit' in df else 0
    print(f"\n--- {title_prefix} Performance Metrics ---")
    print(f"Total Profit: ${total_profit:.2f}")
    print(f"Number of Trades: {num_trades}")
    print(f"Win Rate: {win_rate:.2f}%")
    print(f"Average Win: ${avg_win:.2f}")
    print(f"Average Loss: ${avg_loss:.2f}")
    print(f"Max Drawdown: ${max_drawdown:.2f}")

if __name__ == "__main__":
    # Get filename and title from command line arguments
    if len(sys.argv) >= 2:
        filename = sys.argv[1]
        title_prefix = sys.argv[2] if len(sys.argv) >= 3 else "Trading Strategy Backtest"
    else:
        # Check for 1-year results first, then fallback to original file
        if os.path.exists('backtest_results_1year.csv'):
            print("Using 1-year backtest results...")
            filename = 'backtest_results_1year.csv'
            title_prefix = "Trading Strategy Backtest"
        elif os.path.exists('backtest_results.csv'):
            print("Using original backtest results...")
            filename = 'backtest_results.csv'
            title_prefix = "Trading Strategy Backtest"
        else:
            print("No backtest results found. Please run backtest.py first.")
            exit(1)
    
    if not os.path.exists(filename):
        print(f"File {filename} not found.")
        exit(1)
        
    print(f"Using backtest results from: {filename}")
    df = pd.read_csv(filename)
    
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    df['cum_profit'] = df['expected_profit'].cumsum()
    
    plot_equity_curve(df, title_prefix)
    plot_win_loss(df, title_prefix)
    plot_monthly_returns(df, title_prefix)
    print_performance_metrics(df, title_prefix)
