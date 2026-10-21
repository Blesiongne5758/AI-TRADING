"""
Advanced AI Configuration
Centralized configuration for API keys, models, and settings
"""
import os
from pathlib import Path
from dotenv import load_dotenv
from loguru import logger

# Load environment variables
load_dotenv()


class AdvancedAIConfig:
    """Configuration for Advanced AI module"""
    
    # ============================================
    # API Keys
    # ============================================
    
    # News APIs
    CRYPTOPANIC_API_KEY = os.getenv("CRYPTOPANIC_API_KEY", "")
    NEWSAPI_API_KEY = os.getenv("NEWSAPI_API_KEY", "")
    
    # Social Media APIs
    TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN", "")
    REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID", "")
    REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET", "")
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
    
    # ============================================
    # Model Configuration
    # ============================================
    
    # FinBERT Model
    FINBERT_MODEL_NAME = os.getenv("FINBERT_MODEL_NAME", "yiyanghkust/finbert-tone")
    FINBERT_DEVICE = 0 if os.getenv("USE_GPU", "false").lower() == "true" else -1
    FINBERT_BATCH_SIZE = int(os.getenv("FINBERT_BATCH_SIZE", "32"))
    
    # ============================================
    # Cache Configuration
    # ============================================
    
    CACHE_ENABLED = os.getenv("CACHE_ENABLED", "true").lower() == "true"
    CACHE_DIR = Path(os.getenv("CACHE_DIR", "./cache"))
    CACHE_TTL_NEWS = int(os.getenv("CACHE_TTL_NEWS", "300"))  # 5 minutes
    CACHE_TTL_TWEETS = int(os.getenv("CACHE_TTL_TWEETS", "60"))  # 1 minute
    CACHE_TTL_SENTIMENT = int(os.getenv("CACHE_TTL_SENTIMENT", "900"))  # 15 minutes
    
    # ============================================
    # Rate Limits
    # ============================================
    
    # API Rate Limits (requests per minute)
    CRYPTOPANIC_RATE_LIMIT = int(os.getenv("CRYPTOPANIC_RATE_LIMIT", "30"))
    NEWSAPI_RATE_LIMIT = int(os.getenv("NEWSAPI_RATE_LIMIT", "3"))  # Free tier: 100/day
    TWITTER_RATE_LIMIT = int(os.getenv("TWITTER_RATE_LIMIT", "300"))  # 300/15min
    
    # ============================================
    # Detection Thresholds
    # ============================================
    
    # Pump & Dump Detection
    PUMP_VOLUME_THRESHOLD = float(os.getenv("PUMP_VOLUME_THRESHOLD", "3.0"))
    PUMP_PRICE_THRESHOLD = float(os.getenv("PUMP_PRICE_THRESHOLD", "10.0"))
    PUMP_HYPE_THRESHOLD = float(os.getenv("PUMP_HYPE_THRESHOLD", "70.0"))
    
    # Sentiment Thresholds
    SENTIMENT_POSITIVE_THRESHOLD = float(os.getenv("SENTIMENT_POSITIVE_THRESHOLD", "0.15"))
    SENTIMENT_NEGATIVE_THRESHOLD = float(os.getenv("SENTIMENT_NEGATIVE_THRESHOLD", "-0.15"))
    
    # ============================================
    # Feature Flags
    # ============================================
    
    ENABLE_FINBERT = os.getenv("ENABLE_FINBERT", "true").lower() == "true"
    ENABLE_TWITTER = os.getenv("ENABLE_TWITTER", "true").lower() == "true"
    ENABLE_REDDIT = os.getenv("ENABLE_REDDIT", "false").lower() == "true"
    ENABLE_TELEGRAM = os.getenv("ENABLE_TELEGRAM", "false").lower() == "true"
    ENABLE_CACHE = os.getenv("ENABLE_CACHE", "true").lower() == "true"
    
    # ============================================
    # Logging
    # ============================================
    
    LOG_LEVEL = os.getenv("ADVANCED_AI_LOG_LEVEL", "INFO")
    
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
        
        if not cls.FINBERT_MODEL_NAME and cls.ENABLE_FINBERT:
            warnings.append("⚠️  FINBERT_MODEL_NAME not set (FinBERT disabled)")
            cls.ENABLE_FINBERT = False
        
        for warning in warnings:
            logger.warning(warning)
        
        if not warnings:
            logger.info("✅ Advanced AI configuration validated")
        
        return len(warnings) == 0
    
    @classmethod
    def print_config(cls):
        """Print configuration (for debugging)"""
        logger.info("\n" + "=" * 70)
        logger.info("🧠 ADVANCED AI CONFIGURATION")
        logger.info("=" * 70)
        
        logger.info("\n📰 News APIs:")
        logger.info(f"   CryptoPanic: {'✅' if cls.CRYPTOPANIC_API_KEY else '❌'}")
        logger.info(f"   NewsAPI: {'✅' if cls.NEWSAPI_API_KEY else '❌'}")
        
        logger.info("\n📱 Social Media:")
        logger.info(f"   Twitter: {'✅' if cls.ENABLE_TWITTER else '❌'}")
        logger.info(f"   Reddit: {'✅' if cls.ENABLE_REDDIT else '❌'}")
        logger.info(f"   Telegram: {'✅' if cls.ENABLE_TELEGRAM else '❌'}")
        
        logger.info("\n🧠 Models:")
        logger.info(f"   FinBERT: {'✅' if cls.ENABLE_FINBERT else '❌'}")
        logger.info(f"   Model: {cls.FINBERT_MODEL_NAME}")
        logger.info(f"   Device: {'GPU' if cls.FINBERT_DEVICE == 0 else 'CPU'}")
        
        logger.info("\n💾 Cache:")
        logger.info(f"   Enabled: {'✅' if cls.ENABLE_CACHE else '❌'}")
        logger.info(f"   Directory: {cls.CACHE_DIR}")
        
        logger.info("\n" + "=" * 70 + "\n")


# Validate configuration on import
AdvancedAIConfig.validate()
