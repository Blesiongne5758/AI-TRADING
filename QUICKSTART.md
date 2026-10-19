# 🚀 Quick Start Guide - AI Trading Agent

Panduan cepat untuk memulai AI Trading Agent dalam 5 menit!

## 📋 Prerequisites

Sebelum mulai, pastikan Anda sudah install:
- ✅ Python 3.11 atau lebih baru
- ✅ Git
- ✅ Text editor (VS Code recommended)

## 🎯 Langkah 1: Clone & Setup (2 menit)

```bash
# 1. Clone repository
git clone https://github.com/yourusername/ai-trading-agent.git
cd ai-trading-agent

# 2. Buat virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 4. Install dependencies
cd backend
pip install -r requirements.txt
```

## 🔑 Langkah 2: Dapatkan Binance API Keys (1 menit)

1. Buka https://testnet.binance.vision/
2. Login dengan GitHub account
3. Klik "Generate HMAC_SHA256 Key"
4. Copy API Key dan Secret Key

## ⚙️ Langkah 3: Konfigurasi (1 menit)

```bash
# 1. Copy file konfigurasi
cp .env.example .env

# 2. Edit file .env dengan text editor
# Isi API keys yang sudah didapat:
```

**Isi file `.env`:**
```env
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here
BINANCE_TESTNET=true  # PENTING: true untuk testnet!
```

## ▶️ Langkah 4: Jalankan Aplikasi (30 detik)

```bash
# Pastikan masih di folder backend
python api/main.py
```

**Anda akan melihat output seperti ini:**
```
2024-01-15 10:00:00 | INFO     | Starting AI Trading Agent v1.0.0
2024-01-15 10:00:01 | INFO     | Database initialized successfully
2024-01-15 10:00:02 | INFO     | Exchange initialized successfully
2024-01-15 10:00:03 | INFO     | Application started successfully
2024-01-15 10:00:03 | INFO     | Uvicorn running on http://0.0.0.0:8000
```

## 🎉 Langkah 5: Test Aplikasi (30 detik)

Buka browser dan kunjungi:

### 1. API Documentation (Swagger UI)
```
http://localhost:8000/docs
```
Anda bisa test semua API endpoints langsung dari sini!

### 2. Test Health Check
```bash
curl http://localhost:8000/health
```

**Expected response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:00:00"
}
```

### 3. Test Get Price
```bash
curl http://localhost:8000/price/BTC/USDT
```

**Expected response:**
```json
{
  "symbol": "BTC/USDT",
  "price": 42300.75,
  "timestamp": "2024-01-15T10:00:00"
}
```

### 4. Test Get OHLCV Data
```bash
curl "http://localhost:8000/ohlcv/BTC/USDT/1h?limit=10"
```

**Expected response:**
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

## 📊 Apa yang Terjadi di Background?

Saat aplikasi berjalan, sistem otomatis:

1. **Mengambil data historis** - 500 candle terakhir untuk setiap symbol/timeframe
2. **Mulai real-time collection** - WebSocket ke Binance untuk data live
3. **Fetch berita** - Dari CoinDesk, CoinTelegraph, dll setiap 15 menit
4. **Analisis sentimen** - Menggunakan FinBERT AI untuk setiap berita
5. **Simpan ke database** - Semua data tersimpan di SQLite

## 🔍 Monitoring

### Check Logs
```bash
# Lihat log real-time
tail -f logs/api.log

# Atau lihat log Binance collector
tail -f logs/binance_ws.log

# Atau lihat log news scraper
tail -f logs/news_scraper.log
```

### Check Database
```bash
# Install SQLite browser (opsional)
# Windows: Download dari https://sqlitebrowser.org/
# macOS: brew install --cask sqlitebrowser
# Linux: sudo apt install sqlitebrowser

# Buka database
sqlitebrowser database/trading_data.db
```

### Check System Status
```bash
curl http://localhost:8000/status
```

## 🛑 Stop Aplikasi

Tekan `Ctrl + C` di terminal untuk stop aplikasi.

## 🔄 Restart Aplikasi

```bash
python api/main.py
```

## ❓ Troubleshooting Cepat

### Error: "Port 8000 already in use"
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:8000 | xargs kill -9
```

### Error: "ModuleNotFoundError"
```bash
# Pastikan virtual environment aktif
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Error: "Binance API key invalid"
- Pastikan API key dan secret sudah benar di `.env`
- Pastikan `BINANCE_TESTNET=true` untuk testnet
- Regenerate API keys dari https://testnet.binance.vision/

### Data OHLCV kosong
- Tunggu 1-2 menit untuk data terkumpul
- Check log: `tail -f logs/api.log`
- Pastikan koneksi internet stabil

## 📚 Next Steps

Setelah aplikasi berjalan, Anda bisa:

1. **Explore API Documentation** - http://localhost:8000/docs
2. **Read Full Documentation** - Lihat README.md
3. **Check Database** - Lihat data yang tersimpan
4. **Modify Configuration** - Edit `.env` untuk custom settings
5. **Run Frontend** - Setup React dashboard (opsional)

## 🎓 Belajar Lebih Lanjut

### Konsep yang Dipelajari:
- ✅ WebSocket untuk real-time data
- ✅ REST API dengan FastAPI
- ✅ Database dengan SQLAlchemy
- ✅ Async/await untuk concurrent operations
- ✅ Sentiment analysis dengan AI
- ✅ Error handling dan logging

### File-file Penting:
- `backend/config.py` - Konfigurasi aplikasi
- `backend/database.py` - Database models
- `backend/data_collector/binance_ws.py` - Binance WebSocket
- `backend/data_collector/news_scraper.py` - News scraper
- `backend/api/main.py` - FastAPI application

## 🆘 Butuh Bantuan?

1. Check README.md untuk dokumentasi lengkap
2. Check logs di folder `logs/`
3. Buka issue di GitHub
4. Tanya di community forum

## 🎉 Selamat!

Anda sudah berhasil menjalankan AI Trading Agent! 🚀

Next step: Lanjut ke Phase 2 untuk implementasi Analysis Engine dan Paper Trading.

---

**Happy Coding! 💻📈**
