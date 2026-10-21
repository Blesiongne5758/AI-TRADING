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
├── data_loader.py                 # Load dari database lokal
├── backtest_data_loader.py        # Load dari Binance API (long-term)
├── strategy_runner.py             # Execute strategy candle-by-candle
├── performance_metrics.py         # Calculate performance metrics
├── report_generator.py            # Generate visual reports
├── optimizer.py                   # Grid search & Bayesian optimization
└── main_backtest.py               # Entry point dengan CLI
```

## 📊 Data Loaders

### DataLoader (Local Database)
- Memuat data dari database SQLite lokal
- Cepat untuk data pendek (< 90 hari)
- Termasuk news data untuk sentiment analysis
- **Requirement**: Data collector harus sudah berjalan

### BacktestDataLoader (Binance API)
- Memuat data langsung dari Binance API
- Bisa load ribuan candle (1-5+ tahun)
- Pagination otomatis untuk data besar
- Rate limiting untuk menghindari ban
- **Use case**: Long-term backtesting

## 🎯 Strategy Runner (NEW!)

### Lookahead Bias Prevention
Strategy runner yang baru memastikan **TIDAK ADA lookahead bias**:
- ✅ Strategi hanya melihat data hingga candle saat ini
- ✅ Loop candle-by-candle dengan strict data slicing
- ✅ Exit conditions checked sebelum entry signals
- ✅ No future data leakage

### Example Strategy: RSI + MACD + EMA
Strategi contoh yang sudah diimplementasikan:
```python
def strategy_rsi_macd_ema(data: pd.DataFrame, params: Dict) -> Optional[Dict]:
    """
    BUY jika: RSI < 30 AND MACD crossover up AND price > EMA200
    SELL jika: RSI > 70 AND MACD crossover down
    """
```

**Parameters yang bisa di-optimize:**
- `rsi_period`: Periode RSI (default: 14)
- `rsi_oversold`: Level oversold (default: 30)
- `rsi_overbought`: Level overbought (default: 70)

### Dataclass untuk Type Safety
```python
@dataclass
class BacktestTrade:
    id: int
    symbol: str
    side: str  # 'long' atau 'short'
    entry_time: datetime
    entry_price: float
    quantity: float
    stop_loss: float
    take_profit: float
    exit_time: Optional[datetime]
    exit_price: Optional[float]
    exit_reason: Optional[str]
    pnl: float
    pnl_percent: float
    fee: float
    holding_period: Optional[float]  # dalam jam

@dataclass
class BacktestResult:
    symbol: str
    timeframe: str
    start_date: datetime
    end_date: datetime
    initial_balance: float
    final_balance: float
    trades: List[BacktestTrade]
    equity_curve: List[Dict]
    parameters: Dict
```

## 📈 Performance Metrics (NEW!)

### API Baru: Menerima BacktestResult Langsung
```python
from backtesting.performance_metrics import PerformanceMetrics

# API baru: menerima BacktestResult langsung
metrics_calc = PerformanceMetrics()
metrics = metrics_calc.calculate_all(result)  # result adalah BacktestResult

