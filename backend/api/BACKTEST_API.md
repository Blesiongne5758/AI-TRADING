# Backtesting API Documentation

## Base URL

```
http://localhost:8000/api/backtest
```

## Authentication

No authentication required for backtesting endpoints.

---

## Endpoints

### 1. Run Backtest

**POST** `/run`

Run backtest dengan parameter tertentu.

#### Request Body

```json
{
  "symbol": "BTC/USDT",
  "timeframe": "1h",
  "start_date": "2024-01-01",
  "end_date": "2024-12-31",
  "strategy": "rsi_macd",
  "strategy_params": {
    "rsi_period": 14,
    "rsi_oversold": 30,
    "rsi_overbought": 70
  },
  "initial_balance": 10000.0,
  "commission": 0.001
}
```

#### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `symbol` | string | ✅ Yes | - | Trading pair (e.g., "BTC/USDT") |
| `timeframe` | string | ❌ No | "1h" | Timeframe: 1m, 5m, 15m, 1h, 4h, 1d |
| `start_date` | string | ✅ Yes | - | Start date (YYYY-MM-DD) |
| `end_date` | string | ✅ Yes | - | End date (YYYY-MM-DD) |
| `strategy` | string | ✅ Yes | - | Strategy name |
| `strategy_params` | object | ❌ No | {} | Strategy parameters |
| `initial_balance` | float | ❌ No | 10000.0 | Initial balance in USD |
| `commission` | float | ❌ No | 0.001 | Commission rate (0.001 = 0.1%) |

#### Response

```json
{
  "id": "bt_20241215_143022_BTC_USDT",
  "status": "completed",
  "symbol": "BTC/USDT",
  "timeframe": "1h",
  "strategy": "rsi_macd",
  "start_date": "2024-01-01",
  "end_date": "2024-12-31",
  "initial_balance": 10000.0,
  "final_balance": 12534.50,
  "total_return": 2534.50,
  "total_return_pct": 25.35,
  "max_drawdown": -845.20,
  "max_drawdown_pct": -8.45,
  "sharpe_ratio": 2.45,
  "sortino_ratio": 3.12,
  "calmar_ratio": 3.00,
  "win_rate": 68.09,
  "total_trades": 47,
  "winning_trades": 32,
  "losing_trades": 15,
  "avg_win": 185.50,
  "avg_loss": -95.20,
  "largest_win": 450.00,
  "largest_loss": -210.00,
  "profit_factor": 2.35,
  "expectancy": 53.92,
  "payoff_ratio": 1.95,
  "created_at": "2024-12-15T14:30:22"
}
```

#### Example

```bash
curl -X POST http://localhost:8000/api/backtest/run \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "BTC/USDT",
    "timeframe": "1h",
    "start_date": "2024-01-01",
    "end_date": "2024-12-31",
    "strategy": "rsi_macd",
    "strategy_params": {
      "rsi_period": 14,
      "rsi_oversold": 30,
      "rsi_overbought": 70
    },
    "initial_balance": 10000,
    "commission": 0.001
  }'
```

---

### 2. Get Available Strategies

**GET** `/strategies`

List semua available strategies.

#### Response

```json
[
  {
    "name": "rsi_macd",
    "description": "Buy when RSI < 30 and MACD crosses above signal line",
    "parameters": {
      "rsi_period": {
        "type": "int",
        "default": 14,
        "min": 5,
        "max": 50,
        "description": "RSI calculation period"
      },
      "rsi_oversold": {
        "type": "float",
        "default": 30,
        "min": 10,
        "max": 50,
        "description": "RSI oversold threshold"
      },
      "rsi_overbought": {
        "type": "float",
        "default": 70,
        "min": 50,
        "max": 90,
        "description": "RSI overbought threshold"
      }
    },
    "default_params": {
      "rsi_period": 14,
      "rsi_oversold": 30,
      "rsi_overbought": 70
    }
  },
  {
    "name": "ema_cross",
    "description": "Buy when fast EMA crosses above slow EMA",
    "parameters": {
      "fast_ema": {
        "type": "int",
        "default": 20,
        "min": 5,
        "max": 50,
        "description": "Fast EMA period"
      },
      "slow_ema": {
        "type": "int",
        "default": 50,
        "min": 20,
        "max": 200,
        "description": "Slow EMA period"
      }
    },
    "default_params": {
      "fast_ema": 20,
      "slow_ema": 50
    }
  }
]
```

#### Example

```bash
curl http://localhost:8000/api/backtest/strategies
```

---

### 3. Get Backtest Result

**GET** `/results/{backtest_id}`

