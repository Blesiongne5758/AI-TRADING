"""
Main XAI - Entry point untuk testing Modul D
"""
import asyncio
import sys
from pathlib import Path
from loguru import logger

# Tambahkan parent directory ke path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from data_collector.database import DatabaseManager
from .chat_agent import ChatAgent


# Setup logging
logger.remove()
logger.add(
    sys.stdout,
    level="INFO",
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | {message}",
)


async def interactive_demo():
    """Demo interaktif chat agent"""
    db = DatabaseManager()
    await db.initialize()

    agent = ChatAgent(db)

    print("\n" + "=" * 70)
    print("🤖 AI TRADING ASSISTANT - INTERACTIVE DEMO")
    print("=" * 70)
    print("\nKetik 'quit' atau 'exit' untuk keluar")
    print("Ketik 'help' untuk melihat daftar pertanyaan\n")

    while True:
        try:
            user_input = input("\n👤 You: ").strip()

            if user_input.lower() in ["quit", "exit", "q"]:
                print("\n👋 Sampai jumpa! Selamat trading!")
                break

            if not user_input:
                continue

            # Process message
            response = await agent.process_message(user_input)

            print(f"\n🤖 AI:\n{response}")

        except KeyboardInterrupt:
            print("\n\n⚠️  Demo stopped by user")
            break
        except Exception as e:
            logger.error(f"❌ Error: {e}")


async def test_specific_queries():
    """Test query spesifik"""
    db = DatabaseManager()
    await db.initialize()

    agent = ChatAgent(db)

    test_queries = [
        "Halo",
        "Apa itu RSI?",
        "Jelaskan MACD",
        "Apa artinya stop-loss?",
        "Kenapa bot beli BTC?",
        "Status portfolio saya",
        "Bagaimana kondisi market?",
        "Trade terakhir",
        "Apa itu long vs short?",
        "Help",
    ]

    print("\n" + "=" * 70)
    print("🧪 TESTING SPECIFIC QUERIES")
    print("=" * 70)

    for query in test_queries:
        print(f"\n{'─' * 70}")
        print(f"👤 Query: {query}")
        print(f"{'─' * 70}")

        response = await agent.process_message(query)
        print(f"\n🤖 Response:\n{response}")


async def main():
    """Main entry point"""
    # Pilih mode: interactive atau test
    mode = "interactive"  # Change to "test" for automated testing

    if mode == "interactive":
        await interactive_demo()
    else:
        await test_specific_queries()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logger.exception(f"💥 Fatal error: {e}")
        sys.exit(1)
