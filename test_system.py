#!/usr/bin/env python3
"""
System Test Script for TradeBot
Tests all major components to ensure they work together properly
"""

import sys
import os
from datetime import datetime

def test_imports():
    """Test that all modules can be imported"""
    try:
        import main
        import strategy
        import data
        import config
        import fidelity_api
        import backtest
        import visualize_backtest
        print("✅ All imports successful")
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_strategy():
    """Test that strategy functions work"""
    try:
        from strategy import select_tickers, decide_entry_exit
        from data import get_mock_market_data
        
        market_data = get_mock_market_data()
        tickers = select_tickers(market_data, ['Tech', 'Healthcare'])
        
        if tickers:
            ticker_data = market_data.get(tickers[0], {})
            trade_plan = decide_entry_exit(ticker_data, 25000, 5)
            print(f"✅ Strategy test passed - Generated trade plan: {trade_plan}")
            return True
        else:
            print("❌ Strategy test failed - No tickers selected")
            return False
    except Exception as e:
        print(f"❌ Strategy test error: {e}")
        return False

def test_data():
    """Test that data functions work"""
    try:
        from data import get_mock_market_data
        market_data = get_mock_market_data()
        if market_data and len(market_data) > 0:
            print(f"✅ Data test passed - Got {len(market_data)} stocks")
            return True
        else:
            print("❌ Data test failed - No market data")
            return False
    except Exception as e:
        print(f"❌ Data test error: {e}")
        return False

def test_config():
    """Test that config is readable"""
    try:
        from config import FUNDS, DAILY_TARGET, BROKER
        print(f"✅ Config test passed - Funds: ${FUNDS}, Target: ${DAILY_TARGET}, Broker: {BROKER}")
        return True
    except Exception as e:
        print(f"❌ Config test error: {e}")
        return False

def test_main_demo():
    """Test main.py in demo mode"""
    try:
        os.environ['DEMO_MODE'] = 'true'
        # Import and test main without actually running the OAuth flow
        import main
        print("✅ Main demo mode test passed")
        return True
    except Exception as e:
        print(f"❌ Main demo test error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 TradeBot System Test")
    print("=" * 50)
    
    tests = [
        ("Imports", test_imports),
        ("Config", test_config),
        ("Data", test_data),
        ("Strategy", test_strategy),
        ("Main Demo", test_main_demo)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Testing {test_name}...")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} failed")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! TradeBot is ready to go!")
        return True
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
