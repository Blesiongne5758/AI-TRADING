# Backtesting Engine Documentation

## Overview

Backtesting Engine adalah sistem komprehensif untuk menguji trading strategies menggunakan historical data. Sistem ini mencakup:

- **Advanced Indicators**: Ichimoku Cloud, Fibonacci Retracement, Pivot Points, VWAP, ATR Trailing Stop
- **Custom Strategies Framework**: Buat strategy sendiri dengan mudah
- **Performance Metrics**: Sharpe Ratio, Sortino Ratio, Max Drawdown, Win Rate, Profit Factor, dll
- **Parameter Optimization**: Optimize strategy parameters dengan Optuna
- **REST API**: Endpoints untuk menjalankan backtest dari frontend
- **Interactive UI**: Visualisasi results dengan charts dan tables

## Architecture

```
backend/
├── analysis/
│   ├── indicators_advanced.py    # Ichimoku, Fibonacci, Pivot Points, VWAP, ATR
│   └── custom_strategies.py      # Custom strategies framework
├── backtesting/
│   ├── backtest_engine.py        # Core backtesting engine
│   └── optimizer.py              # Parameter optimization
└── api/routes/
    └── backtest.py               # REST API endpoints

frontend/
└── src/
    ├── components/
    │   ├── BacktestPanel.jsx     # Configuration UI
    │   ├── StrategyEditor.jsx    # Custom strategy editor
    │   └── BacktestResults.jsx   # Results visualization
    └── pages/
        └── Backtest.jsx          # Main backtesting page
```

## Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Run Backtest via API

```bash
# Start backend server
cd backend
python -m api.main

# In another terminal, run backtest
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

### 3. Run Backtest via Frontend

1. Start backend: `python -m api.main`
2. Start frontend: `cd frontend && npm run dev`
3. Open browser: `http://localhost:5173/backtest`
4. Configure parameters dan click "Run Backtest"

## Available Strategies

### Built-in Strategies

#### 1. RSI + MACD Strategy (`rsi_macd`)

**Description**: Buy when RSI < 30 and MACD crosses above signal line

**Parameters**:
- `rsi_period` (default: 14): RSI calculation period
- `rsi_oversold` (default: 30): RSI oversold threshold
- `rsi_overbought` (default: 70): RSI overbought threshold
- `macd_fast` (default: 12): Fast EMA period
- `macd_slow` (default: 26): Slow EMA period
- `macd_signal` (default: 9): Signal line period

**Example**:
```python
from analysis.custom_strategies import StrategyFactory

strategy = StrategyFactory.create_strategy("rsi_macd", {
    "rsi_period": 14,
    "rsi_oversold": 30,
    "rsi_overbought": 70
})
```

#### 2. EMA Crossover Strategy (`ema_cross`)

**Description**: Buy when fast EMA crosses above slow EMA

**Parameters**:
- `fast_ema` (default: 20): Fast EMA period
- `slow_ema` (default: 50): Slow EMA period

#### 3. Bollinger Bands Strategy (`bollinger`)

**Description**: Buy when price touches lower band, sell when touches upper band

**Parameters**:
- `bb_period` (default: 20): Bollinger Bands period
- `bb_std` (default: 2): Standard deviation multiplier

#### 4. Combined Strategy (`combined`)

**Description**: Combines RSI, MACD, and EMA for stronger signals

**Parameters**:
- `rsi_period` (default: 14)
- `rsi_oversold` (default: 35)
- `rsi_overbought` (default: 65)
- `ema_fast` (default: 20)
- `ema_slow` (default: 50)

### Custom Strategies

Create your own strategy:

```python
from analysis.custom_strategies import BaseStrategy
import pandas as pd

class MyCustomStrategy(BaseStrategy):
    def __init__(self, params=None):
        super().__init__("My Custom Strategy", params)
        self.description = "My custom trading logic"
        self.my_param = self.params.get('my_param', 10)
    
    def generate_signal(self, df: pd.DataFrame, index: int) -> dict:
        """
        Generate trading signal
        
        Args:
            df: DataFrame dengan OHLCV data
            index: Current candle index
            
        Returns:
            {
                "action": "BUY" | "SELL" | "HOLD",
                "confidence": float (0-100),
                "stop_loss": float,
                "take_profit": float,
                "reason": str
            }
        """
        current_price = df['close'].iloc[index]
        
        # Your custom logic here
        if current_price > df['close'].iloc[index - self.my_param]:
            return {
                "action": "BUY",
                "confidence": 70,
                "stop_loss": current_price * 0.98,
                "take_profit": current_price * 1.05,
                "reason": "Price broke above previous high"
            }
        
        return {
            "action": "HOLD",
            "confidence": 50,
            "stop_loss": 0,
            "take_profit": 0,
            "reason": "No signal"
        }
```

Register custom strategy:

```python
from analysis.custom_strategies import StrategyFactory

StrategyFactory.AVAILABLE_STRATEGIES["my_custom"] = MyCustomStrategy
```

## Advanced Indicators

### Ichimoku Cloud

Complete Ichimoku system dengan 5 components:

```python
from analysis.indicators_advanced import AdvancedIndicators

indicators = AdvancedIndicators()
result = indicators.calculate_ichimoku(df)

# Returns:
{
    "tenkan_sen": 42500.5,      # Conversion Line
    "kijun_sen": 42300.2,       # Base Line
    "senkou_span_a": 42400.3,   # Leading Span A
    "senkou_span_b": 42200.1,   # Leading Span B
    "chikou_span": 42100.8,     # Lagging Span
    "cloud_bullish": True,      # Cloud color
    "price_position": "ABOVE_CLOUD",
    "signal": "BULLISH",
    "score": 85                 # -100 to +100
}
```

### Fibonacci Retracement

Calculate key support/resistance levels:

```python
result = indicators.calculate_fibonacci_retracement(df, lookback_period=100)

# Returns:
{
    "swing_high": 45000.0,
    "swing_low": 40000.0,
    "fib_levels": {
        "0.0%": 45000.0,
        "23.6%": 43820.0,
        "38.2%": 43090.0,
        "50.0%": 42500.0,
        "61.8%": 41910.0,
        "78.6%": 41073.0,
        "100.0%": 40000.0
    },
    "current_price": 43500.0,
    "position": "BETWEEN_23.6_38.2",
    "signal": "NEUTRAL",
    "nearest_level": "23.6%",
    "score": 30
}
```

### Pivot Points

Classic pivot points dengan support/resistance:

```python
result = indicators.calculate_pivot_points(df)

# Returns:
{
    "pivot": 42500.0,
    "r1": 43000.0,  # Resistance 1
    "r2": 43500.0,  # Resistance 2
    "r3": 44000.0,  # Resistance 3
    "s1": 42000.0,  # Support 1
    "s2": 41500.0,  # Support 2
    "s3": 41000.0,  # Support 3
    "position": "BETWEEN_PIVOT_R1",
    "signal": "SLIGHTLY_BULLISH",
    "score": 20
}
```

### VWAP (Volume Weighted Average Price)

```python
result = indicators.calculate_vwap(df)

# Returns:
{
    "vwap": 42350.5,
    "current_price": 42500.0,
    "price_vs_vwap": 0.35,  # Percentage
    "signal": "BULLISH",
    "score": 40
}
```

### ATR Trailing Stop

Dynamic stop-loss based on volatility:

```python
result = indicators.calculate_atr_trailing_stop(df, atr_period=14, multiplier=2.0)

# Returns:
{
    "atr": 450.5,
    "trailing_stop_long": 41600.0,
    "trailing_stop_short": 43400.0,
    "recommended_stop": 41600.0,
    "trend": "UPTREND",
    "distance_percent": 2.12
}
```

## Performance Metrics

Backtest engine calculates comprehensive performance metrics:

### Return Metrics
- **Total Return**: Absolute profit/loss in USD
- **Total Return %**: Percentage return
- **Annualized Return**: Yearly return rate
- **CAGR**: Compound Annual Growth Rate