Get detailed results untuk specific backtest.

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `backtest_id` | string | ✅ Yes | Backtest ID |

#### Response

```json
{
  "id": "bt_20241215_143022_BTC_USDT",
  "status": "completed",
  "request": {
    "symbol": "BTC/USDT",
    "timeframe": "1h",
    "start_date": "2024-01-01",
    "end_date": "2024-12-31",
    "strategy": "rsi_macd",
    "strategy_params": {
      "rsi_period": 14,
      "rsi_oversold": 30,
      "rsi_overbought": 70
    },
    "initial_balance": 10000.0,
    "commission": 0.001
  },
  "result": {
    "total_return": 2534.50,
    "total_return_pct": 25.35,
    "sharpe_ratio": 2.45,
    "max_drawdown_pct": -8.45,
    "win_rate": 68.09,
    "total_trades": 47,
    "equity_curve": [
      {
        "timestamp": "2024-01-01T00:00:00",
        "balance": 10000.0,
        "drawdown": 0.0
      },
      {
        "timestamp": "2024-01-02T00:00:00",
        "balance": 10150.0,
        "drawdown": -1.5
      }
    ],
    "trades": [
      {
        "type": "BUY",
        "entry_price": 42000.0,
        "exit_price": 43500.0,
        "pnl": 1500.0,
        "pnl_pct": 3.57,
        "entry_time": "2024-01-15T10:00:00",
        "exit_time": "2024-01-20T14:00:00",
        "duration": "5d 4h"
      }
    ]
  },
  "created_at": "2024-12-15T14:30:22"
}
```

#### Example

```bash
curl http://localhost:8000/api/backtest/results/bt_20241215_143022_BTC_USDT
```

---

### 4. List Backtest Results

**GET** `/results`

List semua backtest results dengan pagination.

#### Query Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `limit` | integer | ❌ No | 10 | Number of results per page |
| `offset` | integer | ❌ No | 0 | Offset for pagination |

#### Response

```json
{
  "total": 25,
  "limit": 10,
  "offset": 0,
  "results": [
    {
      "id": "bt_20241215_143022_BTC_USDT",
      "status": "completed",
      "symbol": "BTC/USDT",
      "timeframe": "1h",
      "strategy": "rsi_macd",
      "total_return_pct": 25.35,
      "sharpe_ratio": 2.45,
      "created_at": "2024-12-15T14:30:22"
    },
    {
      "id": "bt_20241215_142500_ETH_USDT",
      "status": "completed",
      "symbol": "ETH/USDT",
      "timeframe": "4h",
      "strategy": "ema_cross",
      "total_return_pct": 18.20,
      "sharpe_ratio": 1.85,
      "created_at": "2024-12-15T14:25:00"
    }
  ]
}
```

#### Example

```bash
curl "http://localhost:8000/api/backtest/results?limit=10&offset=0"
```

---

### 5. Delete Backtest Result

**DELETE** `/results/{backtest_id}`

Delete specific backtest result.

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `backtest_id` | string | ✅ Yes | Backtest ID |

#### Response

```json
{
  "status": "deleted",
  "id": "bt_20241215_143022_BTC_USDT"
}
```

#### Example

```bash
curl -X DELETE http://localhost:8000/api/backtest/results/bt_20241215_143022_BTC_USDT
```

---

### 6. Optimize Strategy

**POST** `/optimize`

Optimize strategy parameters.

#### Request Body

```json
{
  "symbol": "BTC/USDT",
  "timeframe": "1h",
  "start_date": "2024-01-01",
  "end_date": "2024-12-31",
  "strategy": "rsi_macd",
  "param_ranges": {
    "rsi_period": [10, 14, 20],
    "rsi_oversold": [25, 30, 35],
    "rsi_overbought": [65, 70, 75]
  },
  "optimization_metric": "sharpe_ratio",
  "initial_balance": 10000.0
}
```

#### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `symbol` | string | ✅ Yes | - | Trading pair |
| `timeframe` | string | ❌ No | "1h" | Timeframe |
| `start_date` | string | ✅ Yes | - | Start date |
| `end_date` | string | ✅ Yes | - | End date |
| `strategy` | string | ✅ Yes | - | Strategy name |
| `param_ranges` | object | ✅ Yes | - | Parameter ranges |
| `optimization_metric` | string | ❌ No | "sharpe_ratio" | Metric to optimize |
| `initial_balance` | float | ❌ No | 10000.0 | Initial balance |

#### Optimization Metrics

