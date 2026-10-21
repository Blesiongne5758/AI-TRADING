# Backtesting Examples

## Example 1: Simple Backtest

### Python

```python
from backtesting.backtest_engine import BacktestEngine

# Create engine
engine = BacktestEngine(
    symbol="BTC/USDT",
    timeframe="1h",
    start_date="2024-01-01",
    end_date="2024-12-31",
    strategy_name="rsi_macd",
    strategy_params={
        "rsi_period": 14,
        "rsi_oversold": 30,
        "rsi_overbought": 70
    },
    initial_balance=10000,
    commission=0.001
)

# Run backtest
result = engine.run()

# Print results
print(f"Symbol: {result['symbol']}")
print(f"Strategy: {result['strategy']}")
print(f"Period: {result['start_date']} to {result['end_date']}")
print(f"\nPerformance:")
print(f"  Initial Balance: ${result['initial_balance']:,.2f}")
print(f"  Final Balance: ${result['final_balance']:,.2f}")
print(f"  Total Return: ${result['total_return']:,.2f}")
print(f"  Total Return %: {result['total_return_pct']:.2f}%")
print(f"  Sharpe Ratio: {result['sharpe_ratio']:.2f}")
print(f"  Max Drawdown: {result['max_drawdown_pct']:.2f}%")
print(f"  Win Rate: {result['win_rate']:.2f}%")
print(f"  Total Trades: {result['total_trades']}")
```

### JavaScript

```javascript
import axios from 'axios';

const runBacktest = async () => {
  const response = await axios.post('http://localhost:8000/api/backtest/run', {
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
  });

  const result = response.data;
  console.log('Backtest Result:', result);
  console.log(`Return: ${result.total_return_pct.toFixed(2)}%`);
  console.log(`Sharpe: ${result.sharpe_ratio.toFixed(2)}`);
};

runBacktest();
```

### cURL

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

## Example 2: Custom Strategy

### Create Custom Strategy

```python
# backend/analysis/momentum_strategy.py
from analysis.custom_strategies import BaseStrategy
import pandas as pd

class MomentumStrategy(BaseStrategy):
    """
    Momentum-based strategy
    Buy when price breaks above N-period high
    Sell when price breaks below N-period low
    """
    
    def __init__(self, params=None):
        super().__init__("Momentum Strategy", params)
        self.description = "Buy on breakout above N-period high"
        self.lookback = self.params.get('lookback', 20)
        self.threshold = self.params.get('threshold', 0.05)  # 5%
    
    def generate_signal(self, df: pd.DataFrame, index: int) -> dict:
        if index < self.lookback:
            return {
                "action": "HOLD",
                "confidence": 0,
                "stop_loss": 0,
                "take_profit": 0,
                "reason": "Insufficient data"
            }
        
        current_price = df['close'].iloc[index]
        
        # Calculate N-period high and low
        period_high = df['high'].iloc[index - self.lookback:index].max()
        period_low = df['low'].iloc[index - self.lookback:index].min()
        
        # Calculate momentum
        momentum = (current_price - period_low) / period_low
        
        # Buy signal: price breaks above period high with strong momentum
        if current_price > period_high and momentum > self.threshold:
            return {
                "action": "BUY",
                "confidence": min(momentum * 1000, 100),
                "stop_loss": current_price * 0.97,  # 3% below entry
                "take_profit": current_price * 1.10,  # 10% above entry
                "reason": f"Breakout with {momentum:.2%} momentum"
            }
        
        # Sell signal: price breaks below period low
        elif current_price < period_low:
            return {
                "action": "SELL",
                "confidence": min(abs(momentum) * 1000, 100),
                "stop_loss": current_price * 1.03,  # 3% above entry
                "take_profit": current_price * 0.90,  # 10% below entry
                "reason": f"Breakdown with {momentum:.2%} momentum"
            }
        
        return {
            "action": "HOLD",
            "confidence": 50,
            "stop_loss": 0,
            "take_profit": 0,
            "reason": "No signal"
        }
```

### Register Strategy

