# 🔧 Konfigurasi Modul G: Advanced AI

Panduan lengkap untuk mengkonfigurasi Modul G dengan API keys dan parameters.

## 📋 Overview

Modul G menggunakan banyak API external untuk data collection dan analysis. File ini menjelaskan:
- Cara mendapatkan API keys
- Konfigurasi models dan parameters
- Feature flags dan settings
- Best practices

## 🎯 Quick Start

### 1. Copy Template

```bash
cd backend
cp .env.example .env
```

### 2. Edit .env File

```bash
nano .env  # atau text editor lainnya
```

### 3. Isi API Keys

Minimal yang diperlukan untuk basic functionality:
```env
BINANCE_API_KEY=your_key
BINANCE_API_SECRET=your_secret
CRYPTOPANIC_API_KEY=your_key  # Paling penting untuk news
```

### 4. Test Configuration

```bash
python -c "from advanced_ai.config import *; print('✅ Config loaded')"
```

---

## 🔑 API Keys Guide

### **1. Binance API (Required - Phase 1)**

**Purpose:** Data collection (OHLCV, ticker, news)

**How to Get:**
1. Go to https://testnet.binance.vision/
2. Login dengan GitHub account
3. Generate API Key
4. Copy API Key dan Secret Key

**Add to .env:**
```env
BINANCE_API_KEY=your_testnet_api_key
BINANCE_API_SECRET=your_testnet_secret
```

**Cost:** FREE (testnet)  
**Rate Limit:** 1200 requests/minute

---

### **2. CryptoPanic API (Highly Recommended - Phase G)**

**Purpose:** Crypto-specific news aggregation

**Why Recommended:**
- ✅ GRATIS
- ✅ Khusus crypto (lebih relevan)
- ✅ Real-time updates
- ✅ Sentiment labels included
- ✅ High quality sources

**How to Get:**
1. Go to https://cryptopanic.com/
2. Sign up for free account
3. Go to https://cryptopanic.com/developers/api/
4. Copy API key

**Add to .env:**
```env
CRYPTOPANIC_API_KEY=your_cryptopanic_key
```

**Cost:** FREE  
**Rate Limit:** 30 requests/minute

---

### **3. NewsAPI.org (Optional - Phase G)**

**Purpose:** General news (not crypto-specific)

**Pros:**
- ✅ Easy to use
- ✅ Many sources
- ✅ Good for general market sentiment

**Cons:**
- ❌ Not crypto-specific
- ❌ Limited free tier (100 requests/day)
- ❌ Less relevant for crypto trading

**How to Get:**
1. Go to https://newsapi.org/
2. Sign up for free account
3. Copy API key

**Add to .env:**
```env
NEWSAPI_API_KEY=your_newsapi_key
```

**Cost:** FREE (100 requests/day)  
**Rate Limit:** 100 requests/day

---

### **4. Twitter/X API (Optional - Phase G)**

**Purpose:** Social media sentiment analysis

**Pros:**
- ✅ Real-time social sentiment
- ✅ Influencer tracking
- ✅ Hype detection

**Cons:**
- ❌ Expensive ($100/month for Basic)
- ❌ Complex setup
- ❌ Strict rate limits

**Alternative:** Gunakan Nitter (free scraping) - sudah di-configure di config.py

**How to Get (If you want to pay):**
1. Go to https://developer.twitter.com/
2. Apply for developer account
3. Create project dan app
4. Get Bearer Token

**Add to .env:**
```env
TWITTER_BEARER_TOKEN=your_bearer_token
TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET=your_api_secret
```

**Cost:** $100/month (Basic tier)  
**Rate Limit:** 300 requests/15 minutes

**Recommendation:** Skip Twitter API, use Nitter instances instead (free)

---

### **5. Reddit API (Optional - Phase G)**

**Purpose:** Reddit sentiment analysis

**Pros:**
- ✅ FREE
- ✅ Good community sentiment
- ✅ Detailed discussions

**Cons:**
- ❌ Slower than Twitter
- ❌ Less real-time

**How to Get:**
1. Go to https://www.reddit.com/prefs/apps
2. Create app (select "script")
3. Copy client_id dan client_secret

**Add to .env:**
```env
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
```

**Cost:** FREE  
**Rate Limit:** 60 requests/minute

---

### **6. Telegram API (Optional - Phase G)**

**Purpose:** Telegram channel monitoring

