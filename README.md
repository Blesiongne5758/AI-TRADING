# 🤖 AI Trading Agent

Sistem trading otomatis berbasis AI yang dirancang khusus untuk **pemula** agar bisa belajar, meriset, dan memahami pasar crypto dengan aman melalui paper trading.

## 📋 Fitur Fase 1

- ✅ **Koneksi ke Binance REST API** - Data harga historis + real-time dari 5 simbol (BTC, ETH, SOL, BNB, XRP)
- ✅ **6 Timeframes** - 1m, 5m, 15m, 1h, 4h, 1d
- ✅ **News Scraping** - Mengambil berita crypto dari 3 sumber RSS feeds
- ✅ **Database SQLite** - Penyimpanan data OHLCV, ticker, dan berita
- ✅ **Auto-reconnect** - Koneksi otomatis jika terputus
- ✅ **Logging** - Comprehensive logging untuk debugging

## 📁 Struktur Proyek

```
ai-trading-agent/
├── backend/
│   ├── data_collector/
│   │   ├── __init__.py
│   │   ├── config.py          ← Konfigurasi global
│   │   ├── database.py        ← DatabaseManager (SQLite)
│   │   ├── binance_ws.py      ← Binance REST API collector
│   │   ├── news_scraper.py    ← News scraper (RSS)
│   │   └── main_collector.py  ← Entry point
│   ├── .env.example           ← Template konfigurasi
│   └── requirements.txt       ← Python dependencies
├── database/                  ← SQLite database (auto-created)
├── logs/                      ← Log files (auto-created)
├── .env                       ← Environment variables (create from .env.example)
├── .gitignore
└── README.md
```

## 🚀 Quick Start

### 1. Buat folder proyek
```bash
mkdir ai-trading-agent
cd ai-trading-agent
mkdir -p backend/data_collector database
```

### 2. Buat virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# atau: venv\Scripts\activate  # Windows
```

### 3. Install dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 4. Setup environment
```bash
# Copy template konfigurasi
cp .env.example .env

# Edit .env dengan API keys Anda
# Dapatkan dari: https://testnet.binance.vision/
```

### 5. Jalankan aplikasi
```bash
python -m data_collector.main_collector
```

**Output yang diharapkan:**
```
10:00:00 | INFO     | 🚀 Starting AI Trading Agent - Data Collector Service
10:00:00 | INFO     | ============================================================
10:00:01 | INFO     | ✅ Database initialized at database/trading_data.db
10:00:02 | INFO     | 🧪 Menggunakan Binance TESTNET (aman untuk testing)
10:00:03 | INFO     | ✅ Connected to Binance. Markets loaded: 2000
10:00:04 | INFO     | 📊 Fetching historical candles...
10:00:05 | INFO     | ✅ BTC/USDT [1h]: 500 candles loaded
10:00:06 | INFO     | 🔄 Starting real-time ticker loop...
10:00:07 | INFO     | 💹 BTC/USDT: $42,300.75 (+2.50%)
10:00:08 | INFO     | 🔄 Starting news scraper (interval: 900s)
10:00:09 | INFO     | 📰 Fetching news from all sources...
10:00:10 | INFO     | 📰 CoinDesk: 20 articles
```

## 📊 Data yang Dikumpulkan

### Candlestick Data (OHLCV)
- **5 symbols**: BTC/USDT, ETH/USDT, SOL/USDT, BNB/USDT, XRP/USDT
- **6 timeframes**: 1m, 5m, 15m, 1h, 4h, 1d
- **500 candles per symbol/timeframe** (historical)

### Ticker Data (Real-time)
- **5 symbols**: BTC/USDT, ETH/USDT, SOL/USDT, BNB/USDT, XRP/USDT
- **Update interval**: Setiap 10 detik

### News Data
- **3 sources**: CoinDesk, CoinTelegraph, Decrypt
- **Fetch interval**: Setiap 15 menit

## 📦 Dependencies

```txt
ccxt==4.2.25          # Binance API
websockets==12.0      # WebSocket client
aiohttp==3.9.1        # Async HTTP
pandas==2.1.4         # Data processing
numpy==1.26.2         # Numerical computing
feedparser==6.0.11    # RSS parser
aiosqlite==0.19.0     # Async SQLite
python-dotenv==1.0.0  # Environment variables
loguru==0.7.2         # Logging
```

**Total: 9 packages (~150MB)**

## 🔧 Konfigurasi

### File `.env`
```env
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here
```

**Dapatkan API keys dari:**
- Testnet: https://testnet.binance.vision/ (recommended untuk testing)
- Mainnet: https://www.binance.com/en/my/settings/api-management

## 📖 Penjelasan Modul

### 1. `config.py` - Konfigurasi Global
Menyimpan semua konfigurasi aplikasi menggunakan `python-dotenv`.

### 2. `database.py` - DatabaseManager
Mengelola SQLite database dengan aiosqlite (async).

### 3. `binance_ws.py` - Binance REST API Collector
Mengambil data harga dari Binance (historical + real-time).

### 4. `news_scraper.py` - News Scraper
Mengambil berita crypto dari RSS feeds.

### 5. `main_collector.py` - Entry Point
Menjalankan semua collectors secara bersamaan.

## 🎯 Next Steps (Phase 2)

- [ ] Analysis Engine (RSI, MACD, EMA, Bollinger Bands)
- [ ] Sentiment Analysis dengan FinBERT AI
- [ ] Signal Generation
- [ ] Paper Trading Engine
- [ ] Risk Management
- [ ] XAI Module (Explainable AI)
- [ ] Telegram Notifications

## ⚠️ Disclaimer

**PENTING:**
- Ini adalah proyek edukasi dan research
- Paper trading menggunakan uang virtual
- Trading crypto memiliki risiko tinggi
- Jangan invest uang yang tidak siap Anda rugikan
- Selalu lakukan riset sendiri (DYOR)

## 📚 Resources

- [CCXT Documentation](https://docs.ccxt.com/)
- [Binance API Documentation](https://binance-docs.github.io/apidocs/)
- [Python Asyncio Tutorial](https://realpython.com/async-io-python/)

---

**Happy Trading! 🚀📈**
