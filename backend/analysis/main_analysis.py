"""
Main Analysis - Entry point untuk testing Modul B
"""
import asyncio
import sys
from pathlib import Path
from loguru import logger

# Tambahkan parent directory ke path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from data_collector.database import DatabaseManager
from .technical_indicators import TechnicalAnalyzer
from .sentiment_analysis import SentimentAnalyzer
from .signal_generator import SignalGenerator


# Setup logging
logger.remove()
logger.add(
    sys.stdout,
    level="INFO",
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | {message}",
)


async def analyze_symbol(symbol: str, timeframe: str = "1h"):
    """Analisis satu simbol dan tampilkan hasilnya"""
    logger.info(f"\n{'='*70}")
    logger.info(f"🔍 Menganalisis {symbol} [{timeframe}]")
    logger.info(f"{'='*70}")

    db = DatabaseManager()
    await db.initialize()

    # 1. Ambil data candle dari database
    candles = await db.get_candles(symbol, timeframe, limit=250)
    if not candles:
        logger.error(f"❌ Tidak ada data candle untuk {symbol} [{timeframe}]")
        return

    logger.info(f"📊 Loaded {len(candles)} candles")

    # 2. Analisis teknikal
    tech_analyzer = TechnicalAnalyzer()
    tech_result = tech_analyzer.calculate_all(candles)
    if not tech_result:
        logger.error("❌ Analisis teknikal gagal")
        return

    logger.info(f"\n💹 Harga terbaru: ${tech_result['latest_price']:,.2f}")
    logger.info("\n📈 Interpretasi Indikator:")
    for indicator, data in tech_result["interpretation"].items():
        logger.info(
            f"  • {indicator.upper():10} | {data['signal']:20} | "
            f"Score: {data['score']:+4} | {data['reason']}"
        )

    # 3. Analisis sentimen
    news_items = await db.get_latest_news(limit=15)
    logger.info(f"\n📰 Loaded {len(news_items)} news articles")

    sentiment_analyzer = SentimentAnalyzer(use_finbert=False)  # TextBlob untuk MVP
    sentiment_result = sentiment_analyzer.analyze_news_batch(news_items)

    logger.info(
        f"\n🧠 Sentimen Overall: {sentiment_result['overall_label']} "
        f"(score: {sentiment_result['overall_score']:+.3f})"
    )
    logger.info(
        f"   Distribusi: {sentiment_result['positive_count']} positif, "
        f"{sentiment_result['negative_count']} negatif, "
        f"{sentiment_result['neutral_count']} netral"
    )

    # 4. Generate trading signal
    signal_gen = SignalGenerator()
    signal = signal_gen.generate_signal(
        symbol=symbol,
        timeframe=timeframe,
        technical_analysis=tech_result,
        sentiment_analysis=sentiment_result,
    )

    # 5. Tampilkan hasil final
    logger.info(f"\n{'='*70}")
    logger.info(f"🎯 TRADING SIGNAL: {signal['signal']}")
    logger.info(f"{'='*70}")
    logger.info(f"   Confidence: {signal['confidence']:.1f}%")
    logger.info(f"   Final Score: {signal['final_score']:+.2f}")
    logger.info(f"   Technical Score: {signal['technical_score']:+.2f}")
    logger.info(f"   Sentiment: {signal['sentiment_label']} ({signal['sentiment_score']:+.3f})")

    logger.info(f"\n📋 Alasan Utama:")
    for i, reason in enumerate(signal["reasons"], 1):
        logger.info(f"   {i}. {reason}")

    logger.info(f"\n💡 Suggested Actions:")
    actions = signal["suggested_actions"]
    logger.info(f"   Action: {actions['action']}")
    if actions["entry"]:
        logger.info(f"   Entry: ${actions['entry']:,.2f}")
        logger.info(f"   Stop Loss: ${actions['stop_loss']:,.2f} (-{actions['sl_distance_percent']:.2f}%)")
        logger.info(f"   Take Profit: ${actions['take_profit']:,.2f} (+{actions['tp_distance_percent']:.2f}%)")
        logger.info(f"   Risk/Reward: 1:{actions['risk_reward_ratio']}")
        logger.info(f"   Position Size: {actions['position_size_percent']}% dari portfolio")
        logger.info(f"   Max Risk: {actions['max_risk_percent']}% dari portfolio")

    logger.info(f"\n⚠️  Risk Warning:")
    logger.info(f"   {signal['risk_warning']}")

    return signal


async def analyze_all_symbols():
    """Analisis semua simbol yang dipantau"""
    from data_collector.config import TRADING_SYMBOLS

    logger.info("🚀 Starting Analysis Engine - Analyzing all symbols")
    all_signals = []

    for symbol in TRADING_SYMBOLS:
        try:
            signal = await analyze_symbol(symbol, timeframe="1h")
            if signal:
                all_signals.append(signal)
        except Exception as e:
            logger.error(f"❌ Error analyzing {symbol}: {e}")

    # Summary
    logger.info(f"\n{'='*70}")
    logger.info(f"📊 SUMMARY - {len(all_signals)} symbols analyzed")
    logger.info(f"{'='*70}")

    for signal in all_signals:
        emoji = {
            "STRONG_BUY": "🟢🟢",
            "BUY": "🟢",
            "NEUTRAL": "⚪",
            "SELL": "🔴",
            "STRONG_SELL": "🔴🔴",
        }.get(signal["signal"], "⚪")

        logger.info(
            f"  {emoji} {signal['symbol']:12} | {signal['signal']:12} | "
            f"Confidence: {signal['confidence']:5.1f}% | "
            f"Score: {signal['final_score']:+6.2f}"
        )

    return all_signals


async def main():
    """Main entry point"""
    # Analisis 1 simbol saja untuk testing cepat
    await analyze_symbol("BTC/USDT", timeframe="1h")

    # Atau analisis semua simbol (uncomment baris di bawah):
    # await analyze_all_symbols()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("\n⚠️  Analysis stopped by user")
    except Exception as e:
        logger.exception(f"💥 Fatal error: {e}")