**Pros:**
- ✅ FREE
- ✅ Many crypto channels
- ✅ Whale alerts

**Cons:**
- ❌ Complex setup
- ❌ Requires phone number

**How to Get:**
1. Go to https://my.telegram.org/
2. Login dengan phone number
3. Go to API development tools
4. Create application
5. Copy API ID dan API Hash

**Add to .env:**
```env
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash
```

**Cost:** FREE  
**Rate Limit:** 30 messages/second

---

## 🧠 Model Configuration

### **FinBERT Model Selection**

Modul G support 3 FinBERT models:

#### **1. yiyanghkust/finbert-tone (RECOMMENDED)**

```env
FINBERT_MODEL=yiyanghkust/finbert-tone
```

**Pros:**
- ✅ 3 classes (Positive, Negative, Neutral)
- ✅ Trained on financial text
- ✅ Good accuracy (~85%)
- ✅ Fast inference

**Cons:**
- ❌ ~500MB download size

**Use Case:** General purpose sentiment analysis

---

#### **2. ProsusAI/finbert**

```env
FINBERT_MODEL=ProsusAI/finbert
```

**Pros:**
- ✅ 3 classes
- ✅ Well-known model
- ✅ Good documentation

**Cons:**
- ❌ Slower than yiyanghkust
- ❌ Larger model size

**Use Case:** Alternative if yiyanghkust tidak works

---

#### **3. ahmedrachid/FinancialBERT-Sentiment-Analysis**

```env
FINBERT_MODEL=ahmedrachid/FinancialBERT-Sentiment-Analysis
```

**Pros:**
- ✅ 2 classes (simpler)
- ✅ Smaller model

**Cons:**
- ❌ No neutral class
- ❌ Less accurate

**Use Case:** Quick binary classification

---

### **GPU Configuration**

```env
USE_GPU=false  # or true if you have GPU
```

**When to Use GPU:**
- ✅ You have NVIDIA GPU with CUDA
- ✅ You need faster inference (5-7x speedup)
- ✅ You're processing large batches

**When to Use CPU:**
- ✅ No GPU available
- ✅ Development/testing
- ✅ Small batch sizes

**GPU Requirements:**
- NVIDIA GPU with CUDA support
- CUDA 11.8+ installed
- PyTorch with CUDA support

**Install PyTorch with CUDA:**
```bash
pip install torch --index-url https://download.pytorch.org/whl/cu118
```

---

### **Model Cache Directory**

```env
MODEL_CACHE_DIR=./models_cache
```

**Purpose:** Store downloaded models untuk faster loading

**Default:** `./models_cache`

**Recommendations:**
- Use SSD untuk faster loading
- Ensure enough disk space (~2GB)
- Don't delete after first download

---

## 🚨 Pump & Dump Detection

### **Thresholds Configuration**

```env
PUMP_VOLUME_THRESHOLD=3.0      # Volume spike (x average)
PUMP_PRICE_1H_THRESHOLD=15.0   # Price spike 1h (%)
PUMP_PRICE_24H_THRESHOLD=30.0  # Price spike 24h (%)
PUMP_SOCIAL_THRESHOLD=5.0      # Social mention spike (x average)
PUMP_MIN_MENTIONS=50           # Minimum mentions for validation
```

**Tuning Guide:**

#### **Conservative (Fewer False Positives)**
```env
PUMP_VOLUME_THRESHOLD=5.0
PUMP_PRICE_1H_THRESHOLD=20.0
PUMP_PRICE_24H_THRESHOLD=40.0
PUMP_SOCIAL_THRESHOLD=7.0
PUMP_MIN_MENTIONS=100
```

#### **Aggressive (More Detections)**
```env
PUMP_VOLUME_THRESHOLD=2.0
PUMP_PRICE_1H_THRESHOLD=10.0
PUMP_PRICE_24H_THRESHOLD=20.0
PUMP_SOCIAL_THRESHOLD=3.0
PUMP_MIN_MENTIONS=30
```

**Recommendation:** Start dengan default, adjust berdasarkan false positive rate

---

## 💾 Caching Configuration

### **TTL Settings**

```env
CACHE_TTL_NEWS=300       # 5 minutes
CACHE_TTL_TWITTER=60     # 1 minute
CACHE_TTL_SENTIMENT=180  # 3 minutes
CACHE_TTL_REDDIT=300     # 5 minutes
```

**Tuning Guide:**