```python
# backend/analysis/custom_strategies.py
from .momentum_strategy import MomentumStrategy

# Add to available strategies
StrategyFactory.AVAILABLE_STRATEGIES["momentum"] = MomentumStrategy
```

### Use Custom Strategy

```python
from backtesting.backtest_engine import BacktestEngine

engine = BacktestEngine(
    symbol="BTC/USDT",
    timeframe="1h",
    start_date="2024-01-01",
    end_date="2024-12-31",
    strategy_name="momentum",
    strategy_params={
        "lookback": 20,
        "threshold": 0.05
    },
    initial_balance=10000
)

result = engine.run()
print(f"Return: {result['total_return_pct']:.2f}%")
```

---

## Example 3: Parameter Optimization

### Grid Search

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

# Define parameter ranges
param_ranges = {
    "rsi_period": [10, 14, 20, 25],
    "rsi_oversold": [20, 25, 30, 35],
    "rsi_overbought": [65, 70, 75, 80]
}

# Run optimization
result = optimizer.optimize(
    param_ranges=param_ranges,
    optimization_metric="sharpe_ratio",
    n_trials=64  # 4 x 4 x 4 combinations
)

print(f"Best parameters: {result['best_params']}")
print(f"Best Sharpe Ratio: {result['best_score']:.2f}")

# Show top 5 results
print("\nTop 5 parameter sets:")
for i, r in enumerate(result['all_results'][:5], 1):
    print(f"{i}. Params: {r['parameters']}")
    print(f"   Sharpe: {r['metrics']['sharpe_ratio']:.2f}")
    print(f"   Return: {r['metrics']['total_return_pct']:.2f}%")
```

### Bayesian Optimization

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

# Define parameter ranges (continuous)
param_ranges = {
    "rsi_period": (10, 30),      # Integer range
    "rsi_oversold": (20, 40),    # Integer range
    "rsi_overbought": (60, 80)   # Integer range
}

# Run Bayesian optimization
result = optimizer.optimize_bayesian(
    param_ranges=param_ranges,
    optimization_metric="sharpe_ratio",
    n_trials=100
)

print(f"Best parameters: {result['best_params']}")
print(f"Best Sharpe Ratio: {result['best_score']:.2f}")

# Plot optimization history
optimizer.plot_optimization_history(
    result['study'],
    "optimization_history.png"
)
```

---

## Example 4: Multi-Timeframe Analysis

```python
from backtesting.backtest_engine import BacktestEngine

timeframes = ["15m", "1h", "4h", "1d"]
results = {}

for tf in timeframes:
    print(f"\nTesting timeframe: {tf}")
    
    engine = BacktestEngine(
        symbol="BTC/USDT",
        timeframe=tf,
        start_date="2024-01-01",
        end_date="2024-12-31",
        strategy_name="rsi_macd",
        strategy_params={
            "rsi_period": 14,
            "rsi_oversold": 30,
            "rsi_overbought": 70
        },
        initial_balance=10000
    )
    
    result = engine.run()
    results[tf] = result
    
    print(f"  Return: {result['total_return_pct']:.2f}%")
    print(f"  Sharpe: {result['sharpe_ratio']:.2f}")
    print(f"  Max DD: {result['max_drawdown_pct']:.2f}%")
    print(f"  Trades: {result['total_trades']}")

# Find best timeframe
best_tf = max(results.items(), key=lambda x: x[1]['sharpe_ratio'])
print(f"\nBest timeframe: {best_tf[0]} (Sharpe: {best_tf[1]['sharpe_ratio']:.2f})")
```

---

## Example 5: Walk-Forward Validation

