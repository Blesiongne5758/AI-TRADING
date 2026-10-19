# 🚀 Quick Start - AI Trading Agent

Panduan cepat untuk menjalankan AI Trading Agent dalam 5 menit!

## 📋 Langkah-langkah

### 1. Install Dependencies (1 menit)

```bash
cd backend
pip install -r requirements.txt
```

### 2. Setup Environment (1 menit)

```bash
# Copy template konfigurasi
cp .env.example .env

# Edit file .env dengan API keys Anda
# Dapatkan dari: https://testnet.binance.vision/
```

**Isi minimal:**
```env
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here
BINANCE_TESTNET=true
```

### 3. Jalankan Aplikasi (30 detik)

```bash
cd backend
python -m data_collector.main_collector
```

### 4. Selesai! 🎉

Aplikasi akan:
- ✅ Connect ke Binance WebSocket
- ✅ Fetch historical data (500 candles per symbol/timeframe)
- ✅ Start real-time data collection
- ✅ Fetch news setiap 15 menit
- ✅ Analyze sentiment dengan FinBERT
- ✅ Simpan semua data ke database

## 📊 Check Progress

### Lihat Logs
```bash
tail -f logs/main_collector.log
```

### Check Database
```bash
sqlitebrowser database/trading_data.db
```

### Stop Aplikasi
Tekan `Ctrl + C`

## ❓ Troubleshooting

### Error: "BINANCE_API_KEY required"
- Pastikan API keys sudah diisi di `.env`
- Gunakan testnet: `BINANCE_TESTNET=true`

### Error: "ModuleNotFoundError"
```bash
# Pastikan virtual environment aktif
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Data kosong
- Tunggu 1-2 menit untuk data terkumpul
- Check logs: `tail -f logs/main_collector.log`

## 📚 Dokumentasi Lengkap

Lihat `README.md` untuk dokumentasi lengkap.

---

**Happy Trading! 🚀📈**
