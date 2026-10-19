# 🚀 AI Trading Agent - Full Stack

Sistem trading otomatis berbasis AI dengan backend FastAPI dan frontend React.

## 📁 Struktur Proyek

```
ai-trading-agent/
├── backend/
│   ├── data_collector/     # Modul A: Data Collection
│   ├── analysis/           # Modul B: Analysis Engine
│   ├── paper_trading/      # Modul C: Paper Trading
│   ├── xai/                # Modul D: Explainable AI
│   ├── api/                # Modul E: FastAPI Backend
│   │   ├── main.py
│   │   ├── routes/
│   │   │   ├── portfolio.py
│   │   │   ├── signals.py
│   │   │   ├── market.py
│   │   │   └── chat.py
│   │   └── websocket.py
│   └── requirements.txt
│
└── frontend/
    ├── src/
    │   ├── components/
    │   │   ├── Sidebar.jsx
    │   │   ├── Dashboard.jsx
    │   │   └── ChatInterface.jsx
    │   ├── pages/
    │   │   └── Home.jsx
    │   ├── App.jsx
    │   ├── main.jsx
    │   └── index.css
    ├── package.json
    ├── vite.config.js
    └── tailwind.config.js
```

## 🚀 Quick Start

### 1. Backend Setup

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Download TextBlob corpora
python -m textblob.download_corpora

# Setup environment
cp .env.example .env
# Edit .env dengan API keys Anda

# Jalankan backend
python -m api.main
```

Backend akan berjalan di `http://localhost:8000`

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Jalankan frontend
npm run dev
```

Frontend akan berjalan di `http://localhost:3000`

## 📊 API Endpoints

### Portfolio
- `GET /api/portfolio/summary` - Portfolio summary
- `GET /api/portfolio/positions` - Open positions
- `GET /api/portfolio/trades` - Trade history
- `GET /api/portfolio/stats` - Statistics
- `GET /api/portfolio/snapshots` - Equity curve data

### Signals
- `GET /api/signals/analyze/{symbol}` - Analyze symbol
- `GET /api/signals/analyze-all` - Analyze all symbols
- `GET /api/signals/history` - Signal history

### Market
- `GET /api/market/ticker/{symbol}` - Latest ticker
- `GET /api/market/tickers` - All tickers
- `GET /api/market/candles/{symbol}` - Candlestick data
- `GET /api/market/news` - Latest news
- `GET /api/market/symbols` - List of symbols
- `GET /api/market/timeframes` - List of timeframes

### Chat
- `POST /api/chat/message` - Send message to AI
- `GET /api/chat/intents` - List of intents
- `GET /api/chat/dictionary` - Trading dictionary

### WebSocket
- `WS /ws/updates` - Real-time updates

## 🎯 Features

### ✅ Fase 1: Data Collection
- Binance REST API integration
- Real-time ticker data
- Historical candlestick data
- News scraping dari 3 sources

### ✅ Fase 2: Analysis Engine
- Technical indicators (RSI, MACD, EMA, Bollinger, ATR, Volume)
- Sentiment analysis dengan TextBlob
- Signal generation dengan confidence scoring
- ATR-based risk management

### ✅ Fase 3: Paper Trading
- Virtual portfolio management
- Risk management (8-step validation)
- Order execution dengan fee simulation
- Stop-loss & take-profit automation
- Performance tracking

### ✅ Fase 4: XAI Module
- Explanation generator (6-section)
- Trading dictionary (26 terms)
- Context builder (4 methods)
- Chat agent (9 intents)

### ✅ Fase 5: Full Stack
- FastAPI backend dengan REST endpoints
- WebSocket untuk real-time updates
- React frontend dengan Tailwind CSS
- Dashboard, Chart, Signals, Chat pages

## 📖 Documentation

- [README.md](README.md) - Main documentation
- [backend/xai/README.md](backend/xai/README.md) - XAI module
- [backend/analysis/README.md](backend/analysis/README.md) - Analysis engine

## 🛠️ Tech Stack

### Backend
- Python 3.11+
- FastAPI
- SQLAlchemy + aiosqlite
- CCXT (Binance API)
- pandas-ta (technical analysis)
- TextBlob (sentiment analysis)
- Loguru (logging)

### Frontend
- React 18
- Vite
- Tailwind CSS
- React Router
- Axios
- Lightweight Charts

## 📊 System Architecture

```
┌─────────────┐
│   Frontend  │  React + Vite + Tailwind
│  (Port 3000)│
└──────┬──────┘
       │ HTTP/WebSocket
┌──────▼──────┐
│   FastAPI   │  REST API + WebSocket
│  (Port 8000)│
└──────┬──────┘
       │
┌──────▼──────────────────────────────────────┐
│              Backend Modules                 │
├──────────────────────────────────────────────┤
│  Data Collector → Analysis → Paper Trading  │
│                                              │
│              XAI Module                      │
└──────────────────────────────────────────────┘
       │
┌──────▼──────┐
│   SQLite    │  Database
└─────────────┘
```

## 🎓 Learning Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Technical Analysis](https://www.investopedia.com/technical-analysis-4689657)

## ⚠️ Disclaimer

Ini adalah proyek edukasi. Trading crypto memiliki risiko tinggi. Selalu DYOR (Do Your Own Research) dan jangan invest uang yang tidak siap Anda rugikan.

## 📄 License

MIT License

---

**Happy Trading! 🚀📈**