- `sharpe_ratio`: Risk-adjusted return (recommended)
- `total_return_pct`: Total percentage return
- `win_rate`: Percentage of winning trades
- `profit_factor`: Gross profit / Gross loss
- `max_drawdown_pct`: Minimize drawdown (use negative)

#### Response

```json
{
  "id": "opt_20241215_143022_BTC_USDT",
  "status": "completed",
  "strategy": "rsi_macd",
  "optimization_metric": "sharpe_ratio",
  "best_params": {
    "rsi_period": 14,
    "rsi_oversold": 30,
    "rsi_overbought": 70
  },
  "best_score": 2.45,
  "total_combinations": 27,
  "all_results": [
    {
      "params": {
        "rsi_period": 14,
        "rsi_oversold": 30,
        "rsi_overbought": 70
      },
      "score": 2.45
    },
    {
      "params": {
        "rsi_period": 10,
        "rsi_oversold": 25,
        "rsi_overbought": 75
      },
      "score": 2.38
    }
  ],
  "created_at": "2024-12-15T14:30:22"
}
```

#### Example

```bash
curl -X POST http://localhost:8000/api/backtest/optimize \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "BTC/USDT",
    "timeframe": "1h",
    "start_date": "2024-01-01",
    "end_date": "2024-12-31",
    "strategy": "rsi_macd",
    "param_ranges": {
      "rsi_period": [10, 14, 20],
      "rsi_oversold": [25, 30, 35],
      "rsi_overbought": [65, 70, 75]
    },
    "optimization_metric": "sharpe_ratio",
    "initial_balance": 10000
  }'
```

---

### 7. Get Strategy Details

**GET** `/strategy/{strategy_name}`

Get detail strategy tertentu.

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `strategy_name` | string | ✅ Yes | Strategy name |

#### Response

```json
{
  "name": "rsi_macd",
  "description": "Buy when RSI < 30 and MACD crosses above signal line",
  "parameters": {
    "rsi_period": {
      "type": "int",
      "default": 14,
      "min": 5,
      "max": 50,
      "description": "RSI calculation period"
    },
    "rsi_oversold": {
      "type": "float",
      "default": 30,
      "min": 10,
      "max": 50,
      "description": "RSI oversold threshold"
    },
    "rsi_overbought": {
      "type": "float",
      "default": 70,
      "min": 50,
      "max": 90,
      "description": "RSI overbought threshold"
    }
  },
  "default_params": {
    "rsi_period": 14,
    "rsi_oversold": 30,
    "rsi_overbought": 70
  },
  "available": true
}
```

#### Example

```bash
curl http://localhost:8000/api/backtest/strategy/rsi_macd
```

---

### 8. Custom Strategies

#### 8.1 Get Custom Strategies

**GET** `/custom-strategies`

List semua custom strategies.

#### Response

```json
[
  {
    "id": "cs_1234567890",
    "name": "My Custom Strategy",
    "description": "Custom RSI strategy",
    "conditions": [
      {
        "id": 1,
        "indicator": "rsi",
        "operator": "less_than",
        "value": 30,
        "logic": "AND"
      },
      {
        "id": 2,
        "indicator": "macd",
        "operator": "crosses_above",
        "value": 0,
        "logic": "AND"
      }
    ],
    "created_at": "2024-12-15T14:30:22",
    "updated_at": "2024-12-15T14:30:22"
  }
]
```

#### Example

```bash
curl http://localhost:8000/api/backtest/custom-strategies
```

---

#### 8.2 Create Custom Strategy

**POST** `/custom-strategies`

Create new custom strategy.

#### Request Body

```json
{
  "name": "My Custom Strategy",
  "description": "Custom RSI strategy",
  "conditions": [
    {
      "indicator": "rsi",
      "operator": "less_than",
      "value": 30,
      "logic": "AND"
    },
    {
      "indicator": "macd",
      "operator": "crosses_above",
      "value": 0,
      "logic": "AND"
    }
  ]
}
```

#### Response

```json
{
  "id": "cs_1234567890",
  "name": "My Custom Strategy",
  "description": "Custom RSI strategy",
  "conditions": [
    {
      "id": 1,
      "indicator": "rsi",
      "operator": "less_than",
      "value": 30,
      "logic": "AND"
    },
    {
      "id": 2,
      "indicator": "macd",
      "operator": "crosses_above",
      "value": 0,
      "logic": "AND"
    }
  ],
  "created_at": "2024-12-15T14:30:22",
  "updated_at": "2024-12-15T14:30:22"
}
```

#### Example