#### **For High-Frequency Trading**
```env
CACHE_TTL_NEWS=60        # 1 minute
CACHE_TTL_TWITTER=30     # 30 seconds
CACHE_TTL_SENTIMENT=60   # 1 minute
CACHE_TTL_REDDIT=120     # 2 minutes
```

#### **For Cost Optimization**
```env
CACHE_TTL_NEWS=600       # 10 minutes
CACHE_TTL_TWITTER=300    # 5 minutes
CACHE_TTL_SENTIMENT=600  # 10 minutes
CACHE_TTL_REDDIT=600     # 10 minutes
```

**Recommendation:** Balance antara freshness dan API cost

---

## 🎛️ Feature Flags

### **Enable/Disable Features**

```env
ENABLE_FINBERT=true      # FinBERT sentiment analysis
ENABLE_TWITTER=true      # Twitter/X integration
ENABLE_REDDIT=false      # Reddit integration
ENABLE_TELEGRAM=false    # Telegram integration
ENABLE_CACHE=true        # Caching system
```

**Recommendations:**

#### **Minimal Setup (Fast & Simple)**
```env
ENABLE_FINBERT=true
ENABLE_TWITTER=false
ENABLE_REDDIT=false
ENABLE_TELEGRAM=false
ENABLE_CACHE=true
```

#### **Full Setup (All Features)**
```env
ENABLE_FINBERT=true
ENABLE_TWITTER=true
ENABLE_REDDIT=true
ENABLE_TELEGRAM=true
ENABLE_CACHE=true
```

#### **Cost-Optimized Setup**
```env
ENABLE_FINBERT=true
ENABLE_TWITTER=false     # Twitter API is expensive
ENABLE_REDDIT=true       # Reddit is free
ENABLE_TELEGRAM=false    # Telegram setup is complex
ENABLE_CACHE=true
```

---

## 📊 Monitoring Accounts

### **Influential Crypto Accounts**

Configured di `config.py`:

```python
INFLUENTIAL_ACCOUNTS = {
    "whales": [
        "whale_alert",      # Large transactions
        "lookonchain",      # On-chain analysis
        "EmberCN",          # Crypto insights
        "ai_9684xtpa",      # AI analysis
    ],
    "analysts": [
        "PlanB",            # Stock-to-flow model
        "CryptoCapo_",      # Market analysis
        "pentosh1",         # Trading insights
        "CryptoDonAlt",     # Technical analysis
    ],
    "news": [
        "WuBlockchain",     # Crypto news
        "DB_informasi",     # Indonesian crypto news
        "Tree_of_Alpha",    # Fast news updates
    ],
}
```

**Customization:** Edit `config.py` untuk add/remove accounts

---

## 🌐 Reddit Subreddits

### **Monitored Subreddits**

Configured di `config.py`:

```python
REDDIT_SUBREDDITS = [
    "CryptoCurrency",    # General crypto discussion
    "Bitcoin",           # Bitcoin-specific
    "ethereum",          # Ethereum-specific
    "CryptoMarkets",     # Market analysis
    "wallstreetbets",    # Meme stocks & crypto
    "stocks",            # General stocks
]
```

**Customization:** Edit `config.py` untuk add/remove subreddits

---

## 📺 Telegram Channels

### **Monitored Channels**

Configured di `config.py`:

```python
TELEGRAM_CHANNELS = [
    "whale_alert",    # Whale transactions
    "crypto_news",    # Crypto news
    "bitcoinnews",    # Bitcoin news
]
```

**Customization:** Edit `config.py` untuk add/remove channels

---

## 🐦 Nitter Instances

### **Twitter Scraping Alternatives**

Configured di `config.py`:

```python
NITTER_INSTANCES = [
    "https://nitter.privacydev.net",
    "https://nitter.poast.org",
    "https://nitter.net",
]
```

**Note:** Nitter instances may go down. System akan auto-fallback ke next instance.

**Customization:** Edit `config.py` untuk add/remove instances

**Find More Instances:** https://github.com/zedeus/nitter/wiki/Instances

---

## ✅ Validation

### **Test Configuration**

