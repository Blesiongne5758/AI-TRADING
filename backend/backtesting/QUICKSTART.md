# Backtesting Quick Start Guide

## 🚀 5-Minute Setup

### 1. Install Dependencies

```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

### 2. Start Backend

```bash
cd backend
python -m api.main
```

Backend akan berjalan di `http://localhost:8000`

### 3. Start Frontend

```bash
cd frontend
npm run dev
```

Frontend akan berjalan di `http://localhost:5173`

### 4. Open Browser

Navigate to: `http://localhost:5173/backtest`

---

## 📊 First Backtest

### Via Frontend UI

1. **Select Symbol**: BTC/USDT
2. **Select Timeframe**: 1h
3. **Set Date Range**: 2024-01-01 to 2024-12-31
4. **Choose Strategy**: RSI + MACD
5. **Set Initial Balance**: $10,000
6. **Click "Run Backtest"**

### Via API

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

### Via Python

```python
import requests

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
print(f"Sharpe Ratio: {result['sharpe_ratio']:.2f}")
print(f"Max Drawdown: {result['max_drawdown_pct']:.2f}%")
```

---

## 🎯 Understanding Results

### Key Metrics

**Total Return**: Profit/loss in USD
```
Initial: $10,000 → Final: $12,534.50
Total Return: +$2,534.50 (+25.35%)
```

**Sharpe Ratio**: Risk-adjusted return
```
< 1.0: Poor
1.0-2.0: Acceptable
2.0-3.0: Good
> 3.0: Excellent
```

**Max Drawdown**: Largest peak-to-trough decline
```
-8.45% means portfolio dropped 8.45% from peak
Lower is better (< 10% is good)
```

**Win Rate**: Percentage of profitable trades
```
68.09% means 68% of trades were profitable
> 60% is good
```

**Profit Factor**: Gross profit / Gross loss
```
2.35 means for every $1 lost, made $2.35
> 2.0 is excellent
```

---

## 🔧 Custom Strategy

### 1. Create Strategy File

```python
# backend/analysis/my_strategy.py
from analysis.custom_strategies import BaseStrategy
import pandas as pd

class MyStrategy(BaseStrategy):
    def __init__(self, params=None):
        super().__init__("My Strategy", params)
        self.description = "My custom trading logic"
        self.period = self.params.get('period', 20)
    
    def generate_signal(self, df: pd.DataFrame, index: int) -> dict:
        if index < self.period:
            return {"action": "HOLD", "confidence": 0, "stop_loss": 0, "take_profit": 0}
        
        current_price = df['close'].iloc[index]
        prev_high = df['high'].iloc[index - self.period:index].max()
        
        if current_price > prev_high:
            return {
                "action": "BUY",
                "confidence": 75,
                "stop_loss": current_price * 0.97,
                "take_profit": current_price * 1.05,
                "reason": "Breakout above previous high"
            }
        
        return {"action": "HOLD", "confidence": 50, "stop_loss": 0, "take_profit": 0}
```

### 2. Register Strategy

```python
# backend/analysis/custom_strategies.py
from .my_strategy import MyStrategy

StrategyFactory.AVAILABLE_STRATEGIES["my_strategy"] = MyStrategy
```

### 3. Use in Backtest

```python
engine = BacktestEngine(
    symbol="BTC/USDT",
    timeframe="1h",
    start_date="2024-01-01",
    end_date="2024-12-31",
    strategy_name="my_strategy",
    strategy_params={"period": 20},
    initial_balance=10000
)

result = engine.run()
```

---

## 📈 Parameter Optimization

### 1. Define Parameter Ranges

```python
param_ranges = {
    "rsi_period": [10, 14, 20, 25],
    "rsi_oversold": [20, 25, 30, 35],
    "rsi_overbought": [65, 70, 75, 80]
}
```

### 2. Run Optimization

```python
from backtesting.optimizer import ParameterOptimizer

optimizer = ParameterOptimizer(
    symbol="BTC/USDT",
    timeframe="1h",
    start_date="2024-01-01",
    end_date="2024-06-30",
    strategy_name="rsi_macd",
    initial_balance=10000
)

result = optimizer.optimize(
    param_ranges=param_ranges,
    optimization_metric="sharpe_ratio",
    n_trials=50
)

print(f"Best parameters: {result['best_params']}")
print(f"Best Sharpe Ratio: {result['best_score']:.2f}")
```

### 3. Validate Results

```python
# Test on out-of-sample data
optimizer_out = ParameterOptimizer(
    symbol="BTC/USDT",
    timeframe="1h",
    start_date="2024-07-01",
    end_date="2024-12-31",
    strategy_name="rsi_macd",
    strategy_params=result['best_params'],
    initial_balance=10000
)

validation = optimizer_out.run_single_backtest()
print(f"Validation Return: {validation['total_return_pct']:.2f}%")
```

---

## 🎨 Frontend Customization

### 1. Add New Strategy to UI

```jsx
// frontend/src/components/BacktestPanel.jsx
<select value={strategy} onChange={(e) => setStrategy(e.target.value)}>
  <option value="rsi_macd">RSI + MACD</option>
  <option value="ema_cross">EMA Crossover</option>
  <option value="bollinger">Bollinger Bands</option>
  <option value="my_strategy">My Custom Strategy</option>
</select>
```

### 2. Customize Results Display

