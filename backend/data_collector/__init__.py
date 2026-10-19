"""
Data Collector Module

Modul ini bertanggung jawab untuk mengumpulkan data dari berbagai sumber:
- Binance WebSocket (OHLCV data)
- News RSS feeds (crypto news)

Sub-modules:
- binance_ws: Real-time market data collection
- news_scraper: News fetching and sentiment analysis
"""

from .binance_ws import BinanceDataCollector
from .news_scraper import NewsScraper, SentimentAnalyzer

__all__ = ['BinanceDataCollector', 'NewsScraper', 'SentimentAnalyzer']