# Grade strategi
grading = metrics_calc.grade_strategy(metrics)
print(f"Strategy Grade: {grading['overall_grade']}")
print(f"Score: {grading['overall_score']}/100")
print(f"Recommendation: {grading['recommendation']}")
```

### Metrik yang Dihitung (25+ Metrik!)

**Return Metrics:**
- `total_return_percent` - Total return persentase
- `annualized_return_percent` - Return tahunan
- `net_profit` - Profit bersih dalam USD

**Trade Statistics:**
- `total_trades` - Jumlah total trade
- `winning_trades` - Jumlah trade menang
- `losing_trades` - Jumlah trade kalah
- `win_rate_percent` - Win rate persentase
- `avg_win_usd` - Rata-rata profit per trade menang
- `avg_loss_usd` - Rata-rata loss per trade kalah
- `largest_win_usd` - Profit terbesar
- `largest_loss_usd` - Loss terbesar
- `profit_factor` - Profit factor (gross profit / gross loss)
- `expectancy_usd` - Expectancy (harapan matematis per trade)
- `payoff_ratio` - Payoff ratio (avg win / avg loss)

**Risk Metrics:**
- `max_drawdown_percent` - Max drawdown persentase
- `max_drawdown_usd` - Max drawdown dalam USD
- `annualized_volatility_percent` - Volatilitas tahunan
- `sharpe_ratio` - Sharpe ratio
- `sortino_ratio` - Sortino ratio
- `calmar_ratio` - Calmar ratio
- `kelly_criterion_percent` - Kelly criterion untuk position sizing optimal

**Timing & Breakdown:**
- `avg_holding_hours` - Rata-rata holding period
- `backtest_days` - Jumlah hari backtest
- `long_win_rate_percent` - Win rate untuk long positions
- `short_win_rate_percent` - Win rate untuk short positions
- `long_trades` - Jumlah long trades
- `short_trades` - Jumlah short trades
- `exit_reasons` - Distribusi exit reasons (STOP_LOSS, TAKE_PROFIT, dll)

### Strategy Grading System

Sistem grading otomatis dari A+ sampai F:

```python
grading = metrics_calc.grade_strategy(metrics)

# Output:
{
    "grades": {
        "sharpe": ("A+", "Sangat excellent"),
        "drawdown": ("A", "Drawdown kecil"),
        "win_rate": ("B", "Win rate cukup"),
        "profit_factor": ("A", "Profit factor bagus")
    },
    "overall_score": 87.5,
    "overall_grade": "A (STRATEGI BAGUS - layak dipertimbangkan)",
    "recommendation": "✅ STRATEGI LAYAK untuk live trading..."
}
```

**Grade Criteria:**
- **A+ (90-100)**: Strategi excellent, siap live trading
- **A (75-89)**: Strategi bagus, layak dipertimbangkan
- **B (60-74)**: Strategi cukup, perlu optimasi
- **C (40-59)**: Strategi kurang, perlu revisi besar
- **D/F (<40)**: Strategi buruk, jangan dipakai live!

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

### 2. Long-Term Backtest dengan Binance API

Untuk backtest jangka panjang (1+ tahun), gunakan flag `--use-api` untuk memuat data langsung dari Binance API:

```bash
# Backtest 2 tahun data dari Binance API
python -m backtesting.main_backtest \
  --mode backtest \
  --symbol BTC/USDT \
  --timeframe 1h \
  --use-api \
  --start-date 2022-01-01

# Backtest 1 tahun dengan custom start date
python -m backtesting.main_backtest \
  --mode backtest \
  --symbol ETH/USDT \
  --timeframe 4h \
  --use-api \
  --start-date 2023-01-01
```

**Keuntungan menggunakan `--use-api`:**
- ✅ Bisa memuat data hingga ribuan candle
- ✅ Tidak tergantung pada data di database lokal
- ✅ Cocok untuk backtest jangka panjang (1-5 tahun)
- ✅ Data langsung dari Binance (akurat & lengkap)

**Catatan:**
- Membutuhkan koneksi internet yang stabil
- Proses loading mungkin memakan waktu beberapa menit untuk data panjang
- Tidak ada news data (karena hanya load candle data)

### 3. Run Optimization

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

# Optimize dengan data dari Binance API (long-term)
python -m backtesting.main_backtest \
  --mode optimize \
  --symbol BTC/USDT \
  --timeframe 1h \
  --use-api \
  --start-date 2022-01-01
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

### Visual Reports (NEW API!)

ReportGenerator sekarang menerima `BacktestResult` langsung (tidak perlu konversi manual):

```python
from backtesting.report_generator import ReportGenerator

