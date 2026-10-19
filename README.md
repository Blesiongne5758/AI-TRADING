# 🤖 AI Trading Agent

Sistem trading otomatis berbasis AI yang dirancang khusus untuk **pemula** agar bisa belajar, meriset, dan memahami pasar crypto dengan aman melalui paper trading.

## 📋 Fitur Fase 1: Data Collection

- ✅ **Koneksi ke Binance REST API** - Data harga historis + real-time dari 5 simbol (BTC, ETH, SOL, BNB, XRP)
- ✅ **6 Timeframes** - 1m, 5m, 15m, 1h, 4h, 1d
- ✅ **News Scraping** - Mengambil berita crypto dari 3 sumber RSS feeds
- ✅ **Database SQLite** - Penyimpanan data OHLCV, ticker, dan berita
- ✅ **Auto-reconnect** - Koneksi otomatis jika terputus
- ✅ **Logging** - Comprehensive logging untuk debugging

## 📋 Fitur Fase 2: Analysis Engine

- ✅ **Technical Indicators** - RSI, MACD, EMA, Bollinger Bands, Volume Analysis
- ✅ **Sentiment Analysis** - Rule-based (Phase 2a) dengan opsi upgrade ke ML-based (Phase 2b)
- ✅ **Signal Generation** - Menggabungkan technical + sentiment menjadi trading signals
- ✅ **Risk Management** - Stop-loss, take-profit, position sizing
- ✅ **Confidence Scoring** - Weighted voting system dari multiple indicators

## 📋 Fitur Fase 3: Paper Trading Engine

- ✅ **Virtual Portfolio** - Simulasi trading dengan uang virtual ($10,000 initial balance)
- ✅ **Position Management** - Track posisi terbuka (LONG/SHORT) dengan real-time P&L
- ✅ **Risk Management** - 8-step validation (confidence, max positions, duplicate check, daily loss limit, dll)
- ✅ **Order Execution** - Eksekusi otomatis dari analysis signals
- ✅ **Trading Fee Simulation** - 0.1% fee per trade (seperti Binance)
- ✅ **Stop-Loss & Take-Profit** - ATR-based, auto-check setiap 10 detik
- ✅ **Performance Tracking** - Win rate, profit factor, drawdown, equity curve
- ✅ **Time-based Scheduling** - Analisis 5 menit, SL/TP check 10 detik, snapshot 1 jam

## 📋 Fitur Fase 4: XAI (Explainable AI) Module

- ✅ **Explanation Generator** - Mengubah signal teknis menjadi narasi penjelasan bahasa manusia
- ✅ **Trading Dictionary** - Kamus 50+ istilah trading dengan definisi dan contoh
- ✅ **Context Builder** - Bangun konteks dari database untuk penjelasan yang lebih kaya
- ✅ **Chat Agent** - Chat interface dengan pattern matching untuk tanya jawab
- ✅ **Educational Notes** - Catatan edukasi untuk pemula di setiap penjelasan
- ✅ **Interactive Demo** - Testing dan demo semua fitur XAI

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
│   ├── analysis/
│   │   ├── __init__.py
│   │   ├── technical_indicators.py  ← RSI, MACD, EMA, BB, Volume
│   │   ├── sentiment_analysis.py    ← Analisis sentimen berita
│   │   ├── signal_generator.py      ← Gabungkan → Signal + Confidence
│   │   └── main_analysis.py         ← Entry point untuk testing
│   ├── paper_trading/
│   │   ├── __init__.py
│   │   ├── portfolio_manager.py     ← Kelola saldo, posisi, P&L
│   │   ├── risk_manager.py          ← Validasi risiko sebelum trade
│   │   ├── order_executor.py        ← Eksekusi order dari signal
│   │   └── main_paper_trading.py    ← Orchestrator (auto-trade loop)
│   ├── xai/
│   │   ├── __init__.py
│   │   ├── explanation_generator.py ← Generate narasi dari signal
│   │   ├── trading_dictionary.py    ← Kamus istilah trading (50+ istilah)
│   │   ├── context_builder.py       ← Bangun konteks dari database
│   │   ├── chat_agent.py            ← Chat interface dengan pattern matching
│   │   └── main_xai.py              ← Testing & demo
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
mkdir -p backend/data_collector backend/analysis database
```

### 2. Buat virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# atau: venv\Scripts\activate  # Windows
```

