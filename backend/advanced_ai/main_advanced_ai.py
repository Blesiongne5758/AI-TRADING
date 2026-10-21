"""
Main Advanced AI - Entry point untuk testing dan demo
"""
import asyncio
import sys
from pathlib import Path
from loguru import logger

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from .config import AdvancedAIConfig
from .finbert_analyzer import FinBERTAnalyzer
from .news_api_client import NewsAPIClient
from .twitter_analyzer import TwitterAnalyzer
from .sentiment_aggregator import SentimentAggregator
from .pump_dump_detector import PumpDumpDetector
from .advanced_indicators import AdvancedIndicators
from .cache_manager import cache


# Setup logging
logger.remove()
logger.add(
    sys.stdout,
    level="INFO",
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | {message}",
)


async def demo_finbert():
    """Demo FinBERT sentiment analysis"""
    logger.info("\n" + "=" * 70)
    logger.info("🧠 DEMO: FinBERT Sentiment Analysis")
    logger.info("=" * 70)
    
    # Initialize
    analyzer = FinBERTAnalyzer()
    await analyzer.initialize()
    
    # Test texts
    test_texts = [
        "Bitcoin reaches new all-time high as institutional adoption accelerates",
        "Crypto market crashes amid regulatory concerns and fear",
        "Ethereum 2.0 upgrade shows promising results for scalability",
        "Bitcoin price consolidates around key support level",
        "Major exchange hacked, millions in crypto stolen"
    ]
    
    logger.info("\n📝 Analyzing texts with FinBERT:")
    for text in test_texts:
        result = analyzer.analyze_text(text)
        emoji = "🟢" if result["label"] == "POSITIVE" else "🔴" if result["label"] == "NEGATIVE" else "⚪"
        logger.info(f"\n{emoji} {result['label']} (score: {result['sentiment_score']:+.3f})")
        logger.info(f"   Text: {text[:60]}...")


async def demo_news_api():
    """Demo News API integration"""
    logger.info("\n" + "=" * 70)
    logger.info("📰 DEMO: News API Integration")
    logger.info("=" * 70)
    
    # Initialize
    client = NewsAPIClient()
    await client.initialize()
    
    try:
        # Fetch from CryptoPanic
        logger.info("\n📰 Fetching from CryptoPanic...")
        crypto_news = await client.fetch_cryptopanic(
            currencies=["BTC", "ETH"],
            limit=10,
            filter_type="hot"
        )
        
        logger.info(f"✅ Fetched {len(crypto_news)} articles from CryptoPanic")
        for article in crypto_news[:3]:
            logger.info(f"   • [{article['source']}] {article['title'][:60]}...")
        
        # Fetch from NewsAPI
        logger.info("\n📰 Fetching from NewsAPI...")
        general_news = await client.fetch_newsapi(
            query="bitcoin",
            limit=10
        )
        
        logger.info(f"✅ Fetched {len(general_news)} articles from NewsAPI")
        for article in general_news[:3]:
            logger.info(f"   • [{article['source']}] {article['title'][:60]}...")
        
        # Fetch from all sources
        logger.info("\n📰 Fetching from all sources...")
        all_news = await client.fetch_all(
            currencies=["BTC", "ETH"],
            limit_per_source=5
        )
        
        logger.info(f"✅ Total unique articles: {len(all_news)}")
        
        # Show cache stats
        stats = client.get_cache_stats()
        logger.info(f"\n💾 Cache stats: {stats}")
        
    finally:
        await client.close()


