"""
Main Backtest - Entry point for backtesting
"""
import asyncio
import sys
from pathlib import Path
from datetime import datetime, timedelta
from loguru import logger

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from data_collector.database import DatabaseManager
from .data_loader import DataLoader
from .strategy_runner import StrategyRunner
from .performance_metrics import PerformanceMetrics
from .report_generator import ReportGenerator
from .optimizer import StrategyOptimizer


# Setup logging
logger.remove()
logger.add(
    sys.stdout,
    level="INFO",
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | {message}",
)


async def run_backtest(
    symbol: str = "BTC/USDT",
    timeframe: str = "1h",
    initial_balance: float = 10000.0,
    days_back: int = 90,
):
    """
    Run backtest on historical data

    Args:
        symbol: Trading pair
        timeframe: Timeframe
        initial_balance: Starting balance
        days_back: Number of days to backtest
    """
    logger.info("=" * 70)
    logger.info("🚀 STARTING BACKTEST")
    logger.info("=" * 70)
    logger.info(f"Symbol: {symbol}")
    logger.info(f"Timeframe: {timeframe}")
    logger.info(f"Initial Balance: ${initial_balance:,.2f}")
    logger.info(f"Period: Last {days_back} days")
    logger.info("")

    # Initialize database
    db = DatabaseManager()
    await db.initialize()

    # Load data
    logger.info("📊 Loading historical data...")
    data_loader = DataLoader(db)

    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)

    candles_df = await data_loader.load_candles(symbol, timeframe, start_date, end_date)

    if candles_df.empty:
        logger.error("No data available for backtest")
        return

    # Validate data
    if not data_loader.validate_data(candles_df):
        logger.error("Data validation failed")
        return

    # Load news data (optional)
    news_data = await data_loader.load_news(start_date, end_date)

    # Run backtest
    logger.info("\n🏃 Running backtest...")
    runner = StrategyRunner(
        initial_balance=initial_balance,
        max_risk_per_trade=0.02,  # 2% risk per trade
        trading_fee=0.001,  # 0.1% fee
    )

    result = await runner.run(candles_df, news_data)

    # Calculate metrics
    logger.info("\n📈 Calculating performance metrics...")
    metrics_calc = PerformanceMetrics(
        result["trades"], result["equity_curve"]
    )
    metrics = metrics_calc.calculate_all()

    # Print summary
    metrics_calc.print_summary()

    # Generate report
    logger.info("\n📊 Generating visual report...")
    report_gen = ReportGenerator(result["trades"], result["equity_curve"], metrics)
    report_path = report_gen.generate_report()

    if report_path:
        logger.info(f"\n✅ Report saved to: {report_path}/")
        logger.info("   - equity_curve.png")
        logger.info("   - drawdown.png")
        logger.info("   - trade_distribution.png")
        logger.info("   - monthly_returns.png")
        logger.info("   - summary.txt")

    return metrics


async def run_optimization(
    symbol: str = "BTC/USDT",
    timeframe: str = "1h",
    initial_balance: float = 10000.0,
    days_back: int = 90,
):
    """
    Run parameter optimization

    Args:
        symbol: Trading pair
        timeframe: Timeframe
        initial_balance: Starting balance
        days_back: Number of days to optimize
    """
    logger.info("=" * 70)
    logger.info("🔧 STARTING OPTIMIZATION")
    logger.info("=" * 70)

    # Initialize database
    db = DatabaseManager()
    await db.initialize()

    # Load data
    logger.info("📊 Loading historical data...")
    data_loader = DataLoader(db)

    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)

    candles_df = await data_loader.load_candles(symbol, timeframe, start_date, end_date)

    if candles_df.empty:
        logger.error("No data available for optimization")
        return

    news_data = await data_loader.load_news(start_date, end_date)

    # Define parameter grid
    param_grid = {
        "max_risk_per_trade": [0.01, 0.02, 0.03],
        "trading_fee": [0.0005, 0.001, 0.0015],
    }

    # Run optimization
    logger.info("\n🔍 Running grid search optimization...")
    optimizer = StrategyOptimizer(candles_df, news_data)

    best_params, best_metrics, all_results = optimizer.optimize(
        param_grid=param_grid,
        metric_to_optimize="sharpe_ratio",
        initial_balance=initial_balance,
    )

    # Print results
    logger.info("\n" + "=" * 70)
    logger.info("🏆 OPTIMIZATION RESULTS")
    logger.info("=" * 70)

    logger.info("\nBest Parameters:")
    for param, value in best_params.items():
        logger.info(f"  {param}: {value}")

    logger.info("\nBest Performance:")
    logger.info(f"  Sharpe Ratio:    {best_metrics['sharpe_ratio']:.2f}")
    logger.info(f"  Total Return:    {best_metrics['total_return']:+.2f}%")
    logger.info(f"  Max Drawdown:    {best_metrics['max_drawdown']:.2f}%")
    logger.info(f"  Win Rate:        {best_metrics['win_rate']:.2f}%")

    # Generate optimization report
    logger.info("\n📊 Generating optimization report...")
    optimizer.plot_optimization_results(all_results)

    # Save results to CSV
    results_df = optimizer.generate_optimization_report(all_results)
    results_df.to_csv("backtest_reports/optimization_results.csv", index=False)
    logger.info("✅ Optimization results saved to: backtest_reports/optimization_results.csv")


async def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="AI Trading Agent - Backtesting Engine")
    parser.add_argument(
        "--mode",
        type=str,
        choices=["backtest", "optimize"],
        default="backtest",
        help="Run mode: backtest or optimize",
    )
    parser.add_argument(
        "--symbol",
        type=str,
        default="BTC/USDT",
        help="Trading pair (default: BTC/USDT)",
    )
    parser.add_argument(
        "--timeframe",
        type=str,
        default="1h",
        help="Timeframe (default: 1h)",
    )
    parser.add_argument(
        "--balance",
        type=float,
        default=10000.0,
        help="Initial balance (default: 10000)",
    )
    parser.add_argument(
        "--days",
        type=int,
        default=90,
        help="Days to backtest (default: 90)",
    )

    args = parser.parse_args()

    try:
        if args.mode == "backtest":
            await run_backtest(
                symbol=args.symbol,
                timeframe=args.timeframe,
                initial_balance=args.balance,
                days_back=args.days,
            )
        else:
            await run_optimization(
                symbol=args.symbol,
                timeframe=args.timeframe,
                initial_balance=args.balance,
                days_back=args.days,
            )

    except KeyboardInterrupt:
        logger.info("\n⚠️  Backtest stopped by user")
    except Exception as e:
        logger.exception(f"💥 Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
