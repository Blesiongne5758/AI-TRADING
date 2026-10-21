"""
Main Backtest - Entry point untuk testing
"""
import asyncio
import sys
from pathlib import Path
from loguru import logger

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from .backtest_data_loader import BacktestDataLoader
from .strategy_runner import StrategyRunner, strategy_rsi_macd_ema
from .performance_metrics import PerformanceMetrics
from .report_generator import ReportGenerator
from .optimizer import ParameterOptimizer


async def run_single_backtest():
    """Jalankan single backtest"""
    logger.info("🚀 Starting single backtest...")

    # 1. Load data
    loader = BacktestDataLoader()
    await loader.initialize()

    data = await loader.load_historical_data(
        symbol="BTC/USDT",
        timeframe="1h",
        start_date="2023-01-01",
        end_date="2024-12-31",
    )

    await loader.close()

    # 2. Run backtest
    runner = StrategyRunner(initial_balance=10000.0, trading_fee_percent=0.1)
    result = runner.run_backtest(
        data=data,
        symbol="BTC/USDT",
        timeframe="1h",
        strategy_func=strategy_rsi_macd_ema,
        strategy_params={
            "rsi_period": 14,
            "rsi_oversold": 30,
            "rsi_overbought": 70,
        },
    )

    # 3. Calculate metrics
    metrics_calc = PerformanceMetrics()
    metrics = metrics_calc.calculate_all(result)
    grades = metrics_calc.grade_strategy(metrics)

    # 4. Generate report
    reporter = ReportGenerator()
    report_dir = reporter.generate_full_report(result, metrics, grades)

    # 5. Print summary
    print("\n" + "=" * 70)
    print("📊 BACKTEST SUMMARY")
    print("=" * 70)
    print(f"  Symbol:           {result.symbol}")
    print(f"  Period:           {result.start_date.date()} → {result.end_date.date()}")
    print(f"  Initial Balance:  ${metrics['initial_balance']:,.2f}")
    print(f"  Final Balance:    ${metrics['final_balance']:,.2f}")
    print(f"  Total Return:     {metrics['total_return_percent']:+.2f}%")
    print(f"  Sharpe Ratio:     {metrics['sharpe_ratio']:.2f}")
    print(f"  Max Drawdown:     {metrics['max_drawdown_percent']:.2f}%")
    print(f"  Win Rate:         {metrics['win_rate_percent']:.2f}%")
    print(f"  Profit Factor:    {metrics['profit_factor']:.2f}")
    print(f"  Total Trades:     {metrics['total_trades']}")
    print(f"\n  Overall Grade:    {grades['overall_grade']}")
    print(f"  Recommendation:   {grades['recommendation']}")
    print("=" * 70)
    print(f"\n📁 Full report: {report_dir}")


async def run_optimization():
    """Jalankan parameter optimization"""
    logger.info("🔬 Starting parameter optimization...")

    # Load data
    loader = BacktestDataLoader()
    await loader.initialize()

    data = await loader.load_historical_data(
        symbol="BTC/USDT",
        timeframe="1h",
        start_date="2023-01-01",
        end_date="2024-06-30",  # In-sample data
    )

    await loader.close()

    # Setup optimizer
    runner = StrategyRunner(initial_balance=10000.0)
    optimizer = ParameterOptimizer(runner)

    # Grid search
    param_grid = {
        "rsi_period": [10, 14, 20],
        "rsi_oversold": [25, 30, 35],
        "rsi_overbought": [65, 70, 75],
    }

    results = optimizer.grid_search(
        data=data,
        symbol="BTC/USDT",
        timeframe="1h",
        strategy_func=strategy_rsi_macd_ema,
        param_grid=param_grid,
        optimize_for="sharpe_ratio",
    )

    # Print top 5
    print("\n" + "=" * 70)
    print("🏆 TOP 5 PARAMETER SETS")
    print("=" * 70)
    for i, r in enumerate(results[:5], 1):
        print(f"\n#{i}: Sharpe={r['optimize_value']:.2f}")
        print(f"    Params: {r['parameters']}")
        print(f"    Return: {r['metrics']['total_return_percent']:+.2f}%")
        print(f"    Win Rate: {r['metrics']['win_rate_percent']:.2f}%")
        print(f"    Max DD: {r['metrics']['max_drawdown_percent']:.2f}%")
        print(f"    Trades: {r['metrics']['total_trades']}")


async def main():
    """Main entry point"""
    mode = "single"  # Change to "optimize" for optimization

    if mode == "single":
        await run_single_backtest()
    else:
        await run_optimization()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logger.exception(f"💥 Fatal error: {e}")
        sys.exit(1)
