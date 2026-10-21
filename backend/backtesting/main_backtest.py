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
from .backtest_data_loader import BacktestDataLoader
from .strategy_runner import StrategyRunner, BacktestResult, strategy_rsi_macd_ema
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
    use_api: bool = False,
    start_date: str = None,
):
    """
    Run backtest on historical data

    Args:
        symbol: Trading pair
        timeframe: Timeframe
        initial_balance: Starting balance
        days_back: Number of days to backtest (used if start_date not provided)
        use_api: If True, load data directly from Binance API (for long-term backtest)
        start_date: Start date in YYYY-MM-DD format (optional)
    """
    logger.info("=" * 70)
    logger.info("🚀 STARTING BACKTEST")
    logger.info("=" * 70)
    logger.info(f"Symbol: {symbol}")
    logger.info(f"Timeframe: {timeframe}")
    logger.info(f"Initial Balance: ${initial_balance:,.2f}")
    logger.info(f"Data Source: {'Binance API' if use_api else 'Local Database'}")
    logger.info("")

    # Determine date range
    end_date = datetime.now()
    if start_date:
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    else:
        start_dt = end_date - timedelta(days=days_back)
    
    logger.info(f"Period: {start_dt.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    logger.info("")

    # Load data
    logger.info("📊 Loading historical data...")
    
    if use_api:
        # Use BacktestDataLoader to fetch from Binance API
        data_loader = BacktestDataLoader()
        await data_loader.initialize()
        
        candles_df = await data_loader.load_historical_data(
            symbol=symbol,
            timeframe=timeframe,
            start_date=start_dt.strftime("%Y-%m-%d"),
            end_date=end_date.strftime("%Y-%m-%d"),
        )
        
        await data_loader.close()
        
        if candles_df.empty:
            logger.error("No data available from Binance API")
            return
        
        # No news data when using API
        news_data = []
    else:
        # Use DataLoader to fetch from local database
        db = DatabaseManager()
        await db.initialize()
        
        data_loader = DataLoader(db)
        candles_df = await data_loader.load_candles(symbol, timeframe, start_dt, end_date)
        
        if candles_df.empty:
            logger.error("No data available in local database")
            logger.info("💡 Tip: Use --use-api flag to load data directly from Binance")
            return
        
        # Validate data
        if not data_loader.validate_data(candles_df):
            logger.error("Data validation failed")
            return
        
        # Load news data (optional)
        news_data = await data_loader.load_news(start_dt, end_date)

    # Run backtest
    logger.info("\n🏃 Running backtest...")
    logger.info("   Strategy: RSI + MACD + EMA")
    
    runner = StrategyRunner(
        initial_balance=initial_balance,
        trading_fee_percent=0.1,  # 0.1% fee
        max_risk_per_trade=2.0,  # 2% risk per trade
    )

    # Use the new strategy runner with example strategy
    result = runner.run_backtest(
        data=candles_df,
        symbol=symbol,
        timeframe=timeframe,
        strategy_func=strategy_rsi_macd_ema,
        strategy_params={},  # Default parameters
    )

    # Calculate metrics dengan API baru
    logger.info("\n📈 Calculating performance metrics...")
    metrics_calc = PerformanceMetrics()
    metrics = metrics_calc.calculate_all(result)
    
    # Grade strategi
    grading = metrics_calc.grade_strategy(metrics)
    logger.info(f"\n🏆 Strategy Grade: {grading['overall_grade']}")
    logger.info(f"   Score: {grading['overall_score']}/100")
    logger.info(f"   Recommendation: {grading['recommendation']}")

    # Print summary
    metrics_calc.print_summary()

    # Generate report
    logger.info("\n📊 Generating visual report...")
    
    # Convert BacktestResult ke format untuk ReportGenerator
    trades_list = [
        {
            "symbol": trade.symbol,
            "side": trade.side,
            "entry_price": trade.entry_price,
            "exit_price": trade.exit_price,
            "quantity": trade.quantity,
            "entry_time": trade.entry_time,
            "exit_time": trade.exit_time,
            "pnl": trade.pnl,
            "pnl_percent": trade.pnl_percent,
            "fee": trade.fee,
            "exit_reason": trade.exit_reason,
            "holding_period": trade.holding_period,
        }
        for trade in result.trades
    ]
    
    equity_list = [
        {
            "timestamp": point["timestamp"],
            "balance": point["balance"],
            "price": point["price"],
        }
        for point in result.equity_curve
    ]
    
    report_gen = ReportGenerator(trades_list, equity_list, metrics)
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
    use_api: bool = False,
    start_date: str = None,
):
    """
    Run parameter optimization

    Args:
        symbol: Trading pair
        timeframe: Timeframe
        initial_balance: Starting balance
        days_back: Number of days to optimize (used if start_date not provided)
        use_api: If True, load data directly from Binance API
        start_date: Start date in YYYY-MM-DD format (optional)
    """
    logger.info("=" * 70)
    logger.info("🔧 STARTING OPTIMIZATION")
    logger.info("=" * 70)
    logger.info(f"Data Source: {'Binance API' if use_api else 'Local Database'}")

    # Determine date range
    end_date = datetime.now()
    if start_date:
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    else:
        start_dt = end_date - timedelta(days=days_back)

    # Load data
    logger.info("📊 Loading historical data...")
    
    if use_api:
        # Use BacktestDataLoader to fetch from Binance API
        data_loader = BacktestDataLoader()
        await data_loader.initialize()
        
        candles_df = await data_loader.load_historical_data(
            symbol=symbol,
            timeframe=timeframe,
            start_date=start_dt.strftime("%Y-%m-%d"),
            end_date=end_date.strftime("%Y-%m-%d"),
        )
        
        await data_loader.close()
        news_data = []
    else:
        # Use DataLoader to fetch from local database
        db = DatabaseManager()
        await db.initialize()
        
        data_loader = DataLoader(db)
        candles_df = await data_loader.load_candles(symbol, timeframe, start_dt, end_date)
        news_data = await data_loader.load_news(start_dt, end_date)

    if candles_df.empty:
        logger.error("No data available for optimization")
        return

    # Define parameter grid for strategy optimization
    param_grid = {
        "rsi_period": [10, 14, 20],
        "rsi_oversold": [25, 30, 35],
        "rsi_overbought": [65, 70, 75],
    }

    # Run optimization
    logger.info("\n🔍 Running grid search optimization...")
    logger.info("   Strategy: RSI + MACD + EMA")
    logger.info(f"   Parameter grid: {param_grid}")
    
    # Set symbol and timeframe as attributes for optimizer
    candles_df.attrs["symbol"] = symbol
    candles_df.attrs["timeframe"] = timeframe
    
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
    parser.add_argument(
        "--use-api",
        action="store_true",
        help="Load data directly from Binance API (for long-term backtest)",
    )
    parser.add_argument(
        "--start-date",
        type=str,
        default=None,
        help="Start date in YYYY-MM-DD format (overrides --days)",
    )

    args = parser.parse_args()

    try:
        if args.mode == "backtest":
            await run_backtest(
                symbol=args.symbol,
                timeframe=args.timeframe,
                initial_balance=args.balance,
                days_back=args.days,
                use_api=args.use_api,
                start_date=args.start_date,
            )
        else:
            await run_optimization(
                symbol=args.symbol,
                timeframe=args.timeframe,
                initial_balance=args.balance,
                days_back=args.days,
                use_api=args.use_api,
                start_date=args.start_date,
            )

    except KeyboardInterrupt:
        logger.info("\n⚠️  Backtest stopped by user")
    except Exception as e:
        logger.exception(f"💥 Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