async def demo_twitter_analyzer():
    """Demo Twitter/X analyzer"""
    logger.info("\n" + "=" * 70)
    logger.info("📱 DEMO: Twitter/X Analyzer")
    logger.info("=" * 70)
    
    # Initialize
    finbert = FinBERTAnalyzer()
    await finbert.initialize()
    
    analyzer = TwitterAnalyzer(finbert_analyzer=finbert)
    await analyzer.initialize()
    
    try:
        # Fetch tweets
        logger.info("\n🐦 Fetching tweets...")
        tweets = await analyzer.fetch_twitter_mentions(
            query="bitcoin OR BTC",
            max_results=20
        )
        
        logger.info(f"✅ Fetched {len(tweets)} tweets")
        
        if tweets:
            # Analyze sentiment
            logger.info("\n🧠 Analyzing sentiment...")
            sentiment = await analyzer.analyze_sentiment(tweets)
            
            emoji = "🟢" if sentiment["overall_label"] == "POSITIVE" else "🔴" if sentiment["overall_label"] == "NEGATIVE" else "⚪"
            logger.info(f"\n{emoji} Overall: {sentiment['overall_label']} (score: {sentiment['overall_score']:+.3f})")
            logger.info(f"   Positive: {sentiment['positive_count']}")
            logger.info(f"   Negative: {sentiment['negative_count']}")
            logger.info(f"   Neutral: {sentiment['neutral_count']}")
            
            # Detect hype/FUD
            logger.info("\n🔥 Detecting hype/FUD keywords...")
            for tweet in tweets[:5]:
                text = tweet.get("text", "")
                hype_keywords = analyzer.detect_hype_keywords(text)
                fud_keywords = analyzer.detect_fud_keywords(text)
                
                if hype_keywords:
                    logger.info(f"   🔥 Hype: {hype_keywords}")
                if fud_keywords:
                    logger.info(f"   😨 FUD: {fud_keywords}")
        
    finally:
        await analyzer.close()


async def demo_sentiment_aggregator():
    """Demo sentiment aggregator"""
    logger.info("\n" + "=" * 70)
    logger.info("🔄 DEMO: Sentiment Aggregator")
    logger.info("=" * 70)
    
    # Initialize
    aggregator = SentimentAggregator()
    await aggregator.initialize()
    
    try:
        # Aggregate sentiment
        logger.info("\n🔄 Aggregating sentiment from all sources...")
        results = await aggregator.aggregate_sentiment(
            currencies=["BTC", "ETH"],
            include_news=True,
            include_social=True,
            include_pump_detection=True
        )
        
        # Print summary
        summary = aggregator.format_summary(results)
        print(summary)
        
    finally:
        await aggregator.close()


async def demo_pump_dump_detector():
    """Demo pump & dump detector"""
    logger.info("\n" + "=" * 70)
    logger.info("🚨 DEMO: Pump & Dump Detector")
    logger.info("=" * 70)
    
    import pandas as pd
    import numpy as np
    
    # Create sample data with pump pattern
    dates = pd.date_range(end=datetime.now(), periods=100, freq='h')
    
    prices = []
    volumes = []
    
    base_price = 50000
    base_volume = 1000
    
    for i in range(100):
        if i < 80:
            # Normal market
            price = base_price + np.random.normal(0, 100)
            volume = base_volume + np.random.normal(0, 100)
        elif i < 90:
            # Pump phase
            price = base_price * (1 + (i - 80) * 0.05)
            volume = base_volume * (1 + (i - 80) * 0.5)
        else:
            # Dump phase
            price = base_price * 1.5 * (1 - (i - 90) * 0.08)
            volume = base_volume * 3
        
        prices.append(price)
        volumes.append(volume)
    
    candles = pd.DataFrame({
        "timestamp": dates,
        "open": prices,
        "high": [p * 1.01 for p in prices],
        "low": [p * 0.99 for p in prices],
        "close": prices,
        "volume": volumes
    })
    
    # Detect pump & dump
    detector = PumpDumpDetector()
    result = detector.detect_pump_and_dump(candles)
    
    logger.info("\n🚨 Pump & Dump Detection:")
    logger.info(f"   Detected: {result['pump_dump_detected']}")
    logger.info(f"   Overall Risk: {result['overall_risk']}")
    logger.info(f"   Risk Score: {result['risk_score']:.2f}")
    
    logger.info(f"\n📊 Volume Analysis:")
    logger.info(f"   Anomaly: {result['volume_analysis']['anomaly_detected']}")
    logger.info(f"   Volume Ratio: {result['volume_analysis']['volume_ratio']:.2f}x")
    
    logger.info(f"\n💹 Price Analysis:")
    logger.info(f"   Spike: {result['price_analysis']['spike_detected']}")
    logger.info(f"   Price Change: {result['price_analysis']['price_change_percent']:+.2f}%")
    
    logger.info(f"\n💡 Recommendation: {result['recommendation']}")


