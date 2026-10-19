"""
Main Entry Point - Menjalankan semua collector secara bersamaan

File ini adalah entry point utama yang menjalankan semua data collection:
1. Database initialization
2. Binance Collector (historical candles + real-time tickers)
3. News Scraper (RSS feeds)

Untuk pemula:
- File ini yang pertama kali dijalankan
- Akan menjalankan semua collector secara concurrent (bersamaan)
- Menggunakan asyncio untuk menjalankan multiple tasks sekaligus
- Graceful shutdown saat menerima Ctrl+C

Cara menjalankan:
    python -m data_collector.main_collector
    
    Atau:
    cd backend
    python -m data_collector.main_collector
"""

import asyncio
import signal
import sys
from loguru import logger
from data_collector.config import LOG_LEVEL, LOG_FILE
from data_collector.database import DatabaseManager
from data_collector.binance_ws import BinanceCollector
from data_collector.news_scraper import NewsScraper


# ============================================
# LOGGING SETUP
# ============================================
# Konfigurasi logging untuk console dan file
logger.remove()
logger.add(
    sys.stdout,
    level=LOG_LEVEL,
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | {message}"
)
logger.add(
    LOG_FILE,
    rotation="10 MB",
    level="DEBUG"
)


# ============================================
# MAIN SERVICE
# ============================================

class DataCollectorService:
    """
    Service utama yang mengkoordinasi semua collector.
    
    Class ini menangani:
    - Inisialisasi database
    - Start semua collectors secara paralel
    - Graceful shutdown
    
    Attributes:
        db: DatabaseManager instance
        binance: BinanceCollector instance
        news: NewsScraper instance
    """

    def __init__(self):
        """Initialize semua components."""
        self.db = DatabaseManager()
        self.binance = BinanceCollector(self.db)
        self.news = NewsScraper(self.db)

    async def start(self) -> None:
        """
        Menjalankan semua collector secara paralel.
        
        Alur:
        1. Initialize database
        2. Start Binance collector (historical + real-time)
        3. Start News scraper (periodic)
        4. Wait untuk semua tasks selesai
        
        Note:
            - Semua collectors berjalan concurrent menggunakan asyncio.gather
            - Jika ada error, akan di-log tapi tidak menghentikan service lain
            - Graceful shutdown saat menerima signal (Ctrl+C)
        """
        logger.info("🚀 Starting AI Trading Agent - Data Collector Service")
        logger.info("=" * 60)

        # Inisialisasi database
        await self.db.initialize()

        # Jalankan semua collector secara paralel
        tasks = [
            asyncio.create_task(self.binance.start()),
            asyncio.create_task(self.news.start()),
        ]

        try:
            await asyncio.gather(*tasks)
        except asyncio.CancelledError:
            logger.info("🛑 Service cancelled")
        finally:
            await self.stop()

    async def stop(self) -> None:
        """
        Menghentikan semua collector dengan aman.
        
        Dipanggil saat:
        - Service selesai
        - Menerima signal shutdown (Ctrl+C)
        - Error terjadi
        """
        logger.info("🛑 Shutting down services...")
        await self.binance.stop()
        await self.news.stop()
        logger.info("✅ All services stopped. Goodbye!")


# ============================================
# MAIN FUNCTION
# ============================================

async def main() -> None:
    """
    Main async entry point.
    
    Setup:
    - Create DataCollectorService
    - Setup signal handlers untuk graceful shutdown
    - Run service
    """
    service = DataCollectorService()

    # Handle graceful shutdown (Ctrl+C)
    loop = asyncio.get_running_loop()
    stop_event = asyncio.Event()

    def signal_handler():
        """Handle shutdown signals (SIGINT, SIGTERM)."""
        logger.info("\n⚠️  Received shutdown signal")
        stop_event.set()

    # Register signal handlers
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, signal_handler)

    # Jalankan service
    try:
        await service.start()
    except KeyboardInterrupt:
        logger.info("⚠️  Keyboard interrupt received")
    finally:
        await service.stop()


# ============================================
# ENTRY POINT
# ============================================

if __name__ == "__main__":
    """
    Entry point saat file dijalankan langsung.
    
    Cara menjalankan:
        python main_collector.py
        
    Atau:
        python -m data_collector.main_collector
    """
    try:
        asyncio.run(main())
    except Exception as e:
        logger.exception(f"💥 Fatal error: {e}")
        sys.exit(1)
