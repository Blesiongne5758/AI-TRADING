# 🚀 Quick Reference Guide - AI Trading Agent

Panduan cepat untuk memulai dan menggunakan AI Trading Agent.

---

## 📦 Instalasi (5 Menit)

### 1. Setup Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 2. Install Dependencies
```bash
cd backend

# Opsi A: Script otomatis (recommended)
./setup.sh              # Linux/Mac
setup.bat               # Windows

# Opsi B: Manual
pip install -r requirements.txt
python -m textblob.download_corpora
```

### 3. Setup Environment
```bash
cp .env.example .env
# Edit .env dengan API keys dari https://testnet.binance.vision/
```

### 4. Verify Installation
```bash
python test_dependencies.py
```

---

## ▶️ Menjalankan Aplikasi

### Terminal 1: Data Collector
```bash
cd backend
python -m data_collector.main_collector
```

**Output yang diharapkan:**
```
🚀 Starting AI Trading Agent - Data Collector Service
✅ Database initialized at database/trading_data.db
🧪 Menggunakan Binance TESTNET (aman untuk testing)
✅ Connected to Binance. Markets loaded: 2150
📊 Fetching historical candles...
✅ BTC/USDT [1m]: 500 candles loaded
✅ BTC/USDT [5m]: 500 candles loaded
...
🔄 Starting real-time ticker loop...
💹 BTC/USDT: $67,234.50 (+2.34%)
📰 Fetching news from all sources...
📰 CoinDesk: 20 articles
📰 CoinTelegraph: 20 articles
📰 Decrypt: 20 articles
```

### Terminal 2: Analysis Engine
```bash
cd backend
python -m analysis.main_analysis
```

**Output yang diharapkan:**
```
🔍 Analyzing BTC/USDT [1h]
📊 Loaded 500 candles dan 60 news articles

📈 SIGNAL: BUY
🎯 Confidence: 75%
💰 Current Price: $67,234.50

📋 Reasons:
   1. Strong buy signal (score: +0.65)
   2. RSI oversold (28.5)
   3. MACD bullish crossover
   4. EMA alignment bullish
   5. News sentiment bullish (+0.72)

🛡️  Risk Management:
   Stop Loss: $65,889.81
   Take Profit: $70,596.23
   Risk/Reward Ratio: 2.50
   Position Size: 10.0% of portfolio
```

---

## 📊 Struktur Project

```
ai-trading-agent/
├── backend/
│   ├── data_collector/          # Fase 1: Data Collection
│   │   ├── config.py            # Konfigurasi
│   │   ├── database.py          # Database manager
│   │   ├── binance_ws.py        # Binance collector
│   │   ├── news_scraper.py      # News scraper
│   │   └── main_collector.py    # Entry point
│   │
│   ├── analysis/                # Fase 2: Analysis Engine
│   │   ├── technical_indicators.py  # RSI, MACD, EMA, BB
│   │   ├── sentiment_analysis.py    # TextBlob/FinBERT
│   │   ├── signal_generator.py      # Signal generation
│   │   └── main_analysis.py         # Entry point
│   │
│   ├── .env.example             # Template konfigurasi
│   ├── requirements.txt         # Dependencies
│   ├── setup.sh                 # Setup script (Linux/Mac)
│   ├── setup.bat                # Setup script (Windows)
│   └── test_dependencies.py     # Verification script
│
├── database/                    # SQLite database (auto-created)
├── logs/                        # Log files (auto-created)
├── .env                         # Environment variables
├── README.md                    # Dokumentasi utama
├── INSTALL.md                   # Panduan instalasi lengkap
└── QUICK_REFERENCE.md           # File ini
```

---

## 🎯 Command Cheat Sheet

### Setup & Installation
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
cd backend
./setup.sh              # Linux/Mac
setup.bat               # Windows

# Or manual install
pip install -r requirements.txt
python -m textblob.download_corpora

# Verify installation
python test_dependencies.py
```

### Running Application
```bash
# Terminal 1: Data Collector
python -m data_collector.main_collector

# Terminal 2: Analysis Engine
python -m analysis.main_analysis

# Test database
python test_database.py
```

### Database Operations
```bash
# View database with SQLite browser
sqlitebrowser database/trading_data.db

# Or use command line
sqlite3 database/trading_data.db
.tables
SELECT * FROM candles LIMIT 10;
.quit
```

### Logs
```bash
# View logs in real-time
tail -f logs/collector.log

# Search for errors
grep ERROR logs/collector.log