```python
from backtesting.backtest_engine import BacktestEngine
from backtesting.optimizer import ParameterOptimizer

# Define segments
segments = [
    ("2024-01-01", "2024-03-31", "Train"),
    ("2024-04-01", "2024-06-30", "Validate"),
    ("2024-07-01", "2024-09-30", "Test"),
    ("2024-10-01", "2024-12-31", "Out-of-Sample")
]

results = []

for start, end, label in segments:
    print(f"\n{label} segment: {start} to {end}")
    
    if label == "Train":
        # Optimize parameters on training data
        optimizer = ParameterOptimizer(
            symbol="BTC/USDT",
            timeframe="1h",
            start_date=start,
            end_date=end,
            strategy_name="rsi_macd",
            initial_balance=10000
        )
        
        opt_result = optimizer.optimize(
            param_ranges={
                "rsi_period": [10, 14, 20],
                "rsi_oversold": [25, 30, 35],
                "rsi_overbought": [65, 70, 75]
            },
            optimization_metric="sharpe_ratio"
        )
        
        best_params = opt_result['best_params']
        print(f"  Optimized parameters: {best_params}")
    
    # Run backtest with current parameters
    engine = BacktestEngine(
        symbol="BTC/USDT",
        timeframe="1h",
        start_date=start,
        end_date=end,
        strategy_name="rsi_macd",
        strategy_params=best_params if label != "Train" else {},
        initial_balance=10000
    )
    
    result = engine.run()
    results.append({
        "segment": label,
        "start": start,
        "end": end,
        "return": result['total_return_pct'],
        "sharpe": result['sharpe_ratio'],
        "max_dd": result['max_drawdown_pct'],
        "trades": result['total_trades']
    })
    
    print(f"  Return: {result['total_return_pct']:.2f}%")
    print(f"  Sharpe: {result['sharpe_ratio']:.2f}")
    print(f"  Max DD: {result['max_drawdown_pct']:.2f}%")

# Analyze results
print("\n" + "="*60)
print("Walk-Forward Analysis Summary")
print("="*60)

for r in results:
    print(f"\n{r['segment']} ({r['start']} to {r['end']}):")
    print(f"  Return: {r['return']:.2f}%")
    print(f"  Sharpe: {r['sharpe']:.2f}")
    print(f"  Max DD: {r['max_dd']:.2f}%")
    print(f"  Trades: {r['trades']}")

# Check consistency
returns = [r['return'] for r in results]
avg_return = sum(returns) / len(returns)
print(f"\nAverage Return: {avg_return:.2f}%")
print(f"Consistency: {'Good' if all(r > 0 for r in returns) else 'Poor'}")
```

---

## Example 6: Strategy Comparison

```python
from backtesting.backtest_engine import BacktestEngine

strategies = {
    "rsi_macd": {
        "rsi_period": 14,
        "rsi_oversold": 30,
        "rsi_overbought": 70
    },
    "ema_cross": {
        "fast_ema": 20,
        "slow_ema": 50
    },
    "bollinger": {
        "bb_period": 20,
        "bb_std": 2
    },
    "combined": {
        "rsi_period": 14,
        "rsi_oversold": 35,
        "rsi_overbought": 65,
        "ema_fast": 20,
        "ema_slow": 50
    }
}

results = {}

for strategy_name, params in strategies.items():
    print(f"\nTesting strategy: {strategy_name}")
    
    engine = BacktestEngine(
        symbol="BTC/USDT",
        timeframe="1h",
        start_date="2024-01-01",
        end_date="2024-12-31",
        strategy_name=strategy_name,
        strategy_params=params,
        initial_balance=10000
    )
    
    result = engine.run()
    results[strategy_name] = result
    
    print(f"  Return: {result['total_return_pct']:.2f}%")
    print(f"  Sharpe: {result['sharpe_ratio']:.2f}")
    print(f"  Max DD: {result['max_drawdown_pct']:.2f}%")
    print(f"  Win Rate: {result['win_rate']:.2f}%")

# Compare results
print("\n" + "="*80)
print("Strategy Comparison")
print("="*80)
print(f"{'Strategy':<15} {'Return %':<12} {'Sharpe':<10} {'Max DD %':<12} {'Win Rate %':<12} {'Trades':<10}")
print("-"*80)

for name, result in results.items():
    print(f"{name:<15} {result['total_return_pct']:>10.2f}% {result['sharpe_ratio']:>8.2f} "
          f"{result['max_drawdown_pct']:>10.2f}% {result['win_rate']:>10.2f}% {result['total_trades']:>8}")

# Find best strategy by Sharpe ratio
best = max(results.items(), key=lambda x: x[1]['sharpe_ratio'])
print(f"\nBest strategy: {best[0]} (Sharpe: {best[1]['sharpe_ratio']:.2f})")
```

