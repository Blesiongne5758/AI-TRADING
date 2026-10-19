# 📦 Dependencies Guide

Panduan lengkap untuk menginstall dan mengelola dependencies AI Trading Agent.

## 🎯 Overview

AI Trading Agent menggunakan **11 dependencies utama** (~200MB total) yang dibagi menjadi beberapa kategori:

### Phase 1: Data Collection
- `ccxt==4.2.25` - Binance API
- `aiohttp==3.9.1` - Async HTTP client
- `feedparser==6.0.11` - RSS feed parser

### Phase 2: Analysis Engine
- `pandas==2.1.4` - Data processing
- `numpy==1.26.2` - Numerical computing
- `pandas-ta==0.3.14b` - Technical analysis
- `textblob==0.17.1` - Sentiment analysis

### Phase 3: Paper Trading
- `aiosqlite==0.19.0` - Async SQLite database

### Phase 4: XAI Module
- Tidak ada dependency tambahan (rule-based)

### Phase 5: Backend API
- `fastapi==0.109.0` - Web framework
- `uvicorn[standard]==0.27.0` - ASGI server
- `websockets==12.0` - WebSocket support
- `python-multipart==0.0.6` - File upload support

### Utilities
- `python-dotenv==1.0.0` - Environment variables
- `loguru==0.7.2` - Logging

---

## 🚀 Installation

### 1. Install All Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Download TextBlob Corpora

```bash
python -m textblob.download_corpora
```

### 3. Verify Installation

```bash
python test_dependencies.py
```

---

## 📋 Dependencies Detail

### **ccxt==4.2.25**
- **Purpose**: Unified API untuk crypto exchanges
- **Size**: ~15MB
- **Usage**: Binance data collection
- **Docs**: https://docs.ccxt.com/

### **aiohttp==3.9.1**
- **Purpose**: Async HTTP client/server
- **Size**: ~5MB
- **Usage**: HTTP requests untuk news scraping
- **Docs**: https://docs.aiohttp.org/

### **feedparser==6.0.11**
- **Purpose**: Parse RSS/Atom feeds
- **Size**: ~1MB
- **Usage**: News scraping dari RSS feeds
- **Docs**: https://feedparser.readthedocs.io/

### **pandas==2.1.4**
- **Purpose**: Data manipulation & analysis
- **Size**: ~40MB
- **Usage**: Process candlestick data
- **Docs**: https://pandas.pydata.org/

### **numpy==1.26.2**
- **Purpose**: Numerical computing
- **Size**: ~30MB
- **Usage**: Mathematical operations
- **Docs**: https://numpy.org/

### **pandas-ta==0.3.14b**
- **Purpose**: Technical analysis indicators
- **Size**: ~5MB
- **Usage**: Calculate RSI, MACD, EMA, Bollinger Bands, ATR
- **Docs**: https://github.com/twopirllc/pandas-ta

### **textblob==0.17.1**
- **Purpose**: Natural language processing
- **Size**: ~1MB
- **Usage**: Sentiment analysis untuk berita
- **Docs**: https://textblob.readthedocs.io/
- **Note**: Perlu download corpora setelah install

### **aiosqlite==0.19.0**
- **Purpose**: Async SQLite database
- **Size**: ~1MB
- **Usage**: Database untuk paper trading
- **Docs**: https://aiosqlite.omnilib.dev/

### **fastapi==0.109.0**
- **Purpose**: Modern web framework
- **Size**: ~3MB
- **Usage**: REST API backend
- **Docs**: https://fastapi.tiangolo.com/
- **Features**:
  - Auto-generated API docs (Swagger UI)
  - Async support
  - Type validation
  - CORS middleware built-in

### **uvicorn[standard]==0.27.0**
- **Purpose**: ASGI server
- **Size**: ~2MB
- **Usage**: Run FastAPI application
- **Docs**: https://www.uvicorn.org/
- **Note**: `[standard]` includes uvloop dan httptools untuk performance

### **websockets==12.0**
- **Purpose**: WebSocket library
- **Size**: ~2MB
- **Usage**: Real-time updates
- **Docs**: https://websockets.readthedocs.io/

### **python-multipart==0.0.6**
- **Purpose**: Parse multipart/form-data
- **Size**: ~0.5MB
- **Usage**: File upload support di FastAPI
- **Docs**: https://github.com/andrew-d/python-multipart

### **python-dotenv==1.0.0**
- **Purpose**: Load environment variables dari .env file
- **Size**: ~0.5MB
- **Usage**: Configuration management
- **Docs**: https://saurabh-kumar.com/python-dotenv/

