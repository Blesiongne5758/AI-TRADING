"""
Main Collector - Entry Point untuk Data Collection

File ini adalah entry point utama yang menjalankan semua data collection:
1. Binance WebSocket (real-time market data)
2. News Scraper (RSS feeds + sentiment analysis)

Untuk pemula:
- File ini yang pertama kali dijalankan
- Akan menjalankan semua collector secara concurrent (bersamaan)
- Menggunakan asyncio untuk menjalankan multiple tasks sekaligus

Cara menjalankan:
    python -m data_collector.main_collector
    
    Atau:
    cd backend
    python -m data_collector.main_collector
"""

import asyncio
import signal
import sys
from typing import List
from loguru import logger

from data_collector.config import (
    TRADING_SYMBOLS,
    TIMEFRAMES,
    HISTORICAL_CANDLE_LIMIT,
    print_config,
    validate_config,
)
from data_collector.database import DatabaseManager
from data_collector.binance_ws import BinanceDataCollector
from data_collector.news_scraper import NewsScraper


# ============================================
# GLOBAL STATE
# ============================================

class CollectorManager:
    """
    Manager untuk semua data collectors.
    
    Mengkoordinasi:
    - Binance WebSocket collector
    - News scraper
    - Graceful shutdown
    """
    
    def __init__(self):
        """Initialize collector manager."""
        self.db = DatabaseManager()
        self.binance_collector: BinanceDataCollector = None
        self.news_scraper: NewsScraper = None
        self.running = False
        self.tasks: List[asyncio.Task] = []
        
        logger.info("CollectorManager initialized")
    
    async def initialize(self) -> None:
        """
        Initialize semua collectors.
        
        Dipanggil sebelum start().
        """
        logger.info("Initializing collectors...")
        
        try:
            # Initialize database
            logger.info("Initializing database...")
            await self.db.initialize()
            
            # Initialize Binance collector
            logger.info("Initializing Binance data collector...")
            self.binance_collector = BinanceDataCollector(db=self.db)
            await self.binance_collector.initialize()
            
            # Initialize news scraper
            logger.info("Initializing news scraper...")
            self.news_scraper = NewsScraper(db=self.db)
            await self.news_scraper.initialize()
            
            logger.info("All collectors initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize collectors: {e}")
            raise
    
    async def fetch_initial_data(self) -> None:
        """
        Fetch initial historical data.
        
        Ini dijalankan sekali saat startup untuk mengisi database
        dengan data historis sebelum memulai real-time collection.
        """
        logger.info("Fetching initial historical data...")
        
        try:
            for symbol in TRADING_SYMBOLS:
                for timeframe in TIMEFRAMES:
                    try:
                        # Fetch historical data
                        data = await self.binance_collector.fetch_historical_ohlcv(
                            symbol=symbol,
                            timeframe=timeframe,
                            limit=HISTORICAL_CANDLE_LIMIT
                        )
                        
                        # Save to database
                        await self.db.save_candles(symbol, timeframe, data)
                        
                        logger.info(f"Fetched {len(data)} candles for {symbol} {timeframe}")
                        
                        # Small delay to avoid rate limiting
                        await asyncio.sleep(1)
                        
                    except Exception as e:
                        logger.error(f"Failed to fetch {symbol} {timeframe}: {e}")
                        continue
            
            logger.info("Initial data fetch complete")
            
        except Exception as e:
            logger.error(f"Error in initial data fetch: {e}")
    
    async def start(self) -> None:
        """
        Start semua collectors.
        
        Ini akan:
        1. Fetch initial historical data
        2. Start Binance WebSocket (real-time)
        3. Start news scraper (periodic)
        """
        self.running = True
        logger.info("Starting all collectors...")
        
        try:
            # Fetch initial data first
            await self.fetch_initial_data()
            
            # Create tasks for each collector
            # Task 1: Binance WebSocket
            task1 = asyncio.create_task(
                self.binance_collector.start()
            )
            self.tasks.append(task1)
            logger.info("Started Binance WebSocket collector")
            
            # Task 2: News scraper
            task2 = asyncio.create_task(
                self.news_scraper.start()
            )
            self.tasks.append(task2)
            logger.info("Started news scraper")
            
            # Wait for all tasks
            logger.info("All collectors running. Press Ctrl+C to stop.")
            await asyncio.gather(*self.tasks, return_exceptions=True)
            
        except Exception as e:
            logger.error(f"Error in collector manager: {e}")
        finally:
            self.running = False
    
    async def stop(self) -> None:
        """
        Stop semua collectors gracefully.
        
        Dipanggil saat menerima signal shutdown (Ctrl+C).
        """
        logger.info("Stopping all collectors...")
        self.running = False
        
        # Cancel all tasks
        for task in self.tasks:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
        
        # Stop collectors
        if self.binance_collector:
            await self.binance_collector.stop()
        
        if self.news_scraper:
            await self.news_scraper.stop()
        
        # Close database
        await close_db()
        
        logger.info("All collectors stopped")
    
    def get_status(self) -> dict:
        """
        Get status semua collectors.
        
        Returns:
            Dictionary dengan status semua collectors
        """
        status = {
            "running": self.running,
            "binance_collector": None,
            "news_scraper": None
        }
        
        if self.binance_collector:
            status["binance_collector"] = self.binance_collector.get_stats()
        
        if self.news_scraper:
            status["news_scraper"] = self.news_scraper.get_stats()
        
        return status


# ============================================
# SIGNAL HANDLERS
# ============================================

def setup_signal_handlers(manager: CollectorManager) -> None:
    """
    Setup signal handlers untuk graceful shutdown.
    
    Args:
        manager: CollectorManager instance
    """
    def signal_handler(signum, frame):
        """Handle shutdown signals (Ctrl+C)."""
        logger.info(f"Received signal {signum}, shutting down...")
        
        # Create shutdown task
        asyncio.create_task(manager.stop())
    
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)  # Ctrl+C
    signal.signal(signal.SIGTERM, signal_handler)  # Terminate
    
    logger.info("Signal handlers registered")


# ============================================
# MAIN FUNCTION
# ============================================

async def main() -> None:
    """
    Main function - entry point aplikasi.
    
    Alur kerja:
    1. Print konfigurasi
    2. Initialize collector manager
    3. Setup signal handlers
    4. Start all collectors
    5. Wait for shutdown signal
    6. Cleanup and exit
    """
    try:
        # Print configuration
        print_config()
        
        # Create manager
        manager = CollectorManager()
        
        # Setup signal handlers
        setup_signal_handlers(manager)
        
        # Initialize
        await manager.initialize()
        
        # Start collectors
        await manager.start()
        
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt")
    except Exception as e:
        logger.error(f"Error in main: {e}")
        raise
    finally:
        # Cleanup
        if 'manager' in locals():
            await manager.stop()
        
        logger.info("Application shutdown complete")


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
    # Setup logging
    logger.add(
        "logs/main_collector.log",
        rotation="10 MB",
        retention="7 days",
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}"
    )
    
    logger.info("=" * 60)
    logger.info("AI Trading Agent - Data Collector")
    logger.info("=" * 60)
    
    # Run main function
    try:
        asyncio.run(main())
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)
