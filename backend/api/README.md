# 🚀 Backend API Documentation

FastAPI backend untuk AI Trading Agent dengan WebSocket support untuk real-time updates.

## 📋 Overview

Backend API menghubungkan semua modul (Data Collector, Analysis Engine, Paper Trading, XAI) dengan frontend melalui REST API dan WebSocket.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (React)                      │
│              http://localhost:5173                        │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP/WebSocket
┌────────────────────▼────────────────────────────────────┐
│                  FastAPI Backend                         │
│              http://localhost:8000                        │
│                                                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Routes                                           │  │
│  │  ├─ /api/portfolio/*                             │  │
│  │  ├─ /api/signals/*                               │  │
│  │  ├─ /api/market/*                                │  │
│  │  └─ /api/chat/*                                  │  │
│  └──────────────────────────────────────────────────┘  │
│                                                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │  WebSocket                                        │  │
│  │  └─ /ws (real-time updates)                      │  │
│  └──────────────────────────────────────────────────┘  │
│                                                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Global Instances                                 │  │
│  │  ├─ DatabaseManager                              │  │
│  │  ├─ PortfolioManager                             │  │
│  │  ├─ RiskManager                                  │  │
│  │  ├─ TechnicalAnalyzer                            │  │
│  │  ├─ SentimentAnalyzer                            │  │
│  │  ├─ SignalGenerator                              │  │
│  │  └─ ChatAgent                                    │  │
│  └──────────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
   ┌─────────┐  ┌─────────┐  ┌─────────┐
   │  Data   │  │Analysis │  │  XAI    │
   │Collector│  │ Engine  │  │ Module  │
   └─────────┘  └─────────┘  └─────────┘
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Run Backend

```bash
python -m api.main
```

API akan berjalan di `http://localhost:8000`

### 3. Access API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📡 API Endpoints

### Health Check

```http
GET /
```

**Response:**
```json
{
  "status": "ok",
  "service": "AI Trading Agent API",
  "version": "1.0.0",
  "timestamp": "2024-01-15T10:00:00"
}
```

### System Status

```http
GET /api/status
```

**Response:**
```json
{
  "portfolio": {
    "initial_balance": 10000.0,
    "current_balance": 10500.0,
    "total_pnl": 500.0,
    "total_pnl_percent": 5.0,
    "open_positions": 2,
    "total_trades": 15,
    "win_rate": 73.3
  },
  "stats": {
    "total_pnl": 500.0,
    "total_trades": 15,
    "wins": 11,
    "losses": 4,
    "win_rate": 73.3,
    "avg_win": 150.0,
    "avg_loss": -80.0,
    "profit_factor": 2.5,
    "max_loss": -120.0
  },
  "monitoring_symbols": ["BTC/USDT", "ETH/USDT", "SOL/USDT", "BNB/USDT", "XRP/USDT"],
  "connected_clients": 1
}
```

## 📊 Portfolio Routes

### Get Portfolio Summary

```http
GET /api/portfolio/summary
```

**Response:**
```json
{
  "balance": 10500.0,
  "stats": {
    "total_pnl": 500.0,
    "total_trades": 15,
    "win_rate": 73.3
  },
  "open_positions": 2,
  "positions": [
    {
      "id": 1,
      "symbol": "BTC/USDT",
      "side": "long",
      "entry_price": 67000.0,
      "quantity": 0.015,
      "stop_loss": 65000.0,
      "take_profit": 70000.0,
      "entry_time": 1642684522000
    }
  ]
}
```

### Get Open Positions

```http
GET /api/portfolio/positions
```

### Get Trade History

```http
GET /api/portfolio/trades
```

### Get Portfolio Stats

```http
GET /api/portfolio/stats
```

### Get Portfolio Snapshots

```http
GET /api/portfolio/snapshots
```

## 📈 Signals Routes

### Analyze Symbol

```http
GET /api/signals/analyze/{symbol}?timeframe=1h
```

**Parameters:**
- `symbol`: Trading pair (e.g., "BTC/USDT")
- `timeframe`: Timeframe (1m, 5m, 15m, 1h, 4h, 1d)

**Response:**
```json
{
  "symbol": "BTC/USDT",
  "timeframe": "1h",
  "timestamp": "2024-01-15T10:00:00",
  "signal": "STRONG_BUY",
  "confidence": 85.5,
  "final_score": 78.45,
  "latest_price": 67234.50,
  "technical_score": 71.50,
  "sentiment_score": 0.45,
  "sentiment_label": "POSITIVE",
  "component_scores": {
    "rsi": {"score": 80, "signal": "OVERSOLD", "weight": 0.15},
    "macd": {"score": 90, "signal": "BULLISH_CROSSOVER", "weight": 0.25},
    "ema": {"score": 85, "signal": "STRONG_UPTREND", "weight": 0.25}
  },
  "reasons": [
    "[RSI] RSI 28.5 < 30 → potensi rebound",
    "[MACD] MACD histogram baru crossover ke positif"
  ],
  "suggested_actions": {
    "action": "OPEN_LONG",
    "entry": 67234.50,
    "stop_loss": 65834.50,
    "take_profit": 70034.50,
    "position_size_percent": 10.0,
    "risk_reward_ratio": 2.0
  }
}
```

### Analyze All Symbols

```http
GET /api/signals/analyze-all?timeframe=1h
```

### Get Signal History

```http
GET /api/signals/history
```

## 💹 Market Routes

### Get Ticker

```http
GET /api/market/ticker/{symbol}
```

**Response:**
```json
{
  "symbol": "BTC/USDT",
  "price": 67234.50,
  "bid": 67234.00,
  "ask": 67235.00,
  "volume_24h": 1234567.89,
  "price_change_24h": 2.34,
  "last_update": 1642684522000
}
```

### Get All Tickers

```http
GET /api/market/tickers
```

### Get Candlestick Data

```http
GET /api/market/candles/{symbol}?timeframe=1h&limit=100
```

**Parameters:**
- `symbol`: Trading pair
- `timeframe`: Timeframe (default: 1h)
- `limit`: Number of candles (default: 100, max: 1000)

### Get Latest News

```http
GET /api/market/news?limit=20
```

### Get Trading Symbols

```http
GET /api/market/symbols
```

**Response:**
```json
["BTC/USDT", "ETH/USDT", "SOL/USDT", "BNB/USDT", "XRP/USDT"]
```

### Get Timeframes

```http
GET /api/market/timeframes
```

**Response:**
```json
["1m", "5m", "15m", "1h", "4h", "1d"]
```

## 💬 Chat Routes

### Send Message to AI

```http
POST /api/chat/message
Content-Type: application/json

{
  "message": "apa itu RSI?"
}
```

**Response:**
```json
{
  "response": "📖 **RSI (Relative Strength Index)**\n\nIndikator momentum yang mengukur...",
  "intent": "explain_indicator",
  "confidence": 0.9
}
```

### Get Supported Intents

```http
GET /api/chat/intents
```

**Response:**
```json
{
  "greeting": "Salam dan perkenalan",
  "explain_indicator": "Penjelasan indikator teknikal",
  "explain_concept": "Penjelasan konsep trading",
  "why_trade": "Penjelasan keputusan bot",
  "portfolio_status": "Status portfolio dan P&L",
  "market_condition": "Kondisi market dan harga terbaru",
  "recent_trades": "Riwayat trade terakhir",
  "help": "Panduan penggunaan",
  "thanks": "Ucapan terima kasih"
}
```

### Get Trading Dictionary

```http
GET /api/chat/dictionary
```

**Response:**
```json
{
  "terms": {
    "rsi": {
      "name": "RSI (Relative Strength Index)",
      "category": "indicator",
      "simple": "Indikator yang mengukur...",
      "detailed": "RSI membandingkan...",
      "analogy": "Bayangkan seperti speedometer mobil...",
      "example": "RSI BTC = 28 → BTC oversold..."
    }
  },
  "count": 26
}
```

## 🔌 WebSocket

### Connect to WebSocket

```javascript
const ws = new WebSocket('ws://localhost:8000/ws');

ws.onopen = () => {
  console.log('Connected to WebSocket');
  
  // Send ping to keep connection alive
  setInterval(() => {
    ws.send('ping');
  }, 30000);
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Received:', data);
  
  // Handle different update types
  switch(data.type) {
    case 'price_update':
      updatePrice(data.data);
      break;
    case 'signal_update':
      updateSignal(data.data);
      break;
    case 'portfolio_update':
      updatePortfolio(data.data);
      break;
  }
};

ws.onclose = () => {
  console.log('Disconnected from WebSocket');
};
```

### Update Types

**Price Update:**
```json
{
  "type": "price_update",
  "data": {
    "symbol": "BTC/USDT",
    "price": 67234.50,
    "change": 2.34
  },
  "timestamp": "2024-01-15T10:00:00"
}
```

**Signal Update:**
```json
{
  "type": "signal_update",
  "data": {
    "symbol": "BTC/USDT",
    "signal": "STRONG_BUY",
    "confidence": 85.5
  },
  "timestamp": "2024-01-15T10:00:00"
}
```

**Portfolio Update:**
```json
{
  "type": "portfolio_update",
  "data": {
    "balance": 10500.0,
    "pnl": 500.0,
    "open_positions": 2
  },
  "timestamp": "2024-01-15T10:00:00"
}
```

## 🔧 Configuration

### CORS Configuration

CORS sudah dikonfigurasi untuk allow origins:
- `http://localhost:5173` (Vite dev server)
- `http://localhost:3000` (Create React App)

Untuk production, update di `backend/api/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-domain.com"],  # Ganti dengan domain Anda
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Global Instances

Semua global instances di-export melalui `app.state`:

```python
# Di route handlers
from fastapi import Request

@router.get("/example")
async def example(request: Request):
    db = request.app.state.db
    portfolio_manager = request.app.state.portfolio_manager
    # ...
```

## 📝 Error Handling

Semua error di-handle secara global dan return JSON response:

```json
{
  "detail": "Error message",
  "type": "ExceptionType"
}
```

**HTTP Status Codes:**
- `200`: Success
- `400`: Bad Request
- `404`: Not Found
- `500`: Internal Server Error

## 🧪 Testing API

### Using cURL

```bash
# Health check
curl http://localhost:8000/

# Get portfolio summary
curl http://localhost:8000/api/portfolio/summary

# Analyze symbol
curl "http://localhost:8000/api/signals/analyze/BTC/USDT?timeframe=1h"

# Chat with AI
curl -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{"message": "apa itu RSI?"}'
```

### Using Python

```python
import requests

# Get portfolio summary
response = requests.get('http://localhost:8000/api/portfolio/summary')
print(response.json())

# Analyze symbol
response = requests.get('http://localhost:8000/api/signals/analyze/BTC/USDT')
signal = response.json()
print(f"Signal: {signal['signal']}, Confidence: {signal['confidence']}%")

# Chat with AI
response = requests.post(
    'http://localhost:8000/api/chat/message',
    json={'message': 'apa itu RSI?'}
)
print(response.json()['response'])
```

### Using JavaScript (Browser)

```javascript
// GET request
fetch('http://localhost:8000/api/portfolio/summary')
  .then(res => res.json())
  .then(data => console.log(data));

// POST request
fetch('http://localhost:8000/api/chat/message', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({message: 'apa itu RSI?'})
})
  .then(res => res.json())
  .then(data => console.log(data.response));
```

## 📊 Monitoring

### Check Connected WebSocket Clients

```http
GET /api/status
```

Response includes `connected_clients` count.

### Logs

Logs disimpan di `logs/` folder:
- `api.log` - API logs
- `collector.log` - Data collector logs
- `analysis.log` - Analysis engine logs

## 🐛 Troubleshooting

### Port Already in Use

```bash
# Check what's using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>
```

### CORS Error

Pastikan frontend URL ada di `allow_origins` di `main.py`.

### WebSocket Connection Failed

- Check backend is running
- Check firewall settings
- Check browser console for errors

### Database Locked

```bash
# Remove database file
rm database/trading_data.db

# Restart backend
python -m api.main
```

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [WebSocket API](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)
- [Swagger UI](https://swagger.io/tools/swagger-ui/)

---

**Last Updated**: 2024  
**API Version**: 1.0.0  
**FastAPI Version**: 0.109.0