---

## Example 7: Advanced Indicators

```python
from analysis.indicators_advanced import AdvancedIndicators
import pandas as pd

# Load data
df = pd.read_csv('btc_1h.csv', parse_dates=['timestamp'])
df.set_index('timestamp', inplace=True)

# Initialize indicators
indicators = AdvancedIndicators()

# Calculate all advanced indicators
results = indicators.calculate_all(df)

# Ichimoku Cloud
print("Ichimoku Cloud:")
print(f"  Signal: {results['ichimoku']['signal']}")
print(f"  Score: {results['ichimoku']['score']}")
print(f"  Price Position: {results['ichimoku']['price_position']}")
print(f"  TK Cross: {results['ichimoku']['tk_cross']}")

# Fibonacci Retracement
print("\nFibonacci Retracement:")
print(f"  Signal: {results['fibonacci']['signal']}")
print(f"  Score: {results['fibonacci']['score']}")
print(f"  Position: {results['fibonacci']['position']}")
print(f"  Nearest Level: {results['fibonacci']['nearest_level']}")
print(f"  Distance: {results['fibonacci']['distance_to_nearest']:.2f}%")

# Pivot Points
print("\nPivot Points:")
print(f"  Signal: {results['pivot_points']['signal']}")
print(f"  Score: {results['pivot_points']['score']}")
print(f"  Position: {results['pivot_points']['position']}")
print(f"  Pivot: ${results['pivot_points']['pivot']:,.2f}")
print(f"  R1: ${results['pivot_points']['r1']:,.2f}")
print(f"  S1: ${results['pivot_points']['s1']:,.2f}")

# VWAP
print("\nVWAP:")
print(f"  Signal: {results['vwap']['signal']}")
print(f"  Score: {results['vwap']['score']}")
print(f"  VWAP: ${results['vwap']['vwap']:,.2f}")
print(f"  Price vs VWAP: {results['vwap']['price_vs_vwap']:+.2f}%")

# ATR Trailing Stop
print("\nATR Trailing Stop:")
print(f"  Trend: {results['atr_trailing_stop']['trend']}")
print(f"  ATR: ${results['atr_trailing_stop']['atr']:,.2f}")
print(f"  Recommended Stop: ${results['atr_trailing_stop']['recommended_stop']:,.2f}")
print(f"  Distance: {results['atr_trailing_stop']['distance_percent']:.2f}%")

# Overall
print("\nOverall:")
print(f"  Signal: {results['overall']['signal']}")
print(f"  Score: {results['overall']['score']:.1f}")
```

---

## Example 8: Pump & Dump Detection

```python
from advanced_ai.pump_dump_detector import PumpDumpDetector
import pandas as pd

# Load data
df = pd.read_csv('shib_1h.csv', parse_dates=['timestamp'])
df.set_index('timestamp', inplace=True)

# Prepare data
price_data = {
    "current": df['close'].iloc[-1],
    "1h_ago": df['close'].iloc[-2],
    "24h_ago": df['close'].iloc[-24],
    "high_24h": df['high'].tail(24).max(),
    "low_24h": df['low'].tail(24).min()
}

volume_data = df['volume'].tail(24).tolist()

# Social media mentions (example)
social_mentions = [
    {"text": "SHIB to the moon!", "engagement_score": 150},
    {"text": "SHIB 100x incoming!", "engagement_score": 200},
    {"text": "Buy SHIB now!", "engagement_score": 180},
    # ... more mentions
]

# Detect pump & dump
detector = PumpDumpDetector()
result = detector.detect_pump_and_dump(
    candles=df,
    tweets=social_mentions,
    time_window_minutes=60
)

# Print results
print("Pump & Dump Detection:")
print(f"  Detected: {result['pump_dump_detected']}")
print(f"  Overall Risk: {result['overall_risk']}")
print(f"  Risk Score: {result['risk_score']:.2f}")

print("\nVolume Analysis:")
print(f"  Anomaly: {result['volume_analysis']['anomaly_detected']}")
print(f"  Volume Ratio: {result['volume_analysis']['volume_ratio']:.2f}x")

print("\nPrice Analysis:")
print(f"  Spike: {result['price_analysis']['spike_detected']}")
print(f"  Price Change: {result['price_analysis']['price_change_percent']:+.2f}%")

print("\nHype Analysis:")
print(f"  Hype Score: {result['hype_analysis']['hype_score']:.2f}")
print(f"  Hype Level: {result['hype_analysis']['hype_level']}")

print(f"\nRecommendation: {result['recommendation']}")
```

