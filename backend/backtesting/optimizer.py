"""
Parameter Optimizer
Mencari parameter terbaik menggunakan grid search atau Optuna
"""
import itertools
from typing import Dict, List, Callable, Tuple
import pandas as pd
from loguru import logger
from .strategy_runner import StrategyRunner, BacktestResult
from .performance_metrics import PerformanceMetrics


class ParameterOptimizer:
    """Optimizer parameter strategi"""

    def __init__(self, strategy_runner: StrategyRunner):
        self.runner = strategy_runner
        self.metrics_calc = PerformanceMetrics()

    def grid_search(
        self,
         pd.DataFrame,
        symbol: str,
        timeframe: str,
        strategy_func: Callable,
        param_grid: Dict[str, List],
        optimize_for: str = "sharpe_ratio",
    ) -> List[Dict]:
        """
        Grid search untuk mencari parameter terbaik
        
        Args:
             Dict dengan list nilai untuk setiap parameter
                        Contoh: {"rsi_period": [10, 14, 20], "rsi_oversold": [25, 30, 35]}
            optimize_for: Metrik yang dioptimasi (sharpe_ratio, profit_factor, total_return, dll)
            
        Returns:
            List hasil sorted by optimize_for (descending)
        """
        # Generate semua kombinasi parameter
        keys = list(param_grid.keys())
        values = list(param_grid.values())
        combinations = list(itertools.product(*values))

        logger.info(f"🔬 Grid search: {len(combinations)} combinations")
        logger.info(f"   Optimizing for: {optimize_for}")

        results = []

        for i, combo in enumerate(combinations):
            params = dict(zip(keys, combo))

            try:
                # Run backtest
                result = self.runner.run_backtest(
                    data=data,
                    symbol=symbol,
                    timeframe=timeframe,
                    strategy_func=strategy_func,
                    strategy_params=params,
                )

                # Calculate metrics
                metrics = self.metrics_calc.calculate_all(result)

                # Skip jika tidak ada trade
                if metrics["total_trades"] < 10:
                    continue

                results.append({
                    "parameters": params,
                    "metrics": metrics,
                    "optimize_value": metrics.get(optimize_for, 0),
                })

                if (i + 1) % 10 == 0:
                    logger.info(f"   Progress: {i+1}/{len(combinations)}")

            except Exception as e:
                logger.debug(f"Error with params {params}: {e}")
                continue

        # Sort by optimize value (descending)
        results.sort(key=lambda x: x["optimize_value"], reverse=True)

        logger.info(f"✅ Grid search complete: {len(results)} valid results")
        if results:
            logger.info(f"   Best {optimize_for}: {results[0]['optimize_value']:.2f}")
            logger.info(f"   Best params: {results[0]['parameters']}")

        return results

    def optuna_optimize(
        self,
         pd.DataFrame,
        symbol: str,
        timeframe: str,
        strategy_func: Callable,
        param_space: Dict[str, Tuple],
        optimize_for: str = "sharpe_ratio",
        n_trials: int = 50,
    ) -> Dict:
        """
        Optimasi dengan Optuna (lebih efisien dari grid search)
        
        Args:
            param_space: Dict dengan (min, max) untuk setiap parameter
                        Contoh: {"rsi_period": (10, 30), "rsi_oversold": (20, 40)}
        """
        try:
            import optuna
            optuna.logging.set_verbosity(optuna.logging.WARNING)
        except ImportError:
            logger.error("❌ Optuna not installed. Run: pip install optuna")
            return {}

        def objective(trial):
            # Sample parameters
            params = {}
            for param_name, (low, high) in param_space.items():
                params[param_name] = trial.suggest_int(param_name, low, high)

            try:
                result = self.runner.run_backtest(
                    data=data,
                    symbol=symbol,
                    timeframe=timeframe,
                    strategy_func=strategy_func,
                    strategy_params=params,
                )
                metrics = self.metrics_calc.calculate_all(result)

                if metrics["total_trades"] < 10:
                    return -999  # Penalty untuk trade terlalu sedikit

                return metrics.get(optimize_for, 0)
            except Exception:
                return -999

        logger.info(f"🔬 Optuna optimization: {n_trials} trials")
        study = optuna.create_study(direction="maximize")
        study.optimize(objective, n_trials=n_trials, show_progress_bar=True)

        best_params = study.best_params
        best_value = study.best_value

        logger.info(f"✅ Best {optimize_for}: {best_value:.2f}")
        logger.info(f"   Best params: {best_params}")

        return {
            "best_params": best_params,
            "best_value": best_value,
            "all_trials": [
                {"params": t.params, "value": t.value}
                for t in study.trials
                if t.value is not None and t.value > -999
            ],
        }
