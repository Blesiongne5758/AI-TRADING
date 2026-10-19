# 🤖 AI Trading Agent

Sistem trading otomatis berbasis AI yang dirancang khusus untuk **pemula** agar bisa belajar, meriset, dan memahami pasar crypto dengan aman melalui paper trading.

## 📋 Daftar Isi

- [Fitur Utama](#fitur-utama)
- [Arsitektur Sistem](#arsitektur-sistem)
- [Persiapan](#persiapan)
- [Instalasi](#instalasi)
- [Konfigurasi](#konfigurasi)
- [Menjalankan Aplikasi](#menjalankan-aplikasi)
- [Penjelasan Modul](#penjelasan-modul)
- [API Documentation](#api-documentation)
- [Troubleshooting](#troubleshooting)

---

## ✨ Fitur Utama

### ✅ MVP (Minimum Viable Product)

- [x] **Koneksi Real-time ke Binance** - Data harga live dari 5 simbol (BTC, ETH, SOL, BNB, XRP)
- [x] **5 Indikator Teknikal** - RSI, MACD, EMA, Bollinger Bands, Volume Analysis
- [x] **Analisis Sentimen** - FinBERT AI untuk analisis berita dari 3 sumber
- [x] **Paper Trading** - Simulasi trading dengan virtual balance $10,000
- [x] **Dashboard Interaktif** - Chart, portfolio overview, dan analytics
- [x] **Decision Log** - Semua keputusan bot dengan penjelasan lengkap
- [x] **Risk Management** - Stop-loss otomatis dan position sizing
- [x] **Notifikasi Telegram** - Alert untuk setiap trade

### 🎁 Bonus Features

- [ ] Backtesting Engine - Uji strategi dengan data historis
- [ ] Multi-timeframe Analysis - Analisis dari berbagai timeframe
- [ ] Alert System - Notifikasi kondisi market ekstrem

---

## 🏗️ Arsitektur Sistem

```
┌─────────────────────────────────────────────────────────────┐
│                         FRONTEND                             │
│              React + Tailwind CSS + TradingView              │
└────────────────────────┬────────────────────────────────────┘
                         │ REST API
┌────────────────────────▼────────────────────────────────────┐
│                      FASTAPI SERVER                          │
│                    (api/main.py)                             │
└──┬──────────┬──────────┬──────────┬──────────┬─────────────┘
   │          │          │          │          │
   ▼          ▼          ▼          ▼          ▼
┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────────┐
│Data  │  │Anal- │  │Paper │  │ XAI  │  │ Telegram │
│Col-  │  │ysis  │  │Trad- │  │Module│  │   Bot    │
│lector│  │Engine│  │ing   │  │      │  │          │
└──┬───┘  └──┬───┘  └──┬───┘  └──┬───┘  └──────────┘
   │         │         │         │
   ▼         ▼         ▼         ▼
┌──────────────────────────────────────────────────────────┐
│                    SQLite Database                        │
│              (trading_data.db)                            │
└──────────────────────────────────────────────────────────┘
```

### Penjelasan Arsitektur

1. **Frontend (React)** - User interface untuk monitoring dan kontrol
2. **FastAPI Server** - Backend API yang menghubungkan semua modul
3. **Data Collector** - Mengambil data dari Binance dan news sources
4. **Analysis Engine** - Menghitung indikator teknikal dan sentimen
5. **Paper Trading** - Simulasi trading dengan uang virtual
6. **XAI Module** - Explainable AI untuk menjelaskan keputusan bot
7. **Telegram Bot** - Notifikasi real-time ke user
8. **Database** - Penyimpanan semua data (OHLCV, news, trades, signals)

---

## 📦 Persiapan

### Kebutuhan Sistem

- **Python 3.11+** - [Download Python](https://www.python.org/downloads/)
- **Git** - [Download Git](https://git-scm.com/downloads)
- **TA-Lib** (opsional) - Library untuk indikator teknikal

### Instalasi TA-Lib (Opsional)

**Windows:**
```bash
# Download dari: https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib
# Install wheel file:
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

**Catatan:** Jika TA-Lib tidak bisa diinstall, sistem akan otomatis menggunakan `pandas-ta` sebagai alternatif.

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

### 4. Setup Database

```bash
# Buat folder database
mkdir database

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

**Cara membuat Telegram bot:**
1. Buka Telegram, cari @BotFather
2. Kirim `/newbot` dan ikuti instruksi
3. Copy token yang diberikan
4. Cari @userinfobot untuk mendapatkan chat ID Anda

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

### 1. Jalankan Backend

```bash
cd backend
python api/main.py
```

Atau dengan uvicorn:

```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

**Output yang diharapkan:**
```
2024-01-15 10:00:00 | INFO     | Starting AI Trading Agent v1.0.0
2024-01-15 10:00:01 | INFO     | Initializing database...
2024-01-15 10:00:01 | INFO     | Database initialized successfully
2024-01-15 10:00:02 | INFO     | Initializing Binance data collector...
2024-01-15 10:00:03 | INFO     | Exchange initialized successfully
2024-01-15 10:00:04 | INFO     | Starting background tasks...
2024-01-15 10:00:05 | INFO     | Application started successfully
2024-01-15 10:00:05 | INFO     | Uvicorn running on http://0.0.0.0:8000
```

### 2. Akses API Documentation

Buka browser dan kunjungi:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 3. Test API Endpoints

```bash
# Health check
curl http://localhost:8000/health

# Get system status
curl http://localhost:8000/status

# Get OHLCV data
curl http://localhost:8000/ohlcv/BTC/USDT/1h?limit=100

# Get recent news
curl http://localhost:8000/news?limit=10

# Get current price
curl http://localhost:8000/price/BTC/USDT
```

### 4. Jalankan Frontend (Opsional)

```bash
cd frontend
npm install
npm run dev
```

Buka http://localhost:5173 di browser.

---

## 📖 Penjelasan Modul

### 1. Data Collector (`backend/data_collector/`)

#### `binance_ws.py` - Binance WebSocket

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

#### `news_scraper.py` - News Scraper & Sentiment Analysis

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

### 2. Analysis Engine (`backend/analysis/`)

*Modul ini akan diimplementasi di Fase 2*

**Fungsi:**
- Menghitung indikator teknikal (RSI, MACD, EMA, dll)
- Menggabungkan analisis teknikal + sentimen
- Menghasilkan trading signals

**Indikator Teknikal:**

#### RSI (Relative Strength Index)
- Mengukur momentum harga
- Range: 0-100
- > 70 = Overbought (potensi turun)
- < 30 = Oversold (potensi naik)

#### MACD (Moving Average Convergence Divergence)
- Mengukur trend dan momentum
- Terdiri dari MACD line, signal line, histogram
- Crossover = sinyal beli/jual

#### EMA (Exponential Moving Average)
- Rata-rata harga dengan bobot lebih ke data terbaru
- EMA 20, 50, 200 untuk short/mid/long term
- Golden cross = EMA pendek memotong ke atas EMA panjang

---

### 3. Paper Trading (`backend/paper_trading/`)

*Modul ini akan diimplementasi di Fase 2*

**Fungsi:**
- Simulasi trading dengan uang virtual
- Mengelola portfolio
- Menghitung P&L (Profit & Loss)
- Risk management (stop-loss, position sizing)

**Konsep:**
- Initial balance: $10,000 USDT
- Max risk per trade: 2% ($200)
- Stop-loss: Otomatis cut loss jika rugi 2%
- Take-profit: Otomatis ambil profit jika untung 5%

---

### 4. XAI Module (`backend/xai/`)

*Modul ini akan diimplementasi di Fase 2*

**Fungsi:**
- Menjelaskan keputusan bot dalam bahasa manusia
- Chat interface untuk tanya jawab
- Educational content untuk pemula

**Contoh output:**
```
Bot merekomendasikan BUY BTC/USDT karena:
1. RSI menunjukkan oversold (28) - potensi rebound
2. Golden cross pada EMA 20/50 - trend bullish
3. Sentimen berita positif (+0.65) - adopsi institusi
4. Volume meningkat 45% - konfirmasi momentum

Confidence: 78%
Risk: 2% ($200)
Stop-loss: $65,900
Take-profit: $71,000
```

---

## 📡 API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints

#### Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:00:00"
}
```

#### System Status
```http
GET /status
```

**Response:**
```json
{
  "status": "running",
  "version": "1.0.0",
  "timestamp": "2024-01-15T10:00:00",
  "services": {
    "binance_collector": {
      "running": true,
      "symbols": ["BTC/USDT", "ETH/USDT"],
      "messages_received": 1234
    },
    "news_scraper": {
      "running": true,
      "news_fetched": 567,
      "news_saved": 560
    }
  }
}
```

#### Get OHLCV Data
```http
GET /ohlcv/{symbol}/{timeframe}?limit=500
```

**Parameters:**
- `symbol`: Trading pair (e.g., "BTC/USDT")
- `timeframe`: Time interval (e.g., "1h", "1d")
- `limit`: Number of candles (default 500, max 1000)

**Response:**
```json
[
  {
    "timestamp": 1642684522,
    "open": 42000.50,
    "high": 42500.00,
    "low": 41800.00,
    "close": 42300.75,
    "volume": 1234.56
  }
]
```

#### Get News
```http
GET /news?limit=50&hours=24
```

**Parameters:**
- `limit`: Number of news items (default 50)
- `hours`: Time range in hours (default 24)

**Response:**
```json
[
  {
    "id": 1,
    "title": "Bitcoin reaches new all-time high",
    "source": "CoinDesk",
    "url": "https://coindesk.com/...",
    "published_at": "2024-01-15T10:00:00",
    "summary": "Bitcoin price surged...",
    "sentiment_score": 0.85,
    "sentiment_label": "bullish"
  }
]
```

#### Get Current Price
```http
GET /price/{symbol}
```

**Response:**
```json
{
  "symbol": "BTC/USDT",
  "price": 42300.75,
  "timestamp": "2024-01-15T10:00:00"
}
```

---

## 🔧 Troubleshooting

### Error: "TA-Lib not found"

**Solusi:**
- Install TA-Lib C library (lihat bagian Persiapan)
- Atau gunakan pandas-ta sebagai alternatif (sudah termasuk di requirements.txt)

### Error: "Binance API key invalid"

**Solusi:**
- Pastikan API key dan secret sudah benar di file `.env`
- Untuk testing, gunakan testnet: `BINANCE_TESTNET=true`
- Dapatkan API keys dari https://testnet.binance.vision/

### Error: "Database locked"

**Solusi:**
- SQLite tidak mendukung concurrent writes yang tinggi
- Untuk production, gunakan PostgreSQL
- Atau tutup semua koneksi ke database sebelum menjalankan ulang

### Error: "Port 8000 already in use"

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
- Check log: `logs/api.log`
- Pastikan koneksi internet stabil
- Verify Binance API keys valid

---

## 📚 Resources

### Dokumentasi

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [CCXT Documentation](https://docs.ccxt.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Hugging Face Transformers](https://huggingface.co/docs/transformers)

### Trading

- [Binance API Documentation](https://binance-docs.github.io/apidocs/)
- [Technical Analysis Library](https://github.com/bukosabino/ta)
- [FinBERT Model](https://huggingface.co/ProsusAI/finbert)

### Tutorial

- [Python Asyncio Tutorial](https://realpython.com/async-io-python/)
- [WebSocket Tutorial](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)
- [REST API Design](https://restfulapi.net/)

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
