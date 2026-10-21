# 🔑 Setup Environment Variables untuk Modul G

Panduan lengkap untuk setup API keys dan konfigurasi Modul G: Advanced AI.

## 🚀 Quick Start

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
# Binance (untuk data collection)
BINANCE_API_KEY=your_key
BINANCE_API_SECRET=your_secret

# CryptoPanic (untuk news - GRATIS & RECOMMENDED)
CRYPTOPANIC_API_KEY=your_key
```

### 4. Test Configuration

```bash
python -c "from advanced_ai.config import AdvancedAIConfig; AdvancedAIConfig.print_config()"
```

---

## 📋 API Keys Guide

### **1. Binance API** (Required - Phase 1)

**Purpose:** Data collection (OHLCV, ticker, news)

**How to Get:**
1. Go to https://testnet.binance.vision/
2. Login dengan GitHub account
3. Generate API Key
4. Copy API Key dan Secret Key

**Add to .env:**
```env
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here
```

**Cost:** FREE (testnet)  
**Rate Limit:** 1200 requests/minute

---

### **2. CryptoPanic API** (Highly Recommended - Phase G)

**Purpose:** Crypto-specific news aggregation

**Why Recommended:**
- ✅ GRATIS
- ✅ Khusus crypto (lebih relevan)
- ✅ Real-time updates
- ✅ Sentiment labels included
- ✅ Community votes

**How to Get:**
1. Go to https://cryptopanic.com/
2. Sign up for free account
3. Go to https://cryptopanic.com/developers/api/
4. Copy API key

**Add to .env:**
```env
CRYPTOPANIC_API_KEY=your_cryptopanic_key_here
```

**Cost:** FREE  
**Rate Limit:** 30 requests/minute

---

### **3. NewsAPI.org** (Optional - Phase G)

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
NEWSAPI_API_KEY=your_newsapi_key_here
```

**Cost:** FREE (100 requests/day)  
**Rate Limit:** 100 requests/day

---

### **4. GNews** (Optional - Phase G)

**Purpose:** Alternative news source

**Pros:**
- ✅ GRATIS
- ✅ No registration required
- ✅ Simple API

**Cons:**
- ❌ Limited features
- ❌ Less reliable than CryptoPanic

**How to Get:**
1. Go to https://gnews.org/
2. Sign up for free account
3. Copy API key

**Add to .env:**
```env
GNEWS_API_KEY=your_gnews_key_here
```

**Cost:** FREE (100 requests/day)  
**Rate Limit:** 100 requests/day

---

### **5. Twitter/X API** (Optional - Phase G)

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
TWITTER_BEARER_TOKEN=your_bearer_token_here
```

**Cost:** $100/month (Basic tier)  
**Rate Limit:** 300 requests/15 minutes

**Recommendation:** Skip Twitter API, use Nitter instances instead (free)

---

### **6. Reddit API** (Optional - Phase G)

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
REDDIT_CLIENT_ID=your_client_id_here
REDDIT_CLIENT_SECRET=your_client_secret_here
```

**Cost:** FREE  
**Rate Limit:** 60 requests/minute

---

### **7. Telegram API** (Optional - Phase G)

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
TELEGRAM_API_ID=your_api_id_here
TELEGRAM_API_HASH=your_api_hash_here
```

**Cost:** FREE  
**Rate Limit:** 30 messages/second

---

## 🧠 FinBERT Configuration

### **No API Key Needed!**

FinBERT model akan di-download otomatis saat pertama kali digunakan.

**Settings:**
```env
# GPU usage (set true jika punya GPU)
USE_GPU=false

# Model cache directory
MODEL_CACHE_DIR=./models_cache
```

**First Run:**
- Model akan di-download (~400MB)
- Takes 1-2 minutes
- Subsequent runs akan load dari cache

**GPU Support:**
```bash
# Install PyTorch with CUDA
pip install torch --index-url https://download.pytorch.org/whl/cu118

# Enable GPU
USE_GPU=true
```

---

## 🎯 Recommended Setup

### **Minimal Setup (FREE, Simple)**

```env
# Required
BINANCE_API_KEY=your_key
BINANCE_API_SECRET=your_secret
CRYPTOPANIC_API_KEY=your_key

# FinBERT
USE_GPU=false
MODEL_CACHE_DIR=./models_cache

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

### **Intermediate Setup (FREE, More Features)**

```env
# Required
BINANCE_API_KEY=your_key
BINANCE_API_SECRET=your_secret
CRYPTOPANIC_API_KEY=your_key
NEWSAPI_API_KEY=your_key
GNEWS_API_KEY=your_key

# Reddit (FREE)
REDDIT_CLIENT_ID=your_id
REDDIT_CLIENT_SECRET=your_secret

# FinBERT
USE_GPU=false
MODEL_CACHE_DIR=./models_cache

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

### **Advanced Setup (PAID, All Features)**

```env
# All APIs
BINANCE_API_KEY=your_key
BINANCE_API_SECRET=your_secret
CRYPTOPANIC_API_KEY=your_key
NEWSAPI_API_KEY=your_key
GNEWS_API_KEY=your_key
TWITTER_BEARER_TOKEN=your_token
REDDIT_CLIENT_ID=your_id
REDDIT_CLIENT_SECRET=your_secret
TELEGRAM_API_ID=your_id
TELEGRAM_API_HASH=your_hash