### Risk Metrics
- **Max Drawdown**: Largest peak-to-trough decline (USD)
- **Max Drawdown %**: Largest decline percentage
- **Volatility**: Standard deviation of returns
- **Downside Risk**: Negative returns only

### Risk-Adjusted Metrics
- **Sharpe Ratio**: Return per unit of total risk
- **Sortino Ratio**: Return per unit of downside risk
- **Calmar Ratio**: Annualized return / Max drawdown

### Trade Statistics
- **Total Trades**: Number of trades executed
- **Winning Trades**: Number of profitable trades
- **Losing Trades**: Number of losing trades
- **Win Rate**: Percentage of winning trades
- **Average Win**: Average profit per winning trade
- **Average Loss**: Average loss per losing trade
- **Largest Win**: Biggest single trade profit
- **Largest Loss**: Biggest single trade loss
- **Profit Factor**: Gross profit / Gross loss
- **Expectancy**: Expected profit per trade
- **Payoff Ratio**: Average win / Average loss

### Example Output

```json
{
  "total_return": 2534.50,
  "total_return_pct": 25.35,
  "annualized_return": 25.35,
  "max_drawdown": -845.20,
  "max_drawdown_pct": -8.45,
  "sharpe_ratio": 2.45,
  "sortino_ratio": 3.12,
  "calmar_ratio": 3.00,
  "total_trades": 47,
  "winning_trades": 32,
  "losing_trades": 15,
  "win_rate": 68.09,
  "avg_win": 185.50,
  "avg_loss": -95.20,
  "profit_factor": 2.35,
  "expectancy": 53.92
}
```

## Parameter Optimization

Optimize strategy parameters using Optuna:

```python
from backtesting.optimizer import ParameterOptimizer

optimizer = ParameterOptimizer(
    symbol="BTC/USDT",
    timeframe="1h",
    start_date="2024-01-01",
    end_date="2024-12-31",
    strategy_name="rsi_macd",
    initial_balance=10000
)

# Define parameter ranges
param_ranges = {
    "rsi_period": [10, 14, 20],
    "rsi_oversold": [25, 30, 35],
    "rsi_overbought": [65, 70, 75]
}

# Run optimization
result = optimizer.optimize(
    param_ranges=param_ranges,
    optimization_metric="sharpe_ratio",
    n_trials=50
)

print(f"Best parameters: {result['best_params']}")
print(f"Best Sharpe Ratio: {result['best_score']:.2f}")
```

### Optimization Metrics

Choose which metric to optimize:
- `sharpe_ratio`: Risk-adjusted return (recommended)
- `total_return_pct`: Total percentage return
- `win_rate`: Percentage of winning trades
- `profit_factor`: Gross profit / Gross loss
- `max_drawdown_pct`: Minimize drawdown (use negative)

### Via API

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

## API Endpoints

### POST /api/backtest/run

Run backtest dengan parameters tertentu.

