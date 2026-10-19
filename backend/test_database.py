"""
Test Database - Script untuk mengecek data yang sudah dikumpulkan

Cara menjalankan:
    cd backend
    python test_database.py
"""

import asyncio
from data_collector.database import DatabaseManager


async def test():
    """Test database operations"""
    db = DatabaseManager()
    
    print("=" * 70)
    print("🔍 Testing Database - AI Trading Agent")
    print("=" * 70)
    
    # ========================================
    # 1. Cek candle terbaru BTC
    # ========================================
    print("\n📊 BTC/USDT 1H candles (last 5):")
    candles = await db.get_candles("BTC/USDT", "1h", limit=5)
    print(f"   Found: {len(candles)} candles")
    
    for c in candles:
        timestamp = c['timestamp']
        print(f"  - {timestamp}: O={c['open']:.2f} H={c['high']:.2f} L={c['low']:.2f} C={c['close']:.2f}")
    
    # ========================================
    # 2. Cek berita terbaru
    # ========================================
    print("\n📰 Latest news (last 3):")
    news = await db.get_latest_news(limit=3)
    print(f"   Found: {len(news)} articles")
    
    for n in news:
        title = n['title'][:60] + "..." if len(n['title']) > 60 else n['title']
        print(f"  - [{n['source']}] {title}")
    
    # ========================================
    # 3. Statistik database
    # ========================================
    print("\n📈 Database Statistics:")
    
    # Count candles
    candle_count = await db.get_candle_count("BTC/USDT", "1h")
    print(f"   BTC/USDT 1H candles: {candle_count}")
    
    # Count all symbols
    total_candles = 0
    for symbol in ["BTC/USDT", "ETH/USDT", "SOL/USDT", "BNB/USDT", "XRP/USDT"]:
        count = await db.get_candle_count(symbol, "1h")
        total_candles += count
    print(f"   Total 1H candles (all symbols): {total_candles}")
    
    # Count news
    news_count = await db.get_news_count()
    print(f"   Total news articles: {news_count}")
    
    # Latest ticker
    ticker = await db.get_latest_ticker("BTC/USDT")
    if ticker:
        print(f"\n💹 Latest BTC/USDT ticker:")
        print(f"   Price: ${ticker['price']:,.2f}")
        print(f"   24h Change: {ticker['price_change_24h']:+.2f}%")
        print(f"   Volume: {ticker['volume_24h']:,.2f}")
    
    print("\n" + "=" * 70)
    print("✅ Database test completed successfully!")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(test())