### 3. Install dependencies

**Opsi A: Menggunakan Script Otomatis (Recommended)**

```bash
cd backend

# Linux/Mac
chmod +x setup.sh
./setup.sh

# Windows
setup.bat
```

**Opsi B: Manual Installation**

```bash
cd backend

# Install semua dependencies
pip install -r requirements.txt

# Download TextBlob corpora (PENTING!)
python -m textblob.download_corpora
```

### 4. Setup environment
```bash
# Copy template konfigurasi
cp .env.example .env

# Edit .env dengan API keys Anda
# Dapatkan dari: https://testnet.binance.vision/
```

📚 **Panduan instalasi lengkap:** Lihat [INSTALL.md](INSTALL.md)

### 5. Jalankan Data Collector (Fase 1)
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

### 6. Jalankan Analysis Engine (Fase 2)
```bash
# Biarkan data collector berjalan di terminal pertama
# Buka terminal baru untuk analysis
python -m analysis.main_analysis
```

**Output yang diharapkan:**
```
======================================================================
🔍 Analyzing BTC/USDT [1h]
======================================================================
📊 Loaded 500 candles dan 60 news articles

📈 SIGNAL: BUY
🎯 Confidence: 75%
💰 Current Price: $42,300.75

📋 Reasons:
   1. Strong buy signal (score: +0.65)
   2. RSI oversold (28.5)
   3. MACD bullish crossover
   4. EMA alignment bullish
   5. News sentiment bullish (+0.72)

🛡️  Risk Management:
   Stop Loss: $41,454.74
   Take Profit: $44,415.79
   Risk/Reward Ratio: 2.50
   Position Size: 10.0% of portfolio
```

### 7. Jalankan Paper Trading Engine (Fase 3)
```bash
# Terminal baru untuk paper trading
python -m paper_trading.main_paper_trading
```

**Output yang diharapkan:**
```
15:30:01 | INFO     | 🚀 Initializing Paper Trading Service...
15:30:01 | INFO     | 💰 Initial balance: $10,000.00
15:30:01 | INFO     | 📊 Max open positions: 5
15:30:01 | INFO     | ⚠️  Max risk per trade: 2.0%
15:30:02 | INFO     | 🎯 BTC/USDT: LONG executed @ $67,234.50 | Qty: 0.00148700 | Value: $100.00 | Fee: $0.10
15:30:02 | INFO     |    SL: $65,834.50 | TP: $70,034.50
```

### 8. Jalankan XAI Demo (Fase 4)
```bash
# Terminal baru untuk XAI demo
python -m xai.main_xai
```

**Output yang diharapkan:**
```
======================================================================
🤖 XAI MODULE - DEMO & TESTING
======================================================================

📝 DEMO: Explanation Generator
🤖 PENJELASAN KEPUTUSAN BOT
🟢 Bot MEREKOMENDASIKAN BELI BTC/USDT
   Confidence: 85.5% | Score: +78.45

📚 DEMO: Trading Dictionary
📖 RSI (Relative Strength Index)
   Indikator momentum yang mengukur kecepatan dan perubahan pergerakan harga...

💬 DEMO: Chat Agent
👤 User: apa itu RSI?
🤖 Bot: 📖 RSI (Relative Strength Index)...
```