### **loguru==0.7.2**
- **Purpose**: Logging library
- **Size**: ~2MB
- **Usage**: Structured logging
- **Docs**: https://loguru.readthedocs.io/

---

## 🔧 Optional Dependencies

### **FinBERT (Advanced Sentiment Analysis)**

Jika ingin upgrade dari TextBlob ke FinBERT untuk sentiment analysis yang lebih akurat:

```bash
pip install transformers==4.36.2 torch==2.1.2
```

**Size**: ~500MB  
**Usage**: ML-based sentiment analysis  
**Note**: 
- Butuh GPU untuk performance optimal
- First-time load akan download model ~500MB
- Startup lambat (30-60 detik)

**Enable di code**:
```python
# Di sentiment_analysis.py
sentiment_analyzer = SentimentAnalyzer(use_finbert=True)
```

### **LLM-based Chat (Advanced XAI)**

Jika ingin upgrade dari pattern matching ke LLM untuk chat yang lebih natural:

```bash
pip install openai==1.12.0 langchain==0.1.5 langchain-community==0.0.20
```

**Size**: ~100MB  
**Usage**: Natural language understanding  
**Note**: 
- Butuh OpenAI API key
- Cost per query
- Slower response time

---

## 🐛 Troubleshooting

### Error: "ModuleNotFoundError: No module named 'pandas_ta'"

**Solusi**:
```bash
pip install pandas-ta==0.3.14b
```

### Error: "TextBlob corpora not found"

**Solusi**:
```bash
python -m textblob.download_corpora
```

### Error: "ImportError: cannot import name 'CORS' from 'fastapi_cors'"

**Penjelasan**: FastAPI sudah punya CORS middleware built-in, tidak perlu install `fastapi-cors`.

**Solusi**: Gunakan CORS dari FastAPI:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Error: "uvicorn: command not found"

**Solusi**:
```bash
pip install uvicorn[standard]
```

### Error: "WebSockets not supported"

**Solusi**:
```bash
pip install websockets==12.0
```

---

## 📊 Dependency Size Summary

| Category | Packages | Size |
|----------|----------|------|
| **Core Trading** | ccxt, aiohttp, feedparser | ~21MB |
| **Data Processing** | pandas, numpy | ~70MB |
| **Analysis** | pandas-ta, textblob | ~6MB |
| **Database** | aiosqlite | ~1MB |
| **Web Server** | fastapi, uvicorn, websockets, python-multipart | ~7.5MB |
| **Utilities** | python-dotenv, loguru | ~2.5MB |
| **TOTAL** | **11 packages** | **~108MB** |

**Optional:**
- FinBERT: +500MB
- LLM: +100MB

---

## 🔄 Update Dependencies

### Update All
```bash
pip install --upgrade -r requirements.txt
```

### Update Specific Package
```bash
pip install --upgrade pandas-ta
```

### Check for Updates
```bash
pip list --outdated
```

---

## 🗑️ Uninstall Dependencies

### Uninstall All
```bash
pip freeze | xargs pip uninstall -y
```

### Uninstall Specific Package
```bash
pip uninstall pandas-ta
```

---

## 📝 Notes

### **CORS Middleware**
FastAPI sudah include CORS middleware built-in. Tidak perlu install package terpisah seperti `fastapi-cors`.

**Usage**:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### **WebSockets Duplication**
`websockets` package ada di 2 tempat di requirements.txt (line 9 dan 55). Ini tidak masalah karena pip akan install sekali saja.

### **Python Version**
Semua dependencies tested dengan **Python 3.11+**. Pastikan menggunakan versi yang compatible.

### **Virtual Environment**
**SANGAT DIREKOMENDASIKAN** menggunakan virtual environment:

```bash
# Create virtual environment
python -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## ✅ Verification Checklist

Setelah install, pastikan:

- [ ] `pip install -r requirements.txt` berhasil
- [ ] `python -m textblob.download_corpora` berhasil
- [ ] `python test_dependencies.py` semua test pass
- [ ] Backend bisa start: `python -m api.main`
- [ ] Frontend bisa start: `npm run dev`
- [ ] API docs accessible: `http://localhost:8000/docs`

---

## 📚 Resources

- [pip Documentation](https://pip.pypa.io/)
- [Virtual Environments](https://docs.python.org/3/tutorial/venv.html)
- [Requirements Files](https://pip.pypa.io/en/stable/user_guide/#requirements-files)
- [Dependency Conflicts](https://pip.pypa.io/en/stable/topics/dependency-resolution/)

---

**Last Updated**: 2024  
**Python Version**: 3.11+  
**Total Dependencies**: 11 packages (~108MB)