report_gen = ReportGenerator()
report_path = report_gen.generate_full_report(result, metrics, grading)
```

**Output:**
```
backtest_reports/
└── BTC_USDT_20240115_143022/
    ├── equity_curve.png       # Grafik pertumbuhan equity dengan benchmark
    ├── drawdown.png           # Chart drawdown dengan fill area
    ├── trade_distribution.png # Histogram PnL + cumulative PnL
    ├── monthly_returns.png    # Return bulanan (bar chart)
    ├── exit_reasons.png       # Pie chart exit reasons (TP/SL/END)
    └── summary.txt            # Text report lengkap dengan grading
```

**1. Equity Curve** (`equity_curve.png`)
- Line chart pertumbuhan equity
- Reference line initial balance
- Fill area hijau (profit) / merah (loss)
- Title dengan key metrics (Return, Sharpe, Max DD)

**2. Drawdown Chart** (`drawdown.png`)
- Area chart drawdown percentage
- Visualisasi peak-to-trough decline
- Merah untuk drawdown

**3. Trade Distribution** (`trade_distribution.png`)
- **Left**: Histogram PnL distribution
- **Right**: Trade-by-trade PnL dengan cumulative line
- Color-coded hijau (profit) / merah (loss)

**4. Monthly Returns** (`monthly_returns.png`)
- Bar chart return per bulan
- Color-coded hijau (positive) / merah (negative)
- Reference line di 0%

**5. Exit Reasons** (`exit_reasons.png`) - NEW!
- Pie chart distribusi exit reasons
- TAKE_PROFIT (hijau)
- STOP_LOSS (merah)
- BACKTEST_END (abu-abu)

**6. Summary Text** (`summary.txt`) - ENHANCED!
- Periode backtest
- Performance metrics lengkap
- Trade statistics
- Risk metrics
- Long/Short breakdown
- Exit reasons distribution
- **Strategy grading** (A+ to F)
- **Recommendation** (actionable insights)

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

## 💻 Programmatic Usage

### Menggunakan BacktestDataLoader untuk Long-Term Backtest

```python
import asyncio
from backtesting import BacktestDataLoader, StrategyRunner, PerformanceMetrics

async def long_term_backtest():
    # 1. Load data dari Binance API (2 tahun)
    loader = BacktestDataLoader()
    await loader.initialize()
    
    candles_df = await loader.load_historical_data(
        symbol="BTC/USDT",
        timeframe="1h",
        start_date="2022-01-01",
        end_date="2024-01-01",
    )
    
    await loader.close()
    
    print(f"Loaded {len(candles_df)} candles")
    
    # 2. Run backtest dengan strategy runner baru
    from backtesting.strategy_runner import StrategyRunner, strategy_rsi_macd_ema
    
    runner = StrategyRunner(
        initial_balance=10000.0,
        trading_fee_percent=0.1,  # 0.1% fee
        max_risk_per_trade=2.0,  # 2% risk
    )
    
    # Set symbol dan timeframe sebagai attributes
    candles_df.attrs["symbol"] = "BTC/USDT"
    candles_df.attrs["timeframe"] = "1h"
    
    # Run backtest dengan contoh strategi
    result = runner.run_backtest(
        data=candles_df,
        symbol="BTC/USDT",
        timeframe="1h",
        strategy_func=strategy_rsi_macd_ema,
        strategy_params={
            "rsi_period": 14,
            "rsi_oversold": 30,
            "rsi_overbought": 70,
        },
    )
    
    # 3. Calculate metrics dengan API baru
    metrics_calc = PerformanceMetrics()
    metrics = metrics_calc.calculate_all(result)  # Langsung pakai BacktestResult!
    
    # Grade strategi
    grading = metrics_calc.grade_strategy(metrics)
    print(f"\n🏆 Strategy Grade: {grading['overall_grade']}")
    print(f"   Score: {grading['overall_score']}/100")
    print(f"   Recommendation: {grading['recommendation']}")
    
    # Print summary
    print(f"\n📊 Performance Summary:")
    print(f"   Total Return: {metrics['total_return_percent']:.2f}%")
    print(f"   Sharpe Ratio: {metrics['sharpe_ratio']:.2f}")
    print(f"   Max Drawdown: {metrics['max_drawdown_percent']:.2f}%")
    print(f"   Win Rate: {metrics['win_rate_percent']:.2f}%")
    print(f"   Profit Factor: {metrics['profit_factor']:.2f}")
    
    # 4. Generate reports
    from backtesting.report_generator import ReportGenerator
    
    # Convert ke format untuk ReportGenerator
    trades_list = [trade.__dict__ for trade in result.trades]
    equity_list = result.equity_curve
    
    report_gen = ReportGenerator(trades_list, equity_list, metrics)
    report_gen.generate_report()
    report_gen.generate_interactive_report()
    report_gen.generate_seaborn_report()

