import pandas as pd
import numpy as np
import sys

# Get year from command line argument, default to analyzing 1year results
year = sys.argv[1] if len(sys.argv) > 1 else '1year'
filename = f'backtest_results_{year}.csv'

# Load and analyze backtest results
df = pd.read_csv(filename)

print(f'=== ENHANCED BACKTEST ANALYSIS ({year.upper()}) ===')
print(f'Total Trades Executed: {len(df):,}')
print(f'Total Expected Profit: ${df["expected_profit"].sum():,.2f}')
print()

# Exit type analysis
print('=== EXIT TYPE BREAKDOWN ===')
exit_counts = df['exit_type'].value_counts()
for exit_type, count in exit_counts.items():
    pct = (count / len(df)) * 100
    print(f'{exit_type}: {count:,} trades ({pct:.1f}%)')
print()

# Profitable vs non-profitable trades
profitable = df[df['expected_profit'] > 0]
non_profitable = df[df['expected_profit'] <= 0]

print('=== PROFITABILITY ANALYSIS ===')
print(f'Profitable Trades: {len(profitable):,} ({len(profitable)/len(df)*100:.1f}%)')
print(f'Non-Profitable Trades: {len(non_profitable):,} ({len(non_profitable)/len(df)*100:.1f}%)')
if len(profitable) > 0:
    print(f'Average Profitable Trade: ${profitable["expected_profit"].mean():.2f}')
print()

# Daily performance
df['date'] = pd.to_datetime(df['date'])
daily_profits = df.groupby('date')['expected_profit'].sum()

print('=== DAILY PERFORMANCE ===')
print(f'Trading Days: {len(daily_profits)}')
print(f'Average Daily Profit: ${daily_profits.mean():.2f}')
print(f'Best Day: ${daily_profits.max():.2f}')
print(f'Worst Day: ${daily_profits.min():.2f}')
print(f'Positive Days: {(daily_profits > 0).sum()} ({(daily_profits > 0).sum()/len(daily_profits)*100:.1f}%)')
print(f'Days Above $150 Target: {(daily_profits >= 150).sum()} ({(daily_profits >= 150).sum()/len(daily_profits)*100:.1f}%)')
print()

# Technical indicators impact (if available)
if 'confidence' in df.columns:
    print('=== TECHNICAL CONFIDENCE ANALYSIS ===')
    high_conf = df[df['confidence'] >= 0.7]
    med_conf = df[(df['confidence'] >= 0.5) & (df['confidence'] < 0.7)]
    low_conf = df[df['confidence'] < 0.5]
    
    print(f'High Confidence Trades (≥0.7): {len(high_conf):,}')
    print(f'Medium Confidence Trades (0.5-0.7): {len(med_conf):,}')
    print(f'Low Confidence Trades (<0.5): {len(low_conf):,}')
    
    if len(high_conf) > 0:
        print(f'High Confidence Avg Profit: ${high_conf["expected_profit"].mean():.2f}')
    if len(med_conf) > 0:
        print(f'Medium Confidence Avg Profit: ${med_conf["expected_profit"].mean():.2f}')
    if len(low_conf) > 0:
        print(f'Low Confidence Avg Profit: ${low_conf["expected_profit"].mean():.2f}')

print()
print('=== TARGET ACHIEVEMENT ===')
total_profit = df["expected_profit"].sum()
target = 37650  # $150/day × 251 trading days
print(f'Target: $150/day × 251 trading days = ${target:,.2f}')
print(f'Actual: ${total_profit:,.2f}')
print(f'Performance: {(total_profit / target) * 100:.1f}% of target')
print(f'Excess Return: ${total_profit - target:,.2f}')

# Monthly breakdown
df['month'] = df['date'].dt.to_period('M')
monthly_profits = df.groupby('month')['expected_profit'].sum()
print()
print('=== MONTHLY PERFORMANCE ===')
for month, profit in monthly_profits.items():
    print(f'{month}: ${profit:,.2f}')
