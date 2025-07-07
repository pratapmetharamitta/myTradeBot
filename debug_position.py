from strategy import decide_entry_exit_adaptive

# Test March 1st MSFT trade
ticker_data = {
    'open': 407.405953,
    'high': 415.0,  # Estimated high
    'low': 405.0,   # Estimated low
    'close': 411.596222,
    'volume': 20000000,
    'sector': 'Tech'
}

print("Testing MSFT March 1st trade:")
print(f"Entry: ${ticker_data['open']:.2f}")
print(f"Exit: ${ticker_data['close']:.2f}")
print(f"Profit per share: ${ticker_data['close'] - ticker_data['open']:.2f}")

result = decide_entry_exit_adaptive(ticker_data, 25000, 8, 'normal')
print(f"Result: {result}")

# Test with simplified calculation
entry = ticker_data['open']
exit_price = ticker_data['close']
profit_per_share = exit_price - entry
print(f"\nManual calculation:")
print(f"Profit per share: ${profit_per_share:.2f}")
print(f"Target profit for normal regime: ${100/8:.2f}")
print(f"Target shares: {int(12.5 / profit_per_share)}")
print(f"Allocation: ${25000/8:.2f}")
print(f"Max shares by allocation: {int(25000/8 * 0.7 / entry)}")
