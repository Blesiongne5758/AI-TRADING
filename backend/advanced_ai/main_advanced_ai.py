"""
Main Advanced AI - Testing & Demo
"""
import asyncio
import sys
import json
from pathlib import Path
from loguru import logger

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from .finbert_analyzer import FinBERTAnalyzer
from .news_api_client import NewsAPIClient
from .twitter_analyzer import SocialMediaAnalyzer
from .pump_dump_detector import PumpDumpDetector
from .sentiment_aggregator import SentimentAggregator


async def test_finbert():
    """Test FinBERT analyzer"""
    logger.info("\n" + "="*70)
    logger.info("🧠 TESTING FINBERT ANALYZER")
    logger.info("="*70)

    analyzer = FinBERTAnalyzer()

    test_texts = [
        "Bitcoin reaches new all-time high as institutional adoption accelerates",
        "Major crypto exchange hacked, millions stolen in security breach",
        "Federal Reserve announces interest rate decision, markets react",
        "Ethereum upgrade successfully deployed, gas fees drop significantly",
        "Regulatory crackdown looms as SEC announces new crypto enforcement actions",
    ]

    for text in test_texts:
        result = await analyzer.analyze(text, use_cache=False)
        emoji = "🟢" if result["score"] > 0.1 else "🔴" if result["score"] < -0.1 else "⚪"
        logger.info(
            f"{emoji} [{result['label']:8}] {result['score']:+.3f} "
            f"(conf: {result['confidence']:.2f}) | {text[:60]}..."
        )


async def test_news_sources():
    """Test news API sources"""
    logger.info("\n" + "="*70)
    logger.info("📰 TESTING NEWS SOURCES")
    logger.info("="*70)

    client = NewsAPIClient()
    logger.info(f"Enabled sources: {client.get_enabled_sources()}")

    # Test CryptoPanic
    articles = await client.fetch_cryptopanic(currencies=["BTC"], limit=5)
    logger.info(f"CryptoPanic: {len(articles)} articles")
    for a in articles[:3]:
        logger.info(f"  - {a['title'][:70]}...")

    await client.close()


async def test_social_media():
    """Test social media analyzer"""
    logger.info("\n" + "="*70)
    logger.info("📱 TESTING SOCIAL MEDIA ANALYZER")
    logger.info("="*70)

    analyzer = SocialMediaAnalyzer()

    # Test Reddit
    posts = await analyzer.fetch_reddit(query="bitcoin", limit=5)
    logger.info(f"Reddit: {len(posts)} posts")
    for p in posts[:3]:
        logger.info(f"  - [{p['source']}] {p['title'][:60]}...")

    await analyzer.close()


async def test_full_sentiment_analysis():
    """Test full sentiment aggregation"""
    logger.info("\n" + "="*70)
    logger.info("🎯 TESTING FULL SENTIMENT ANALYSIS")
    logger.info("="*70)

    aggregator = SentimentAggregator()

    result = await aggregator.analyze_symbol("BTC/USDT", include_pump_detection=False)

    logger.info(f"\n📊 FINAL RESULT for BTC/USDT:")
    logger.info(f"   Label: {result['label']}")
    logger.info(f"   Score: {result['final_score']:+.3f}")
    logger.info(f"   Confidence: {result['confidence']}%")
    logger.info(f"   Total samples: {result['total_samples']}")

    logger.info(f"\n📈 SOURCE BREAKDOWN:")
    for source,  in result["source_breakdown"].items():
        logger.info(
            f"   {source:25} | Score: {data['score']:+.3f} | "
            f"Weight: {data['weight']:.2f} | Samples: {data['sample_size']}"
        )

    logger.info(f"\n🟢 TOP POSITIVE:")
    for item in result["top_positive"][:3]:
        logger.info(f"   [{item['score']:+.3f}] {item['text'][:80]}...")

    logger.info(f"\n🔴 TOP NEGATIVE:")
    for item in result["top_negative"][:3]:
        logger.info(f"   [{item['score']:+.3f}] {item['text'][:80]}...")

    await aggregator.close()


async def test_pump_detection():
    """Test pump & dump detector"""
    logger.info("\n" + "="*70)
    logger.info("🚨 TESTING PUMP & DUMP DETECTOR")
    logger.info("="*70)

    detector = PumpDumpDetector()

    # Simulasi data pump
    test_data = {
        "symbol": "SHIB/USDT",
        "price_ {
            "current": 0.000025,
            "1h_ago": 0.000018,  # +38% dalam 1 jam
            "24h_ago": 0.000015,  # +66% dalam 24 jam
            "high_24h": 0.000026,
            "low_24h": 0.000014,
        },
        "volume_ [100] * 21 + [500, 800, 1200],  # Volume spike
        "social_mentions": [
            {"text": "SHIB to the moon!", "engagement_score": 100}
            for _ in range(60)
        ],
    }

    result = detector.analyze_symbol(**test_data)

    logger.info(f"\n📊 PUMP DETECTION RESULT:")
    logger.info(f"   Symbol: {result['symbol']}")
    logger.info(f"   Pattern: {result['pattern']}")
    logger.info(f"   Risk Level: {result['risk_level']}")
    logger.info(f"   Pump Score: {result['pump_score']}")
    logger.info(f"   Dump Score: {result['dump_score']}")
    logger.info(f"\n🚨 SIGNALS:")
    for signal in result["signals"]:
        logger.info(f"   [{signal['severity']:6}] {signal['type']}: {signal['message']}")
    logger.info(f"\n💡 RECOMMENDATION:")
    logger.info(f"   {result['recommendation']}")


async def main():
    """Main entry point"""
    mode = "full"  # Options: finbert, news, social, pump, full

    try:
        if mode == "finbert":
            await test_finbert()
        elif mode == "news":
            await test_news_sources()
        elif mode == "social":
            await test_social_media()
        elif mode == "pump":
            await test_pump_detection()
        elif mode == "full":
            await test_finbert()
            await test_pump_detection()
            await test_full_sentiment_analysis()
    except Exception as e:
        logger.exception(f"💥 Error: {e}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logger.exception(f"💥 Fatal error: {e}")
        sys.exit(1)
