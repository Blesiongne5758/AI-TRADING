"""
Report Generator
Menghasilkan laporan visual dari hasil backtest
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from typing import Dict
from datetime import datetime
from loguru import logger
from .strategy_runner import BacktestResult


class ReportGenerator:
    """Menghasilkan laporan visual backtest"""

    def __init__(self, output_dir: str = "backtest_reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        # Style
        plt.style.use("dark_background")
        sns.set_theme(style="darkgrid")

    def generate_full_report(self, result: BacktestResult, metrics: Dict, grades: Dict):
        """Generate laporan lengkap dengan multiple charts"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_dir = self.output_dir / f"{result.symbol.replace('/', '_')}_{timestamp}"
        report_dir.mkdir(exist_ok=True)

        logger.info(f"📊 Generating report in {report_dir}")

        # 1. Equity Curve
        self._plot_equity_curve(result, metrics, report_dir / "equity_curve.png")

        # 2. Drawdown Chart
        self._plot_drawdown(result, report_dir / "drawdown.png")

        # 3. Trade Distribution
        self._plot_trade_distribution(result, report_dir / "trade_distribution.png")

        # 4. Monthly Returns Heatmap
        self._plot_monthly_returns(result, report_dir / "monthly_returns.png")

        # 5. Win/Loss by Exit Reason
        self._plot_exit_reasons(result, report_dir / "exit_reasons.png")

        # 6. Summary Text Report
        self._generate_text_report(result, metrics, grades, report_dir / "summary.txt")

        logger.info(f"✅ Report generated: {report_dir}")
        return report_dir

    def _plot_equity_curve(self, result: BacktestResult, metrics: Dict, output_path: Path):
        """Plot equity curve dengan benchmark"""
        equity_df = pd.DataFrame(result.equity_curve)
        
        fig, ax = plt.subplots(figsize=(14, 7))
        
        # Equity curve
        ax.plot(
            equity_df["timestamp"],
            equity_df["balance"],
            color="#10b981",
            linewidth=2,
            label=f"Strategy (${result.final_balance:,.2f})",
        )
        
        # Initial balance reference
        ax.axhline(
            y=result.initial_balance,
            color="#64748b",
            linestyle="--",
            label=f"Initial (${result.initial_balance:,.2f})",
        )
        
        ax.fill_between(
            equity_df["timestamp"],
            result.initial_balance,
            equity_df["balance"],
            where=equity_df["balance"] >= result.initial_balance,
            color="#10b981",
            alpha=0.1,
        )
        ax.fill_between(
            equity_df["timestamp"],
            result.initial_balance,
            equity_df["balance"],
            where=equity_df["balance"] < result.initial_balance,
            color="#ef4444",
            alpha=0.1,
        )

        ax.set_title(
            f"Equity Curve - {result.symbol} [{result.timeframe}]\n"
            f"Return: {metrics['total_return_percent']:+.2f}% | "
            f"Sharpe: {metrics['sharpe_ratio']:.2f} | "
            f"Max DD: {metrics['max_drawdown_percent']:.2f}%",
            fontsize=14,
            fontweight="bold",
            color="white",
        )
        ax.set_ylabel("Balance ($)", color="white")
        ax.set_xlabel("Date", color="white")
        ax.legend(loc="upper left")
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches="tight")
        plt.close()

    def _plot_drawdown(self, result: BacktestResult, output_path: Path):
        """Plot drawdown chart"""
        equity_df = pd.DataFrame(result.equity_curve)
        equity_df["peak"] = equity_df["balance"].cummax()
        equity_df["drawdown"] = (equity_df["balance"] - equity_df["peak"]) / equity_df["peak"] * 100

        fig, ax = plt.subplots(figsize=(14, 5))
        
        ax.fill_between(
            equity_df["timestamp"],
            0,
            equity_df["drawdown"],
            color="#ef4444",
            alpha=0.5,
        )
        ax.plot(
            equity_df["timestamp"],
            equity_df["drawdown"],
            color="#ef4444",
            linewidth=1,
        )

        ax.set_title("Drawdown (%)", fontsize=14, fontweight="bold", color="white")
        ax.set_ylabel("Drawdown %", color="white")
        ax.set_xlabel("Date", color="white")
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches="tight")
        plt.close()

    def _plot_trade_distribution(self, result: BacktestResult, output_path: Path):
        """Plot distribusi PnL per trade"""
        if not result.trades:
            return

        pnls = [t.pnl for t in result.trades]
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        # Histogram PnL
        axes[0].hist(pnls, bins=30, color="#0ea5e9", alpha=0.7, edgecolor="black")
        axes[0].axvline(x=0, color="red", linestyle="--", linewidth=2)
        axes[0].set_title("PnL Distribution", fontsize=12, fontweight="bold", color="white")
        axes[0].set_xlabel("PnL ($)", color="white")
        axes[0].set_ylabel("Frequency", color="white")
        
        # Cumulative PnL
        cum_pnl = pd.Series(pnls).cumsum()
        colors = ["#10b981" if p > 0 else "#ef4444" for p in pnls]
        axes[1].bar(range(len(cum_pnl)), pnls, color=colors, alpha=0.7)
        axes[1].plot(range(len(cum_pnl)), cum_pnl, color="#f59e0b", linewidth=2, label="Cumulative")
        axes[1].set_title("Trade-by-Trade PnL", fontsize=12, fontweight="bold", color="white")
        axes[1].set_xlabel("Trade #", color="white")
        axes[1].set_ylabel("PnL ($)", color="white")
        axes[1].legend()
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches="tight")
        plt.close()

    def _plot_monthly_returns(self, result: BacktestResult, output_path: Path):
        """Plot heatmap return bulanan"""
        if not result.trades:
            return

        # Group trades by month
        trades_df = pd.DataFrame([t.__dict__ for t in result.trades])
        trades_df["month"] = pd.to_datetime(trades_df["exit_time"]).dt.to_period("M")
        monthly_pnl = trades_df.groupby("month")["pnl"].sum()
        
        # Convert to percentage
        monthly_return = (monthly_pnl / result.initial_balance) * 100

        fig, ax = plt.subplots(figsize=(14, 4))
        colors = ["#10b981" if r > 0 else "#ef4444" for r in monthly_return]
        ax.bar(range(len(monthly_return)), monthly_return, color=colors, alpha=0.7)
        ax.set_xticks(range(len(monthly_return)))
        ax.set_xticklabels([str(m) for m in monthly_return.index], rotation=45, ha="right")
        ax.axhline(y=0, color="white", linestyle="-", linewidth=1)
        ax.set_title("Monthly Returns (%)", fontsize=14, fontweight="bold", color="white")
        ax.set_ylabel("Return %", color="white")
        ax.grid(True, alpha=0.3, axis="y")
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches="tight")
        plt.close()

    def _plot_exit_reasons(self, result: BacktestResult, output_path: Path):
        """Plot distribusi exit reasons"""
        if not result.trades:
            return

        trades_df = pd.DataFrame([t.__dict__ for t in result.trades])
        exit_counts = trades_df["exit_reason"].value_counts()

        fig, ax = plt.subplots(figsize=(8, 6))
        colors = {
            "TAKE_PROFIT": "#10b981",
            "STOP_LOSS": "#ef4444",
            "BACKTEST_END": "#64748b",
        }
        bar_colors = [colors.get(reason, "#0ea5e9") for reason in exit_counts.index]
        
        ax.pie(
            exit_counts.values,
            labels=exit_counts.index,
            colors=bar_colors,
            autopct="%1.1f%%",
            startangle=90,
        )
        ax.set_title("Exit Reasons Distribution", fontsize=14, fontweight="bold", color="white")
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches="tight")
        plt.close()

    def _generate_text_report(
        self, result: BacktestResult, metrics: Dict, grades: Dict, output_path: Path
    ):
        """Generate text report"""
        report = f"""
{'='*70}
BACKTEST REPORT - {result.symbol} [{result.timeframe}]
{'='*70}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📅 PERIODE BACKTEST
  Start: {result.start_date}
  End:   {result.end_date}
  Days:  {metrics['backtest_days']}

💰 PERFORMANCE
  Initial Balance:  ${metrics['initial_balance']:>12,.2f}
  Final Balance:    ${metrics['final_balance']:>12,.2f}
  Net Profit:       ${metrics['net_profit']:>+12,.2f}
  Total Return:     {metrics['total_return_percent']:>+11.2f}%
  Annualized Return:{metrics['annualized_return_percent']:>+11.2f}%

📊 TRADE STATISTICS
  Total Trades:     {metrics['total_trades']:>12}
  Winning Trades:   {metrics['winning_trades']:>12}
  Losing Trades:    {metrics['losing_trades']:>12}
  Win Rate:         {metrics['win_rate_percent']:>11.2f}%
  Avg Win:          ${metrics['avg_win_usd']:>12,.2f}
  Avg Loss:         ${metrics['avg_loss_usd']:>12,.2f}
  Largest Win:      ${metrics['largest_win_usd']:>12,.2f}
  Largest Loss:     ${metrics['largest_loss_usd']:>12,.2f}
  Profit Factor:    {metrics['profit_factor']:>12.2f}
  Expectancy:       ${metrics['expectancy_usd']:>12,.2f}

⚠️  RISK METRICS
  Max Drawdown:     {metrics['max_drawdown_percent']:>11.2f}%
  Max DD (USD):     ${metrics['max_drawdown_usd']:>12,.2f}
  Volatility:       {metrics['annualized_volatility_percent']:>11.2f}%
  Sharpe Ratio:     {metrics['sharpe_ratio']:>12.2f}
  Sortino Ratio:    {metrics['sortino_ratio']:>12.2f}
  Calmar Ratio:     {metrics['calmar_ratio']:>12.2f}
  Kelly Criterion:  {metrics['kelly_criterion_percent']:>11.2f}%

🔀 BREAKDOWN
  Long Trades:      {metrics['long_trades']:>12} (WR: {metrics['long_win_rate_percent']:.1f}%)
  Short Trades:     {metrics['short_trades']:>12} (WR: {metrics['short_win_rate_percent']:.1f}%)
  Avg Holding:      {metrics['avg_holding_hours']:>10.1f} hours

📤 EXIT REASONS
"""
        for reason, count in metrics.get("exit_reasons", {}).items():
            pct = count / metrics["total_trades"] * 100
            report += f"  {reason:20} {count:>5} ({pct:.1f}%)\n"

        report += f"""
🎯 STRATEGY GRADING
"""
        for metric_name, (grade, desc) in grades["grades"].items():
            report += f"  {metric_name.upper():20} [{grade:>2}] - {desc}\n"

        report += f"""
  Overall Score:      {grades['overall_score']:.1f}/100
  Overall Grade:      {grades['overall_grade']}

💡 RECOMMENDATION
  {grades['recommendation']}

{'='*70}
"""

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(report)