# View last 100 lines
tail -n 100 logs/collector.log
```

---

## 🔧 Troubleshooting Cepat

### Dependencies Issues
```bash
# Reinstall all dependencies
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
python -m textblob.download_corpora
```

### Database Issues
```bash
# Reset database
rm database/trading_data.db
python -m data_collector.main_collector
```

### Connection Issues
```bash
# Test Binance connection
python -c "import ccxt; exchange = ccxt.binance(); exchange.load_markets(); print('OK')"

# Check API keys
cat .env | grep BINANCE
```

### Analysis Issues
```bash
# Test pandas-ta
python -c "import pandas_ta as ta; print('pandas-ta OK')"

# Test TextBlob
python -c "from textblob import TextBlob; print('TextBlob OK')"
```

---

## 📈 Understanding Output

### Data Collector Output
- `✅ BTC/USDT [1h]: 500 candles loaded` - Historical data collected
- `💹 BTC/USDT: $67,234.50 (+2.34%)` - Real-time price update
- `📰 CoinDesk: 20 articles` - News articles fetched

### Analysis Engine Output
- `📈 SIGNAL: BUY/SELL/HOLD` - Trading signal
- `🎯 Confidence: 75%` - Confidence level (0-100%)
- `💰 Current Price: $67,234.50` - Current market price
- `📋 Reasons:` - Why this signal was generated
- `🛡️ Risk Management:` - Stop-loss and take-profit levels

### Signal Interpretation
- **BUY** + High Confidence (>70%) = Strong buy signal
- **SELL** + High Confidence (>70%) = Strong sell signal
- **HOLD** = Wait for better opportunity
- **Low Confidence (<50%)** = Weak signal, be cautious

---

## 📚 Documentation

- **[README.md](README.md)** - Dokumentasi utama
- **[INSTALL.md](INSTALL.md)** - Panduan instalasi lengkap
- **[backend/analysis/README.md](backend/analysis/README.md)** - Analysis Engine docs
- **[backend/analysis/QUICK_REFERENCE.md](backend/analysis/QUICK_REFERENCE.md)** - Analysis quick reference

---

## 🎓 Learning Path

### Day 1: Setup & Data Collection
1. Install dependencies
2. Run data collector
3. Understand OHLCV data
4. Check database

### Day 2: Analysis Engine
1. Run analysis engine
2. Understand technical indicators
3. Understand sentiment analysis
4. Interpret signals

### Day 3: Deep Dive
1. Read technical_indicators.py
2. Read sentiment_analysis.py
3. Read signal_generator.py
4. Experiment with parameters

### Day 4+: Advanced
1. Modify indicators
2. Add new strategies
3. Backtest signals
4. Prepare for Phase 3

---

## 🔗 Useful Links

### Documentation
- [pandas-ta](https://github.com/twopirllc/pandas-ta) - Technical analysis
- [TextBlob](https://textblob.readthedocs.io/) - Sentiment analysis
- [CCXT](https://docs.ccxt.com/) - Exchange library
- [Binance API](https://binance-docs.github.io/apidocs/) - Exchange API

### Learning Resources
- [Technical Analysis](https://www.investopedia.com/technical-analysis-4689657)
- [RSI Indicator](https://www.investopedia.com/terms/r/rsi.asp)
- [MACD Indicator](https://www.investopedia.com/terms/m/macd.asp)
- [Sentiment Analysis](https://en.wikipedia.org/wiki/Sentiment_analysis)

### Tools
- [SQLite Browser](https://sqlitebrowser.org/) - Database viewer
- [Binance Testnet](https://testnet.binance.vision/) - Test trading
- [Python.org](https://www.python.org/) - Python download

---

## ⚡ Quick Tips

### Performance
- Data collector uses ~50MB RAM
- Analysis engine uses ~100MB RAM
- Total: ~150MB RAM
- CPU usage: <10%

### Best Practices
- Always use virtual environment
- Keep .env file secure (never commit)
- Monitor logs regularly
- Test with small amounts first

### Common Mistakes
- ❌ Forgetting to activate virtual environment
- ❌ Not downloading TextBlob corpora
- ❌ Using mainnet instead of testnet
- ❌ Ignoring risk management

---

## 🆘 Need Help?

1. **Check logs**: `tail -f logs/collector.log`
2. **Run tests**: `python test_dependencies.py`
3. **Read docs**: INSTALL.md, README.md
4. **Search issues**: GitHub Issues
5. **Ask community**: Stack Overflow, forums

---

## 🎉 You're Ready!

Anda sekarang memiliki:
- ✅ Data collection system
- ✅ Technical analysis engine
- ✅ Sentiment analysis
- ✅ Signal generation
- ✅ Risk management

**Next step**: Run the application and start analyzing!

```bash
# Terminal 1
python -m data_collector.main_collector

# Terminal 2
python -m analysis.main_analysis
```

**Happy Trading! 🚀📈**