```bash
curl -X POST http://localhost:8000/api/backtest/custom-strategies \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Custom Strategy",
    "description": "Custom RSI strategy",
    "conditions": [
      {
        "indicator": "rsi",
        "operator": "less_than",
        "value": 30,
        "logic": "AND"
      }
    ]
  }'
```

---

#### 8.3 Update Custom Strategy

**PUT** `/custom-strategies/{strategy_id}`

Update existing custom strategy.

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `strategy_id` | string | ✅ Yes | Strategy ID |

#### Request Body

```json
{
  "name": "Updated Strategy",
  "description": "Updated description",
  "conditions": [
    {
      "indicator": "rsi",
      "operator": "less_than",
      "value": 25,
      "logic": "AND"
    }
  ]
}
```

#### Response

```json
{
  "id": "cs_1234567890",
  "name": "Updated Strategy",
  "description": "Updated description",
  "conditions": [
    {
      "id": 1,
      "indicator": "rsi",
      "operator": "less_than",
      "value": 25,
      "logic": "AND"
    }
  ],
  "created_at": "2024-12-15T14:30:22",
  "updated_at": "2024-12-15T15:00:00"
}
```

#### Example

```bash
curl -X PUT http://localhost:8000/api/backtest/custom-strategies/cs_1234567890 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Strategy",
    "description": "Updated description",
    "conditions": [
      {
        "indicator": "rsi",
        "operator": "less_than",
        "value": 25,
        "logic": "AND"
      }
    ]
  }'
```

---

#### 8.4 Delete Custom Strategy

**DELETE** `/custom-strategies/{strategy_id}`

Delete custom strategy.

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `strategy_id` | string | ✅ Yes | Strategy ID |

#### Response

```json
{
  "status": "deleted",
  "id": "cs_1234567890"
}
```

#### Example

```bash
curl -X DELETE http://localhost:8000/api/backtest/custom-strategies/cs_1234567890
```

---

## Error Responses

### 400 Bad Request

```json
{
  "detail": "Unknown strategy: invalid_strategy. Available: ['rsi_macd', 'ema_cross', 'bollinger', 'combined']"
}
```

### 404 Not Found

```json
{
  "detail": "Backtest not found: bt_invalid_id"
}
```

### 500 Internal Server Error

```json
{
  "detail": "Backtest failed: No data available for BTC/USDT"
}
```

---

## Rate Limiting

No rate limiting untuk backtesting endpoints.

---

## WebSocket

### Real-time Backtest Progress

**WS** `/ws/backtest/{backtest_id}`

Subscribe ke real-time progress updates.

#### Message Format

```json
{
  "type": "progress",
  "backtest_id": "bt_20241215_143022_BTC_USDT",
  "progress": 45.5,
  "status": "running",
  "current_candle": 4550,
  "total_candles": 10000,
  "trades_executed": 12,
  "current_balance": 10450.50
}
```

#### Example (JavaScript)

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/backtest/bt_20241215_143022_BTC_USDT');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log(`Progress: ${data.progress}%`);
  console.log(`Trades: ${data.trades_executed}`);
  console.log(`Balance: $${data.current_balance}`);
};

ws.onclose = () => {
  console.log('Backtest completed');
};
```

---

## Examples

### Python Example

```python
import requests
import json

# Run backtest
response = requests.post(
    'http://localhost:8000/api/backtest/run',
    json={
        'symbol': 'BTC/USDT',
        'timeframe': '1h',
        'start_date': '2024-01-01',
        'end_date': '2024-12-31',
        'strategy': 'rsi_macd',
        'strategy_params': {
            'rsi_period': 14,
            'rsi_oversold': 30,
            'rsi_overbought': 70
        },
        'initial_balance': 10000,
        'commission': 0.001
    }
)

result = response.json()
print(f"Return: {result['total_return_pct']:.2f}%")
print(f"Sharpe: {result['sharpe_ratio']:.2f}")
print(f"Max DD: {result['max_drawdown_pct']:.2f}%")

# Get backtest result
backtest_id = result['id']
response = requests.get(f'http://localhost:8000/api/backtest/results/{backtest_id}')
details = response.json()

# Print trade history
for trade in details['result']['trades'][:5]:
    print(f"{trade['type']} @ ${trade['entry_price']:.2f} → ${trade['exit_price']:.2f}")
    print(f"  P&L: ${trade['pnl']:.2f} ({trade['pnl_pct']:.2f}%)")
```

### JavaScript Example

```javascript
// Run backtest
const response = await fetch('http://localhost:8000/api/backtest/run', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    symbol: 'BTC/USDT',
    timeframe: '1h',
    start_date: '2024-01-01',
    end_date: '2024-12-31',
    strategy: 'rsi_macd',
    strategy_params: {
      rsi_period: 14,
      rsi_oversold: 30,
      rsi_overbought: 70
    },
    initial_balance: 10000,
    commission: 0.001
  })
});

