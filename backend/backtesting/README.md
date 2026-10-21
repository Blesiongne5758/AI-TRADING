# 📊 Backtesting Engine

Modul backtesting untuk menguji strategi trading AI dengan data historis.

## 🎯 Fitur

- ✅ **Data Loader** - Load data historis dari database dengan validasi
- ✅ **Strategy Runner** - Jalankan strategi candle-by-candle (no look-ahead bias)
- ✅ **Performance Metrics** - Hitung Sharpe, Sortino, Calmar, Max Drawdown, dll
- ✅ **Report Generator** - Generate laporan visual (equity curve, drawdown, dll)
- ✅ **Strategy Optimizer** - Grid search untuk optimal parameter

## 📁 Struktur File

```
backtesting/
├── __init__.py                    # Module exports
├── data_loader.py                 # Load & validate historical data
├── strategy_runner.py             # Execute strategy candle-by-candle
├── performance_metrics.py         # Calculate performance metrics
├── report_generator.py            # Generate visual reports
├── optimizer.py                   # Grid search optimization
└── main_backtest.py               # Entry point
```

## 🚀 Cara Menggunakan

### 1. Run Backtest

```bash
cd backend
python -m backtesting.main_backtest --mode backtest
```

**Options:**
```bash
# Custom symbol & timeframe
python -m backtesting.main_backtest --symbol ETH/USDT --timeframe 4h

# Custom balance & period
python -m backtesting.main_backtest --balance 20000 --days 180

# Full example
python -m backtesting.main_backtest \
  --mode backtest \
  --symbol BTC/USDT \
  --timeframe 1h \
  --balance 10000 \
  --days 90
```

### 2. Run Optimization

```bash
python -m backtesting.main_backtest --mode optimize
```

**Options:**
```bash
# Optimize with custom parameters
python -m backtesting.main_backtest \
  --mode optimize \
  --symbol BTC/USDT \
  --timeframe 1h \
  --balance 10000 \
  --days 90
```

## 📊 Output

### Console Output

```
======================================================================
🚀 STARTING BACKTEST
======================================================================
Symbol: BTC/USDT
Timeframe: 1h
Initial Balance: $10,000.00
Period: Last 90 days

📊 Loading historical data...
Loaded 2160 candles for BTC/USDT 1h from 2024-01-01 to 2024-03-31

🏃 Running backtest...
Opened LONG position @ $42,500.00, Qty: 0.002353, Fee: $100.00
Closed LONG position @ $43,800.00, PnL: +$305.50 (+3.06%), Reason: TAKE_PROFIT
...

📈 Calculating performance metrics...

======================================================================
📊 BACKTEST PERFORMANCE SUMMARY
======================================================================

💰 RETURNS:
   Total Return:        +25.34%
   CAGR:                +101.36%

📈 RISK-ADJUSTED METRICS:
   Sharpe Ratio:        2.45
   Sortino Ratio:       3.12
   Calmar Ratio:        1.85

📉 DRAWDOWN:
   Max Drawdown:        -8.45%
   Max DD Duration:     12 days

🎯 TRADE STATISTICS:
   Total Trades:        47
   Winning Trades:      32
   Losing Trades:       15
   Win Rate:            68.09%

💵 PROFIT/LOSS:
   Avg Win:             +$185.50
   Avg Loss:            -$95.20
   Largest Win:         +$450.00
   Largest Loss:        -$210.00
   Profit Factor:       2.35
   Payoff Ratio:        1.95
   Expectancy:          +$53.85

⏱️  DURATION:
   Avg Trade Duration:  18.5 hours

======================================================================

📊 Generating visual report...
✅ Report saved to: backtest_reports/
   - equity_curve.png
   - drawdown.png
   - trade_distribution.png
   - monthly_returns.png
   - summary.txt
```

### Visual Reports

**1. Equity Curve**
- Grafik pertumbuhan equity over time
- Comparison dengan initial balance
- Metrics overlay (Total Return, Sharpe, Max DD)

**2. Drawdown Chart**
- Visualisasi drawdown periods
- Max drawdown highlight
- Duration analysis

**3. Trade Distribution**
- Histogram PnL distribution
- Winning vs losing trades
- Outlier detection

**4. Monthly Returns Heatmap**
- Monthly returns by year
- Color-coded (green = profit, red = loss)
- Seasonal patterns

### Text Summary

File `summary.txt` berisi ringkasan lengkap performa dalam format text.

## 📈 Performance Metrics

### Returns
- **Total Return**: Total persentase return
- **CAGR**: Compound Annual Growth Rate

### Risk-Adjusted
- **Sharpe Ratio**: Return per unit of total risk (>1 good, >2 excellent)
- **Sortino Ratio**: Return per unit of downside risk
- **Calmar Ratio**: CAGR / Max Drawdown

### Drawdown
- **Max Drawdown**: Maximum peak-to-trough decline
- **Max DD Duration**: Longest drawdown period

### Trade Statistics
- **Win Rate**: Percentage of winning trades
- **Profit Factor**: Gross profit / Gross loss
- **Payoff Ratio**: Average win / Average loss
- **Expectancy**: Average profit per trade