# Run
asyncio.run(long_term_backtest())
```

### Multi-Timeframe Analysis

```python
async def multi_timeframe_backtest():
    loader = BacktestDataLoader()
    await loader.initialize()
    
    # Load multiple timeframes
    data = await loader.load_multi_timeframe(
        symbol="BTC/USDT",
        timeframes=["1h", "4h", "1d"],
        start_date="2023-01-01",
    )
    
    await loader.close()
    
    # Run backtest on each timeframe
    from backtesting.strategy_runner import strategy_rsi_macd_ema
    
    for timeframe, candles_df in data.items():
        print(f"\n{'='*70}")
        print(f"Backtesting {timeframe} timeframe")
        print(f"{'='*70}")
        
        # Set attributes
        candles_df.attrs["symbol"] = "BTC/USDT"
        candles_df.attrs["timeframe"] = timeframe
        
        runner = StrategyRunner(initial_balance=10000.0)
        result = runner.run_backtest(
            data=candles_df,
            symbol="BTC/USDT",
            timeframe=timeframe,
            strategy_func=strategy_rsi_macd_ema,
            strategy_params={},
        )
        
        # Calculate metrics dengan API baru
        metrics_calc = PerformanceMetrics()
        metrics = metrics_calc.calculate_all(result)
        
        # Grade strategi
        grading = metrics_calc.grade_strategy(metrics)
        print(f"\n🏆 Grade: {grading['overall_grade']} (Score: {grading['overall_score']}/100)")
        print(f"   Return: {metrics['total_return_percent']:.2f}%")
        print(f"   Sharpe: {metrics['sharpe_ratio']:.2f}")
        print(f"   Max DD: {metrics['max_drawdown_percent']:.2f}%")
```

## 🎨 Custom Strategy

Anda bisa membuat custom strategy function dengan signature:

```python
def my_strategy(data: pd.DataFrame, params: Dict) -> Optional[Dict]:
    """
    Custom strategy logic
    
    Args:
        data: Historical candles UP TO CURRENT candle (no lookahead!)
        params: Strategy parameters (untuk optimization)
    
    Returns:
        Signal dictionary atau None
        {
            "action": "BUY" | "SELL",
            "stop_loss": float,
            "take_profit": float,
            "position_size_percent": float,  # optional, default 10%
        }
    """
    # IMPORTANT: data hanya berisi candle hingga saat ini
    # JANGAN gunakan data.iloc[-1] untuk melihat masa depan!
    
    if len(data) < 200:
        return None
    
    # Contoh: Simple moving average crossover
    sma_20 = data['close'].rolling(20).mean().iloc[-1]
    sma_50 = data['close'].rolling(50).mean().iloc[-1]
    
    current_price = float(data['close'].iloc[-1])
    
    # BUY signal
    if sma_20 > sma_50:
        return {
            "action": "BUY",
            "stop_loss": current_price * 0.98,  # 2% below entry
            "take_profit": current_price * 1.06,  # 6% above entry
            "position_size_percent": 10,
        }
    
    return None

# Use custom strategy
runner = StrategyRunner(initial_balance=10000.0)
result = runner.run_backtest(
    data=candles_df,
    symbol="BTC/USDT",
    timeframe="1h",
    strategy_func=my_strategy,  # Your custom strategy
    strategy_params={},
)
```

## 🎛️ Parameter Optimization (NEW!)

### Method 1: Grid Search (Exhaustive)

Grid search mencoba **semua kombinasi** parameter yang didefinisikan.

```python
from backtesting import StrategyRunner, ParameterOptimizer, strategy_rsi_macd_ema