---

## Example 9: Sentiment Aggregation

```python
from advanced_ai.sentiment_aggregator import SentimentAggregator
import asyncio

async def analyze_sentiment():
    # Initialize aggregator
    aggregator = SentimentAggregator()
    
    # Analyze sentiment for BTC
    result = await aggregator.analyze_symbol(
        symbol="BTC/USDT",
        currency_code="BTC",
        include_pump_detection=True
    )
    
    # Print results
    print(f"Symbol: {result['symbol']}")
    print(f"Sentiment: {result['label']}")
    print(f"Score: {result['final_score']:+.3f}")
    print(f"Confidence: {result['confidence']}%")
    print(f"Total Samples: {result['total_samples']}")
    
    print("\nSource Breakdown:")
    for source, data in result['source_breakdown'].items():
        print(f"  {source}:")
        print(f"    Score: {data['score']:+.3f}")
        print(f"    Weight: {data['weight']:.0%}")
        print(f"    Samples: {data['sample_size']}")
    
    print("\nTop Positive Articles:")
    for article in result['top_positive'][:3]:
        print(f"  [{article['score']:+.3f}] {article['text'][:80]}...")
    
    print("\nTop Negative Articles:")
    for article in result['top_negative'][:3]:
        print(f"  [{article['score']:+.3f}] {article['text'][:80]}...")
    
    # Cleanup
    await aggregator.close()

# Run
asyncio.run(analyze_sentiment())
```

---

## Example 10: Complete Trading Pipeline

