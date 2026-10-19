"""
Data Collector Module - AI Trading Agent

Modul ini bertanggung jawab untuk mengumpulkan data dari berbagai sumber:
- Binance WebSocket (OHLCV data real-time)
- News RSS feeds (crypto news + sentiment analysis)

Struktur Module:
- config.py: Konfigurasi global (API keys, settings)
- database.py: Database models & operations (SQLite)
- binance_ws.py: Binance WebSocket connection
- news_scraper.py: News scraping + FinBERT sentiment
- main_collector.py: Entry point (menjalankan semua collector)

Cara penggunaan:
    # Jalankan semua collectors
    python -m data_collector.main_collector
    
    # Atau import individual components
    from data_collector import BinanceDataCollector, NewsScraper
    from data_collector.config import TRADING_SYMBOLS, DATABASE_PATH
    from data_collector.database import init_db, save_ohlcv_data
"""

from data_collector.binance_ws import BinanceDataCollector
from data_collector.news_scraper import NewsScraper, SentimentAnalyzer
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
from data_collector.database import (
    init_db, close_db,
    save_ohlcv_data, get_ohlcv_data,
    save_news_data, get_recent_news
)

__version__ = "1.0.0"
__all__ = [
    'BinanceDataCollector',
    'NewsScraper',
    'SentimentAnalyzer',
    'TRADING_SYMBOLS',
    'TIMEFRAMES',
    'DATABASE_PATH',
    'BINANCE_API_KEY',
    'USE_TESTNET',
    'NEWS_FEEDS',
    'print_config',
    'validate_config',
    'init_db',
    'close_db',
    'save_ohlcv_data',
    'get_ohlcv_data',
    'save_news_data',
    'get_recent_news'
]