```bash
python -c "
from advanced_ai.config import *

print('🔍 Validating configuration...\n')

# Check required keys
required = ['BINANCE_API_KEY', 'BINANCE_API_SECRET']
for key in required:
    value = globals().get(key, '')
    if value and value != 'your_key':
        print(f'✅ {key}: configured')
    else:
        print(f'❌ {key}: NOT configured')

# Check optional keys
optional = ['CRYPTOPANIC_API_KEY', 'NEWSAPI_API_KEY', 'TWITTER_BEARER_TOKEN']
print('\n📝 Optional APIs:')
for key in optional:
    value = globals().get(key, '')
    if value and value != 'your_key':
        print(f'✅ {key}: configured')
    else:
        print(f'⚠️  {key}: not configured (optional)')

# Check model
print(f'\n🧠 FinBERT Model: {DEFAULT_FINBERT_MODEL}')
print(f'💻 Device: {DEVICE}')
print(f'💾 Cache Dir: {MODEL_CACHE_DIR}')

print('\n✅ Configuration validation complete!')
"
```

---

## 🎯 Recommended Setup

### **For Beginners (Minimal)**

```env
# Required
BINANCE_API_KEY=your_key
BINANCE_API_SECRET=your_secret
CRYPTOPANIC_API_KEY=your_key

# Model
FINBERT_MODEL=yiyanghkust/finbert-tone
USE_GPU=false

# Features
ENABLE_FINBERT=true
ENABLE_TWITTER=false
ENABLE_REDDIT=false
ENABLE_TELEGRAM=false
ENABLE_CACHE=true
```

**Cost:** FREE  
**Complexity:** Low  
**Features:** Basic sentiment + news

---

### **For Intermediate Users**

```env
# Required
BINANCE_API_KEY=your_key
BINANCE_API_SECRET=your_secret
CRYPTOPANIC_API_KEY=your_key
NEWSAPI_API_KEY=your_key

# Model
FINBERT_MODEL=yiyanghkust/finbert-tone
USE_GPU=false

# Features
ENABLE_FINBERT=true
ENABLE_TWITTER=false
ENABLE_REDDIT=true
ENABLE_TELEGRAM=false
ENABLE_CACHE=true
```

**Cost:** FREE  
**Complexity:** Medium  
**Features:** Sentiment + news + Reddit

---

### **For Advanced Users**

```env
# All APIs
BINANCE_API_KEY=your_key
BINANCE_API_SECRET=your_secret
CRYPTOPANIC_API_KEY=your_key
NEWSAPI_API_KEY=your_key
TWITTER_BEARER_TOKEN=your_token
REDDIT_CLIENT_ID=your_id
REDDIT_CLIENT_SECRET=your_secret
TELEGRAM_API_ID=your_id
TELEGRAM_API_HASH=your_hash

# Model
FINBERT_MODEL=yiyanghkust/finbert-tone
USE_GPU=true

# Features
ENABLE_FINBERT=true
ENABLE_TWITTER=true
ENABLE_REDDIT=true
ENABLE_TELEGRAM=true
ENABLE_CACHE=true
```

**Cost:** $100/month (Twitter API)  
**Complexity:** High  
**Features:** All features enabled

---

## 📚 Resources

### **API Documentation:**
- [Binance API](https://binance-docs.github.io/apidocs/)
- [CryptoPanic API](https://cryptopanic.com/developers/api/)
- [NewsAPI](https://newsapi.org/docs)
- [Twitter API](https://developer.twitter.com/en/docs)
- [Reddit API](https://www.reddit.com/dev/api/)
- [Telegram API](https://core.telegram.org/api)

### **Model Documentation:**
- [FinBERT Tone](https://huggingface.co/yiyanghkust/finbert-tone)
- [ProsusAI FinBERT](https://huggingface.co/ProsusAI/finbert)
- [FinancialBERT](https://huggingface.co/ahmedrachid/FinancialBERT-Sentiment-Analysis)

### **Nitter Instances:**
- [Nitter Wiki](https://github.com/zedeus/nitter/wiki/Instances)

---

## 🎉 Summary

**Minimum Required APIs:**
1. ✅ Binance API (FREE)
2. ✅ CryptoPanic API (FREE)

**Optional APIs:**
3. ⚠️ NewsAPI (FREE, 100 req/day)
4. ⚠️ Twitter API ($100/month)
5. ⚠️ Reddit API (FREE)
6. ⚠️ Telegram API (FREE)

**Total Cost:**
- **Minimal Setup:** FREE
- **Intermediate Setup:** FREE
- **Advanced Setup:** $100/month

**Recommendation:** Start dengan minimal setup, upgrade as needed.

---

**Configuration complete! 🎯**

Next step: Test dengan `python -m advanced_ai.main_advanced_ai`