# 1. Create StrategyRunner
runner = StrategyRunner(
    initial_balance=10000.0,
    trading_fee_percent=0.1,
    max_risk_per_trade=2.0,
)

# 2. Create ParameterOptimizer
optimizer = ParameterOptimizer(runner)

# 3. Define parameter grid
param_grid = {
    'rsi_period': [10, 14, 20],
    'rsi_oversold': [25, 30, 35],
    'rsi_overbought': [65, 70, 75],
}

# 4. Run grid search
results = optimizer.grid_search(
    data=candles_df,
    symbol="BTC/USDT",
    timeframe="1h",
    strategy_func=strategy_rsi_macd_ema,
    param_grid=param_grid,
    optimize_for="sharpe_ratio",  # atau "profit_factor", "total_return_percent", dll
)

# 5. Access best result
best_result = results[0]
print(f"Best parameters: {best_result['parameters']}")
print(f"Best Sharpe Ratio: {best_result['optimize_value']:.2f}")
print(f"Total Return: {best_result['metrics']['total_return_percent']:.2f}%")
```

**When to use Grid Search:**
- ✅ Parameter space kecil (< 100 combinations)
- ✅ Ingin memastikan menemukan global optimum
- ✅ Waktu bukan masalah

### Method 2: Optuna (Bayesian Optimization)

Optuna menggunakan **Bayesian optimization** untuk mencari parameter optimal lebih efisien.

```python
from backtesting import StrategyRunner, ParameterOptimizer, strategy_rsi_macd_ema

# 1. Create StrategyRunner
runner = StrategyRunner(initial_balance=10000.0)

# 2. Create ParameterOptimizer
optimizer = ParameterOptimizer(runner)

# 3. Define parameter space (ranges)
param_space = {
    'rsi_period': (10, 30),        # Integer range
    'rsi_oversold': (20, 40),      # Integer range
    'rsi_overbought': (60, 80),    # Integer range
}

# 4. Run Optuna optimization
result = optimizer.optuna_optimize(
    data=candles_df,
    symbol="BTC/USDT",
    timeframe="1h",
    strategy_func=strategy_rsi_macd_ema,
    param_space=param_space,
    optimize_for="sharpe_ratio",
    n_trials=50,  # Number of trials
)

# 5. Access best result
print(f"Best parameters: {result['best_params']}")
print(f"Best Sharpe Ratio: {result['best_value']:.2f}")
print(f"Total trials: {len(result['all_trials'])}")
```

**When to use Optuna:**
- ✅ Parameter space besar (> 100 combinations)
- ✅ Waktu terbatas
- ✅ Continuous parameters (float ranges)
- ✅ Lebih efisien dari grid search

### Optimization Output

```
🔬 Grid search: 27 combinations
   Optimizing for: sharpe_ratio
   Progress: 10/27
   Progress: 20/27
✅ Grid search complete: 27 valid results
   Best sharpe_ratio: 2.45
   Best params: {'rsi_period': 14, 'rsi_oversold': 30, 'rsi_overbought': 70}

======================================================================
🏆 OPTIMIZATION RESULTS
======================================================================

Best Parameters:
  rsi_period: 14
  rsi_oversold: 30
  rsi_overbought: 70

Best Performance:
  Sharpe Ratio:    2.45
  Total Return:    +25.34%
  Max Drawdown:    -8.45%
  Win Rate:        68.09%
  Profit Factor:   2.35

📊 Saving optimization results...
✅ Optimization results saved to: backtest_reports/optimization_results.csv
   Total combinations tested: 27
```

### Optimization Metrics

Anda bisa optimize untuk metrik apapun:

```python
# Sharpe Ratio (risk-adjusted return)
optimizer.grid_search(..., optimize_for="sharpe_ratio")