**Request**:
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
  "initial_balance": 10000,
  "commission": 0.001
}
```

**Response**:
```json
{
  "id": "bt_20241215_143022_BTC_USDT",
  "status": "completed",
  "symbol": "BTC/USDT",
  "timeframe": "1h",
  "strategy": "rsi_macd",
  "start_date": "2024-01-01",
  "end_date": "2024-12-31",
  "initial_balance": 10000,
  "final_balance": 12534.50,
  "total_return": 2534.50,
  "total_return_pct": 25.35,
  "max_drawdown": -845.20,
  "max_drawdown_pct": -8.45,
  "sharpe_ratio": 2.45,
  "win_rate": 68.09,
  "total_trades": 47,
  "winning_trades": 32,
  "losing_trades": 15,
  "avg_win": 185.50,
  "avg_loss": -95.20,
  "profit_factor": 2.35,
  "created_at": "2024-12-15T14:30:22"
}
```

### GET /api/backtest/strategies

List semua available strategies.

**Response**:
```json
[
  {
    "name": "rsi_macd",
    "description": "Buy when RSI < 30 and MACD crosses above signal line",
    "parameters": {
      "rsi_period": {"type": "int", "default": 14, "min": 5, "max": 50},
      "rsi_oversold": {"type": "float", "default": 30, "min": 10, "max": 50},
      "rsi_overbought": {"type": "float", "default": 70, "min": 50, "max": 90}
    },
    "default_params": {
      "rsi_period": 14,
      "rsi_oversold": 30,
      "rsi_overbought": 70
    }
  }
]
```

### GET /api/backtest/results/{backtest_id}

Get detailed results untuk specific backtest.

### GET /api/backtest/results

List semua backtest results dengan pagination.

**Query Parameters**:
- `limit`: Number of results per page (default: 10)
- `offset`: Offset for pagination (default: 0)

### DELETE /api/backtest/results/{backtest_id}

Delete specific backtest result.

### POST /api/backtest/optimize

Optimize strategy parameters.

**Request**:
```json
{
  "symbol": "BTC/USDT",
  "timeframe": "1h",
  "start_date": "2024-01-01",
  "end_date": "2024-12-31",
  "strategy": "rsi_macd",
  "param_ranges": {
    "rsi_period": [10, 14, 20],
    "rsi_oversold": [25, 30, 35]
  },
  "optimization_metric": "sharpe_ratio",
  "initial_balance": 10000
}
```

**Response**:
```json
{
  "id": "opt_20241215_143022_BTC_USDT",
  "status": "completed",
  "strategy": "rsi_macd",
  "optimization_metric": "sharpe_ratio",
  "best_params": {
    "rsi_period": 14,
    "rsi_oversold": 30
  },
  "best_score": 2.45,
  "total_combinations": 9,
  "created_at": "2024-12-15T14:30:22"
}
```

## Frontend Components

### BacktestPanel.jsx

Configuration panel untuk running backtest:

**Features**:
- Symbol selection
- Timeframe selection
- Date range picker
- Strategy selection dengan dynamic parameters
- Initial balance dan commission settings
- Real-time validation

**Usage**:
```jsx
import BacktestPanel from './components/BacktestPanel';

<BacktestPanel onBacktestComplete={handleResult} />
```

### StrategyEditor.jsx

Visual editor untuk custom strategies:

**Features**:
- Create new custom strategies
- Edit existing strategies
- Add/remove conditions
- Set condition parameters
- Save strategies ke backend

**Usage**:
```jsx
import StrategyEditor from './components/StrategyEditor';

<StrategyEditor onStrategySaved={handleSave} />
```

### BacktestResults.jsx

Comprehensive results visualization:

**Features**:
- Summary metrics cards
- Equity curve chart
- Drawdown chart
- Trade history table
- Performance statistics
- Visual indicators

**Usage**:
```jsx
import BacktestResults from './components/BacktestResults';

<BacktestResults result={backtestData} />
```

### Backtest.jsx (Page)

Main page yang menggabungkan semua components:

**Features**:
- Tab navigation (Backtest, Strategy Editor, Results)
- State management
- API integration
- Error handling

## Examples

### Example 1: Simple Backtest

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
print(f"Total Return: ${result['total_return']:.2f}")
print(f"Return %: {result['total_return_pct']:.2f}%")
print(f"Sharpe Ratio: {result['sharpe_ratio']:.2f}")
print(f"Max Drawdown: {result['max_drawdown_pct']:.2f}%")
print(f"Win Rate: {result['win_rate']:.2f}%")
print(f"Total Trades: {result['total_trades']}")
```

### Example 2: Custom Strategy

