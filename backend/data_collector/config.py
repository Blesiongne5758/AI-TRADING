"""
Konfigurasi Global untuk AI Trading Agent - Fase 1

File ini berisi SEMUA konfigurasi yang dibutuhkan oleh sistem.
Menggunakan python-dotenv untuk load environment variables.

Untuk pemula:
- os.getenv() mengambil nilai dari environment variables atau file .env
- Path dari pathlib untuk manipulasi path yang cross-platform
- Konfigurasi dibagi per section untuk memudahkan pembacaan

Cara penggunaan:
    from data_collector.config import (
        BINANCE_API_KEY, TRADING_SYMBOLS, DATABASE_PATH
    )
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables dari file .env
load_dotenv()

# ============================================
# PATH & DIRECTORI
# ============================================
# BASE_DIR = root folder proyek (ai-trading-agent/)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# DATA_DIR = folder untuk database dan logs
DATA_DIR = BASE_DIR / "database"
DATA_DIR.mkdir(exist_ok=True)  # Buat folder jika belum ada

# LOG_DIR = folder untuk log files
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

# Path ke database SQLite
DATABASE_PATH = DATA_DIR / "trading_data.db"

# ============================================
# BINANCE CONFIGURATION
# ============================================
# Gunakan testnet untuk testing (aman, tidak pakai uang asli)
# Daftar di: https://testnet.binance.vision/
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY", "")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET", "")
USE_TESTNET = True  # Set False untuk production

# Daftar simbol yang akan dipantau (MVP: 5 simbol utama)
TRADING_SYMBOLS = [
    "BTC/USDT",
    "ETH/USDT",
    "SOL/USDT",
    "BNB/USDT",
    "XRP/USDT",
]

# Timeframe untuk data historis (candlestick)
TIMEFRAMES = ["1m", "5m", "15m", "1h", "4h", "1d"]

# Jumlah candle historis yang diambil saat startup
HISTORICAL_CANDLE_LIMIT = 500

# ============================================
# NEWS RSS FEEDS
# ============================================
# Daftar sumber berita crypto (RSS feeds)
NEWS_FEEDS = [
    {
        "name": "CoinDesk",
        "url": "https://www.coindesk.com/arc/outboundfeeds/rss/",
        "category": "crypto",
    },
    {
        "name": "CoinTelegraph",
        "url": "https://cointelegraph.com/rss",
        "category": "crypto",
    },
    {
        "name": "Decrypt",
        "url": "https://decrypt.co/feed",
        "category": "crypto",
    },
]

# Interval pengambilan berita (dalam detik)
NEWS_FETCH_INTERVAL = 900  # 15 menit

# ============================================
# TRADING SETTINGS (untuk Fase 2)
# ============================================
PAPER_TRADING = True  # True = simulasi, False = real trading
INITIAL_BALANCE = 10000.0  # Saldo awal virtual (USDT)

# Risk management
MAX_RISK_PER_TRADE = 0.02  # 2% dari portfolio per trade
MAX_OPEN_POSITIONS = 5
STOP_LOSS_PERCENT = 0.02  # 2% stop loss
TAKE_PROFIT_PERCENT = 0.05  # 5% take profit

# Signal threshold
MIN_CONFIDENCE_THRESHOLD = 0.60  # Minimum 60% confidence untuk trade

# ============================================
# ANALYSIS SETTINGS (untuk Fase 2)
# ============================================
# Technical indicators
RSI_PERIOD = 14
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9
EMA_PERIODS = [20, 50, 200]
BOLLINGER_PERIOD = 20
BOLLINGER_STD = 2

# Sentiment analysis
SENTIMENT_MODEL = "ProsusAI/finbert"  # Model FinBERT

# ============================================
# TELEGRAM BOT (untuk Fase 2)
# ============================================
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# ============================================
# LOGGING
# ============================================
LOG_LEVEL = "INFO"
LOG_FILE = LOG_DIR / "collector.log"  # Single log file untuk semua collector

# ============================================
# HELPER FUNCTIONS
# ============================================

def print_config() -> None:
    """
    Print semua konfigurasi (untuk debugging).
    
    Note: API keys dan secrets akan di-mask untuk keamanan.
    """
    print("\n" + "=" * 60)
    print("AI Trading Agent - Configuration")
    print("=" * 60)
    print(f"Base Directory: {BASE_DIR}")
    print(f"Database Path: {DATABASE_PATH}")
    print(f"\nBinance Testnet: {USE_TESTNET}")
    print(f"Binance API Key: {'*' * 10 if BINANCE_API_KEY else 'Not set'}")
    print(f"Trading Symbols: {', '.join(TRADING_SYMBOLS)}")
    print(f"Timeframes: {', '.join(TIMEFRAMES)}")
    print(f"Historical Candle Limit: {HISTORICAL_CANDLE_LIMIT}")
    print(f"\nPaper Trading: {PAPER_TRADING}")
    print(f"Initial Balance: ${INITIAL_BALANCE:,.2f}")
    print(f"Max Risk per Trade: {MAX_RISK_PER_TRADE:.1%}")
    print(f"Max Open Positions: {MAX_OPEN_POSITIONS}")
    print(f"Stop Loss: {STOP_LOSS_PERCENT:.1%}")
    print(f"Take Profit: {TAKE_PROFIT_PERCENT:.1%}")
    print(f"\nNews Sources: {len(NEWS_FEEDS)} feeds")
    for feed in NEWS_FEEDS:
        print(f"  - {feed['name']}: {feed['url']}")
    print(f"News Fetch Interval: {NEWS_FETCH_INTERVAL} seconds")
    print(f"\nLog Level: {LOG_LEVEL}")
    print(f"Log File: {LOG_FILE}")
    print("=" * 60 + "\n")


def validate_config() -> None:
    """
    Validasi konfigurasi penting.
    Dipanggil saat aplikasi dimulai.
    
    Raises:
        ValueError: Jika konfigurasi tidak valid
    """
    if not BINANCE_API_KEY and not USE_TESTNET:
        raise ValueError(
            "BINANCE_API_KEY required for mainnet trading. "
            "Set USE_TESTNET=True for testnet."
        )
    
    if TELEGRAM_BOT_TOKEN and not TELEGRAM_CHAT_ID:
        raise ValueError(
            "TELEGRAM_CHAT_ID required when TELEGRAM_BOT_TOKEN is set"
        )
    
    if MAX_RISK_PER_TRADE > 0.05:
        raise ValueError(
            "MAX_RISK_PER_TRADE too high (>5%). "
            "This is dangerous for beginners."
        )
    
    print("✅ Configuration validated successfully")


if __name__ == "__main__":
    # Test konfigurasi
    validate_config()
    print_config()
