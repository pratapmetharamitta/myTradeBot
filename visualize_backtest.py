import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

def preprocess_data(df):
    """Clean and prepare data for visualization."""
    # Remove null profit rows and ensure proper data types
    df_clean = df[df['expected_profit'].notnull()].copy()
    df_clean['date'] = pd.to_datetime(df_clean['date'])
    df_clean = df_clean.sort_values('date')
    df_clean['cum_profit'] = df_clean['expected_profit'].cumsum()
    return df_clean

def plot_equity_curve(df, title_prefix="Trading Strategy"):
    """Plot cumulative profit over time."""
    plt.figure(figsize=(12, 6))
    plt.plot(df['date'], df['cum_profit'], linewidth=2, color='blue', label='Cumulative Profit')
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Cumulative Profit ($)', fontsize=12)
    plt.title(f'{title_prefix} - Equity Curve', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=11)
    plt.tight_layout()
    plt.show()

def plot_win_loss(df, title_prefix="Trading Strategy"):
    """Plot win/loss distribution."""
    profits = df['expected_profit']
    wins = (profits > 0).sum()
    losses = (profits <= 0).sum()
    
    plt.figure(figsize=(8, 6))
    bars = plt.bar(['Wins', 'Losses'], [wins, losses], 
                   color=['#2E8B57', '#DC143C'], alpha=0.8, width=0.6)
    plt.title(f'{title_prefix} - Win/Loss Distribution', fontsize=14, fontweight='bold')
    plt.ylabel('Number of Trades', fontsize=12)
    
    # Add value labels on bars
    for bar, value in zip(bars, [wins, losses]):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                f'{value}', ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    plt.grid(True, axis='y', alpha=0.3)
    plt.tight_layout()
    plt.show()

def plot_monthly_returns(df, title_prefix="Trading Strategy"):
    """Plot monthly profit distribution."""
    df['month'] = df['date'].dt.to_period('M')
    monthly = df.groupby('month')['expected_profit'].sum()
    
    plt.figure(figsize=(14, 6))
    colors = ['#2E8B57' if x > 0 else '#DC143C' for x in monthly]
    bars = monthly.plot(kind='bar', color=colors, alpha=0.8)
    plt.xlabel('Month', fontsize=12)
    plt.ylabel('Monthly Profit ($)', fontsize=12)
    plt.title(f'{title_prefix} - Monthly Returns', fontsize=14, fontweight='bold')
    plt.xticks(rotation=45)
    plt.grid(True, axis='y', alpha=0.3)
    plt.axhline(y=0, color='black', linestyle='-', alpha=0.5)
    plt.tight_layout()
    plt.show()

def print_performance_metrics(df, title_prefix="Trading Strategy"):
    """Calculate and display comprehensive performance metrics."""
    profits = df['expected_profit']
    total_profit = profits.sum()
    num_trades = len(df)
    
    # Win/Loss analysis
    winning_trades = profits[profits > 0]
    losing_trades = profits[profits < 0]
    neutral_trades = profits[profits == 0]
    
    win_count = len(winning_trades)
    loss_count = len(losing_trades)
    neutral_count = len(neutral_trades)
    
    win_rate = (win_count / num_trades * 100) if num_trades > 0 else 0
    avg_win = winning_trades.mean() if win_count > 0 else 0
    avg_loss = losing_trades.mean() if loss_count > 0 else 0
    
    # Risk metrics
    max_drawdown = (df['cum_profit'].cummax() - df['cum_profit']).max()
    profit_factor = abs(winning_trades.sum() / losing_trades.sum()) if loss_count > 0 else float('inf')
    
    # Display metrics
    print(f"\n{'='*60}")
    print(f"{title_prefix} - PERFORMANCE SUMMARY".center(60))
    print(f"{'='*60}")
    print(f"Total Profit:           ${total_profit:>12,.2f}")
    print(f"Total Trades:           {num_trades:>12,}")
    print(f"Win Rate:               {win_rate:>12.1f}%")
    print(f"Winning Trades:         {win_count:>12,}")
    print(f"Losing Trades:          {loss_count:>12,}")
    print(f"Neutral Trades:         {neutral_count:>12,}")
    print(f"Average Win:            ${avg_win:>12.2f}")
    print(f"Average Loss:           ${avg_loss:>12.2f}")
    print(f"Profit Factor:          {profit_factor:>12.2f}")
    print(f"Max Drawdown:           ${max_drawdown:>12.2f}")
    print(f"{'='*60}")

def get_default_filename():
    """Find the most appropriate default backtest file."""
    file_priorities = [
        'backtest_results_2024.csv',
        'backtest_results_2023.csv', 
        'backtest_results.csv'
    ]
    
    for filename in file_priorities:
        if os.path.exists(filename):
            return filename, f"{filename.split('_')[-1].split('.')[0]} Trading Strategy"
    
    return None, None

def main():
    """Main function to handle command line arguments and execute visualization."""
    # Parse command line arguments
    if len(sys.argv) >= 2:
        filename = sys.argv[1]
        title_prefix = sys.argv[2] if len(sys.argv) >= 3 else "Trading Strategy Backtest"
    else:
        filename, title_prefix = get_default_filename()
        if filename is None:
            print("❌ No backtest results found. Please run backtest.py first.")
            print("Looking for: backtest_results_2024.csv, backtest_results_2023.csv, or backtest_results.csv")
            sys.exit(1)
        print(f"📊 Using default file: {filename}")
    
    # Validate file exists
    if not os.path.exists(filename):
        print(f"❌ File '{filename}' not found.")
        sys.exit(1)
    
    try:
        # Load and preprocess data
        print(f"📈 Loading backtest results from: {filename}")
        df = pd.read_csv(filename)
        df_clean = preprocess_data(df)
        
        if len(df_clean) == 0:
            print("❌ No valid data found in the file.")
            sys.exit(1)
        
        print(f"✅ Loaded {len(df_clean):,} trades successfully")
        print(f"📅 Date range: {df_clean['date'].min().date()} to {df_clean['date'].max().date()}")
        
        # Generate all visualizations
        print("\n🎨 Generating visualizations...")
        plot_equity_curve(df_clean, title_prefix)
        plot_win_loss(df_clean, title_prefix)
        plot_monthly_returns(df_clean, title_prefix)
        print_performance_metrics(df_clean, title_prefix)
        
        print("\n✅ All visualizations completed successfully!")
        
    except Exception as e:
        print(f"❌ Error processing file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
