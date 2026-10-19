"""
Main Analysis - Entry point untuk testing Analysis Engine

Cara menjalankan:
    cd backend
    python -m analysis.main_analysis
"""

import asyncio
from typing import List
from loguru import logger

from data_collector.database import DatabaseManager
from .technical_indicators import TechnicalAnalyzer
from .sentiment_analysis import SentimentAnalyzer
from .signal_generator import SignalGenerator


async def analyze_symbol(symbol: str, timeframe: str = "1h") -> None:
    """
    Analisis satu symbol
    
    Args:
        symbol: Trading pair (e.g., "BTC/USDT")
        timeframe: Timeframe (e.g., "1h")
    """
    logger.info(f"\n{'='*70}")
    logger.info(f"🔍 Analyzing {symbol} [{timeframe}]")
    logger.info(f"{'='*70}")
    
    # 1. Load data dari database
    db = DatabaseManager()
    candles = await db.get_candles(symbol, timeframe, limit=500)
    
    if len(candles) < 200:
        logger.warning(f"⚠️  Data tidak cukup ({len(candles)} candles), butuh minimal 200")
        return
    
    # 2. Load news untuk sentiment analysis
    news = await db.get_latest_news(limit=20)
    
    logger.info(f"📊 Loaded {len(candles)} candles dan {len(news)} news articles")
    
    # 3. Technical Analysis
    tech_analyzer = TechnicalAnalyzer()
    technical_result = tech_analyzer.calculate_all(candles)
    
    if technical_result is None:
        logger.warning(f"❌ Technical analysis gagal untuk {symbol}")
        return
    
    # 4. Sentiment Analysis
    sentiment_analyzer = SentimentAnalyzer(use_finbert=False)
    sentiment_result = sentiment_analyzer.analyze_news_batch(news)
    
    # 5. Generate Signal
    signal_gen = SignalGenerator()
    signal = signal_gen.generate_signal(
        symbol=symbol,
        timeframe=timeframe,
        technical_analysis=technical_result,
        sentiment_analysis=sentiment_result,
    )
    
    # 6. Print results
    print(f"\n📈 SIGNAL: {signal['signal']}")
    print(f"🎯 Confidence: {signal['confidence']:.1f}%")
    print(f"💰 Current Price: ${signal['latest_price']:,.2f}")
    print(f"📊 Final Score: {signal['final_score']:+.2f}")
    
    print(f"\n📋 Reasons:")
    for i, reason in enumerate(signal['reasons'], 1):
        print(f"   {i}. {reason}")
    
    print(f"\n🎯 Component Scores:")
    for component, data in signal['component_scores'].items():
        score = data['score']
        sig = data['signal']
        weight = data['weight']
        print(f"   {component.upper():12} | Score: {score:+6.1f} | Signal: {sig:20} | Weight: {weight:.0%}")
    
    print(f"\n🛡️  Suggested Actions:")
    actions = signal['suggested_actions']
    print(f"   Action: {actions['action']}")
    if actions['action'] != "HOLD":
        print(f"   Entry: ${actions['entry']:,.2f}")
        print(f"   Stop Loss: ${actions['stop_loss']:,.2f} ({actions['sl_distance_percent']:.2f}%)")
        print(f"   Take Profit: ${actions['take_profit']:,.2f} ({actions['tp_distance_percent']:.2f}%)")
        print(f"   Risk/Reward Ratio: {actions['risk_reward_ratio']:.1f}:1")
        print(f"   Position Size: {actions['position_size_percent']:.1f}% of portfolio")
        print(f"   Max Risk: {actions['max_risk_percent']:.1f}% of portfolio")
    else:
        print(f"   Reason: {actions['reason']}")
    
    print(f"\n📰 Sentiment Analysis:")
    print(f"   Overall Score: {signal['sentiment_score']:+.3f}")
    print(f"   Overall Label: {signal['sentiment_label']}")
    print(f"   Total Articles: {sentiment_result['total_articles']}")
    print(f"   Distribution: {sentiment_result['positive_count']} positive, {sentiment_result['negative_count']} negative, {sentiment_result['neutral_count']} neutral")
    
    print(f"\n⚠️  Risk Warning:")
    print(f"   {signal['risk_warning']}")
    
    # Show top 3 news articles with sentiment
    if sentiment_result.get('articles'):
        print(f"\n📰 Top News Articles:")
        for i, article in enumerate(sentiment_result['articles'][:3], 1):
            sent_data = article.get('sentiment', {})
            print(f"   {i}. [{article.get('source', 'Unknown')}] {article.get('title', 'No title')[:60]}...")
            print(f"      Sentiment: {sent_data.get('label', 'N/A')} (score: {sent_data.get('score', 0):+.3f})")
    
    print(f"\n{'='*70}\n")


async def analyze_all_symbols() -> None:
    """Analisis semua symbols"""
    symbols = ["BTC/USDT", "ETH/USDT", "SOL/USDT", "BNB/USDT", "XRP/USDT"]
    timeframe = "1h"
    
    logger.info(f"\n🚀 Starting Analysis Engine")
    logger.info(f"📊 Symbols: {', '.join(symbols)}")
    logger.info(f"⏰ Timeframe: {timeframe}")
    
    for symbol in symbols:
        try:
            await analyze_symbol(symbol, timeframe)
        except Exception as e:
            logger.error(f"❌ Error analyzing {symbol}: {e}")
    
    logger.info(f"\n✅ Analysis completed!")


async def main():
    """Main entry point"""
    try:
        # Analyze all symbols
        await analyze_all_symbols()
        
    except KeyboardInterrupt:
        logger.info("\n⚠️  Analysis interrupted by user")
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
        raise


if __name__ == "__main__":
    # Setup logging
    logger.add(
        "logs/analysis.log",
        rotation="10 MB",
        level="DEBUG"
    )
    
    # Run main
    asyncio.run(main())