**Interactive Chat:**
```bash
# Ketik 'y' saat ditanya untuk mulai interactive chat
Mulai interactive chat? (y/n): y

👤 You: apa itu stop loss?
🤖 Bot: 📖 Stop Loss (SL)
   Order otomatis untuk menutup posisi saat harga mencapai level tertentu...

👤 You: portfolio
🤖 Bot: 💼 PORTFOLIO STATUS:
   📊 Total Trades: 10
   🎯 Win Rate: 70.0%
   💰 Total P&L: $+1,234.56

👤 You: quit
🤖 Bot: 👋 Sampai jumpa!
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

### Fase 1: Data Collection
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

### Fase 2: Analysis Engine
```txt
pandas-ta==0.3.14b    # Technical analysis (RSI, MACD, EMA, BB)
textblob==0.17.1      # Sentiment analysis (simple & lightweight)
```

**Optional (untuk upgrade ke ML-based sentiment):**
```txt
# transformers==4.36.2  # FinBERT model (~500MB)
# torch==2.1.2          # PyTorch
```

### Fase 3: Paper Trading Engine
```txt
# Tidak ada dependency tambahan
# Menggunakan modules dari Fase 1 & 2
```

### Fase 4: XAI (Explainable AI)
```txt
# Tidak ada dependency tambahan (MVP - ringan)
# Menggunakan pattern matching untuk chat agent
# Rule-based explanations (tidak perlu LLM)
```

**Optional (untuk upgrade ke LLM-based chat):**
```txt
# openai==1.12.0              # OpenAI API
# langchain==0.1.5            # LangChain framework
# langchain-community==0.0.20 # LangChain community models
```

**Total: 11 packages (~200MB)** - Sangat ringan untuk sistem trading lengkap!

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

### Data Collection (Fase 1)

#### 1. `config.py` - Konfigurasi Global
Menyimpan semua konfigurasi aplikasi menggunakan `python-dotenv`.

#### 2. `database.py` - DatabaseManager
Mengelola SQLite database dengan aiosqlite (async).

#### 3. `binance_ws.py` - Binance REST API Collector
Mengambil data harga dari Binance (historical + real-time).

#### 4. `news_scraper.py` - News Scraper
Mengambil berita crypto dari RSS feeds.

#### 5. `main_collector.py` - Entry Point
Menjalankan semua collectors secara bersamaan.

### Analysis Engine (Fase 2)

#### 6. `technical_indicators.py` - Technical Analysis
Menghitung indikator teknikal menggunakan **pandas-ta**:
- **RSI** (Relative Strength Index) - Mengukur overbought/oversold
- **MACD** (Moving Average Convergence Divergence) - Mengukur momentum
- **EMA** (Exponential Moving Average) - Mengukur trend
- **Bollinger Bands** - Mengukur volatilitas
- **Volume Analysis** - Mengkonfirmasi strength pergerakan

#### 7. `sentiment_analysis.py` - Sentiment Analysis
Menganalisis sentimen berita crypto:
- **Phase 2a**: TextBlob (simple, lightweight, ~1MB)
- **Phase 2b**: FinBERT (ML-based, optional upgrade, ~500MB)

#### 8. `signal_generator.py` - Signal Generation
Menggabungkan technical + sentiment menjadi trading signal:
- Weighted voting system (70% technical, 30% sentiment)
- Confidence scoring (0-100%)
- Risk management (stop-loss, take-profit, position sizing)

#### 9. `main_analysis.py` - Entry Point
Entry point untuk testing analysis engine.

### Paper Trading Engine (Fase 3)

#### 10. `portfolio_manager.py` - Portfolio Management
Mengelola portfolio virtual untuk paper trading:
- **In-memory state management** - Track saldo, posisi, P&L secara real-time
- **Margin management** - Reserve/release margin untuk posisi
- **P&L calculation** - Hitung unrealized & realized P&L
- **Drawdown tracking** - Track peak balance dan max drawdown

#### 11. `risk_manager.py` - Risk Management
Validasi risiko sebelum eksekusi trade (8-step validation):
- **Confidence check** - Min 55% confidence untuk trade
- **Max positions check** - Max 5 posisi terbuka
- **Duplicate symbol check** - Cegah double entry
- **Daily loss limit** - Stop trading jika loss > 5% per hari
- **Position size limit** - Max 20% portfolio per posisi
- **Risk per trade** - Max 2% risk per trade
- **Balance check** - Pastikan saldo cukup
- **Auto-adjust** - Otomatis adjust position size jika risk terlalu besar

#### 12. `order_executor.py` - Order Execution
Eksekusi order berdasarkan trading signals:
- **Signal validation** - Validasi signal dengan risk manager
- **Position creation** - Buat posisi di database
- **Fee calculation** - Hitung trading fee (0.1% seperti Binance)
- **SL/TP monitoring** - Check stop-loss & take-profit setiap 10 detik
- **P&L tracking** - Hitung P&L setelah fee

#### 13. `main_paper_trading.py` - Orchestrator
Auto-trade loop dengan time-based scheduling:
- **Analysis cycle** - Setiap 5 menit
- **SL/TP check** - Setiap 10 detik
- **Portfolio snapshot** - Setiap 1 jam
- **Status print** - Setelah setiap analysis cycle

### XAI Module (Fase 4)

#### 14. `explanation_generator.py` - Explanation Generator
Mengubah signal teknis menjadi narasi penjelasan bahasa manusia:
- **Layered explanation** - Summary → Detail → Risk → Education
- **Visual indicators** - Emoji untuk quick scanning (🟢 bullish, 🔴 bearish)
- **Educational notes** - Catatan edukasi untuk pemula
- **Simple explanation** - Penjelasan 1 paragraf

#### 15. `trading_dictionary.py` - Trading Dictionary
Kamus 50+ istilah trading dengan penjelasan lengkap:
- **Technical Analysis** - RSI, MACD, EMA, Bollinger Bands, ATR, Volume
- **Trading Terms** - Long, Short, Entry, Exit, Stop Loss, Take Profit
- **Risk Management** - Position Sizing, Daily Loss Limit, Drawdown
- **Market Conditions** - Overbought, Oversold, Breakout, Consolidation
- **Performance Metrics** - Win Rate, Profit Factor, Sharpe Ratio

#### 16. `context_builder.py` - Context Builder
Membangun konteks dari database untuk penjelasan yang lebih kaya:
- **Symbol context** - Current price, 24h range, recent news
- **Trade context** - Position details, unrealized P&L, distance to SL/TP
- **Performance context** - Stats, snapshots, trade history

#### 17. `chat_agent.py` - Chat Agent
Chat interface dengan pattern matching untuk tanya jawab:
- **Pattern matching** - Pahami pertanyaan user
- **Dictionary queries** - "apa itu RSI?", "jelaskan MACD"
- **Portfolio queries** - "portfolio", "status", "performance"
- **Signal queries** - "kenapa bot buy?", "signal terakhir"
- **Analysis queries** - "analisis BTC", "bagaimana ETH?"
- **Interactive chat** - Real-time conversation

#### 18. `main_xai.py` - XAI Demo
Entry point untuk testing dan demo XAI module:
- **Demo explanation generator**
- **Demo trading dictionary**
- **Demo context builder**
- **Demo chat agent**
- **Interactive chat session**

## 🧪 Verify Installation

Setelah instalasi, verifikasi semua dependencies terinstall dengan benar:

```bash
cd backend
python test_dependencies.py
```

Script ini akan test:
- ✅ Python version (3.11+)
- ✅ Basic imports (ccxt, pandas, numpy, dll)
- ✅ pandas-ta functionality
- ✅ TextBlob functionality
- ✅ Database connection
- ✅ Binance connection

Jika semua test passed, Anda siap menggunakan aplikasi!

## 🔧 Troubleshooting

### Error: "ModuleNotFoundError: No module named 'pandas_ta'"
```bash
pip install pandas-ta==0.3.14b
```

### Error: "ModuleNotFoundError: No module named 'textblob'"
```bash
pip install textblob==0.17.1
python -m textblob.download_corpora
```

### Error: "TextBlob corpora not found"
```bash
python -m textblob.download_corpora
```

### Other Issues
Lihat [INSTALL.md](INSTALL.md) untuk panduan troubleshooting lengkap.

## 🎯 Next Steps (Phase 3)

- [ ] Paper Trading Engine (virtual portfolio, order execution)
- [ ] XAI Module (Explainable AI, chat interface)
- [ ] Telegram Notifications (trade alerts, daily reports)
- [ ] Backtesting Engine (test strategies with historical data)
- [ ] Frontend Dashboard (React + TradingView charts)

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
