"""
Main Analysis - Entry point untuk testing Analysis Engine

Cara menjalankan:
    cd backend
    python -m analysis.main_analysis
"""

import asyncio
import pandas as pd
from typing import List
from loguru import logger

from data_collector.database import DatabaseManager
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
    
    # Convert to DataFrame
    df = pd.DataFrame(candles)
    
    # 2. Load news untuk sentiment analysis
    news = await db.get_latest_news(limit=20)
    news_texts = [n['title'] + " " + (n.get('summary') or '') for n in news]
    
    logger.info(f"📊 Loaded {len(df)} candles dan {len(news_texts)} news articles")
    
    # 3. Generate signal
    generator = SignalGenerator(use_ml_sentiment=False)
    signal = generator.generate(df, news_texts, symbol, timeframe)
    
    # 4. Print results
    print(f"\n📈 SIGNAL: {signal['action']}")
    print(f"🎯 Confidence: {signal['confidence']}%")
    print(f"💰 Current Price: ${signal['price']:,.2f}")
    
    print(f"\n📋 Reasons:")
    for i, reason in enumerate(signal['reasons'], 1):
        print(f"   {i}. {reason}")
    
    print(f"\n🛡️  Risk Management:")
    rm = signal['risk_management']
    print(f"   Stop Loss: ${rm['stop_loss']:,.2f}")
    print(f"   Take Profit: ${rm['take_profit']:,.2f}")
    print(f"   Risk/Reward Ratio: {rm['risk_reward_ratio']:.2f}")
    print(f"   Position Size: {rm['position_size_percent']:.1f}% of portfolio")
    
    print(f"\n📊 Technical Indicators:")
    tech = signal['technical']
    print(f"   RSI: {tech.get('rsi', 0):.2f} ({tech.get('rsi_signal', 'N/A')})")
    print(f"   MACD: {tech.get('macd', 0):.2f} ({tech.get('macd_signal', 'N/A')})")
    print(f"   EMA 20/50/200: {tech.get('ema_20', 0):.2f} / {tech.get('ema_50', 0):.2f} / {tech.get('ema_200', 0):.2f}")
    print(f"   Bollinger Bands: {tech.get('bb_lower', 0):.2f} - {tech.get('bb_upper', 0):.2f}")
    print(f"   Volume Ratio: {tech.get('volume_ratio', 0):.2f}x")
    
    print(f"\n📰 Sentiment Analysis:")
    sent = signal['sentiment']
    print(f"   Score: {sent.get('score', 0):+.3f}")
    print(f"   Label: {sent.get('label', 'N/A')}")
    print(f"   Confidence: {sent.get('confidence', 0)}%")
    print(f"   Method: {sent.get('method', 'N/A')}")
    
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
