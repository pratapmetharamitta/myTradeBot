# 🛠️ TradeBot Custom Configuration Guide

Your TradeBot is now fully customizable! You can easily modify the ticker list and position sizes to match your trading preferences.

## 🚀 Quick Start

### 1. Use the Configuration Tool
```bash
python configure_bot.py
```

### 2. Edit Configuration Directly
Edit `config.py` to customize:
- `CUSTOM_TICKERS`: Your preferred stock list
- `POSITION_SIZING`: How much to invest per stock
- `STRATEGY_CONFIG`: Trading strategy parameters

### 3. Test Your Settings
```bash
python main.py  # Demo mode test
python backtest.py  # Historical validation
```

## 📊 Configuration Options

### Ticker Selection
```python
CUSTOM_TICKERS = [
    'AAPL', 'MSFT', 'NVDA', 'TSLA', 'GOOG'  # Your choice!
]
```

### Position Sizing Methods

#### 1. Adaptive (Recommended)
```python
POSITION_SIZING = {
    'method': 'adaptive',  # Smart sizing based on market conditions
    'min_position_value': 1000,  # Min $1000 per trade
    'max_position_value': 5000,  # Max $5000 per trade
    'max_positions': 12,  # Trade up to 12 stocks
}
```

#### 2. Equal Sizing
```python
POSITION_SIZING = {
    'method': 'equal',  # Same amount for each stock
    'min_position_value': 2000,
    'max_position_value': 3000,
    'max_positions': 8,
}
```

#### 3. Custom Sizing
```python
POSITION_SIZING = {
    'method': 'custom',  # Specific amount per ticker
}

CUSTOM_POSITION_SIZES = {
    'AAPL': 3000,   # $3000 for Apple
    'MSFT': 2500,   # $2500 for Microsoft
    'NVDA': 2000,   # $2000 for Nvidia
}
```

## 🎯 Pre-Built Configurations

### 🚀 Aggressive Tech (High Risk/Reward)
```python
CUSTOM_TICKERS = ['AAPL', 'MSFT', 'NVDA', 'TSLA', 'GOOGL']
POSITION_SIZING = {
    'method': 'custom',
    'max_positions': 5,
}
CUSTOM_POSITION_SIZES = {
    'AAPL': 4000, 'MSFT': 4000, 'NVDA': 3000,
    'TSLA': 3000, 'GOOGL': 4000
}
```

### 🛡️ Conservative Diversified
```python
CUSTOM_TICKERS = ['AAPL', 'MSFT', 'JNJ', 'WMT', 'JPM', 'PG', 'KO', 'PFE']
POSITION_SIZING = {
    'method': 'equal',
    'min_position_value': 1500,
    'max_position_value': 2500,
    'max_positions': 8,
}
```

### ⚡ Momentum Trading
```python
CUSTOM_TICKERS = ['TSLA', 'NVDA', 'AMD', 'NFLX', 'ZOOM', 'PTON']
POSITION_SIZING = {
    'method': 'adaptive',
    'min_position_value': 2000,
    'max_position_value': 4000,
    'max_positions': 6,
}
```

## 🔧 Strategy Parameters

```python
STRATEGY_CONFIG = {
    'profit_threshold': 0.03,      # 3% profit target
    'stop_loss_pct': 0.025,        # 2.5% stop loss
    'trailing_stop_pct': 0.02,     # 2% trailing stop
    'volume_threshold': 1000000,   # Min daily volume
    'volatility_threshold': 0.02,  # Min volatility
}
```

## 📈 Example Usage

After configuring, run your bot:

```bash
# Test with demo mode
python main.py

# Backtest your configuration
python backtest.py

# Visualize results
python visualize_backtest.py
```

## 💡 Tips

1. **Start Conservative**: Begin with diversified tickers and smaller position sizes
2. **Test Thoroughly**: Always backtest new configurations before live trading
3. **Monitor Performance**: Track which settings work best for your goals
4. **Adjust Gradually**: Make incremental changes rather than dramatic shifts

Your bot will automatically use your custom settings while maintaining all the advanced risk management and market analysis features!
