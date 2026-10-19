# 🤖 AI Trading Agent

Sistem trading otomatis berbasis AI yang dirancang khusus untuk **pemula** agar bisa belajar, meriset, dan memahami pasar crypto dengan aman melalui paper trading.

## 📋 Daftar Isi

- [Fitur Utama](#fitur-utama)
- [Arsitektur Sistem](#arsitektur-sistem)
- [Struktur Folder](#struktur-folder)
- [Persiapan](#persiapan)
- [Instalasi](#instalasi)
- [Konfigurasi](#konfigurasi)
- [Menjalankan Aplikasi](#menjalankan-aplikasi)
- [Penjelasan Modul](#penjelasan-modul)
- [Troubleshooting](#troubleshooting)

---

## ✨ Fitur Utama

### ✅ Phase 1: Data Collection (COMPLETE)

- [x] **Koneksi Real-time ke Binance** - Data harga live dari 5 simbol (BTC, ETH, SOL, BNB, XRP)
- [x] **6 Timeframes** - 1m, 5m, 15m, 1h, 4h, 1d
- [x] **Analisis Sentimen** - FinBERT AI untuk analisis berita dari 3 sumber
- [x] **Database SQLite** - Penyimpanan data OHLCV dan berita
- [x] **Auto-reconnect** - Koneksi otomatis jika terputus
- [x] **Logging** - Comprehensive logging untuk debugging

### ⏳ Phase 2: Analysis & Trading (TODO)

- [ ] **5 Indikator Teknikal** - RSI, MACD, EMA, Bollinger Bands, Volume
- [ ] **Signal Generation** - BUY/SELL/HOLD dengan confidence score
- [ ] **Paper Trading** - Simulasi trading dengan virtual balance $10,000
- [ ] **Risk Management** - Stop-loss otomatis dan position sizing
- [ ] **XAI Module** - Explainable AI untuk menjelaskan keputusan bot
- [ ] **Notifikasi Telegram** - Alert untuk setiap trade

---

## 🏗️ Arsitektur Sistem

```
┌─────────────────────────────────────────────────────────────┐
│                    DATA COLLECTOR MODULE                     │
│                                                              │
│  ┌──────────────┐         ┌──────────────┐                 │
│  │   Binance    │         │     News     │                 │
│  │  WebSocket   │         │   Scraper    │                 │
│  │              │         │  + FinBERT   │                 │
│  └──────┬───────┘         └──────┬───────┘                 │
│         │                        │                          │
│         └────────┬───────────────┘                          │
│                  │                                          │
│         ┌────────▼────────┐                                 │
│         │    Database     │                                 │
│         │    (SQLite)     │                                 │
│         └─────────────────┘                                 │
│                                                              │
│  main_collector.py ← Entry Point                            │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Struktur Folder

```
ai-trading-agent/
├── backend/
│   ├── data_collector/              # Modul utama
│   │   ├── __init__.py              # Package marker
│   │   ├── config.py                # Konfigurasi global
│   │   ├── database.py              # Database setup & operations
│   │   ├── binance_ws.py            # Binance WebSocket
│   │   ├── news_scraper.py          # News scraper + sentiment
│   │   └── main_collector.py        # Entry point
│   └── requirements.txt             # Python dependencies
├── database/                        # SQLite database (auto-created)
│   └── trading_data.db
├── logs/                            # Log files (auto-created)
│   ├── main_collector.log
│   ├── binance_ws.log
│   └── news_scraper.log
├── .env                             # Environment variables (create from .env.example)
├── .env.example                     # Template konfigurasi
├── README.md                        # Dokumentasi ini
└── .gitignore                       # Git ignore rules
```

---

## 📦 Persiapan

### Kebutuhan Sistem

- **Python 3.11+** - [Download Python](https://www.python.org/downloads/)
- **Git** - [Download Git](https://git-scm.com/downloads)

### Instalasi TA-Lib (Opsional)

TA-Lib diperlukan untuk Phase 2 (indikator teknikal). Untuk Phase 1, tidak diperlukan.

**Windows:**
```bash
# Download dari: https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib
pip install TA_Lib‑0.4.28‑cp311‑cp311‑win_amd64.whl
```

**macOS:**
```bash
brew install ta-lib
pip install ta-lib
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install -y build-essential wget
wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
tar -xzf ta-lib-0.4.0-src.tar.gz
cd ta-lib/
./configure --prefix=/usr
make
sudo make install
pip install ta-lib
```

---

## 🚀 Instalasi

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/ai-trading-agent.git
cd ai-trading-agent
```

### 2. Buat Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

**Dependencies yang diinstall:**
- `ccxt` - Library untuk koneksi ke Binance
- `websockets` - WebSocket client
- `aiohttp` - Async HTTP client
- `pandas` - Data processing
- `numpy` - Numerical computing
- `feedparser` - RSS feed parser
- `aiosqlite` - Async SQLite (database)
- `python-dotenv` - Environment variables
- `loguru` - Logging

**Note:** Library untuk sentiment analysis (`transformers`, `torch`) akan diinstall di Phase 2.

### 4. Setup Database

```bash
# Buat folder database dan logs
mkdir database
mkdir logs

# Database akan otomatis dibuat saat aplikasi pertama kali dijalankan
```

### 5. Konfigurasi Environment

```bash
# Copy file .env.example ke .env
cp .env.example .env

# Edit file .env dengan text editor
# Isi API keys dan konfigurasi lainnya
```

---

## ⚙️ Konfigurasi

### File `.env`

Buka file `.env` dan isi konfigurasi berikut:

#### Binance API Keys (WAJIB)

```env
# Untuk testing, gunakan testnet (aman, tidak pakai uang asli)
BINANCE_TESTNET=true

# Dapatkan API keys dari:
# Testnet: https://testnet.binance.vision/
# Mainnet: https://www.binance.com/en/my/settings/api-management

BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here
```

**Cara mendapatkan API keys:**
1. Buka https://testnet.binance.vision/
2. Register dengan GitHub account
3. Generate API keys
4. Copy dan paste ke file `.env`

#### Telegram Bot (OPSIONAL)

```env
# Buat bot via @BotFather di Telegram
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz

# Dapatkan chat ID via @userinfobot
TELEGRAM_CHAT_ID=123456789
```

#### Trading Settings

```env
# Paper trading (simulasi, tidak pakai uang asli)
PAPER_TRADING=true

# Saldo awal virtual
INITIAL_BALANCE=10000.0

# Risk management
MAX_RISK_PER_TRADE=0.02  # 2% dari portfolio per trade
MAX_OPEN_POSITIONS=5     # Maksimum 5 posisi terbuka
STOP_LOSS_PERCENT=0.02   # Stop loss 2%
TAKE_PROFIT_PERCENT=0.05 # Take profit 5%

# Minimum confidence untuk trade
MIN_CONFIDENCE_THRESHOLD=0.60  # 60%
```

---

## ▶️ Menjalankan Aplikasi

### 1. Jalankan Data Collector

```bash
cd backend
python -m data_collector.main_collector
```

**Output yang diharapkan:**
```
2024-01-15 10:00:00 | INFO     | AI Trading Agent - Data Collector
2024-01-15 10:00:01 | INFO     | Configuration validated successfully
2024-01-15 10:00:02 | INFO     | Initializing collectors...
2024-01-15 10:00:03 | INFO     | Database initialized successfully
2024-01-15 10:00:04 | INFO     | Exchange initialized successfully
2024-01-15 10:00:05 | INFO     | Sentiment model loaded successfully
2024-01-15 10:00:06 | INFO     | Fetching initial historical data...
2024-01-15 10:00:07 | INFO     | Fetched 500 candles for BTC/USDT 1m
2024-01-15 10:00:08 | INFO     | All collectors running. Press Ctrl+C to stop.
```

### 2. Check Logs

```bash
# Lihat log real-time
tail -f logs/main_collector.log

# Atau lihat log individual
tail -f logs/binance_ws.log
tail -f logs/news_scraper.log
```

### 3. Check Database

```bash
# Install SQLite browser (opsional)
# Windows: Download dari https://sqlitebrowser.org/
# macOS: brew install --cask sqlitebrowser
# Linux: sudo apt install sqlitebrowser

# Buka database
sqlitebrowser database/trading_data.db
```

### 4. Stop Aplikasi

Tekan `Ctrl + C` untuk stop aplikasi dengan graceful shutdown.

---

## 📖 Penjelasan Modul

### 1. `config.py` - Konfigurasi Global

**Fungsi:** Menyimpan semua konfigurasi aplikasi

**Isi:**
- Application settings (name, version, debug mode)
- Binance API settings (keys, symbols, timeframes)
- Database settings (SQLite path)
- Telegram bot settings
- Trading settings (risk management)
- Analysis settings (indicators parameters)

**Cara penggunaan:**
```python
from data_collector.config import settings

print(settings.BINANCE_API_KEY)
print(settings.TRADING_SYMBOLS)
```

**Untuk pemula:**
- Menggunakan `pydantic-settings` untuk validasi
- Semua values bisa di-override via `.env` file
- Type hints untuk autocomplete di IDE

---

### 2. `database.py` - Database Operations

**Fungsi:** Mengelola database SQLite

**Isi:**
- Database models (tables):
  - `OHLCVData` - Candlestick data
  - `NewsData` - News with sentiment
  - `TradingSignal` - Bot signals
- Database initialization
- CRUD operations (save, get, update, delete)
- Async session management

**Cara penggunaan:**
```python
from data_collector.database import (
    init_db, save_ohlcv_data, get_ohlcv_data
)

# Initialize database
await init_db()

# Save data
await save_ohlcv_data("BTC/USDT", "1h", [candle_data])

# Get data
data = await get_ohlcv_data("BTC/USDT", "1h", limit=100)
```

**Untuk pemula:**
- ORM = Object-Relational Mapping
- Kita kerja dengan Python objects, bukan SQL queries
- Async/await untuk non-blocking operations

---

### 3. `binance_ws.py` - Binance WebSocket

**Fungsi:** Mengambil data harga real-time dari Binance

**Cara kerja:**
1. Connect ke Binance WebSocket
2. Subscribe ke candlestick streams
3. Terima data setiap ada candle baru
4. Simpan ke database

**Contoh data yang dikumpulkan:**
```python
{
    "symbol": "BTC/USDT",
    "timeframe": "1h",
    "timestamp": 1642684522,
    "open": 42000.50,
    "high": 42500.00,
    "low": 41800.00,
    "close": 42300.75,
    "volume": 1234.56
}
```

**Untuk pemula:**
- OHLCV = Open, High, Low, Close, Volume
- Ini adalah data dasar untuk analisis teknikal
- Setiap candle mewakili 1 periode waktu (1 menit, 1 jam, 1 hari, dll)

---

### 4. `news_scraper.py` - News Scraper & Sentiment

**Fungsi:** Mengambil berita crypto dan menganalisis sentimen

**Cara kerja:**
1. Fetch RSS feeds dari CoinDesk, CoinTelegraph, dll
2. Parse berita (title, summary, date)
3. Analisis sentimen dengan FinBERT AI
4. Simpan ke database dengan sentiment score

**Sentiment Score:**
- `+1.0` = Sangat bullish (positif untuk harga)
- `0.0` = Netral
- `-1.0` = Sangat bearish (negatif untuk harga)

**Contoh:**
```python
# Berita: "Bitcoin reaches new all-time high"
{
    "title": "Bitcoin reaches new all-time high",
    "sentiment_score": 0.85,
    "sentiment_label": "bullish"
}

# Berita: "SEC bans cryptocurrency trading"
{
    "title": "SEC bans cryptocurrency trading",
    "sentiment_score": -0.92,
    "sentiment_label": "bearish"
}
```

**Untuk pemula:**
- FinBERT adalah AI yang dilatih khusus untuk financial text
- Sentimen berita mempengaruhi keputusan trading bot
- Berita positif → bot lebih cenderung BUY
- Berita negatif → bot lebih cenderung SELL

---

### 5. `main_collector.py` - Entry Point

**Fungsi:** Menjalankan semua collectors secara bersamaan

**Cara kerja:**
1. Initialize database
2. Initialize Binance collector
3. Initialize news scraper
4. Fetch initial historical data
5. Start real-time data collection
6. Start news scraping (setiap 15 menit)

**Untuk pemula:**
- Ini adalah file yang pertama kali dijalankan
- Menggunakan asyncio untuk menjalankan multiple tasks sekaligus
- Graceful shutdown saat menerima Ctrl+C

---

## 🔧 Troubleshooting

### Error: "BINANCE_API_KEY required"

**Solusi:**
- Pastikan API key dan secret sudah benar di file `.env`
- Untuk testing, gunakan testnet: `BINANCE_TESTNET=true`
- Dapatkan API keys dari https://testnet.binance.vision/

### Error: "Database locked"

**Solusi:**
- SQLite tidak mendukung concurrent writes yang tinggi
- Tutup semua koneksi ke database sebelum menjalankan ulang
- Untuk production, gunakan PostgreSQL

### Error: "Port already in use"

**Solusi:**
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:8000 | xargs kill -9
```

### Aplikasi lambat startup

**Solusi:**
- FinBERT model download pertama kali (~440MB)
- Tunggu sampai download selesai
- Model akan di-cache untuk startup berikutnya

### Data OHLCV kosong

**Solusi:**
- Tunggu beberapa menit untuk data terkumpul
- Check log: `logs/main_collector.log`
- Pastikan koneksi internet stabil
- Verify Binance API keys valid

### ModuleNotFoundError

**Solusi:**
```bash
# Pastikan virtual environment aktif
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

---

## 📊 Data yang Dikumpulkan

### OHLCV Data
- **5 symbols**: BTC/USDT, ETH/USDT, SOL/USDT, BNB/USDT, XRP/USDT
- **6 timeframes**: 1m, 5m, 15m, 1h, 4h, 1d
- **500 candles per symbol/timeframe** (historical)
- **Real-time updates** via WebSocket

### News Data
- **3 sources**: CoinDesk, CoinTelegraph, CryptoNews
- **Fetch interval**: Setiap 15 menit
- **Sentiment analysis**: FinBERT AI
- **Deduplication**: Mencegah berita duplikat

---

## 🎓 Learning Points untuk Pemula

### Konsep yang Dipelajari:
1. **Async/Await** - Non-blocking operations
2. **WebSocket** - Real-time data streaming
3. **ORM** - Database abstraction
4. **Sentiment Analysis** - NLP dengan AI
5. **Error Handling** - Robust code
6. **Logging** - Debugging & monitoring
7. **Configuration Management** - Environment variables

### Best Practices yang Diterapkan:
1. Type hints untuk type safety
2. Docstrings untuk documentation
3. Modular code structure
4. Separation of concerns
5. Error handling
6. Logging
7. Configuration management

---

## 📚 Resources

### Dokumentasi
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [CCXT Documentation](https://docs.ccxt.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Hugging Face Transformers](https://huggingface.co/docs/transformers)

### Tutorial
- [Python Asyncio Tutorial](https://realpython.com/async-io-python/)
- [WebSocket Tutorial](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)

### Trading
- [Binance API Documentation](https://binance-docs.github.io/apidocs/)
- [Technical Analysis Library](https://github.com/bukosabino/ta)
- [FinBERT Model](https://huggingface.co/ProsusAI/finbert)

---

## 🎯 Next Steps (Phase 2)

### Yang Akan Diimplementasi:

1. **Analysis Engine**
   - Technical indicators (RSI, MACD, EMA, Bollinger Bands)
   - Sentiment aggregation
   - Signal generation

2. **Paper Trading Engine**
   - Portfolio management
   - Order execution simulation
   - Risk management

3. **XAI Module**
   - Explanation generation
   - Chat interface

4. **Telegram Notifications**
   - Trade alerts
   - Daily reports

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📄 License

This project is licensed under the MIT License.

---

## ⚠️ Disclaimer

**PENTING:**
- Ini adalah proyek edukasi dan research
- Paper trading menggunakan uang virtual
- Trading crypto memiliki risiko tinggi
- Jangan invest uang yang tidak siap Anda rugikan
- Past performance ≠ future results
- Selalu lakukan riset sendiri (DYOR)

---

## 📞 Support

Untuk pertanyaan dan support:
- Buka issue di GitHub
- Email: your.email@example.com
- Telegram: @yourusername

---

**Happy Trading! 🚀📈**
