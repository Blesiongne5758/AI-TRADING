"""
Performance Metrics - Calculate trading performance metrics
"""
import pandas as pd
import numpy as np
from typing import List, Dict
from loguru import logger
import empyrical
from scipy import stats


class PerformanceMetrics:
    """Calculate performance metrics from backtest results"""

    def __init__(self, trades: List[Dict], equity_curve: List[Dict], risk_free_rate: float = 0.0):
        """
        Initialize performance metrics calculator

        Args:
            trades: List of completed trades
            equity_curve: List of equity snapshots
            risk_free_rate: Risk-free rate for Sharpe/Sortino (annualized)
        """
        self.trades = trades
        self.equity_curve = equity_curve
        self.risk_free_rate = risk_free_rate

        # Convert to DataFrames
        self.trades_df = pd.DataFrame(trades)
        self.equity_df = pd.DataFrame(equity_curve)

        if not self.equity_df.empty:
            self.equity_df.set_index("timestamp", inplace=True)

    def calculate_all(self) -> Dict:
        """
        Calculate all performance metrics

        Returns:
            Dictionary with all metrics
        """
        metrics = {
            "total_return": self.total_return(),
            "cagr": self.cagr(),
            "sharpe_ratio": self.sharpe_ratio(),
            "sortino_ratio": self.sortino_ratio(),
            "calmar_ratio": self.calmar_ratio(),
            "max_drawdown": self.max_drawdown(),
            "max_drawdown_duration": self.max_drawdown_duration(),
            "win_rate": self.win_rate(),
            "profit_factor": self.profit_factor(),
            "avg_win": self.avg_win(),
            "avg_loss": self.avg_loss(),
            "largest_win": self.largest_win(),
            "largest_loss": self.largest_loss(),
            "total_trades": self.total_trades(),
            "winning_trades": self.winning_trades(),
            "losing_trades": self.losing_trades(),
            "avg_trade_duration": self.avg_trade_duration(),
            "expectancy": self.expectancy(),
            "payoff_ratio": self.payoff_ratio(),
        }

        return metrics

    def total_return(self) -> float:
        """Calculate total return percentage"""
        if self.equity_df.empty:
            return 0.0

        initial_equity = self.equity_df["equity"].iloc[0]
        final_equity = self.equity_df["equity"].iloc[-1]

        return ((final_equity - initial_equity) / initial_equity) * 100

    def cagr(self) -> float:
        """Calculate Compound Annual Growth Rate"""
        if self.equity_df.empty or len(self.equity_df) < 2:
            return 0.0

        initial_equity = self.equity_df["equity"].iloc[0]
        final_equity = self.equity_df["equity"].iloc[-1]

        # Calculate years
        time_diff = self.equity_df.index[-1] - self.equity_df.index[0]
        years = time_diff.days / 365.25

        if years <= 0:
            return 0.0

        # CAGR formula
        cagr = ((final_equity / initial_equity) ** (1 / years) - 1) * 100

        return cagr

    def sharpe_ratio(self) -> float:
        """Calculate Sharpe Ratio (annualized)"""
        if self.equity_df.empty or len(self.equity_df) < 2:
            return 0.0

        # Calculate daily returns
        returns = self.equity_df["equity"].pct_change().dropna()

        if returns.empty or returns.std() == 0:
            return 0.0

        # Annualize (assuming hourly data, 24 * 365 = 8760 periods per year)
        periods_per_year = 8760
        excess_returns = returns - (self.risk_free_rate / periods_per_year)

        sharpe = (excess_returns.mean() / excess_returns.std()) * np.sqrt(periods_per_year)

        return sharpe

    def sortino_ratio(self) -> float:
        """Calculate Sortino Ratio (focuses on downside risk)"""
        if self.equity_df.empty or len(self.equity_df) < 2:
            return 0.0

        # Calculate daily returns
        returns = self.equity_df["equity"].pct_change().dropna()

        if returns.empty:
            return 0.0

        # Calculate downside deviation
        downside_returns = returns[returns < 0]
        if downside_returns.empty or downside_returns.std() == 0:
            return 0.0

        # Annualize
        periods_per_year = 8760
        excess_returns = returns - (self.risk_free_rate / periods_per_year)

        sortino = (excess_returns.mean() / downside_returns.std()) * np.sqrt(periods_per_year)

        return sortino

    def calmar_ratio(self) -> float:
        """Calculate Calmar Ratio (CAGR / Max Drawdown)"""
        cagr = self.cagr()
        max_dd = abs(self.max_drawdown())

        if max_dd == 0:
            return 0.0

        return cagr / max_dd

    def max_drawdown(self) -> float:
        """Calculate maximum drawdown percentage"""
        if self.equity_df.empty:
            return 0.0

        equity = self.equity_df["equity"]
        running_max = equity.expanding().max()
        drawdown = (equity - running_max) / running_max * 100

        return drawdown.min()

    def max_drawdown_duration(self) -> int:
        """Calculate maximum drawdown duration in days"""
        if self.equity_df.empty:
            return 0

        equity = self.equity_df["equity"]
        running_max = equity.expanding().max()

        # Find drawdown periods
        in_drawdown = equity < running_max
        drawdown_groups = (~in_drawdown).cumsum()
        drawdown_durations = in_drawdown.groupby(drawdown_groups).sum()

        if drawdown_durations.empty:
            return 0

        # Convert to days (assuming hourly data)
        max_duration_hours = drawdown_durations.max()
        max_duration_days = max_duration_hours / 24

        return int(max_duration_days)

    def win_rate(self) -> float:
        """Calculate win rate percentage"""
        if self.trades_df.empty:
            return 0.0

        winning_trades = self.trades_df[self.trades_df["pnl"] > 0]
        total_trades = len(self.trades_df)

        if total_trades == 0:
            return 0.0

        return (len(winning_trades) / total_trades) * 100

    def profit_factor(self) -> float:
        """Calculate profit factor (gross profit / gross loss)"""
        if self.trades_df.empty:
            return 0.0

        winning_trades = self.trades_df[self.trades_df["pnl"] > 0]
        losing_trades = self.trades_df[self.trades_df["pnl"] < 0]

        gross_profit = winning_trades["pnl"].sum()
        gross_loss = abs(losing_trades["pnl"].sum())

        if gross_loss == 0:
            return 0.0

        return gross_profit / gross_loss

    def avg_win(self) -> float:
        """Calculate average winning trade"""
        if self.trades_df.empty:
            return 0.0

        winning_trades = self.trades_df[self.trades_df["pnl"] > 0]

        if winning_trades.empty:
            return 0.0

        return winning_trades["pnl"].mean()

    def avg_loss(self) -> float:
        """Calculate average losing trade"""
        if self.trades_df.empty:
            return 0.0

        losing_trades = self.trades_df[self.trades_df["pnl"] < 0]

        if losing_trades.empty:
            return 0.0

        return losing_trades["pnl"].mean()

    def largest_win(self) -> float:
        """Calculate largest winning trade"""
        if self.trades_df.empty:
            return 0.0

        return self.trades_df["pnl"].max()

    def largest_loss(self) -> float:
        """Calculate largest losing trade"""
        if self.trades_df.empty:
            return 0.0

        return self.trades_df["pnl"].min()

    def total_trades(self) -> int:
        """Calculate total number of trades"""
        return len(self.trades_df)

    def winning_trades(self) -> int:
        """Calculate number of winning trades"""
        if self.trades_df.empty:
            return 0

        return len(self.trades_df[self.trades_df["pnl"] > 0])

    def losing_trades(self) -> int:
        """Calculate number of losing trades"""
        if self.trades_df.empty:
            return 0

        return len(self.trades_df[self.trades_df["pnl"] < 0])

    def avg_trade_duration(self) -> float:
        """Calculate average trade duration in hours"""
        if self.trades_df.empty:
            return 0.0

        durations = []
        for _, trade in self.trades_df.iterrows():
            duration = trade["exit_time"] - trade["entry_time"]
            durations.append(duration.total_seconds() / 3600)  # Convert to hours

        return np.mean(durations) if durations else 0.0

    def expectancy(self) -> float:
        """Calculate expectancy (average profit per trade)"""
        if self.trades_df.empty:
            return 0.0

        return self.trades_df["pnl"].mean()

    def payoff_ratio(self) -> float:
        """Calculate payoff ratio (avg win / avg loss)"""
        avg_win = self.avg_win()
        avg_loss = abs(self.avg_loss())

        if avg_loss == 0:
            return 0.0

        return avg_win / avg_loss

    # ============================================
    # ADVANCED METRICS (Empyrical & Scipy)
    # ============================================

    def annual_return(self) -> float:
        """Calculate annualized return using empyrical"""
        if self.equity_df.empty or len(self.equity_df) < 2:
            return 0.0

        returns = self.equity_df["equity"].pct_change().dropna()
        
        try:
            # Annualize returns (assuming hourly data)
            periods_per_year = 8760  # 24 * 365
            annualized = empyrical.annual_return(returns, period="hourly")
            return annualized * 100
        except:
            return self.cagr()

    def annual_volatility(self) -> float:
        """Calculate annualized volatility using empyrical"""
        if self.equity_df.empty or len(self.equity_df) < 2:
            return 0.0

        returns = self.equity_df["equity"].pct_change().dropna()
        
        try:
            annualized_vol = empyrical.annual_volatility(returns, period="hourly")
            return annualized_vol * 100
        except:
            return 0.0

    def alpha_beta(self, benchmark_returns: pd.Series = None) -> Dict[str, float]:
        """
        Calculate alpha and beta using empyrical
        
        Args:
            benchmark_returns: Benchmark returns series (optional)
        
        Returns:
            Dictionary with alpha and beta
        """
        if self.equity_df.empty or len(self.equity_df) < 2:
            return {"alpha": 0.0, "beta": 0.0}

        returns = self.equity_df["equity"].pct_change().dropna()
        
        # If no benchmark, use zero returns
        if benchmark_returns is None:
            benchmark_returns = pd.Series(0, index=returns.index)
        
        try:
            alpha, beta = empyrical.alpha_beta(returns, benchmark_returns)
            return {"alpha": alpha, "beta": beta}
        except:
            return {"alpha": 0.0, "beta": 0.0}

    def information_ratio(self, benchmark_returns: pd.Series = None) -> float:
        """
        Calculate information ratio using empyrical
        
        Args:
            benchmark_returns: Benchmark returns series (optional)
        
        Returns:
            Information ratio
        """
        if self.equity_df.empty or len(self.equity_df) < 2:
            return 0.0

        returns = self.equity_df["equity"].pct_change().dropna()
        
        if benchmark_returns is None:
            benchmark_returns = pd.Series(0, index=returns.index)
        
        try:
            ir = empyrical.information_ratio(returns, benchmark_returns)
            return ir
        except:
            return 0.0

    def tail_ratio(self) -> float:
        """
        Calculate tail ratio (right tail / left tail) using empyrical
        
        Returns:
            Tail ratio
        """
        if self.equity_df.empty or len(self.equity_df) < 2:
            return 0.0

        returns = self.equity_df["equity"].pct_change().dropna()
        
        try:
            tail_ratio = empyrical.tail_ratio(returns)
            return tail_ratio
        except:
            return 0.0

    def skewness(self) -> float:
        """Calculate return distribution skewness using scipy"""
        if self.equity_df.empty or len(self.equity_df) < 2:
            return 0.0

        returns = self.equity_df["equity"].pct_change().dropna()
        
        try:
            skew = stats.skew(returns)
            return skew
        except:
            return 0.0

    def kurtosis(self) -> float:
        """Calculate return distribution kurtosis using scipy"""
        if self.equity_df.empty or len(self.equity_df) < 2:
            return 0.0

        returns = self.equity_df["equity"].pct_change().dropna()
        
        try:
            kurt = stats.kurtosis(returns)
            return kurt
        except:
            return 0.0

    def jarque_bera_test(self) -> Dict[str, float]:
        """
        Perform Jarque-Bera test for normality using scipy
        
        Returns:
            Dictionary with test statistic and p-value
        """
        if self.equity_df.empty or len(self.equity_df) < 2:
            return {"statistic": 0.0, "p_value": 1.0}

        returns = self.equity_df["equity"].pct_change().dropna()
        
        try:
            jb_stat, p_value = stats.jarque_bera(returns)
            return {"statistic": jb_stat, "p_value": p_value}
        except:
            return {"statistic": 0.0, "p_value": 1.0}

    def calculate_advanced_metrics(self) -> Dict:
        """
        Calculate all advanced metrics
        
        Returns:
            Dictionary with advanced metrics
        """
        metrics = {
            "annual_return": self.annual_return(),
            "annual_volatility": self.annual_volatility(),
            "alpha_beta": self.alpha_beta(),
            "information_ratio": self.information_ratio(),
            "tail_ratio": self.tail_ratio(),
            "skewness": self.skewness(),
            "kurtosis": self.kurtosis(),
            "jarque_bera_test": self.jarque_bera_test(),
        }

        return metrics

    def print_summary(self):
        """Print performance summary"""
        metrics = self.calculate_all()

        logger.info("\n" + "=" * 70)
        logger.info("📊 BACKTEST PERFORMANCE SUMMARY")
        logger.info("=" * 70)

        logger.info(f"\n💰 RETURNS:")
        logger.info(f"   Total Return:        {metrics['total_return']:+.2f}%")
        logger.info(f"   CAGR:                {metrics['cagr']:+.2f}%")

        logger.info(f"\n📈 RISK-ADJUSTED METRICS:")
        logger.info(f"   Sharpe Ratio:        {metrics['sharpe_ratio']:.2f}")
        logger.info(f"   Sortino Ratio:       {metrics['sortino_ratio']:.2f}")
        logger.info(f"   Calmar Ratio:        {metrics['calmar_ratio']:.2f}")

        logger.info(f"\n📉 DRAWDOWN:")
        logger.info(f"   Max Drawdown:        {metrics['max_drawdown']:.2f}%")
        logger.info(f"   Max DD Duration:     {metrics['max_drawdown_duration']} days")

        logger.info(f"\n🎯 TRADE STATISTICS:")
        logger.info(f"   Total Trades:        {metrics['total_trades']}")
        logger.info(f"   Winning Trades:      {metrics['winning_trades']}")
        logger.info(f"   Losing Trades:       {metrics['losing_trades']}")
        logger.info(f"   Win Rate:            {metrics['win_rate']:.2f}%")

        logger.info(f"\n💵 PROFIT/LOSS:")
        logger.info(f"   Avg Win:             ${metrics['avg_win']:+,.2f}")
        logger.info(f"   Avg Loss:            ${metrics['avg_loss']:+,.2f}")
        logger.info(f"   Largest Win:         ${metrics['largest_win']:+,.2f}")
        logger.info(f"   Largest Loss:        ${metrics['largest_loss']:+,.2f}")
        logger.info(f"   Profit Factor:       {metrics['profit_factor']:.2f}")
        logger.info(f"   Payoff Ratio:        {metrics['payoff_ratio']:.2f}")
        logger.info(f"   Expectancy:          ${metrics['expectancy']:+,.2f}")

        logger.info(f"\n⏱️  DURATION:")
        logger.info(f"   Avg Trade Duration:  {metrics['avg_trade_duration']:.2f} hours")

        logger.info("=" * 70 + "\n")
