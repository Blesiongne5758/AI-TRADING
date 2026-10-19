"""
Data Collector Module - AI Trading Agent

Modul ini bertanggung jawab untuk mengumpulkan data dari berbagai sumber:
- Binance REST API (OHLCV data historis + ticker real-time)
- News RSS feeds (crypto news + sentiment analysis)

Struktur Module:
- config.py: Konfigurasi global (API keys, settings)
- database.py: DatabaseManager untuk SQLite operations
- binance_ws.py: Binance REST API collector
- news_scraper.py: News scraping + FinBERT sentiment
- main_collector.py: Entry point (menjalankan semua collector)

Cara penggunaan:
    # Jalankan semua collectors
    python -m data_collector.main_collector
    
    # Atau import individual components
    from data_collector import BinanceCollector, NewsScraper, DatabaseManager
    from data_collector.config import TRADING_SYMBOLS, DATABASE_PATH
"""

from data_collector.binance_ws import BinanceCollector
from data_collector.news_scraper import NewsScraper
from data_collector.config import (
    TRADING_SYMBOLS,
    TIMEFRAMES,
    DATABASE_PATH,
    BINANCE_API_KEY,
    USE_TESTNET,
    NEWS_FEEDS,
    print_config,
    validate_config,
)
from data_collector.database import DatabaseManager

__version__ = "1.0.0"
__all__ = [
    'BinanceCollector',
    'NewsScraper',
    'DatabaseManager',
    'TRADING_SYMBOLS',
    'TIMEFRAMES',
    'DATABASE_PATH',
    'BINANCE_API_KEY',
    'USE_TESTNET',
    'NEWS_FEEDS',
    'print_config',
    'validate_config',
]
