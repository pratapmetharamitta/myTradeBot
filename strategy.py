# Advanced adaptive trading strategy with market regime detection

import numpy as np
from datetime import datetime, timedelta
from config import CUSTOM_TICKERS, POSITION_SIZING, CUSTOM_POSITION_SIZES, STRATEGY_CONFIG, FUNDS

def detect_market_regime(market_data, lookback_days=20):
    """
    Detect market regime (high volatility vs low volatility) and adjust thresholds
    """
    if not market_data:
        return 'normal'
    
    # Calculate average volatility over the period
    volatilities = []
    for ticker, d in market_data.items():
        try:
            volatility = (float(d['high']) - float(d['low'])) / float(d['open'])
            volatilities.append(volatility)
        except:
            continue
    
    if not volatilities:
        return 'normal'
    
    avg_vol = np.mean(volatilities)
    
    # Define regimes based on volatility
    if avg_vol > 0.035:  # High volatility (3.5%+)
        return 'high_volatility'
    elif avg_vol < 0.015:  # Low volatility (1.5%-)
        return 'low_volatility'
    else:
        return 'normal'

def select_tickers_adaptive(market_data, allowed_sectors=None, min_per_sector=1, market_regime='normal'):
    """
    Adaptive ticker selection based on market regime
    """
    if allowed_sectors is None:
        allowed_sectors = ['Tech', 'Auto', 'Media', 'E-Commerce', 'Finance', 'Healthcare', 'Energy', 'Consumer']
    
    gainers = []
    
    # Safety check for empty market data
    if not market_data:
        return []
    
    # Calculate market statistics
    gains = []
    volumes = []
    volatilities = []
    
    for ticker, d in market_data.items():
        try:
            gain = (float(d['close']) - float(d['open'])) / float(d['open'])
            vol = (float(d['high']) - float(d['low'])) / float(d['open'])
            gains.append(gain)
            volumes.append(float(d['volume']))
            volatilities.append(vol)
        except:
            continue
    
    if not gains:
        return []
    
    avg_gain = np.mean(gains)
    avg_vol = np.mean(volumes)
    avg_volatility = np.mean(volatilities)
    median_vol = np.median(volumes)
    
    # Adaptive thresholds based on market regime - ENHANCED FOR HIGHER PROFITS
    if market_regime == 'high_volatility':
        min_gain = 0.0008  # 0.08% minimum gain (slightly higher)
        min_volatility = 0.012  # 1.2% minimum volatility (lower to catch more opportunities)
        max_volatility = 0.15   # 15% maximum volatility (increased for more aggressive trades)
        volume_threshold = 0.25   # 25% of median volume (lower to include more stocks)
    elif market_regime == 'low_volatility':
        min_gain = -0.008  # Accept larger losses for momentum (more aggressive)
        min_volatility = 0.003  # 0.3% minimum volatility (lower)
        max_volatility = 0.08   # 8% maximum volatility (increased)
        volume_threshold = 0.15   # 15% of median volume (much lower)
    else:  # normal
        min_gain = 0.0003  # 0.03% minimum gain (lower to catch more opportunities)
        min_volatility = 0.005  # 0.5% minimum volatility (lower)
        max_volatility = 0.12   # 12% maximum volatility (increased)
        volume_threshold = 0.2   # 20% of median volume (lower)
    
    # Score and filter tickers
    for ticker, d in market_data.items():
        if allowed_sectors and d.get('sector') not in allowed_sectors:
            continue
        
        try:
            close_val = float(d['close'])
            open_val = float(d['open'])
            high_val = float(d['high'])
            low_val = float(d['low'])
            volume = float(d['volume'])
            
            gain_pct = (close_val - open_val) / open_val
            volatility = (high_val - low_val) / open_val
            rel_strength = gain_pct - avg_gain
            vol_score = volume / avg_vol
            
            # Adaptive filtering
            if (gain_pct >= min_gain and 
                min_volatility <= volatility <= max_volatility and
                volume >= median_vol * volume_threshold):
                
                # Advanced scoring based on market regime
                if market_regime == 'high_volatility':
                    # In high volatility, favor momentum and volume
                    score = (
                        0.4 * gain_pct +
                        0.3 * vol_score +
                        0.2 * volatility +
                        0.1 * rel_strength
                    )
                elif market_regime == 'low_volatility':
                    # In low volatility, favor any movement and relative strength
                    score = (
                        0.3 * abs(gain_pct) +  # Any movement is good
                        0.3 * rel_strength +
                        0.2 * vol_score +
                        0.2 * volatility
                    )
                else:  # normal
                    # Balanced scoring
                    score = (
                        0.4 * gain_pct +
                        0.25 * vol_score +
                        0.2 * volatility +
                        0.15 * rel_strength
                    )
                
                gainers.append((ticker, score, gain_pct, volume, volatility, d.get('sector', 'Unknown')))
        except Exception as e:
            continue
    
    # Sort by score and diversify
    gainers.sort(key=lambda x: x[1], reverse=True)
    
    # Diversification logic
    diversified = []
    used = set()
    
    # First, try to get at least one from each sector
    for sector in allowed_sectors:
        sector_tickers = [g for g in gainers if g[5] == sector and g[0] not in used]
        if sector_tickers:
            diversified.append(sector_tickers[0])
            used.add(sector_tickers[0][0])
    
    # Fill remaining spots with best candidates
    for g in gainers:
        if g[0] not in used and len(diversified) < 12:  # Increased to 12 stocks for more opportunities
            diversified.append(g)
            used.add(g[0])
    
    # If we still don't have enough, relax constraints
    if len(diversified) < 5:
        for ticker, d in market_data.items():
            if ticker not in used and len(diversified) < 12:
                try:
                    close_val = float(d['close'])
                    open_val = float(d['open'])
                    if abs(close_val - open_val) / open_val > 0.0005:  # Any 0.05% movement (lower threshold)
                        diversified.append((ticker, 0, 0, 0, 0, 'Unknown'))
                        used.add(ticker)
                except:
                    continue
    
    return [g[0] for g in diversified[:12]]