```python
from advanced_ai.sentiment_aggregator import SentimentAggregator
from advanced_ai.pump_dump_detector import PumpDumpDetector
from backtesting.backtest_engine import BacktestEngine
import asyncio

async def complete_analysis(symbol: str):
    """Complete analysis pipeline before trading"""
    
    print(f"\n{'='*70}")
    print(f"Analyzing {symbol}")
    print(f"{'='*70}")
    
    # 1. Sentiment Analysis
    print("\n1. Sentiment Analysis...")
    aggregator = SentimentAggregator()
    sentiment = await aggregator.analyze_symbol(symbol)
    
    print(f"   Label: {sentiment['label']}")
    print(f"   Score: {sentiment['final_score']:+.3f}")
    print(f"   Confidence: {sentiment['confidence']}%")
    
    # 2. Pump Detection
    print("\n2. Pump Detection...")
    detector = PumpDumpDetector()
    
    # Get price and volume data (from your data source)
    price_data = get_price_data(symbol)  # Implement this
    volume_data = get_volume_data(symbol)  # Implement this
    
    pump_result = detector.analyze_symbol(
        symbol=symbol,
        price_data=price_data,
        volume_data=volume_data,
        social_mentions=sentiment.get('tweets', [])
    )
    
    print(f"   Pattern: {pump_result['pattern']}")
    print(f"   Risk: {pump_result['overall_risk']}")
    print(f"   Recommendation: {pump_result['recommendation']}")
    
    # 3. Backtest Strategy
    print("\n3. Backtesting Strategy...")
    engine = BacktestEngine(
        symbol=symbol,
        timeframe="1h",
        start_date="2024-01-01",
        end_date="2024-12-31",
        strategy_name="rsi_macd",
        initial_balance=10000
    )
    
    backtest_result = engine.run()
    
    print(f"   Return: {backtest_result['total_return_pct']:.2f}%")
    print(f"   Sharpe: {backtest_result['sharpe_ratio']:.2f}")
    print(f"   Max DD: {backtest_result['max_drawdown_pct']:.2f}%")
    print(f"   Win Rate: {backtest_result['win_rate']:.2f}%")
    
    # 4. Trading Decision
    print("\n4. Trading Decision...")
    
    # Check pump warning
    if pump_result['pump_dump_detected']:
        print(f"   ❌ AVOID: {pump_result['recommendation']}")
        decision = "SKIP"
    
    # Check sentiment
    elif sentiment['confidence'] < 60:
        print(f"   ⚠️  LOW CONFIDENCE: Sentiment confidence too low")
        decision = "SKIP"
    
    # Check backtest performance
    elif backtest_result['sharpe_ratio'] < 1.0:
        print(f"   ⚠️  POOR PERFORMANCE: Sharpe ratio too low")
        decision = "SKIP"
    
    # Make trading decision
    elif sentiment['label'] == 'BULLISH' and backtest_result['total_return_pct'] > 10:
        print(f"   ✅ BUY: Strong bullish sentiment + good backtest performance")
        decision = "BUY"
    
    elif sentiment['label'] == 'BEARISH' and backtest_result['total_return_pct'] < -10:
        print(f"   ✅ SELL: Strong bearish sentiment + good backtest performance")
        decision = "SELL"
    
    else:
        print(f"   ⚠️  HOLD: Mixed signals")
        decision = "HOLD"
    
    # 5. Position Sizing
    if decision in ["BUY", "SELL"]:
        position_size = calculate_position_size(
            balance=10000,
            confidence=sentiment['confidence'],
            risk_per_trade=0.02  # 2%
        )
        print(f"\n5. Position Sizing:")
        print(f"   Position Size: ${position_size:,.2f}")
        print(f"   Risk: ${position_size * 0.02:,.2f} (2%)")
    
    # Cleanup
    await aggregator.close()
    
    return {
        "symbol": symbol,
        "decision": decision,
        "sentiment": sentiment,
        "pump_warning": pump_result['pump_dump_detected'],
        "backtest": backtest_result
    }

def calculate_position_size(balance, confidence, risk_per_trade):
    """Calculate position size based on confidence"""
    if confidence >= 75:
        return balance * 0.10  # 10%
    elif confidence >= 60:
        return balance * 0.05  # 5%
    else:
        return balance * 0.02  # 2%

# Run analysis
async def main():
    symbols = ["BTC/USDT", "ETH/USDT", "SOL/USDT"]
    
    for symbol in symbols:
        result = await complete_analysis(symbol)
        print(f"\n{'='*70}")
        print(f"Final Decision for {symbol}: {result['decision']}")
        print(f"{'='*70}")

asyncio.run(main())
```

---

## Example 11: Frontend Integration

### React Component

```jsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';

function BacktestDashboard() {
  const [strategies, setStrategies] = useState([]);
  const [selectedStrategy, setSelectedStrategy] = useState('rsi_macd');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Load available strategies
    axios.get('http://localhost:8000/api/backtest/strategies')
      .then(response => setStrategies(response.data))
      .catch(error => console.error(error));
  }, []);

  const runBacktest = async () => {
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/api/backtest/run', {
        symbol: 'BTC/USDT',
        timeframe: '1h',
        start_date: '2024-01-01',
        end_date: '2024-12-31',
        strategy: selectedStrategy,
        initial_balance: 10000
      });
      setResult(response.data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Backtest Dashboard</h1>
      
      <div className="mb-4">
        <label className="block mb-2">Strategy:</label>
        <select 
          value={selectedStrategy}
          onChange={(e) => setSelectedStrategy(e.target.value)}
          className="border rounded px-3 py-2"
        >
          {strategies.map(s => (
            <option key={s.name} value={s.name}>{s.name}</option>
          ))}
        </select>
      </div>
      
      <button 
        onClick={runBacktest}
        disabled={loading}
        className="bg-blue-500 text-white px-4 py-2 rounded"
      >
        {loading ? 'Running...' : 'Run Backtest'}
      </button>
      
      {result && (
        <div className="mt-6">
          <h2 className="text-xl font-bold mb-4">Results</h2>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <p>Return: {result.total_return_pct.toFixed(2)}%</p>
              <p>Sharpe: {result.sharpe_ratio.toFixed(2)}</p>
              <p>Max DD: {result.max_drawdown_pct.toFixed(2)}%</p>
            </div>
            <div>
              <p>Win Rate: {result.win_rate.toFixed(2)}%</p>
              <p>Trades: {result.total_trades}</p>
              <p>Profit Factor: {result.profit_factor.toFixed(2)}</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default BacktestDashboard;
```