# FinBERT with GPU
USE_GPU=true
MODEL_CACHE_DIR=./models_cache

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

## 🧪 Testing Configuration

### **Test 1: Check Config**

```bash
python -c "
from advanced_ai.config import AdvancedAIConfig
AdvancedAIConfig.print_config()
"
```

**Expected Output:**
```
======================================================================
🧠 ADVANCED AI CONFIGURATION
======================================================================

📰 News APIs:
   CryptoPanic: ✅
   NewsAPI: ✅
   GNews: ❌

📱 Social Media:
   Twitter: ❌
   Reddit: ✅
   Telegram: ❌

🧠 Models:
   FinBERT: ✅
   Model: yiyanghkust/finbert-tone
   Device: cpu

💾 Cache:
   Enabled: ✅
   Directory: ./cache

======================================================================
```

### **Test 2: Test FinBERT**

```bash
python -c "
import asyncio
from advanced_ai import FinBERTAnalyzer

async def test():
    analyzer = FinBERTAnalyzer()
    result = await analyzer.analyze('Bitcoin is bullish today')
    print(f'Sentiment: {result}')

asyncio.run(test())
"
```

**Expected Output:**
```
🧠 Initializing FinBERT analyzer: yiyanghkust/finbert-tone
   Device: cpu
   Cache: ./models_cache
📥 Loading FinBERT model (first time may download ~400MB)...
✅ FinBERT model loaded successfully
Sentiment: {'label': 'POSITIVE', 'confidence': 0.85, 'score': 0.85, 'method': 'finbert'}
```

### **Test 3: Test News API**

```bash
python -c "
import asyncio
from advanced_ai import NewsAPIClient

async def test():
    client = NewsAPIClient()
    await client.initialize()
    articles = await client.fetch_cryptopanic(currencies=['BTC'], limit=5)
    print(f'Fetched {len(articles)} articles')
    await client.close()

asyncio.run(test())
"
```

### **Test 4: Full Demo**

```bash
python -m advanced_ai.main_advanced_ai
```

---

## 🐛 Troubleshooting

### **Error: "API key not configured"**

**Solusi:**
```bash
# Check .env file
cat .env | grep API_KEY

# Make sure keys are not empty
CRYPTOPANIC_API_KEY=your_actual_key_here
```

### **Error: "FinBERT model download failed"**

**Solusi:**
```bash
# Check internet connection
ping huggingface.co

# Manual download
python -c "
from transformers import AutoModel, AutoTokenizer
model_name = 'yiyanghkust/finbert-tone'
AutoTokenizer.from_pretrained(model_name)
AutoModel.from_pretrained(model_name)
print('✅ Model downloaded')
"
```

### **Error: "Rate limit exceeded"**

**Solusi:**
```bash
# Enable caching
ENABLE_CACHE=true

# Increase cache TTL
CACHE_TTL_NEWS=600  # 10 minutes
CACHE_TTL_TWITTER=120  # 2 minutes
```

### **Error: "GPU not available"**

**Solusi:**
```bash
# Disable GPU
USE_GPU=false

# Or install CUDA-enabled PyTorch
pip install torch --index-url https://download.pytorch.org/whl/cu118
```

---

## 📊 API Keys Summary

| API | Cost | Rate Limit | Required | Recommended |
|-----|------|------------|----------|-------------|
| **Binance** | FREE | 1200 req/min | ✅ Yes | ✅ Yes |
| **CryptoPanic** | FREE | 30 req/min | ❌ No | ✅ Yes |
| **NewsAPI** | FREE | 100 req/day | ❌ No | ⚠️ Optional |
| **GNews** | FREE | 100 req/day | ❌ No | ⚠️ Optional |
| **Twitter** | $100/month | 300 req/15min | ❌ No | ❌ No (use Nitter) |
| **Reddit** | FREE | 60 req/min | ❌ No | ⚠️ Optional |
| **Telegram** | FREE | 30 msg/sec | ❌ No | ❌ No |
| **FinBERT** | FREE | N/A | ✅ Yes | ✅ Yes |

**Total Cost:**
- **Minimal Setup:** FREE
- **Intermediate Setup:** FREE
- **Advanced Setup:** $100/month (Twitter API)

---

## ✅ Checklist

Sebelum running Modul G:

- [ ] Copy `.env.example` ke `.env`
- [ ] Isi Binance API keys
- [ ] Isi CryptoPanic API key (recommended)
- [ ] Isi NewsAPI key (optional)
- [ ] Isi GNews key (optional)
- [ ] Set `USE_GPU=false` (or `true` jika punya GPU)
- [ ] Set `ENABLE_CACHE=true`
- [ ] Test configuration dengan `AdvancedAIConfig.print_config()`
- [ ] Test FinBERT dengan demo script
- [ ] Test News API dengan demo script

---

## 🎉 Success Criteria

Modul G siap digunakan jika:

✅ Semua required API keys sudah di-setup  
✅ FinBERT model bisa di-load  
✅ News API bisa fetch articles  
✅ Cache system berfungsi  
✅ Demo tests passed  

---

**Your environment is ready! 🚀**

Silakan jalankan `python -m advanced_ai.main_advanced_ai` untuk test semua komponen!