def decide_entry_exit_adaptive(ticker_data, available_funds=25000, min_tickers=5, market_regime='normal'):
    """
    Adaptive entry/exit decisions based on market regime
    """
    if not ticker_data:
        return {'entry': None, 'exit': None}
    
    entry = ticker_data['open']
    high = ticker_data['high']
    low = ticker_data['low']
    close = ticker_data['close']
    
    # Adaptive parameters based on market regime - ENHANCED FOR $150/DAY TARGET
    if market_regime == 'high_volatility':
        stop_loss_pct = 0.03   # 3% stop loss (increased for more aggressive trades)
        trailing_trigger = 1.12  # 12% gain to trigger trailing stop (higher threshold)
        trailing_stop_pct = 0.04  # 4% trailing stop (wider to capture more gains)
        min_profit_pct = 0.008   # 0.8% minimum profit (higher for better trades)
        max_allocation = 0.85     # 85% max allocation per trade (more aggressive)
    elif market_regime == 'low_volatility':
        stop_loss_pct = 0.02   # 2% stop loss
        trailing_trigger = 1.04  # 4% gain to trigger trailing stop
        trailing_stop_pct = 0.02  # 2% trailing stop
        min_profit_pct = 0.002   # 0.2% minimum profit
        max_allocation = 0.9     # 90% max allocation per trade (very aggressive for low vol)
    else:  # normal
        stop_loss_pct = 0.025   # 2.5% stop loss
        trailing_trigger = 1.08  # 8% gain to trigger trailing stop
        trailing_stop_pct = 0.03  # 3% trailing stop
        min_profit_pct = 0.004   # 0.4% minimum profit (higher threshold)
        max_allocation = 0.8     # 80% max allocation per trade
    
    # Calculate stop loss and exit strategy
    stop_loss = round(entry * (1 - stop_loss_pct), 2)
    
    # Determine exit price and type
    if high >= entry * trailing_trigger:
        # Trailing stop triggered
        trail_exit = round(high * (1 - trailing_stop_pct), 2)
        if trail_exit > close:
            exit_price = trail_exit
            exit_type = 'trailing_stop'
        else:
            exit_price = close
            exit_type = 'close'
    elif low <= stop_loss:
        # Stop loss hit
        exit_price = stop_loss
        exit_type = 'stop_loss'
    else:
        # Normal close
        exit_price = close
        exit_type = 'close'
    
    # Check minimum profit requirement - RESTORE ORIGINAL WORKING LOGIC
    if exit_price > entry:
        profit_pct = (exit_price - entry) / entry
        if profit_pct < min_profit_pct:
            return {'entry': entry, 'exit': None, 'exit_type': 'skip_low_reward'}
    
    # RESTORE ORIGINAL WORKING POSITION SIZING LOGIC
    allocation = available_funds / max(1, min_tickers)
    
    if exit_price > entry:
        # Calculate aggressive position sizing - ORIGINAL LOGIC THAT WORKED
        profit_per_share = exit_price - entry
        
        # Target different profit levels based on market regime - ENHANCED FOR $150/DAY TARGET
        if market_regime == 'high_volatility':
            target_profit = 250 / max(1, min_tickers)  # $250 per trade (increased from $150)
        elif market_regime == 'low_volatility':
            target_profit = 120 / max(1, min_tickers)   # $120 per trade (increased from $50)
        else:
            target_profit = 180 / max(1, min_tickers)  # $180 per trade (increased from $100)
        
        # Calculate shares needed for target profit
        target_shares = int(target_profit / profit_per_share) if profit_per_share > 0 else 0
        
        # Limit by available allocation
        max_shares_by_allocation = int(allocation * max_allocation / entry)
        
        # Take the minimum of target and allocation limit, but ensure reasonable minimum
        shares = min(target_shares, max_shares_by_allocation)
        
        # ENHANCED: Ensure we actually buy shares even if target is small
        if shares < 15:  # If calculated shares are too small (increased from 10)
            # Use a percentage of allocation instead - MORE AGGRESSIVE
            shares = max(15, int(allocation * 0.5 / entry))  # Use 50% of allocation minimum (increased from 30%)
            shares = min(shares, max_shares_by_allocation)  # But don't exceed allocation limit
    else:
        # Loss trade
        shares = 0
    
    invested = round(shares * entry, 2) if shares > 0 else 0
    expected_profit = round((exit_price - entry) * shares, 2) if shares > 0 else 0
    
    return {
        'entry': entry,
        'exit': exit_price,
        'exit_type': exit_type,
        'stop_loss': stop_loss,
        'shares': shares,
        'invested': invested,
        'expected_profit': expected_profit,
        'market_regime': market_regime
    }

