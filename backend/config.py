"""
Konfigurasi Aplikasi AI Trading Agent

File ini berisi semua konfigurasi yang dibutuhkan oleh sistem.
Menggunakan pydantic-settings untuk validasi dan type safety.

Untuk pemula:
- Type hints (str, int, float, dll) membantu IDE memberikan autocomplete
- Pydantic memvalidasi konfigurasi saat aplikasi dimulai
- .env file digunakan untuk menyimpan secret (API keys, dll)
"""

from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import Field
import os


class Settings(BaseSettings):
    """
    Konfigurasi utama aplikasi.
    
    Semua nilai default bisa di-override via environment variables atau file .env
    """
    
    # ============================================
    # APPLICATION SETTINGS
    # ============================================
    APP_NAME: str = "AI Trading Agent"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    
    # ============================================
    # BINANCE API SETTINGS
    # ============================================
    # Untuk testing, gunakan testnet: https://testnet.binance.vision/
    BINANCE_API_KEY: str = ""
    BINANCE_API_SECRET: str = ""
    BINANCE_TESTNET: bool = True  # True = testnet, False = mainnet
    
    # Symbol yang akan di-trade
    TRADING_SYMBOLS: List[str] = Field(
        default=["BTC/USDT", "ETH/USDT", "SOL/USDT", "BNB/USDT", "XRP/USDT"]
    )
    
    # Timeframe untuk analisis
    TIMEFRAMES: List[str] = Field(
        default=["1m", "5m", "15m", "1h", "4h", "1d"]
    )
    
    # ============================================
    # DATABASE SETTINGS
    # ============================================
    DATABASE_URL: str = "sqlite+aiosqlite:///./database/trading_data.db"
    
    # ============================================
    # TELEGRAM BOT SETTINGS
    # ============================================
    TELEGRAM_BOT_TOKEN: str = ""
    TELEGRAM_CHAT_ID: str = ""  # Chat ID untuk menerima notifikasi
    
    # ============================================
    # TRADING SETTINGS
    # ============================================
    # Paper trading
    PAPER_TRADING: bool = True  # True = simulasi, False = real trading
    INITIAL_BALANCE: float = 10000.0  # Saldo awal virtual (USDT)
    
    # Risk management
    MAX_RISK_PER_TRADE: float = 0.02  # 2% dari portfolio per trade
    MAX_OPEN_POSITIONS: int = 5
    STOP_LOSS_PERCENT: float = 0.02  # 2% stop loss
    TAKE_PROFIT_PERCENT: float = 0.05  # 5% take profit
    
    # Signal threshold
    MIN_CONFIDENCE_THRESHOLD: float = 0.60  # Minimum 60% confidence untuk trade
    
    # ============================================
    # ANALYSIS SETTINGS
    # ============================================
    # Technical indicators
    RSI_PERIOD: int = 14
    MACD_FAST: int = 12
    MACD_SLOW: int = 26
    MACD_SIGNAL: int = 9
    EMA_PERIODS: List[int] = Field(default=[20, 50, 200])
    BOLLINGER_PERIOD: int = 20
    BOLLINGER_STD: int = 2
    
    # Sentiment analysis
    SENTIMENT_MODEL: str = "ProsusAI/finbert"  # Model FinBERT untuk financial sentiment
    NEWS_SOURCES: List[str] = Field(
        default=[
            "https://cointelegraph.com/rss",
            "https://www.coindesk.com/arc/outboundfeeds/rss/",
            "https://cryptonews.com/news/feed/",
        ]
    )
    NEWS_FETCH_INTERVAL: int = 900  # 15 menit dalam detik
    
    # ============================================
    # API SETTINGS
    # ============================================
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()

# Validasi konfigurasi saat import
def validate_settings() -> None:
    """
    Validasi konfigurasi penting.
    Dipanggil saat aplikasi dimulai.
    """
    if not settings.BINANCE_API_KEY and not settings.BINANCE_TESTNET:
        raise ValueError(
            "BINANCE_API_KEY required for mainnet trading. "
            "Set BINANCE_TESTNET=true for testnet."
        )
    
    if settings.TELEGRAM_BOT_TOKEN and not settings.TELEGRAM_CHAT_ID:
        raise ValueError(
            "TELEGRAM_CHAT_ID required when TELEGRAM_BOT_TOKEN is set"
        )
    
    if settings.MAX_RISK_PER_TRADE > 0.05:
        raise ValueError(
            "MAX_RISK_PER_TRADE too high (>5%). "
            "This is dangerous for beginners."
        )


# Panggil validasi saat module di-import
validate_settings()