const result = await response.json();
console.log(`Return: ${result.total_return_pct.toFixed(2)}%`);
console.log(`Sharpe: ${result.sharpe_ratio.toFixed(2)}`);

// Get strategies
const strategiesResponse = await fetch('http://localhost:8000/api/backtest/strategies');
const strategies = await strategiesResponse.json();
console.log('Available strategies:', strategies.map(s => s.name));
```

---

## Best Practices

### 1. Use Appropriate Timeframes

```python
# For intraday trading
timeframe = "15m"  # or "1h"

# For swing trading
timeframe = "4h"  # or "1d"

# For position trading
timeframe = "1d"
```

### 2. Sufficient Historical Data

```python
# Minimum 6 months
start_date = "2024-06-01"

# Recommended 1-2 years
start_date = "2023-01-01"
```

### 3. Realistic Commission

```python
# Typical crypto exchange commission
commission = 0.001  # 0.1%

# High-frequency trading
commission = 0.0005  # 0.05%
```

### 4. Validate Results

```python
# Split data into train/test
train_end = "2024-06-30"
test_start = "2024-07-01"

# Optimize on train data
optimizer = ParameterOptimizer(
    start_date="2024-01-01",
    end_date=train_end
)
best_params = optimizer.optimize(...)

# Validate on test data
engine = BacktestEngine(
    start_date=test_start,
    end_date="2024-12-31",
    strategy_params=best_params
)
validation_result = engine.run()
```

### 5. Compare Multiple Strategies

```python
strategies = ["rsi_macd", "ema_cross", "bollinger"]
results = {}

for strategy in strategies:
    engine = BacktestEngine(strategy_name=strategy)
    results[strategy] = engine.run()

# Find best strategy
best = max(results.items(), key=lambda x: x[1]['sharpe_ratio'])
print(f"Best strategy: {best[0]}")
```

---

## Troubleshooting

### Issue: API returns 404

**Solution**: Ensure backend server is running
```bash
cd backend
python -m api.main
```

### Issue: Backtest takes too long

**Solution**: 
- Use larger timeframe (1d instead of 1h)
- Reduce date range
- Enable caching

### Issue: No data available

**Solution**:
```bash
# Run data collector
cd backend
python -m data_collector.main_collector

# Wait for data collection (200+ candles)
```

### Issue: CORS errors

**Solution**: Add CORS middleware
```python
# backend/api/main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## API Client Libraries

### Python

```python
# Install
pip install requests

# Usage
import requests

class BacktestAPI:
    def __init__(self, base_url="http://localhost:8000/api/backtest"):
        self.base_url = base_url
    
    def run_backtest(self, params):
        response = requests.post(f"{self.base_url}/run", json=params)
        return response.json()
    
    def get_strategies(self):
        response = requests.get(f"{self.base_url}/strategies")
        return response.json()
    
    def get_result(self, backtest_id):
        response = requests.get(f"{self.base_url}/results/{backtest_id}")
        return response.json()

# Usage
api = BacktestAPI()
result = api.run_backtest({
    "symbol": "BTC/USDT",
    "timeframe": "1h",
    "start_date": "2024-01-01",
    "end_date": "2024-12-31",
    "strategy": "rsi_macd"
})
```

### JavaScript

```javascript
// Install
npm install axios

// Usage
import axios from 'axios';

class BacktestAPI {
  constructor(baseUrl = 'http://localhost:8000/api/backtest') {
    this.baseUrl = baseUrl;
  }
  
  async runBacktest(params) {
    const response = await axios.post(`${this.baseUrl}/run`, params);
    return response.data;
  }
  
  async getStrategies() {
    const response = await axios.get(`${this.baseUrl}/strategies`);
    return response.data;
  }
  
  async getResult(backtestId) {
    const response = await axios.get(`${this.baseUrl}/results/${backtestId}`);
    return response.data;
  }
}

// Usage
const api = new BacktestAPI();
const result = await api.runBacktest({
  symbol: 'BTC/USDT',
  timeframe: '1h',
  start_date: '2024-01-01',
  end_date: '2024-12-31',
  strategy: 'rsi_macd'
});
```

---

**API Documentation Complete! 📚**

For more information, see:
- Backend README: `backend/backtesting/README.md`
- Frontend Guide: `frontend/BACKTESTING.md`
- Quick Start: `backend/backtesting/QUICKSTART.md`
