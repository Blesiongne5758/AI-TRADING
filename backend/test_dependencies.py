"""
Test Dependencies - Verifikasi semua dependencies terinstall dengan benar

Cara menjalankan:
    cd backend
    python test_dependencies.py
"""

import sys
from loguru import logger

# Setup logging
logger.remove()
logger.add(sys.stdout, format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | {message}", level="INFO")


def test_python_version():
    """Test Python version"""
    logger.info("🐍 Testing Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 11:
        logger.info(f"✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        logger.error(f"❌ Python {version.major}.{version.minor}.{version.micro} (butuh 3.11+)")
        return False


def test_import(module_name, package_name=None):
    """Test import module"""
    package_name = package_name or module_name
    try:
        __import__(module_name)
        logger.info(f"✅ {package_name} imported successfully")
        return True
    except ImportError as e:
        logger.error(f"❌ {package_name} not installed: {e}")
        return False


def test_pandas_ta():
    """Test pandas-ta functionality"""
    logger.info("📊 Testing pandas-ta...")
    try:
        import pandas as pd
        import pandas_ta as ta
        
        # Create sample data
        df = pd.DataFrame({
            'close': [100, 102, 101, 103, 105, 104, 106, 108, 107, 109] * 20
        })
        
        # Test RSI
        rsi = ta.rsi(df['close'], length=14)
        logger.info(f"✅ pandas-ta RSI calculation: {rsi.iloc[-1]:.2f}")
        
        # Test MACD
        macd = ta.macd(df['close'], fast=12, slow=26, signal=9)
        logger.info(f"✅ pandas-ta MACD calculation: {macd.iloc[-1, 0]:.2f}")
        
        return True
    except Exception as e:
        logger.error(f"❌ pandas-ta test failed: {e}")
        return False


def test_textblob():
    """Test TextBlob functionality"""
    logger.info("📝 Testing TextBlob...")
    try:
        from textblob import TextBlob
        
        # Test sentiment analysis
        text = "Bitcoin price is rising strongly, very bullish!"
        blob = TextBlob(text)
        
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        logger.info(f"✅ TextBlob sentiment: polarity={polarity:.3f}, subjectivity={subjectivity:.3f}")
        
        # Test corpora
        if polarity > 0:
            logger.info("✅ TextBlob corpora loaded correctly")
            return True
        else:
            logger.warning("⚠️  TextBlob sentiment seems incorrect, corpora might not be downloaded")
            logger.info("💡 Run: python -m textblob.download_corpora")
            return False
            
    except Exception as e:
        logger.error(f"❌ TextBlob test failed: {e}")
        return False


def test_database():
    """Test database connection"""
    logger.info("🗄️  Testing database...")
    try:
        import asyncio
        from data_collector.database import DatabaseManager
        
        async def test():
            db = DatabaseManager()
            await db.initialize()
            logger.info("✅ Database initialized successfully")
            return True
        
        return asyncio.run(test())
    except Exception as e:
        logger.error(f"❌ Database test failed: {e}")
        return False


def test_binance_connection():
    """Test Binance connection"""
    logger.info("🔌 Testing Binance connection...")
    try:
        import asyncio
        import ccxt.async_support as ccxt
        
        async def test():
            exchange = ccxt.binance({
                'enableRateLimit': True,
                'options': {'defaultType': 'spot'}
            })
            exchange.set_sandbox_mode(True)
            
            await exchange.load_markets()
            logger.info(f"✅ Binance connected, {len(exchange.markets)} markets loaded")
            
            await exchange.close()
            return True
        
        return asyncio.run(test())
    except Exception as e:
        logger.error(f"❌ Binance connection test failed: {e}")
        return False


def main():
    """Run all tests"""
    logger.info("=" * 70)
    logger.info("🧪 Testing AI Trading Agent Dependencies")
    logger.info("=" * 70)
    logger.info("")
    
    results = []
    
    # Test Python version
    results.append(("Python 3.11+", test_python_version()))
    logger.info("")
    
    # Test basic imports
    logger.info("📦 Testing basic imports...")
    results.append(("ccxt", test_import("ccxt")))
    results.append(("pandas", test_import("pandas")))
    results.append(("numpy", test_import("numpy")))
    results.append(("aiosqlite", test_import("aiosqlite")))
    results.append(("loguru", test_import("loguru")))
    results.append(("feedparser", test_import("feedparser")))
    logger.info("")
    
    # Test pandas-ta
    results.append(("pandas-ta", test_pandas_ta()))
    logger.info("")
    
    # Test TextBlob
    results.append(("TextBlob", test_textblob()))
    logger.info("")
    
    # Test database
    results.append(("Database", test_database()))
    logger.info("")
    
    # Test Binance connection
    results.append(("Binance", test_binance_connection()))
    logger.info("")
    
    # Summary
    logger.info("=" * 70)
    logger.info("📊 Test Summary")
    logger.info("=" * 70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        logger.info(f"{status} - {name}")
    
    logger.info("")
    logger.info(f"🎯 Results: {passed}/{total} tests passed")
    logger.info("")
    
    if passed == total:
        logger.info("🎉 All tests passed! Ready to use!")
        logger.info("")
        logger.info("🚀 Next steps:")
        logger.info("   1. Setup .env file with Binance API keys")
        logger.info("   2. Run data collector: python -m data_collector.main_collector")
        logger.info("   3. Run analysis engine: python -m analysis.main_analysis")
        return 0
    else:
        logger.error("❌ Some tests failed. Please fix the issues above.")
        logger.info("")
        logger.info("💡 Common fixes:")
        logger.info("   - Install missing packages: pip install -r requirements.txt")
        logger.info("   - Download TextBlob corpora: python -m textblob.download_corpora")
        logger.info("   - Check Python version: python --version (butuh 3.11+)")
        logger.info("   - See INSTALL.md for detailed troubleshooting")
        return 1


if __name__ == "__main__":
    sys.exit(main())
