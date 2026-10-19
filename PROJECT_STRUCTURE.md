# 📁 Project Structure

Struktur folder lengkap AI Trading Agent dengan penjelasan setiap file.

```
ai-trading-agent/
│
├── backend/                          # Backend Python application
│   ├── __init__.py                   # Package marker
│   ├── config.py                     # Konfigurasi aplikasi (API keys, settings)
│   ├── database.py                   # Database models & operations (SQLAlchemy)
│   │
│   ├── data_collector/               # Modul A: Data Collection
│   │   ├── __init__.py
│   │   ├── binance_ws.py            # Binance WebSocket connection
│   │   └── news_scraper.py          # RSS feed scraper + sentiment analysis
│   │
│   ├── analysis/                     # Modul B: Analysis Engine (Phase 2)
│   │   ├── __init__.py
│   │   ├── technical_indicators.py  # RSI, MACD, EMA, Bollinger Bands
│   │   ├── sentiment_analysis.py    # News sentiment aggregation
│   │   └── signal_generator.py      # Trading signal generation
│   │
│   ├── paper_trading/                # Modul C: Paper Trading (Phase 2)
│   │   ├── __init__.py
│   │   ├── portfolio_manager.py     # Virtual portfolio management
│   │   ├── order_executor.py        # Simulated order execution
│   │   └── risk_manager.py          # Stop-loss, position sizing
│   │
│   ├── xai/                          # Modul D: Explainable AI (Phase 2)
│   │   ├── __init__.py
│   │   ├── explanation_generator.py # Human-readable explanations
│   │   └── chat_agent.py            # Interactive chat interface
│   │
│   ├── api/                          # FastAPI Application
│   │   ├── __init__.py
│   │   └── main.py                  # Main FastAPI app & routes
│   │
│   ├── tests/                        # Unit tests
│   │   ├── __init__.py
│   │   └── test_database.py         # Database tests
│   │
│   ├── requirements.txt              # Python dependencies
│   ├── .env.example                  # Environment variables template
│   └── logs/                         # Log files (auto-created)
│       ├── api.log
│       ├── binance_ws.log
│       └── news_scraper.log
│
├── frontend/                         # React Frontend (sudah ada)
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── App.tsx
│   └── package.json
│
├── database/                         # SQLite database (auto-created)
│   └── trading_data.db
│
├── README.md                         # Dokumentasi lengkap
├── QUICKSTART.md                     # Panduan cepat 5 menit
├── PROJECT_STRUCTURE.md              # File ini
├── .gitignore                        # Git ignore rules
└── .env                              # Environment variables (create from .env.example)
```

---

## 📝 Penjelasan File per File

### Root Level

#### `README.md`
Dokumentasi lengkap proyek mencakup:
- Overview dan fitur
- Arsitektur sistem
- Instalasi dan konfigurasi
- Penjelasan setiap modul
- API documentation
- Troubleshooting

#### `QUICKSTART.md`
Panduan cepat untuk memulai dalam 5 menit:
- Step-by-step setup
- Cara mendapatkan API keys
- Cara menjalankan aplikasi
- Testing endpoints

#### `.gitignore`
File-file yang diabaikan oleh Git:
- Virtual environment (`venv/`)
- Python cache (`__pycache__/`)
- Database files (`*.db`)
- Log files (`logs/`)
- Environment variables (`.env`)

#### `.env`
Environment variables (TIDAK di-commit ke Git):
- API keys (Binance, Telegram)
- Database URL
- Trading settings
- Analysis parameters

**PENTING:** Copy dari `.env.example` dan isi dengan values Anda.

---

### Backend Files

#### `backend/config.py`
**Fungsi:** Konfigurasi aplikasi

**Isi:**
- Application settings (name, version, debug mode)
- Binance API settings (keys, symbols, timeframes)
- Database settings (SQLite URL)
- Telegram bot settings
- Trading settings (risk management)
- Analysis settings (indicators parameters)

