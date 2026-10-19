"""
Main XAI - Entry point untuk testing dan demo XAI Module
"""
import asyncio
import sys
from pathlib import Path
from loguru import logger

# Tambahkan parent directory ke path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from data_collector.database import DatabaseManager
from .explanation_generator import ExplanationGenerator
from .trading_dictionary import TradingDictionary
from .context_builder import ContextBuilder
from .chat_agent import ChatAgent


# Setup logging
logger.remove()
logger.add(
    sys.stdout,
    level="INFO",
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | {message}",
)


async def demo_explanation_generator():
    """Demo explanation generator"""
    logger.info("\n" + "="*70)
    logger.info("📝 DEMO: Explanation Generator")
    logger.info("="*70)
    
    # Sample signal (mock data)
    sample_signal = {
        "symbol": "BTC/USDT",
        "signal": "STRONG_BUY",
        "confidence": 85.5,
        "final_score": 78.45,
        "interpretation": {
            "rsi": {
                "signal": "OVERSOLD",
                "score": 80,
                "reason": "RSI 28.5 < 30 → potensi rebound"
            },
            "macd": {
                "signal": "BULLISH_CROSSOVER",
                "score": 90,
                "reason": "MACD histogram baru crossover ke positif → sinyal beli kuat"
            },
            "ema": {
                "signal": "STRONG_UPTREND",
                "score": 85,
                "reason": "Harga > EMA20 > EMA50 > EMA200 → uptrend kuat"
            }
        },
        "sentiment": {
            "overall_score": 0.45,
            "overall_label": "POSITIVE",
            "positive_count": 12,
            "negative_count": 3,
            "total_articles": 20
        },
        "suggested_actions": {
            "action": "OPEN_LONG",
            "entry": 67234.50,
            "stop_loss": 65834.50,
            "take_profit": 70034.50,
            "position_size_percent": 10.0,
            "risk_reward_ratio": 2.0
        },
        "reasons": [
            "[RSI] RSI 28.5 < 30 → potensi rebound",
            "[MACD] MACD histogram baru crossover ke positif → sinyal beli kuat",
            "[EMA] Harga > EMA20 > EMA50 > EMA200 → uptrend kuat",
            "[SENTIMENT] POSITIVE → 12 positif, 3 negatif dari 20 artikel"
        ]
    }
    
    # Generate explanation
    generator = ExplanationGenerator()
    explanation = generator.generate_explanation(sample_signal)
    
    print(explanation)
    
    # Simple explanation
    simple = generator.generate_simple_explanation(sample_signal)
    logger.info(f"\n💡 Penjelasan Sederhana:\n{simple}")


async def demo_trading_dictionary():
    """Demo trading dictionary"""
    logger.info("\n" + "="*70)
    logger.info("📚 DEMO: Trading Dictionary")
    logger.info("="*70)
    
    dictionary = TradingDictionary()
    
    # Test some terms dari berbagai kategori
    test_terms = ["rsi", "macd", "stop_loss", "confidence", "bullish", "scalping"]
    
    for term in test_terms:
        term_data = dictionary.get_term(term)
        if term_data:
            print(dictionary.format_explanation(term_data, level="full"))
            print()


async def demo_context_builder():
    """Demo context builder"""
    logger.info("\n" + "="*70)
    logger.info("🏗️  DEMO: Context Builder")
    logger.info("="*70)
    
    db = DatabaseManager()
    await db.initialize()
    
    context_builder = ContextBuilder(db)
    
    # Build context for BTC
    context = await context_builder.build_symbol_context("BTC/USDT", "1h")
    
    # Print summary
    summary = context_builder.format_context_summary(context)
    print(summary)


async def demo_chat_agent():
    """Demo chat agent"""
    logger.info("\n" + "="*70)
    logger.info("💬 DEMO: Chat Agent")
    logger.info("="*70)
    
    db = DatabaseManager()
    await db.initialize()
    
    chat_agent = ChatAgent(db)
    
    # Test messages
    test_messages = [
        "halo",
        "apa itu RSI?",
        "portfolio",
        "kenapa bot buy?",
        "analisis BTC",
        "help"
    ]
    
    for message in test_messages:
        logger.info(f"\n👤 User: {message}")
        response = await chat_agent.process_message(message)
        logger.info(f"🤖 Bot:\n{response}\n")


async def interactive_chat():
    """Interactive chat session"""
    logger.info("\n" + "="*70)
    logger.info("💬 INTERACTIVE CHAT SESSION")
    logger.info("="*70)
    logger.info("Ketik 'quit' atau 'exit' untuk keluar")
    logger.info("Ketik 'help' untuk bantuan\n")
    
    db = DatabaseManager()
    await db.initialize()
    
    chat_agent = ChatAgent(db)
    
    while True:
        try:
            message = input("\n👤 You: ").strip()
            
            if message.lower() in ["quit", "exit", "keluar"]:
                logger.info("\n👋 Sampai jumpa!")
                break
            
            if not message:
                continue
            
            response = await chat_agent.process_message(message)
            print(f"\n🤖 Bot:\n{response}")
            
        except KeyboardInterrupt:
            logger.info("\n\n👋 Sampai jumpa!")
            break
        except Exception as e:
            logger.error(f"❌ Error: {e}")


async def main():
    """Main entry point"""
    logger.info("\n" + "="*70)
    logger.info("🤖 XAI MODULE - DEMO & TESTING")
    logger.info("="*70)
    
    # Run all demos
    await demo_explanation_generator()
    await demo_trading_dictionary()
    await demo_context_builder()
    await demo_chat_agent()
    
    # Ask for interactive chat
    logger.info("\n" + "="*70)
    choice = input("Mulai interactive chat? (y/n): ").strip().lower()
    
    if choice == 'y':
        await interactive_chat()
    
    logger.info("\n✅ XAI Demo completed!")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("\n\n⚠️  Demo stopped by user")
    except Exception as e:
        logger.exception(f"💥 Fatal error: {e}")
        sys.exit(1)