---

## Example 12: Export Results

### Export to CSV

```python
import pandas as pd
from backtesting.backtest_engine import BacktestEngine

# Run backtest
engine = BacktestEngine(
    symbol="BTC/USDT",
    timeframe="1h",
    start_date="2024-01-01",
    end_date="2024-12-31",
    strategy_name="rsi_macd",
    initial_balance=10000
)

result = engine.run()

# Export trades to CSV
trades_df = pd.DataFrame(result['trades'])
trades_df.to_csv('backtest_trades.csv', index=False)

# Export equity curve to CSV
equity_df = pd.DataFrame(result['equity_curve'])
equity_df.to_csv('equity_curve.csv', index=False)

# Export summary to CSV
summary_df = pd.DataFrame([{
    'symbol': result['symbol'],
    'strategy': result['strategy'],
    'total_return_pct': result['total_return_pct'],
    'sharpe_ratio': result['sharpe_ratio'],
    'max_drawdown_pct': result['max_drawdown_pct'],
    'win_rate': result['win_rate'],
    'total_trades': result['total_trades']
}])
summary_df.to_csv('backtest_summary.csv', index=False)

print("Results exported to CSV files")
```

### Export to JSON

```python
import json

# Export full result to JSON
with open('backtest_result.json', 'w') as f:
    json.dump(result, f, indent=2, default=str)

print("Result exported to JSON")
```

---

## Example 13: Visualization

```python
import matplotlib.pyplot as plt
import pandas as pd
from backtesting.backtest_engine import BacktestEngine

# Run backtest
engine = BacktestEngine(
    symbol="BTC/USDT",
    timeframe="1h",
    start_date="2024-01-01",
    end_date="2024-12-31",
    strategy_name="rsi_macd",
    initial_balance=10000
)

result = engine.run()

# Plot equity curve
equity_df = pd.DataFrame(result['equity_curve'])
equity_df['timestamp'] = pd.to_datetime(equity_df['timestamp'])

plt.figure(figsize=(14, 7))
plt.plot(equity_df['timestamp'], equity_df['balance'], label='Portfolio Value')
plt.axhline(y=10000, color='r', linestyle='--', label='Initial Balance')
plt.xlabel('Date')
plt.ylabel('Balance ($)')
plt.title('Equity Curve')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('equity_curve.png', dpi=150)
plt.show()

# Plot drawdown
plt.figure(figsize=(14, 5))
plt.fill_between(equity_df['timestamp'], equity_df['drawdown'], 0, 
                 color='red', alpha=0.3, label='Drawdown')
plt.plot(equity_df['timestamp'], equity_df['drawdown'], 
         color='red', linewidth=1)
plt.xlabel('Date')
plt.ylabel('Drawdown (%)')
plt.title('Drawdown Chart')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('drawdown.png', dpi=150)
plt.show()

# Plot trade distribution
trades_df = pd.DataFrame(result['trades'])
plt.figure(figsize=(10, 6))
plt.hist(trades_df['pnl'], bins=30, color='blue', alpha=0.7, edgecolor='black')
plt.axvline(x=0, color='red', linestyle='--', linewidth=2)
plt.xlabel('PnL ($)')
plt.ylabel('Frequency')
plt.title('Trade PnL Distribution')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('trade_distribution.png', dpi=150)
plt.show()
```

---

These examples demonstrate various use cases for the backtesting system. Adapt them to your specific needs and trading strategies.