# Profit Factor (gross profit / gross loss)
optimizer.grid_search(..., optimize_for="profit_factor")

# Total Return (percentage)
optimizer.grid_search(..., optimize_for="total_return_percent")

# Win Rate (percentage)
optimizer.grid_search(..., optimize_for="win_rate_percent")

# Max Drawdown (lower is better, tapi optimizer maximize)
# Note: Untuk minimize, gunakan negative value atau custom logic
optimizer.grid_search(..., optimize_for="calmar_ratio")  # Alternative
```

### CLI Usage

```bash
# Run optimization via CLI
python -m backtesting.main_backtest \
  --mode optimize \
  --symbol BTC/USDT \
  --timeframe 1h \
  --balance 10000 \
  --use-api \
  --start-date 2022-01-01
```

### Best Practices

**1. Start with Grid Search untuk small parameter space:**
```python
# 3 parameters × 3 values each = 27 combinations (fast)
param_grid = {
    'rsi_period': [10, 14, 20],
    'rsi_oversold': [25, 30, 35],
    'rsi_overbought': [65, 70, 75],
}
```

**2. Use Optuna untuk large parameter space:**
```python
# 5 parameters × continuous ranges = infinite combinations
param_space = {
    'rsi_period': (10, 30),
    'rsi_oversold': (20, 40),
    'rsi_overbought': (60, 80),
    'macd_fast': (8, 16),
    'macd_slow': (20, 30),
}
```

**3. Filter results dengan minimum trades:**
```python
# Optimizer automatically skip results with < 10 trades
# Ini memastikan statistical significance
```

**4. Validate dengan out-of-sample data:**
```python
# Split data: 70% for optimization, 30% for validation
train_data = candles_df.iloc[:int(len(candles_df) * 0.7)]
test_data = candles_df.iloc[int(len(candles_df) * 0.7):]

# Optimize on train_data
results = optimizer.grid_search(data=train_data, ...)

# Validate best params on test_data
best_params = results[0]['parameters']
validation_result = runner.run_backtest(
    data=test_data,
    strategy_func=strategy_rsi_macd_ema,
    strategy_params=best_params,
)
```

**5. Avoid overfitting:**
- ✅ Use walk-forward validation
- ✅ Test on multiple time periods
- ✅ Check if results are stable across different parameter values
- ❌ Don't optimize terlalu banyak parameters sekaligus

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

**Menggunakan Local Database (default):**
- Minimal 200 candles untuk analysis
- Data harus valid (no NaN, logical OHLC)
- Timeframe consistent
- Data collector harus sudah berjalan untuk mengumpulkan data

**Menggunakan Binance API (`--use-api`):**
- Bisa memuat ribuan candle (hingga 5+ tahun data)
- Data langsung dari Binance (akurat & lengkap)
- Tidak perlu data collector berjalan
- Membutuhkan koneksi internet yang stabil
- Proses loading lebih lama untuk data panjang

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

- ✅ Data loader dari database lokal (DataLoader)
- ✅ Data loader dari Binance API (BacktestDataLoader) - untuk long-term backtest
- ✅ **NEW!** Strategy runner dengan lookahead bias prevention
- ✅ **NEW!** Dataclass untuk type safety (BacktestTrade, BacktestResult)
- ✅ **NEW!** Example strategy: RSI + MACD + EMA
- ✅ **NEW!** Candle-by-candle execution dengan strict data slicing
- ✅ Performance metrics (15+ basic + 8 advanced metrics)
- ✅ Visual report generator (Matplotlib, Seaborn, Plotly)
- ✅ Parameter optimizer (Grid search & Bayesian dengan Optuna)
- ✅ Multi-timeframe support
- ✅ CLI interface dengan flag `--use-api`
- ✅ Build successful

---

**Your backtesting engine is production-ready with lookahead bias prevention! 📊🚀**

Silakan jalankan backtest dengan strategy runner yang baru:

```bash
cd backend
python -m backtesting.main_backtest --mode backtest --use-api --start-date 2022-01-01
```