```python
from analysis.custom_strategies import BaseStrategy
from backtesting.backtest_engine import BacktestEngine
import pandas as pd

class MomentumStrategy(BaseStrategy):
    def __init__(self, params=None):
        super().__init__("Momentum Strategy", params)
        self.lookback = self.params.get('lookback', 20)
    
    def generate_signal(self, df: pd.DataFrame, index: int) -> dict:
        if index < self.lookback:
            return {"action": "HOLD", "confidence": 0, "stop_loss": 0, "take_profit": 0}
        
        # Calculate momentum
        momentum = (df['close'].iloc[index] - df['close'].iloc[index - self.lookback]) / df['close'].iloc[index - self.lookback]
        
        current_price = df['close'].iloc[index]
        
        if momentum > 0.05:  # 5% momentum
            return {
                "action": "BUY",
                "confidence": min(momentum * 1000, 100),
                "stop_loss": current_price * 0.97,
                "take_profit": current_price * 1.10,
                "reason": f"Strong momentum: {momentum:.2%}"
            }
        elif momentum < -0.05:
            return {
                "action": "SELL",
                "confidence": min(abs(momentum) * 1000, 100),
                "stop_loss": current_price * 1.03,
                "take_profit": current_price * 0.90,
                "reason": f"Negative momentum: {momentum:.2%}"
            }
        
        return {"action": "HOLD", "confidence": 50, "stop_loss": 0, "take_profit": 0}

# Register strategy
from analysis.custom_strategies import StrategyFactory
StrategyFactory.AVAILABLE_STRATEGIES["momentum"] = MomentumStrategy

# Run backtest
engine = BacktestEngine(
    symbol="BTC/USDT",
    timeframe="1h",
    start_date="2024-01-01",
    end_date="2024-12-31",
    strategy_name="momentum",
    strategy_params={"lookback": 20},
    initial_balance=10000
)

result = engine.run()
print(f"Return: {result['total_return_pct']:.2f}%")
```

### Example 3: Parameter Optimization

```python
from backtesting.optimizer import ParameterOptimizer

optimizer = ParameterOptimizer(
    symbol="BTC/USDT",
    timeframe="1h",
    start_date="2024-01-01",
    end_date="2024-06-30",  # In-sample data
    strategy_name="rsi_macd",
    initial_balance=10000
)

# Optimize RSI parameters
result = optimizer.optimize(
    param_ranges={
        "rsi_period": [10, 14, 20, 25],
        "rsi_oversold": [20, 25, 30, 35],
        "rsi_overbought": [65, 70, 75, 80]
    },
    optimization_metric="sharpe_ratio",
    n_trials=100
)

print(f"Best parameters: {result['best_params']}")
print(f"Best Sharpe Ratio: {result['best_score']:.2f}")

# Validate on out-of-sample data
optimizer_out = ParameterOptimizer(
    symbol="BTC/USDT",
    timeframe="1h",
    start_date="2024-07-01",
    end_date="2024-12-31",  # Out-of-sample data
    strategy_name="rsi_macd",
    strategy_params=result['best_params'],
    initial_balance=10000
)

validation_result = optimizer_out.run_single_backtest()
print(f"Validation Return: {validation_result['total_return_pct']:.2f}%")
```

### Example 4: Compare Multiple Strategies

```python
from backtesting.backtest_engine import BacktestEngine

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
    
    result = engine.run()
    results[strategy_name] = result
    
    print(f"\n{strategy_name}:")
    print(f"  Return: {result['total_return_pct']:.2f}%")
    print(f"  Sharpe: {result['sharpe_ratio']:.2f}")
    print(f"  Max DD: {result['max_drawdown_pct']:.2f}%")
    print(f"  Win Rate: {result['win_rate']:.2f}%")

# Find best strategy
best_strategy = max(results.items(), key=lambda x: x[1]['sharpe_ratio'])
print(f"\nBest strategy: {best_strategy[0]} (Sharpe: {best_strategy[1]['sharpe_ratio']:.2f})")
```

## Performance Metrics Explained

### Sharpe Ratio

**Formula**: `(Return - Risk-Free Rate) / Standard Deviation`

**Interpretation**:
- `< 1.0`: Poor risk-adjusted return
- `1.0 - 2.0`: Acceptable
- `2.0 - 3.0`: Good
- `> 3.0`: Excellent

**Example**: Sharpe ratio 2.45 means strategy generates 2.45 units of return per unit of risk.

### Sortino Ratio

**Formula**: `(Return - Risk-Free Rate) / Downside Deviation`

**Difference from Sharpe**: Only considers downside risk (negative returns), not total volatility.

**Interpretation**:
- Higher is better
- Focuses on harmful volatility only

### Max Drawdown

**Definition**: Largest peak-to-trough decline in portfolio value.

