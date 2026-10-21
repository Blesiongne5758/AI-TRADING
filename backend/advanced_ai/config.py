"""
Konfigurasi Advanced AI Module
API keys, model paths, dan parameter global
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ============================================
# HUGGINGFACE MODELS
# ============================================
# FinBERT: Model khusus untuk sentimen finansial
# Pilihan model (pilih salah satu):
FINBERT_MODELS = {
    "yiyanghkust/finbert-tone": {
        "description": "FinBERT Tone - 3 kelas (Positive, Negative, Neutral)",
        "labels": ["Positive", "Negative", "Neutral"],
        "recommended": True,
    },
    "ProsusAI/finbert": {
        "description": "ProsusAI FinBERT - 3 kelas",
        "labels": ["positive", "negative", "neutral"],
        "recommended": False,
    },
    "ahmedrachid/FinancialBERT-Sentiment-Analysis": {
        "description": "FinancialBERT - 2 kelas (positive, negative)",
        "labels": ["positive", "negative"],
        "recommended": False,
    },
}

DEFAULT_FINBERT_MODEL = os.getenv("FINBERT_MODEL", "yiyanghkust/finbert-tone")

# Device untuk inference
# "cuda" untuk GPU, "cpu" untuk CPU (lebih lambat)
DEVICE = "cuda" if os.getenv("USE_GPU", "false").lower() == "true" else "cpu"

# Model cache directory
MODEL_CACHE_DIR = Path(os.getenv("MODEL_CACHE_DIR", "./models_cache"))
MODEL_CACHE_DIR.mkdir(exist_ok=True)

# ============================================
# NEWS API KEYS
# ============================================
# CryptoPanic (GRATIS, khusus crypto - PALING DIREKOMENDASIKAN)
# Daftar: https://cryptopanic.com/developers/api/
CRYPTOPANIC_API_KEY = os.getenv("CRYPTOPANIC_API_KEY", "")

# NewsAPI.org (Freemium, 100 requests/hari gratis)
# Daftar: https://newsapi.org/
NEWSAPI_API_KEY = os.getenv("NEWSAPI_API_KEY", "")

# GNews (Gratis, 100 requests/hari)
# Daftar: https://gnews.org/
GNEWS_API_KEY = os.getenv("GNEWS_API_KEY", "")

# ============================================
# TWITTER/X API KEYS
# ============================================
# Twitter API v2 (berbayar, $100/bulan untuk Basic)
# Daftar: https://developer.twitter.com/
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN", "")
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY", "")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET", "")

# Nitter instances (GRATIS, alternative scraping Twitter)
# Daftar instance publik: https://github.com/zedeus/nitter/wiki/Instances
NITTER_INSTANCES = [
    "https://nitter.privacydev.net",
    "https://nitter.poast.org",
    "https://nitter.net",
]

# ============================================
# REDDIT API (GRATIS)
# ============================================
# Daftar: https://www.reddit.com/prefs/apps
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID", "")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET", "")
REDDIT_USER_AGENT = "AI-Trading-Agent/1.0"

# Subreddits yang dipantau
REDDIT_SUBREDDITS = [
    "CryptoCurrency",
    "Bitcoin",
    "ethereum",
    "CryptoMarkets",
    "wallstreetbets",
    "stocks",
]

# ============================================
# TELEGRAM (untuk monitoring channel publik)
# ============================================
TELEGRAM_API_ID = os.getenv("TELEGRAM_API_ID", "")
TELEGRAM_API_HASH = os.getenv("TELEGRAM_API_HASH", "")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")

# Channel publik crypto yang dipantau
TELEGRAM_CHANNELS = [
    "whale_alert",
    "crypto_news",
    "bitcoinnews",
]

# ============================================
# PUMP & DUMP DETECTION PARAMETERS
# ============================================
PUMP_DETECTION = {
    # Volume spike threshold (x rata-rata)
    "volume_spike_threshold": float(os.getenv("PUMP_VOLUME_THRESHOLD", "3.0")),
    # Price spike dalam 1 jam (%)
    "price_spike_1h_threshold": float(os.getenv("PUMP_PRICE_1H_THRESHOLD", "15.0")),
    # Price spike dalam 24 jam (%)
    "price_spike_24h_threshold": float(os.getenv("PUMP_PRICE_24H_THRESHOLD", "30.0")),
    # Social mention spike (x rata-rata)
    "social_spike_threshold": float(os.getenv("PUMP_SOCIAL_THRESHOLD", "5.0")),
    # Minimum social mentions untuk validasi
    "min_social_mentions": int(os.getenv("PUMP_MIN_MENTIONS", "50")),
    # Window untuk deteksi (jam)
    "detection_window_hours": 24,
}

# ============================================
# CACHING
# ============================================
CACHE_TTL = {
    "news": int(os.getenv("CACHE_TTL_NEWS", "300")),  # 5 menit
    "twitter": int(os.getenv("CACHE_TTL_TWITTER", "60")),  # 1 menit
    "sentiment": int(os.getenv("CACHE_TTL_SENTIMENT", "180")),  # 3 menit
    "reddit": int(os.getenv("CACHE_TTL_REDDIT", "300")),  # 5 menit
}

# Backward compatibility
CACHE_TTL_NEWS = CACHE_TTL["news"]
CACHE_TTL_TWEETS = CACHE_TTL["twitter"]
CACHE_TTL_SENTIMENT = CACHE_TTL["sentiment"]

# ============================================
# FEATURE FLAGS
# ============================================
ENABLE_FINBERT = os.getenv("ENABLE_FINBERT", "true").lower() == "true"
ENABLE_TWITTER = os.getenv("ENABLE_TWITTER", "true").lower() == "true"
ENABLE_REDDIT = os.getenv("ENABLE_REDDIT", "false").lower() == "true"
ENABLE_TELEGRAM = os.getenv("ENABLE_TELEGRAM", "false").lower() == "true"
ENABLE_CACHE = os.getenv("ENABLE_CACHE", "true").lower() == "true"

# ============================================
# SENTIMENT THRESHOLDS
# ============================================
SENTIMENT_POSITIVE_THRESHOLD = 0.15
SENTIMENT_NEGATIVE_THRESHOLD = -0.15

# ============================================
# KEY ACCOUNTS TO MONITOR (Crypto Twitter)
# ============================================
INFLUENTIAL_ACCOUNTS = {
    "whales": [
        "whale_alert",
        "lookonchain",
        "EmberCN",
        "ai_9684xtpa",
    ],
    "analysts": [
        "PlanB",
        "CryptoCapo_",
        "pentosh1",
        "CryptoDonAlt",
    ],
    "news": [
        "WuBlockchain",
        "DB_informasi",
        "Tree_of_Alpha",
    ],
}

# ============================================
# BACKWARD COMPATIBILITY CLASS
# ============================================
class AdvancedAIConfig:
    """
    Backward compatibility class untuk code lama
    Semua attributes sekarang available sebagai module-level constants
    """
    
    # Models
    FINBERT_MODELS = FINBERT_MODELS
    DEFAULT_FINBERT_MODEL = DEFAULT_FINBERT_MODEL
    DEVICE = DEVICE
    MODEL_CACHE_DIR = MODEL_CACHE_DIR
    
    # News APIs
    CRYPTOPANIC_API_KEY = CRYPTOPANIC_API_KEY
    NEWSAPI_API_KEY = NEWSAPI_API_KEY
    GNEWS_API_KEY = GNEWS_API_KEY
    
    # Twitter
    TWITTER_BEARER_TOKEN = TWITTER_BEARER_TOKEN
    TWITTER_API_KEY = TWITTER_API_KEY
    TWITTER_API_SECRET = TWITTER_API_SECRET
    NITTER_INSTANCES = NITTER_INSTANCES
    
    # Reddit
    REDDIT_CLIENT_ID = REDDIT_CLIENT_ID
    REDDIT_CLIENT_SECRET = REDDIT_CLIENT_SECRET
    REDDIT_USER_AGENT = REDDIT_USER_AGENT
    REDDIT_SUBREDDITS = REDDIT_SUBREDDITS
    
    # Telegram
    TELEGRAM_API_ID = TELEGRAM_API_ID
    TELEGRAM_API_HASH = TELEGRAM_API_HASH
    TELEGRAM_BOT_TOKEN = TELEGRAM_BOT_TOKEN
    TELEGRAM_CHANNELS = TELEGRAM_CHANNELS
    
    # Pump Detection
    PUMP_DETECTION = PUMP_DETECTION
    
    # Caching
    CACHE_TTL = CACHE_TTL
    CACHE_TTL_NEWS = CACHE_TTL_NEWS
    CACHE_TTL_TWEETS = CACHE_TTL_TWEETS
    CACHE_TTL_SENTIMENT = CACHE_TTL_SENTIMENT
    
    # Feature Flags
    ENABLE_FINBERT = ENABLE_FINBERT
    ENABLE_TWITTER = ENABLE_TWITTER
    ENABLE_REDDIT = ENABLE_REDDIT
    ENABLE_TELEGRAM = ENABLE_TELEGRAM
    ENABLE_CACHE = ENABLE_CACHE
    
    # Sentiment
    SENTIMENT_POSITIVE_THRESHOLD = SENTIMENT_POSITIVE_THRESHOLD
    SENTIMENT_NEGATIVE_THRESHOLD = SENTIMENT_NEGATIVE_THRESHOLD
    
    # Accounts
    INFLUENTIAL_ACCOUNTS = INFLUENTIAL_ACCOUNTS
    
    # Rate Limits
    CRYPTOPANIC_RATE_LIMIT = 30
    NEWSAPI_RATE_LIMIT = 3
    TWITTER_RATE_LIMIT = 300
    
    @classmethod
    def validate(cls):
        """Validate configuration"""
        warnings = []
        
        if not cls.CRYPTOPANIC_API_KEY:
            warnings.append("⚠️  CRYPTOPANIC_API_KEY not set")
        
        if not cls.NEWSAPI_API_KEY:
            warnings.append("⚠️  NEWSAPI_API_KEY not set")
        
        if not cls.TWITTER_BEARER_TOKEN and cls.ENABLE_TWITTER:
            warnings.append("⚠️  TWITTER_BEARER_TOKEN not set (Twitter disabled)")
            cls.ENABLE_TWITTER = False
        
        for warning in warnings:
            print(warning)
        
        return len(warnings) == 0
    
    @classmethod
    def print_config(cls):
        """Print configuration (for debugging)"""
        print("\n" + "=" * 70)
        print("🧠 ADVANCED AI CONFIGURATION")
        print("=" * 70)
        
        print("\n📰 News APIs:")
        print(f"   CryptoPanic: {'✅' if cls.CRYPTOPANIC_API_KEY else '❌'}")
        print(f"   NewsAPI: {'✅' if cls.NEWSAPI_API_KEY else '❌'}")
        
        print("\n📱 Social Media:")
        print(f"   Twitter: {'✅' if cls.ENABLE_TWITTER else '❌'}")
        print(f"   Reddit: {'✅' if cls.ENABLE_REDDIT else '❌'}")
        print(f"   Telegram: {'✅' if cls.ENABLE_TELEGRAM else '❌'}")
        
        print("\n🧠 Models:")
        print(f"   FinBERT: {'✅' if cls.ENABLE_FINBERT else '❌'}")
        print(f"   Model: {cls.DEFAULT_FINBERT_MODEL}")
        print(f"   Device: {cls.DEVICE}")
        
        print("\n💾 Cache:")
        print(f"   Enabled: {'✅' if cls.ENABLE_CACHE else '❌'}")
        
        print("\n" + "=" * 70 + "\n")