```jsx
// frontend/src/components/BacktestResults.jsx
<div className="grid grid-cols-3 gap-4">
  <MetricCard 
    title="Total Return" 
    value={`${result.total_return_pct.toFixed(2)}%`}
    color={result.total_return_pct > 0 ? 'green' : 'red'}
  />
  <MetricCard 
    title="Sharpe Ratio" 
    value={result.sharpe_ratio.toFixed(2)}
    color="blue"
  />
  <MetricCard 
    title="Max Drawdown" 
    value={`${result.max_drawdown_pct.toFixed(2)}%`}
    color="red"
  />
</div>
```

---

## 🐛 Common Issues

### Issue 1: No Data Available

**Symptom**: Error "No data available for backtest"

**Solution**:
```bash
# Ensure data collector is running
cd backend
python -m data_collector.main_collector

# Wait for data to be collected (200+ candles)
```

### Issue 2: Strategy Not Found

**Symptom**: Error "Unknown strategy: my_strategy"

**Solution**:
```python
# Register strategy in custom_strategies.py
StrategyFactory.AVAILABLE_STRATEGIES["my_strategy"] = MyStrategy

# Restart backend server
```

### Issue 3: Slow Backtest

**Symptom**: Backtest takes > 30 seconds

**Solution**:
```python
# Use larger timeframe
timeframe = "4h"  # Instead of "1h"

# Reduce date range
start_date = "2024-06-01"  # Instead of "2024-01-01"

# Enable data caching
ENABLE_CACHE=true
```

### Issue 4: CORS Errors

**Symptom**: Frontend can't connect to backend

**Solution**:
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

## 📚 Advanced Examples

### Example 1: Multi-Timeframe Analysis

```python
timeframes = ["1h", "4h", "1d"]
results = {}

for tf in timeframes:
    engine = BacktestEngine(
        symbol="BTC/USDT",
        timeframe=tf,
        start_date="2024-01-01",
        end_date="2024-12-31",
        strategy_name="rsi_macd",
        initial_balance=10000
    )
    results[tf] = engine.run()

# Compare results
for tf, result in results.items():
    print(f"{tf}: Return {result['total_return_pct']:.2f}%, Sharpe {result['sharpe_ratio']:.2f}")
```

### Example 2: Walk-Forward Validation

```python
# Split data into segments
segments = [
    ("2024-01-01", "2024-03-31"),  # Train
    ("2024-04-01", "2024-06-30"),  # Validate
    ("2024-07-01", "2024-09-30"),  # Test
    ("2024-10-01", "2024-12-31")   # Out-of-sample
]

results = []
for start, end in segments:
    engine = BacktestEngine(
        symbol="BTC/USDT",
        timeframe="1h",
        start_date=start,
        end_date=end,
        strategy_name="rsi_macd",
        initial_balance=10000
    )
    results.append(engine.run())

# Analyze performance across segments
for i, (segment, result) in enumerate(zip(segments, results)):
    print(f"Segment {i+1} ({segment[0]} to {segment[1]}):")
    print(f"  Return: {result['total_return_pct']:.2f}%")
    print(f"  Sharpe: {result['sharpe_ratio']:.2f}")
```

### Example 3: Strategy Comparison

```python
strategies = ["rsi_macd", "ema_cross", "bollinger", "combined"]
results = {}

for strategy_name in strategies:
    engine = BacktestEngine(
        symbol="BTC/USDT",
        timeframe="1h",
        start_date="2024-01-01",
        end_date="2024-12-31",
        strategy_name=strategy_name,
        initial_balance=10000
    )
    results[strategy_name] = engine.run()

# Find best strategy
best = max(results.items(), key=lambda x: x[1]['sharpe_ratio'])
print(f"Best strategy: {best[0]} (Sharpe: {best[1]['sharpe_ratio']:.2f})")

# Compare all strategies
for name, result in results.items():
    print(f"\n{name}:")
    print(f"  Return: {result['total_return_pct']:.2f}%")
    print(f"  Sharpe: {result['sharpe_ratio']:.2f}")
    print(f"  Max DD: {result['max_drawdown_pct']:.2f}%")
    print(f"  Win Rate: {result['win_rate']:.2f}%")
```

---

## 🎓 Learning Path

### Beginner

1. ✅ Run first backtest with built-in strategy
2. ✅ Understand performance metrics
3. ✅ Try different parameters
4. ✅ Compare multiple strategies

### Intermediate

1. ✅ Create custom strategy
2. ✅ Optimize parameters
3. ✅ Validate with walk-forward
4. ✅ Analyze trade history

### Advanced

1. ✅ Implement machine learning strategies
2. ✅ Multi-timeframe analysis
3. ✅ Portfolio optimization
4. ✅ Real-time paper trading

---

## 📞 Support

### Documentation

- **Backend**: `backend/backtesting/README.md`
- **Frontend**: `frontend/BACKTESTING.md`
- **API**: `backend/api/README.md`

### Examples

- **Python**: See `backend/backtesting/examples/`
- **JavaScript**: See `frontend/src/examples/`

### Community

- GitHub Issues: Report bugs
- GitHub Discussions: Ask questions
- Discord: Join community chat

---

## ✅ Checklist

Before running backtest:

- [ ] Backend server running
- [ ] Frontend server running
- [ ] Data collected (200+ candles)
- [ ] API keys configured (if using external APIs)
- [ ] Strategy registered (if using custom strategy)

After running backtest:

- [ ] Review performance metrics
- [ ] Check equity curve
- [ ] Analyze trade history
- [ ] Validate results with out-of-sample data
- [ ] Document findings

---

**Ready to start backtesting! 🚀**

Follow this guide to get up and running in 5 minutes. For detailed documentation, see the full README files.