## 🔧 Custom Strategy

Anda bisa menggunakan custom strategy function:

```python
from backtesting.strategy_runner import StrategyRunner

def my_custom_strategy(candles_df, news_data):
    """
    Custom strategy logic
    
    Args:
        candles_df: Historical candles up to current point
        news_data: News up to current point
    
    Returns:
        Signal dictionary or None
    """
    # Your strategy logic here
    # Example: Simple moving average crossover
    
    if len(candles_df) < 50:
        return None
    
    # Calculate indicators
    sma_20 = candles_df['close'].rolling(20).mean().iloc[-1]
    sma_50 = candles_df['close'].rolling(50).mean().iloc[-1]
    
    # Generate signal
    if sma_20 > sma_50:
        return {
            'action': 'BUY',
            'suggested_actions': {
                'stop_loss': candles_df['close'].iloc[-1] * 0.98,
                'take_profit': candles_df['close'].iloc[-1] * 1.04,
            }
        }
    
    return None

# Run with custom strategy
runner = StrategyRunner(initial_balance=10000)
result = await runner.run(candles_df, news_data, strategy_func=my_custom_strategy)
```

## 🎛️ Parameter Optimization

### Define Parameter Grid

```python
from backtesting.optimizer import StrategyOptimizer

param_grid = {
    'max_risk_per_trade': [0.01, 0.02, 0.03],
    'trading_fee': [0.0005, 0.001, 0.0015],
    # Add more parameters as needed
}

optimizer = StrategyOptimizer(candles_df, news_data)
best_params, best_metrics, all_results = optimizer.optimize(
    param_grid=param_grid,
    metric_to_optimize='sharpe_ratio',
    initial_balance=10000.0,
)

print(f"Best parameters: {best_params}")
print(f"Best Sharpe Ratio: {best_metrics['sharpe_ratio']:.2f}")
```

### Optimization Output

```
🔍 Running grid search optimization...
Testing combination 1/9: {'max_risk_per_trade': 0.01, 'trading_fee': 0.0005}
Testing combination 2/9: {'max_risk_per_trade': 0.01, 'trading_fee': 0.001}
...

======================================================================
🏆 OPTIMIZATION RESULTS
======================================================================

Best Parameters:
  max_risk_per_trade: 0.02
  trading_fee: 0.001

Best Performance:
  Sharpe Ratio:    2.45
  Total Return:    +25.34%
  Max Drawdown:    -8.45%
  Win Rate:        68.09%

✅ Optimization results saved to: backtest_reports/optimization_results.csv
```

## ⚠️ Important Notes

### No Look-Ahead Bias
- Strategy hanya menggunakan data yang tersedia pada saat itu
- Tidak ada informasi masa depan yang bocor ke masa lalu
- Realistic simulation

### Trading Fees
- Default fee: 0.1% per trade (seperti Binance)
- Fee diterapkan saat entry dan exit
- Realistic cost simulation

### Risk Management
- Max risk per trade: 2% (configurable)
- Stop-loss dan take-profit otomatis
- Position sizing berdasarkan risk

### Data Requirements
- Minimal 200 candles untuk analysis
- Data harus valid (no NaN, logical OHLC)
- Timeframe consistent

## 📊 Interpretasi Hasil

### Sharpe Ratio
- **< 1**: Poor risk-adjusted return
- **1-2**: Acceptable
- **2-3**: Good
- **> 3**: Excellent

### Max Drawdown
- **< 10%**: Conservative
- **10-20%**: Moderate
- **20-30%**: Aggressive
- **> 30%**: Very risky

### Win Rate
- **< 40%**: Poor (need high payoff ratio)
- **40-50%**: Average
- **50-60%**: Good
- **> 60%**: Excellent

### Profit Factor
- **< 1**: Losing strategy
- **1-1.5**: Marginal
- **1.5-2**: Good
- **> 2**: Excellent

## 🐛 Troubleshooting

### Error: "No data available"
```bash
# Pastikan data collector sudah berjalan
python -m data_collector.main_collector

# Tunggu sampai data terkumpul (minimal 200 candles)
```

### Error: "Data validation failed"
- Check data quality (no NaN, logical OHLC)
- Pastikan timeframe consistent
- Check date range

### Empty backtest results
- Pastikan ada cukup data (minimal 200 candles)
- Check strategy logic
- Verify signal generation

## 📚 Resources

- [Backtesting Guide](https://www.investopedia.com/terms/b/backtesting.asp)
- [Performance Metrics](https://www.investopedia.com/terms/s/sharperatio.asp)
- [Risk Management](https://www.investopedia.com/terms/r/riskmanagement.asp)

## ✅ Status

**Backtesting Engine: COMPLETE ✅**

- ✅ Data loader dengan validation
- ✅ Strategy runner (no look-ahead bias)
- ✅ Performance metrics (15+ metrics)
- ✅ Visual report generator
- ✅ Parameter optimizer
- ✅ Build successful

---

**Your backtesting engine is production-ready! 📊🚀**