**Untuk pemula:**
- Menggunakan `pydantic-settings` untuk validasi
- Semua values bisa di-override via `.env` file
- Type hints untuk autocomplete di IDE

#### `backend/database.py`
**Fungsi:** Database models dan operations

**Isi:**
- SQLAlchemy models (tables):
  - `OHLCVData` - Candlestick data
  - `NewsData` - News with sentiment
  - `TradingSignal` - Bot signals
  - `PaperTrade` - Trade history
  - `PortfolioSnapshot` - Portfolio snapshots
- Database initialization
- CRUD operations (save, get, update, delete)
- Async session management

**Untuk pemula:**
- ORM = Object-Relational Mapping
- Kita kerja dengan Python objects, bukan SQL queries
- Async/await untuk non-blocking operations

#### `backend/data_collector/binance_ws.py`
**Fungsi:** Real-time data collection dari Binance

**Isi:**
- `BinanceDataCollector` class
- WebSocket connection ke Binance
- Fetch historical OHLCV data
- Watch real-time candlestick streams
- Auto-reconnect on connection loss
- Save data to database

**Untuk pemula:**
- WebSocket = koneksi dua arah real-time
- CCXT library handle semua kompleksitas
- Data disimpan ke database untuk analisis

#### `backend/data_collector/news_scraper.py`
**Fungsi:** News scraping dan sentiment analysis

**Isi:**
- `SentimentAnalyzer` class (FinBERT model)
- `NewsScraper` class (RSS feeds)
- Parse RSS feeds dari multiple sources
- Analyze sentiment dengan AI
- Save news + sentiment to database

**Untuk pemula:**
- RSS = format untuk distribute berita
- FinBERT = AI model untuk financial text
- Sentiment score: -1.0 (bearish) sampai +1.0 (bullish)

#### `backend/api/main.py`
**Fungsi:** FastAPI application dan routes

**Isi:**
- FastAPI app initialization
- Lifespan handler (startup/shutdown)
- Background tasks (data collection)
- API endpoints:
  - `GET /` - Root
  - `GET /health` - Health check
  - `GET /status` - System status
  - `GET /ohlcv/{symbol}/{timeframe}` - OHLCV data
  - `GET /news` - Recent news
  - `GET /price/{symbol}` - Current price
- CORS middleware
- Pydantic models (request/response schemas)

**Untuk pemula:**
- FastAPI = web framework modern untuk Python
- Async/await untuk handle banyak request
- Swagger UI otomatis di `/docs`

---

## 🗄️ Database Schema

### Tabel: `ohlcv_data`
Menyimpan data candlestick dari Binance

**Kolom:**
- `id` - Primary key
- `symbol` - Trading pair (e.g., "BTC/USDT")
- `timeframe` - Time interval (e.g., "1h")
- `timestamp` - Unix timestamp
- `open` - Opening price
- `high` - Highest price
- `low` - Lowest price
- `close` - Closing price
- `volume` - Trading volume
- `created_at` - Record creation time

**Indexes:**
- `symbol` - Fast lookup by symbol
- `timeframe` - Fast lookup by timeframe
- `(symbol, timeframe, timestamp)` - Composite index

### Tabel: `news_data`
Menyimpan berita crypto dengan sentiment

**Kolom:**
- `id` - Primary key
- `title` - News title
- `source` - News source (e.g., "CoinDesk")
- `url` - News URL (unique)
- `published_at` - Publication time
- `summary` - News summary
- `sentiment_score` - Sentiment (-1.0 to 1.0)
- `sentiment_label` - "bullish", "bearish", "neutral"
- `created_at` - Record creation time

### Tabel: `trading_signals`
Menyimpan sinyal trading dari bot

**Kolom:**
- `id` - Signal ID (primary key)
- `symbol` - Trading pair
- `timeframe` - Time interval
- `signal` - "BUY", "SELL", "HOLD"
- `confidence` - Confidence score (0.0 to 1.0)
- `reasons` - JSON array of reasons
- `price` - Price at signal time
- `timestamp` - Signal time
- `executed` - Whether signal was executed
- `created_at` - Record creation time

