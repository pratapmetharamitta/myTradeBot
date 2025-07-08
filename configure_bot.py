#!/usr/bin/env python3
"""
TradeBot Configuration Tool
Easy way to customize your trading bot settings
"""

from config import CUSTOM_TICKERS, POSITION_SIZING, CUSTOM_POSITION_SIZES, STRATEGY_CONFIG

def display_current_config():
    """Display current configuration"""
    print("=" * 60)
    print("🤖 CURRENT TRADEBOT CONFIGURATION")
    print("=" * 60)
    
    print(f"\n📊 TICKER LIST ({len(CUSTOM_TICKERS)} tickers):")
    for i, ticker in enumerate(CUSTOM_TICKERS, 1):
        print(f"  {i:2d}. {ticker}")
    
    print(f"\n💰 POSITION SIZING:")
    print(f"  Method: {POSITION_SIZING['method']}")
    print(f"  Min Position Value: ${POSITION_SIZING['min_position_value']:,}")
    print(f"  Max Position Value: ${POSITION_SIZING['max_position_value']:,}")
    print(f"  Max Positions: {POSITION_SIZING['max_positions']}")
    print(f"  Risk Per Trade: {POSITION_SIZING['risk_per_trade']*100:.1f}%")
    
    print(f"\n🎯 STRATEGY SETTINGS:")
    print(f"  Profit Threshold: {STRATEGY_CONFIG['profit_threshold']*100:.1f}%")
    print(f"  Stop Loss: {STRATEGY_CONFIG['stop_loss_pct']*100:.1f}%")
    print(f"  Trailing Stop: {STRATEGY_CONFIG['trailing_stop_pct']*100:.1f}%")
    print(f"  Min Volume: {STRATEGY_CONFIG['volume_threshold']:,}")
    print(f"  Min Volatility: {STRATEGY_CONFIG['volatility_threshold']*100:.1f}%")
    
    if CUSTOM_POSITION_SIZES:
        print(f"\n🔧 CUSTOM POSITION SIZES:")
        for ticker, size in CUSTOM_POSITION_SIZES.items():
            print(f"  {ticker}: ${size:,}")

def suggest_configurations():
    """Suggest different configuration templates"""
    print("\n" + "=" * 60)
    print("💡 SUGGESTED CONFIGURATIONS")
    print("=" * 60)
    
    print("\n🚀 AGGRESSIVE TRADING (High Risk/High Reward):")
    print("  - Large tech stocks: AAPL, MSFT, NVDA, TSLA, GOOGL")
    print("  - Position sizes: $3000-5000 each")
    print("  - Max 5 positions")
    print("  - 4% profit target, 3% stop loss")
    
    print("\n🛡️  CONSERVATIVE TRADING (Lower Risk):")
    print("  - Diversified: AAPL, MSFT, JNJ, PG, KO, WMT, PFE, XOM")
    print("  - Position sizes: $1500-2500 each")
    print("  - Max 8 positions")
    print("  - 2% profit target, 1.5% stop loss")
    
    print("\n⚡ MOMENTUM TRADING (Volatile Stocks):")
    print("  - High volatility: TSLA, NVDA, AMD, NFLX, ZOOM")
    print("  - Position sizes: $2000-4000 each")
    print("  - Max 6 positions")
    print("  - 5% profit target, 3.5% stop loss")
    
    print("\n💎 BLUE CHIP TRADING (Stable Large Caps):")
    print("  - Stable giants: AAPL, MSFT, GOOGL, AMZN, BRK.B, JPM")
    print("  - Position sizes: $2500-4000 each")
    print("  - Max 7 positions")
    print("  - 2.5% profit target, 2% stop loss")

def quick_setup_guide():
    """Quick setup guide"""
    print("\n" + "=" * 60)
    print("🛠️  QUICK SETUP GUIDE")
    print("=" * 60)
    
    print("\n1️⃣  CUSTOMIZE YOUR TICKERS:")
    print("   Edit config.py -> CUSTOM_TICKERS list")
    print("   Add your preferred stocks (e.g., ['AAPL', 'MSFT', 'TSLA'])")
    
    print("\n2️⃣  CHOOSE POSITION SIZING METHOD:")
    print("   'adaptive' - Smart sizing based on market conditions")
    print("   'equal' - Equal dollar amount for each position")
    print("   'custom' - Specific amount for each ticker")
    
    print("\n3️⃣  SET POSITION SIZES:")
    print("   min_position_value: Minimum $ per trade")
    print("   max_position_value: Maximum $ per trade")
    print("   max_positions: How many stocks to trade per day")
    
    print("\n4️⃣  ADJUST STRATEGY:")
    print("   profit_threshold: Target profit % (e.g., 0.03 = 3%)")
    print("   stop_loss_pct: Max loss % (e.g., 0.02 = 2%)")
    
    print("\n5️⃣  TEST YOUR SETTINGS:")
    print("   Run: python main.py (demo mode)")
    print("   Run: python backtest.py (historical test)")

def example_custom_configs():
    """Show example configurations you can copy"""
    print("\n" + "=" * 60)
    print("📝 COPY-PASTE EXAMPLES")
    print("=" * 60)
    
    print("\n🔥 EXAMPLE 1: Tech Focus")
    print("CUSTOM_TICKERS = ['AAPL', 'MSFT', 'NVDA', 'GOOGL', 'TSLA']")
    print("POSITION_SIZING = {")
    print("    'method': 'custom',")
    print("    'min_position_value': 2000,")
    print("    'max_position_value': 4000,")
    print("    'max_positions': 5,")
    print("}")
    print("CUSTOM_POSITION_SIZES = {")
    print("    'AAPL': 3000, 'MSFT': 3000, 'NVDA': 2500,")
    print("    'GOOGL': 3500, 'TSLA': 2000")
    print("}")
    
    print("\n💼 EXAMPLE 2: Diversified Portfolio")
    print("CUSTOM_TICKERS = ['AAPL', 'MSFT', 'JNJ', 'WMT', 'JPM', 'PG', 'XOM', 'KO']")
    print("POSITION_SIZING = {")
    print("    'method': 'equal',")
    print("    'min_position_value': 1500,")
    print("    'max_position_value': 2500,")
    print("    'max_positions': 8,")
    print("}")

def main():
    """Main configuration tool"""
    print("🤖 TradeBot Configuration Tool")
    
    while True:
        print("\n" + "=" * 60)
        print("MENU:")
        print("1. Show Current Configuration")
        print("2. View Suggested Configurations")
        print("3. Quick Setup Guide")
        print("4. Copy-Paste Examples")
        print("5. Exit")
        
        choice = input("\nSelect option (1-5): ").strip()
        
        if choice == '1':
            display_current_config()
        elif choice == '2':
            suggest_configurations()
        elif choice == '3':
            quick_setup_guide()
        elif choice == '4':
            example_custom_configs()
        elif choice == '5':
            print("\n👋 Happy Trading!")
            break
        else:
            print("Invalid choice. Please select 1-5.")

if __name__ == "__main__":
    main()
