"""
Konfigurasi Global - AI Trading Agent

File ini berisi SEMUA konfigurasi yang dibutuhkan oleh sistem.
Menggunakan pydantic-settings untuk validasi dan type safety.

Untuk pemula:
- Type hints (str, int, float, dll) membantu IDE memberikan autocomplete
- Pydantic memvalidasi konfigurasi saat aplikasi dimulai
- .env file digunakan untuk menyimpan secret (API keys, dll)
- Semua nilai default bisa di-override via environment variables

Cara penggunaan:
    from data_collector.config import settings
    
    print(settings.BINANCE_API_KEY)
    print(settings.TRADING_SYMBOLS)
"""

from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field
from loguru import logger


class Settings(BaseSettings):
    """
    Konfigurasi utama aplikasi.
    
    Semua nilai default bisa di-override via environment variables atau file .env
    
    Attributes:
        APP_NAME: Nama aplikasi
        DEBUG: Mode debug (True/False)
        LOG_LEVEL: Level logging (DEBUG, INFO, WARNING, ERROR)
        BINANCE_API_KEY: API key dari Binance
        BINANCE_API_SECRET: API secret dari Binance
        BINANCE_TESTNET: Gunakan testnet (True) atau mainnet (False)
        TRADING_SYMBOLS: List simbol yang akan di-trade
        TIMEFRAMES: List timeframe untuk analisis
        DATABASE_PATH: Path ke file database SQLite
        TELEGRAM_BOT_TOKEN: Token bot Telegram
        TELEGRAM_CHAT_ID: Chat ID untuk notifikasi
        PAPER_TRADING: Mode paper trading (True) atau real trading (False)
        INITIAL_BALANCE: Saldo awal virtual (USDT)
        MAX_RISK_PER_TRADE: Maksimum risiko per trade (0.02 = 2%)
        MAX_OPEN_POSITIONS: Maksimum posisi terbuka
        STOP_LOSS_PERCENT: Persentase stop loss (0.02 = 2%)
        TAKE_PROFIT_PERCENT: Persentase take profit (0.05 = 5%)
        MIN_CONFIDENCE_THRESHOLD: Minimum confidence untuk trade (0.60 = 60%)
        NEWS_SOURCES: List URL RSS feed berita
        NEWS_FETCH_INTERVAL: Interval fetch berita (detik)
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
    DATABASE_PATH: str = "./database/trading_data.db"
    
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
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()


def validate_settings() -> None:
    """
    Validasi konfigurasi penting.
    Dipanggil saat aplikasi dimulai.
    
    Raises:
        ValueError: Jika konfigurasi tidak valid
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
    
    logger.info("Configuration validated successfully")


# Panggil validasi saat module di-import
validate_settings()


# Helper function untuk print config (debugging)
def print_config() -> None:
    """
    Print semua konfigurasi (untuk debugging).
    
    Note: API keys dan secrets akan di-mask untuk keamanan.
    """
    print("\n" + "=" * 60)
    print("AI Trading Agent - Configuration")
    print("=" * 60)
    print(f"App Name: {settings.APP_NAME}")
    print(f"Version: {settings.APP_VERSION}")
    print(f"Debug: {settings.DEBUG}")
    print(f"Log Level: {settings.LOG_LEVEL}")
    print(f"\nBinance Testnet: {settings.BINANCE_TESTNET}")
    print(f"Binance API Key: {'*' * 10 if settings.BINANCE_API_KEY else 'Not set'}")
    print(f"Trading Symbols: {', '.join(settings.TRADING_SYMBOLS)}")
    print(f"Timeframes: {', '.join(settings.TIMEFRAMES)}")
    print(f"\nPaper Trading: {settings.PAPER_TRADING}")
    print(f"Initial Balance: ${settings.INITIAL_BALANCE:,.2f}")
    print(f"Max Risk per Trade: {settings.MAX_RISK_PER_TRADE:.1%}")
    print(f"Max Open Positions: {settings.MAX_OPEN_POSITIONS}")
    print(f"Stop Loss: {settings.STOP_LOSS_PERCENT:.1%}")
    print(f"Take Profit: {settings.TAKE_PROFIT_PERCENT:.1%}")
    print(f"\nNews Sources: {len(settings.NEWS_SOURCES)} sources")
    print(f"News Fetch Interval: {settings.NEWS_FETCH_INTERVAL} seconds")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    # Test konfigurasi
    print_config()