def get_custom_tickers():
    """
    Get the custom ticker list from configuration
    """
    return CUSTOM_TICKERS

def select_custom_tickers(market_data=None):
    """
    Select tickers from the custom configuration list
    """
    custom_tickers = get_custom_tickers()
    
    if market_data:
        # Filter to only include tickers that have market data
        available_tickers = [ticker for ticker in custom_tickers if ticker in market_data]
        return available_tickers[:POSITION_SIZING['max_positions']]
    else:
        # Return all custom tickers up to max positions
        return custom_tickers[:POSITION_SIZING['max_positions']]

def calculate_position_size(ticker, price, available_funds, market_regime='normal'):
    """
    Calculate position size based on configuration method
    """
    method = POSITION_SIZING['method']
    
    if method == 'custom' and ticker in CUSTOM_POSITION_SIZES:
        # Use custom position size for this ticker
        target_value = CUSTOM_POSITION_SIZES[ticker]
    elif method == 'equal':
        # Equal position sizing
        target_value = available_funds / POSITION_SIZING['max_positions']
    else:
        # Adaptive position sizing (default)
        base_allocation = available_funds / POSITION_SIZING['max_positions']
        
        # Adjust based on market regime
        if market_regime == 'high_volatility':
            target_value = base_allocation * 0.8  # Reduce size in volatile markets
        elif market_regime == 'low_volatility':
            target_value = base_allocation * 1.2  # Increase size in stable markets
        else:
            target_value = base_allocation
    
    # Apply min/max constraints
    target_value = max(target_value, POSITION_SIZING['min_position_value'])
    target_value = min(target_value, POSITION_SIZING['max_position_value'])
    target_value = min(target_value, available_funds)
    
    # Calculate number of shares
    shares = int(target_value / price) if price > 0 else 0
    actual_investment = shares * price
    
    return shares, actual_investment

# Legacy function names for backward compatibility
def select_tickers(market_data, allowed_sectors=None, min_per_sector=1):
    """Legacy wrapper for backward compatibility"""
    market_regime = detect_market_regime(market_data)
    return select_tickers_adaptive(market_data, allowed_sectors, min_per_sector, market_regime)

def decide_entry_exit(ticker_data, available_funds=25000, min_tickers=5):
    """Legacy wrapper for backward compatibility"""
    # For legacy calls, we don't have market context, so use normal regime
    market_regime = 'normal'
    return decide_entry_exit_adaptive(ticker_data, available_funds, min_tickers, market_regime)
