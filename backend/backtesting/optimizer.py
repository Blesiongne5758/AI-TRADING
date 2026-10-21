"""
Strategy Optimizer - Grid search for optimal parameters
"""
import pandas as pd
from typing import List, Dict, Tuple
from itertools import product
from loguru import logger
from .strategy_runner import StrategyRunner
from .performance_metrics import PerformanceMetrics


class StrategyOptimizer:
    """Optimize strategy parameters using grid search"""

    def __init__(self, candles_df: pd.DataFrame, news_data: List[Dict] = None):
        """
        Initialize optimizer

        Args:
            candles_df: Historical candle data
            news_data: Historical news data (optional)
        """
        self.candles_df = candles_df
        self.news_data = news_data or []

    def optimize(
        self,
        param_grid: Dict[str, List],
        metric_to_optimize: str = "sharpe_ratio",
        initial_balance: float = 10000.0,
    ) -> Tuple[Dict, Dict, List[Dict]]:
        """
        Run grid search optimization

        Args:
            param_grid: Dictionary of parameter names and values to test
            metric_to_optimize: Metric to maximize (e.g., "sharpe_ratio", "total_return")
            initial_balance: Starting balance for each backtest

        Returns:
            Tuple of (best_params, best_metrics, all_results)
        """
        logger.info(f"Starting optimization with {self._count_combinations(param_grid)} combinations")

        # Generate all parameter combinations
        param_names = list(param_grid.keys())
        param_values = list(param_grid.values())
        combinations = list(product(*param_values))

        all_results = []
        best_score = float("-inf")
        best_params = None
        best_metrics = None

        # Test each combination
        for i, combo in enumerate(combinations):
            params = dict(zip(param_names, combo))

            logger.info(f"Testing combination {i+1}/{len(combinations)}: {params}")

            try:
                # Run backtest with these parameters
                runner = StrategyRunner(
                    initial_balance=initial_balance,
                    max_risk_per_trade=params.get("max_risk_per_trade", 0.02),
                    trading_fee=params.get("trading_fee", 0.001),
                )

                # Note: For full optimization, you'd need to modify StrategyRunner
                # to accept custom parameters for indicators, thresholds, etc.
                # For now, we'll just vary risk management parameters

                import asyncio
                result = asyncio.run(runner.run(self.candles_df, self.news_data))

                # Calculate metrics
                metrics_calc = PerformanceMetrics(
                    result["trades"], result["equity_curve"]
                )
                metrics = metrics_calc.calculate_all()

                # Store result
                result_entry = {
                    "params": params,
                    "metrics": metrics,
                }
                all_results.append(result_entry)

                # Check if this is the best
                score = metrics.get(metric_to_optimize, 0)
                if score > best_score:
                    best_score = score
                    best_params = params
                    best_metrics = metrics

            except Exception as e:
                logger.error(f"Error testing combination {params}: {e}")
                continue

        logger.info(f"Optimization complete. Best {metric_to_optimize}: {best_score:.2f}")

        return best_params, best_metrics, all_results

    def _count_combinations(self, param_grid: Dict[str, List]) -> int:
        """Count total number of parameter combinations"""
        count = 1
        for values in param_grid.values():
            count *= len(values)
        return count

    def generate_optimization_report(self, all_results: List[Dict]) -> pd.DataFrame:
        """
        Generate optimization report as DataFrame

        Args:
            all_results: List of all optimization results

        Returns:
            DataFrame with parameters and metrics
        """
        if not all_results:
            return pd.DataFrame()

        # Flatten results
        rows = []
        for result in all_results:
            row = {**result["params"], **result["metrics"]}
            rows.append(row)

        df = pd.DataFrame(rows)

        # Sort by Sharpe ratio
        if "sharpe_ratio" in df.columns:
            df = df.sort_values("sharpe_ratio", ascending=False)

        return df

    def plot_optimization_results(self, all_results: List[Dict], output_path: str = "optimization_results.png"):
        """
        Plot optimization results

        Args:
            all_results: List of all optimization results
            output_path: Path to save plot
        """
        try:
            import matplotlib.pyplot as plt

            df = self.generate_optimization_report(all_results)

            if df.empty:
                logger.warning("No results to plot")
                return

            # Plot top 10 results
            top_10 = df.head(10)

            fig, axes = plt.subplots(2, 2, figsize=(14, 10))

            # Sharpe Ratio
            ax = axes[0, 0]
            ax.bar(range(len(top_10)), top_10["sharpe_ratio"], color="#0ea5e9")
            ax.set_title("Top 10 - Sharpe Ratio")
            ax.set_ylabel("Sharpe Ratio")
            ax.set_xticks(range(len(top_10)))
            ax.set_xticklabels(range(len(top_10)), rotation=45)

            # Total Return
            ax = axes[0, 1]
            ax.bar(range(len(top_10)), top_10["total_return"], color="#10b981")
            ax.set_title("Top 10 - Total Return (%)")
            ax.set_ylabel("Return (%)")
            ax.set_xticks(range(len(top_10)))
            ax.set_xticklabels(range(len(top_10)), rotation=45)

            # Max Drawdown
            ax = axes[1, 0]
            ax.bar(range(len(top_10)), top_10["max_drawdown"], color="#ef4444")
            ax.set_title("Top 10 - Max Drawdown (%)")
            ax.set_ylabel("Drawdown (%)")
            ax.set_xticks(range(len(top_10)))
            ax.set_xticklabels(range(len(top_10)), rotation=45)

            # Win Rate
            ax = axes[1, 1]
            ax.bar(range(len(top_10)), top_10["win_rate"], color="#f59e0b")
            ax.set_title("Top 10 - Win Rate (%)")
            ax.set_ylabel("Win Rate (%)")
            ax.set_xticks(range(len(top_10)))
            ax.set_xticklabels(range(len(top_10)), rotation=45)

            plt.tight_layout()
            plt.savefig(output_path, dpi=150)
            plt.close()

            logger.info(f"Optimization plot saved: {output_path}")

        except Exception as e:
            logger.error(f"Error plotting optimization results: {e}")