### Tabel: `paper_trades`
Menyimpan riwayat paper trading

**Kolom:**
- `id` - Trade ID (primary key)
- `signal_id` - Foreign key to trading_signals
- `symbol` - Trading pair
- `side` - "BUY" or "SELL"
- `type` - "MARKET" or "LIMIT"
- `price` - Execution price
- `quantity` - Amount traded
- `total` - Total value
- `fee` - Trading fee
- `timestamp` - Trade time
- `status` - "FILLED", "PARTIAL", "CANCELLED"
- `pnl` - Profit/Loss
- `created_at` - Record creation time

### Tabel: `portfolio_snapshots`
Menyimpan snapshot portfolio berkala

**Kolom:**
- `id` - Primary key
- `timestamp` - Snapshot time
- `total_balance` - Total portfolio value
- `available_balance` - Available balance
- `total_pnl` - Total profit/loss
- `total_pnl_percent` - P&L percentage
- `open_positions` - Number of open positions

---

## 🔄 Data Flow

### 1. Data Collection Flow
```
Binance WebSocket → BinanceDataCollector → Database
RSS Feeds → NewsScraper → SentimentAnalyzer → Database
```

### 2. Analysis Flow (Phase 2)
```
Database (OHLCV) → TechnicalIndicators → AnalysisEngine
Database (News) → SentimentAggregator → AnalysisEngine
AnalysisEngine → SignalGenerator → Database (Signals)
```

### 3. Trading Flow (Phase 2)
```
Database (Signals) → PaperTradingEngine → OrderExecutor
OrderExecutor → RiskManager → PortfolioManager
PortfolioManager → Database (Trades)
```

### 4. API Flow
```
Frontend → FastAPI → Database
FastAPI → BinanceDataCollector (real-time price)
FastAPI → AnalysisEngine (signals)
FastAPI → PortfolioManager (portfolio)
```

---

## 🚀 Running the Application

### Development Mode
```bash
cd backend
python api/main.py
```

### Production Mode
```bash
cd backend
uvicorn api.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Testing
```bash
cd backend
pytest tests/ -v
```

---

## 📊 Monitoring

### Logs
```bash
# API logs
tail -f logs/api.log

# Binance collector logs
tail -f logs/binance_ws.log

# News scraper logs
tail -f logs/news_scraper.log
```

### Database
```bash
# Using SQLite browser
sqlitebrowser database/trading_data.db

# Or using command line
sqlite3 database/trading_data.db
> SELECT * FROM ohlcv_data LIMIT 10;
```

### System Status
```bash
curl http://localhost:8000/status
```

---

## 🎯 Next Steps (Phase 2)

### Modul yang Akan Diimplementasi:

1. **Analysis Engine** (`backend/analysis/`)
   - `technical_indicators.py` - RSI, MACD, EMA, Bollinger Bands
   - `sentiment_analysis.py` - News sentiment aggregation
   - `signal_generator.py` - Trading signal generation

2. **Paper Trading** (`backend/paper_trading/`)
   - `portfolio_manager.py` - Virtual portfolio management
   - `order_executor.py` - Simulated order execution
   - `risk_manager.py` - Stop-loss, position sizing

3. **XAI Module** (`backend/xai/`)
   - `explanation_generator.py` - Human-readable explanations
   - `chat_agent.py` - Interactive chat interface

---

## 📚 Resources

### Documentation
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://docs.sqlalchemy.org/)
- [CCXT](https://docs.ccxt.com/)
- [Hugging Face Transformers](https://huggingface.co/docs/transformers)

### Tutorials
- [Python Asyncio](https://realpython.com/async-io-python/)
- [WebSocket Tutorial](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)
- [REST API Design](https://restfulapi.net/)

---

**Happy Coding! 💻🚀**