**Example**: Max drawdown -8.45% means portfolio dropped 8.45% from its peak before recovering.

**Interpretation**:
- `< 10%`: Conservative
- `10% - 20%`: Moderate
- `20% - 30%`: Aggressive
- `> 30%`: Very risky

### Win Rate

**Formula**: `(Winning Trades / Total Trades) × 100`

**Interpretation**:
- `< 40%`: Poor (need high payoff ratio)
- `40% - 50%`: Average
- `50% - 60%`: Good
- `> 60%`: Excellent

**Note**: High win rate doesn't guarantee profitability if losses are larger than wins.

### Profit Factor

**Formula**: `Gross Profit / Gross Loss`

**Interpretation**:
- `< 1.0`: Losing strategy
- `1.0 - 1.5`: Marginal
- `1.5 - 2.0`: Good
- `> 2.0`: Excellent

**Example**: Profit factor 2.35 means for every $1 lost, strategy makes $2.35.

### Expectancy

**Formula**: `(Win Rate × Average Win) - (Loss Rate × Average Loss)`

**Interpretation**: Expected profit per trade.

**Example**: Expectancy $53.92 means average trade profits $53.92.

## Best Practices

### 1. Use Sufficient Historical Data

- Minimum 6 months for reliable results
- 1-2 years recommended
- Include different market conditions (bull, bear, sideways)

### 2. Avoid Overfitting

- Don't optimize too many parameters
- Use out-of-sample validation
- Keep strategy logic simple and robust

### 3. Consider Transaction Costs

- Include realistic commission (0.1% typical)
- Account for slippage in volatile markets
- Consider spread costs

### 4. Test Multiple Timeframes

- Test strategy on different timeframes
- Verify robustness across timeframes
- Avoid curve-fitting to specific timeframe

### 5. Validate with Walk-Forward Analysis

```python
# Split data into segments
segments = [
    ("2024-01-01", "2024-03-31"),  # Train
    ("2024-04-01", "2024-06-30"),  # Validate
    ("2024-07-01", "2024-09-30"),  # Test
    ("2024-10-01", "2024-12-31")   # Out-of-sample
]

# Optimize on train, validate on validate, test on test
# Final test on out-of-sample
```

### 6. Monitor Performance Decay

- Track performance over time
- Re-optimize parameters periodically
- Consider market regime changes

## Troubleshooting

### Issue: No trades executed

**Cause**: Strategy conditions too strict

**Solution**:
- Relax entry conditions
- Check parameter ranges
- Verify data quality

### Issue: Extremely high returns

**Cause**: Overfitting atau look-ahead bias

**Solution**:
- Use out-of-sample testing
- Simplify strategy
- Check for data snooping

### Issue: High drawdown

**Cause**: Insufficient risk management

**Solution**:
- Add stop-loss
- Reduce position size
- Improve entry timing

### Issue: Low win rate

**Cause**: Strategy not suited for market conditions

**Solution**:
- Adjust parameters
- Add filters (trend, volatility)
- Consider different strategy

## Future Enhancements

### Planned Features

1. **Multi-Asset Backtesting**: Test strategies across multiple symbols
2. **Portfolio Optimization**: Optimize allocation across multiple strategies
3. **Machine Learning Strategies**: Integrate ML models for signal generation
4. **Real-Time Backtesting**: Paper trading with live data
5. **Advanced Risk Metrics**: VaR, CVaR, Beta, Alpha
6. **Strategy Composition**: Combine multiple strategies
7. **Monte Carlo Simulation**: Statistical significance testing
8. **Walk-Forward Optimization**: Automated out-of-sample validation

### Contributing

Contributions welcome! Areas for improvement:
- Additional built-in strategies
- More performance metrics
- Better visualization
- Performance optimization
- Documentation improvements

## Support

For issues, questions, or feature requests:
- Check existing documentation
- Review example code
- Open issue on GitHub

## License

MIT License - See LICENSE file for details

---

**Version**: 1.0.0  
**Last Updated**: 2024-12-15  
**Python Version**: 3.11+  
**Dependencies**: See `requirements.txt`