async def demo_advanced_indicators():
    """Demo advanced indicators"""
    logger.info("\n" + "=" * 70)
    logger.info("📊 DEMO: Advanced Indicators")
    logger.info("=" * 70)
    
    import pandas as pd
    import numpy as np
    
    # Create sample data
    dates = pd.date_range(end=pd.Timestamp.now(), periods=200, freq='h')
    
    base_price = 50000
    prices = [base_price + np.random.normal(0, 100) for _ in range(200)]
    
    df = pd.DataFrame({
        "timestamp": dates,
        "open": prices,
        "high": [p * 1.01 for p in prices],
        "low": [p * 0.99 for p in prices],
        "close": prices,
        "volume": [1000 + np.random.normal(0, 100) for _ in range(200)]
    })
    
    # Calculate advanced indicators
    indicators = AdvancedIndicators()
    results = indicators.calculate_all(df)
    
    logger.info("\n📊 Advanced Indicators:")
    
    logger.info(f"\n🌥️  Ichimoku Cloud:")
    logger.info(f"   Signal: {results['ichimoku']['signal']}")
    logger.info(f"   Score: {results['ichimoku']['score']}")
    logger.info(f"   Price Position: {results['ichimoku']['price_position']}")
    
    logger.info(f"\n📐 Fibonacci Retracement:")
    logger.info(f"   Signal: {results['fibonacci']['signal']}")
    logger.info(f"   Score: {results['fibonacci']['score']}")
    logger.info(f"   Position: {results['fibonacci']['position']}")
    logger.info(f"   Nearest Level: {results['fibonacci']['nearest_level']}")
    
    logger.info(f"\n🎯 Pivot Points:")
    logger.info(f"   Signal: {results['pivot_points']['signal']}")
    logger.info(f"   Score: {results['pivot_points']['score']}")
    logger.info(f"   Position: {results['pivot_points']['position']}")
    
    logger.info(f"\n📈 VWAP:")
    logger.info(f"   Signal: {results['vwap']['signal']}")
    logger.info(f"   Price vs VWAP: {results['vwap']['price_vs_vwap']:+.2f}%")
    
    logger.info(f"\n🛑 ATR Trailing Stop:")
    logger.info(f"   Trend: {results['atr_trailing_stop']['trend']}")
    logger.info(f"   Recommended Stop: ${results['atr_trailing_stop']['recommended_stop']:,.2f}")
    logger.info(f"   Distance: {results['atr_trailing_stop']['distance_percent']:.2f}%")
    
    logger.info(f"\n🎯 Overall:")
    logger.info(f"   Signal: {results['overall']['signal']}")
    logger.info(f"   Score: {results['overall']['score']:.1f}")


async def main():
    """Main entry point"""
    logger.info("\n" + "=" * 70)
    logger.info("🧠 ADVANCED AI MODULE - DEMO & TESTING")
    logger.info("=" * 70)
    
    # Print configuration
    AdvancedAIConfig.print_config()
    
    # Run all demos
    await demo_finbert()
    await demo_news_api()
    await demo_twitter_analyzer()
    await demo_sentiment_aggregator()
    await demo_pump_dump_detector()
    await demo_advanced_indicators()
    
    # Print cache stats
    logger.info("\n" + "=" * 70)
    logger.info("💾 CACHE STATISTICS")
    logger.info("=" * 70)
    cache.print_stats()
    
    logger.info("\n✅ All demos completed!")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("\n\n⚠️  Demo stopped by user")
    except Exception as e:
        logger.exception(f"💥 Fatal error: {e}")
        sys.exit(1)
