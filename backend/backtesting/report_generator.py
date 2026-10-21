"""
Report Generator - Generate visual reports from backtest results
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from typing import Dict, List
from datetime import datetime
from loguru import logger
import os


class ReportGenerator:
    """Generate visual reports from backtest results"""

    def __init__(self, trades: List[Dict], equity_curve: List[Dict], metrics: Dict):
        """
        Initialize report generator

        Args:
            trades: List of completed trades
            equity_curve: List of equity snapshots
            metrics: Performance metrics dictionary
        """
        self.trades = trades
        self.equity_curve = equity_curve
        self.metrics = metrics

        # Convert to DataFrames
        self.trades_df = pd.DataFrame(trades)
        self.equity_df = pd.DataFrame(equity_curve)

        if not self.equity_df.empty:
            self.equity_df.set_index("timestamp", inplace=True)

    def generate_report(self, output_dir: str = "backtest_reports") -> str:
        """
        Generate complete backtest report

        Args:
            output_dir: Directory to save reports

        Returns:
            Path to generated report
        """
        try:
            # Create output directory
            os.makedirs(output_dir, exist_ok=True)

            # Generate timestamp for filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_name = f"backtest_report_{timestamp}"

            # Generate plots
            self._plot_equity_curve(output_dir, report_name)
            self._plot_drawdown(output_dir, report_name)
            self._plot_trade_distribution(output_dir, report_name)
            self._plot_monthly_returns(output_dir, report_name)

            # Generate summary text
            summary_path = self._generate_summary(output_dir, report_name)

            logger.info(f"Report generated: {output_dir}/{report_name}")

            return f"{output_dir}/{report_name}"

        except Exception as e:
            logger.error(f"Error generating report: {e}")
            return ""

    def _plot_equity_curve(self, output_dir: str, report_name: str):
        """Plot equity curve"""
        if self.equity_df.empty:
            return

        try:
            fig, ax = plt.subplots(figsize=(12, 6))

            # Plot equity curve
            ax.plot(
                self.equity_df.index,
                self.equity_df["equity"],
                label="Equity",
                color="#0ea5e9",
                linewidth=2,
            )

            # Plot initial balance
            initial_balance = self.equity_df["equity"].iloc[0]
            ax.axhline(
                y=initial_balance,
                color="#94a3b8",
                linestyle="--",
                label="Initial Balance",
                linewidth=1,
            )

            # Formatting
            ax.set_title("Equity Curve", fontsize=16, fontweight="bold", pad=20)
            ax.set_xlabel("Date", fontsize=12)
            ax.set_ylabel("Equity ($)", fontsize=12)
            ax.legend(loc="upper left", fontsize=10)
            ax.grid(True, alpha=0.3)

            # Format x-axis
            ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
            ax.xaxis.set_major_locator(mdates.AutoDateLocator())
            fig.autofmt_xdate()

            # Add metrics text box
            metrics_text = (
                f"Total Return: {self.metrics['total_return']:+.2f}%\n"
                f"Sharpe Ratio: {self.metrics['sharpe_ratio']:.2f}\n"
                f"Max Drawdown: {self.metrics['max_drawdown']:.2f}%"
            )
            ax.text(
                0.02,
                0.98,
                metrics_text,
                transform=ax.transAxes,
                fontsize=10,
                verticalalignment="top",
                bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5),
            )

            plt.tight_layout()
            plt.savefig(f"{output_dir}/{report_name}_equity_curve.png", dpi=150)
            plt.close()

        except Exception as e:
            logger.error(f"Error plotting equity curve: {e}")

    def _plot_drawdown(self, output_dir: str, report_name: str):
        """Plot drawdown chart"""
        if self.equity_df.empty:
            return

        try:
            fig, ax = plt.subplots(figsize=(12, 4))

            # Calculate drawdown
            equity = self.equity_df["equity"]
            running_max = equity.expanding().max()
            drawdown = (equity - running_max) / running_max * 100

            # Plot drawdown
            ax.fill_between(
                drawdown.index,
                drawdown.values,
                0,
                color="#ef4444",
                alpha=0.3,
                label="Drawdown",
            )
            ax.plot(drawdown.index, drawdown.values, color="#ef4444", linewidth=1)

            # Formatting
            ax.set_title("Drawdown", fontsize=16, fontweight="bold", pad=20)
            ax.set_xlabel("Date", fontsize=12)
            ax.set_ylabel("Drawdown (%)", fontsize=12)
            ax.grid(True, alpha=0.3)

            # Format x-axis
            ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
            ax.xaxis.set_major_locator(mdates.AutoDateLocator())
            fig.autofmt_xdate()

            plt.tight_layout()
            plt.savefig(f"{output_dir}/{report_name}_drawdown.png", dpi=150)
            plt.close()

        except Exception as e:
            logger.error(f"Error plotting drawdown: {e}")

    def _plot_trade_distribution(self, output_dir: str, report_name: str):
        """Plot trade PnL distribution"""
        if self.trades_df.empty:
            return

        try:
            fig, ax = plt.subplots(figsize=(10, 6))

            # Separate winning and losing trades
            winning = self.trades_df[self.trades_df["pnl"] > 0]["pnl"]
            losing = self.trades_df[self.trades_df["pnl"] < 0]["pnl"]

            # Plot histogram
            if not winning.empty:
                ax.hist(
                    winning,
                    bins=20,
                    color="#10b981",
                    alpha=0.7,
                    label=f"Winning Trades ({len(winning)})",
                )
            if not losing.empty:
                ax.hist(
                    losing,
                    bins=20,
                    color="#ef4444",
                    alpha=0.7,
                    label=f"Losing Trades ({len(losing)})",
                )

            # Add vertical line at zero
            ax.axvline(x=0, color="#94a3b8", linestyle="--", linewidth=1)

            # Formatting
            ax.set_title("Trade PnL Distribution", fontsize=16, fontweight="bold", pad=20)
            ax.set_xlabel("PnL ($)", fontsize=12)
            ax.set_ylabel("Frequency", fontsize=12)
            ax.legend(loc="upper right", fontsize=10)
            ax.grid(True, alpha=0.3, axis="y")

            plt.tight_layout()
            plt.savefig(f"{output_dir}/{report_name}_trade_distribution.png", dpi=150)
            plt.close()

        except Exception as e:
            logger.error(f"Error plotting trade distribution: {e}")

    def _plot_monthly_returns(self, output_dir: str, report_name: str):
        """Plot monthly returns heatmap"""
        if self.equity_df.empty:
            return

        try:
            # Calculate monthly returns
            monthly_returns = self.equity_df["equity"].resample("M").last().pct_change() * 100
            monthly_returns = monthly_returns.dropna()

            if monthly_returns.empty:
                return

            # Group by year and month
            monthly_df = pd.DataFrame(
                {
                    "Year": monthly_returns.index.year,
                    "Month": monthly_returns.index.month,
                    "Return": monthly_returns.values,
                }
            )

            # Create pivot table
            pivot = monthly_df.pivot(index="Year", columns="Month", values="Return")

            # Plot heatmap
            fig, ax = plt.subplots(figsize=(12, max(4, len(pivot) * 0.5)))

            im = ax.imshow(
                pivot.values,
                cmap="RdYlGn",
                aspect="auto",
                vmin=-10,
                vmax=10,
            )

            # Set ticks
            ax.set_xticks(range(12))
            ax.set_xticklabels(
                [
                    "Jan",
                    "Feb",
                    "Mar",
                    "Apr",
                    "May",
                    "Jun",
                    "Jul",
                    "Aug",
                    "Sep",
                    "Oct",
                    "Nov",
                    "Dec",
                ]
            )
            ax.set_yticks(range(len(pivot)))
            ax.set_yticklabels(pivot.index)

            # Add text annotations
            for i in range(len(pivot)):
                for j in range(12):
                    if j < pivot.shape[1]:
                        value = pivot.values[i, j]
                        if not pd.isna(value):
                            text = ax.text(
                                j,
                                i,
                                f"{value:.1f}%",
                                ha="center",
                                va="center",
                                color="black",
                                fontsize=9,
                            )

            # Formatting
            ax.set_title("Monthly Returns (%)", fontsize=16, fontweight="bold", pad=20)
            ax.set_xlabel("Month", fontsize=12)
            ax.set_ylabel("Year", fontsize=12)

            # Add colorbar
            cbar = plt.colorbar(im, ax=ax, shrink=0.8)
            cbar.set_label("Return (%)", fontsize=10)

            plt.tight_layout()
            plt.savefig(f"{output_dir}/{report_name}_monthly_returns.png", dpi=150)
            plt.close()

        except Exception as e:
            logger.error(f"Error plotting monthly returns: {e}")

    def _generate_summary(self, output_dir: str, report_name: str) -> str:
        """Generate text summary"""
        try:
            summary_path = f"{output_dir}/{report_name}_summary.txt"

            with open(summary_path, "w") as f:
                f.write("=" * 70 + "\n")
                f.write("BACKTEST PERFORMANCE SUMMARY\n")
                f.write("=" * 70 + "\n\n")

                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

                f.write("RETURNS:\n")
                f.write(f"  Total Return:        {self.metrics['total_return']:+.2f}%\n")
                f.write(f"  CAGR:                {self.metrics['cagr']:+.2f}%\n\n")

                f.write("RISK-ADJUSTED METRICS:\n")
                f.write(f"  Sharpe Ratio:        {self.metrics['sharpe_ratio']:.2f}\n")
                f.write(f"  Sortino Ratio:       {self.metrics['sortino_ratio']:.2f}\n")
                f.write(f"  Calmar Ratio:        {self.metrics['calmar_ratio']:.2f}\n\n")

                f.write("DRAWDOWN:\n")
                f.write(f"  Max Drawdown:        {self.metrics['max_drawdown']:.2f}%\n")
                f.write(
                    f"  Max DD Duration:     {self.metrics['max_drawdown_duration']} days\n\n"
                )

                f.write("TRADE STATISTICS:\n")
                f.write(f"  Total Trades:        {self.metrics['total_trades']}\n")
                f.write(f"  Winning Trades:      {self.metrics['winning_trades']}\n")
                f.write(f"  Losing Trades:       {self.metrics['losing_trades']}\n")
                f.write(f"  Win Rate:            {self.metrics['win_rate']:.2f}%\n\n")

                f.write("PROFIT/LOSS:\n")
                f.write(f"  Avg Win:             ${self.metrics['avg_win']:+,.2f}\n")
                f.write(f"  Avg Loss:            ${self.metrics['avg_loss']:+,.2f}\n")
                f.write(f"  Largest Win:         ${self.metrics['largest_win']:+,.2f}\n")
                f.write(f"  Largest Loss:        ${self.metrics['largest_loss']:+,.2f}\n")
                f.write(f"  Profit Factor:       {self.metrics['profit_factor']:.2f}\n")
                f.write(f"  Payoff Ratio:        {self.metrics['payoff_ratio']:.2f}\n")
                f.write(f"  Expectancy:          ${self.metrics['expectancy']:+,.2f}\n\n")

                f.write("DURATION:\n")
                f.write(
                    f"  Avg Trade Duration:  {self.metrics['avg_trade_duration']:.2f} hours\n\n"
                )

                f.write("=" * 70 + "\n")

            return summary_path

        except Exception as e:
            logger.error(f"Error generating summary: {e}")
            return ""

    def generate_interactive_report(self, output_dir: str = "backtest_reports") -> str:
        """
        Generate interactive HTML report with Plotly

        Args:
            output_dir: Directory to save reports

        Returns:
            Path to generated HTML report
        """
        try:
            os.makedirs(output_dir, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_path = f"{output_dir}/interactive_report_{timestamp}.html"

            # Create subplots
            fig = make_subplots(
                rows=3,
                cols=2,
                subplot_titles=(
                    "Equity Curve",
                    "Drawdown",
                    "Trade PnL Distribution",
                    "Monthly Returns",
                    "Cumulative Trades",
                    "Risk Metrics",
                ),
                specs=[
                    [{"secondary_y": False}, {"secondary_y": False}],
                    [{"secondary_y": False}, {"secondary_y": False}],
                    [{"secondary_y": False}, {"type": "indicator"}],
                ],
            )

            # 1. Equity Curve
            if not self.equity_df.empty:
                fig.add_trace(
                    go.Scatter(
                        x=self.equity_df.index,
                        y=self.equity_df["equity"],
                        name="Equity",
                        line=dict(color="#0ea5e9", width=2),
                    ),
                    row=1,
                    col=1,
                )

            # 2. Drawdown
            if not self.equity_df.empty:
                equity = self.equity_df["equity"]
                running_max = equity.expanding().max()
                drawdown = (equity - running_max) / running_max * 100

                fig.add_trace(
                    go.Scatter(
                        x=drawdown.index,
                        y=drawdown.values,
                        name="Drawdown",
                        fill="tozeroy",
                        line=dict(color="#ef4444", width=1),
                        fillcolor="rgba(239, 68, 68, 0.3)",
                    ),
                    row=1,
                    col=2,
                )

            # 3. Trade PnL Distribution
            if not self.trades_df.empty:
                fig.add_trace(
                    go.Histogram(
                        x=self.trades_df["pnl"],
                        name="PnL Distribution",
                        marker_color="#10b981",
                        opacity=0.7,
                    ),
                    row=2,
                    col=1,
                )

            # 4. Monthly Returns
            if not self.equity_df.empty:
                monthly_returns = (
                    self.equity_df["equity"].resample("M").last().pct_change() * 100
                )
                monthly_returns = monthly_returns.dropna()

                if not monthly_returns.empty:
                    fig.add_trace(
                        go.Bar(
                            x=monthly_returns.index,
                            y=monthly_returns.values,
                            name="Monthly Returns",
                            marker_color=[
                                "#10b981" if r >= 0 else "#ef4444"
                                for r in monthly_returns.values
                            ],
                        ),
                        row=2,
                        col=2,
                    )

            # 5. Cumulative Trades
            if not self.trades_df.empty:
                cumulative_trades = range(1, len(self.trades_df) + 1)
                fig.add_trace(
                    go.Scatter(
                        x=list(cumulative_trades),
                        y=self.trades_df["pnl"].cumsum(),
                        name="Cumulative PnL",
                        line=dict(color="#f59e0b", width=2),
                    ),
                    row=3,
                    col=1,
                )

            # 6. Risk Metrics Indicator
            fig.add_trace(
                go.Indicator(
                    mode="gauge+number+delta",
                    value=self.metrics.get("sharpe_ratio", 0),
                    title={"text": "Sharpe Ratio"},
                    gauge={
                        "axis": {"range": [None, 3]},
                        "bar": {"color": "#0ea5e9"},
                        "steps": [
                            {"range": [0, 1], "color": "#ef4444"},
                            {"range": [1, 2], "color": "#f59e0b"},
                            {"range": [2, 3], "color": "#10b981"},
                        ],
                    },
                ),
                row=3,
                col=2,
            )

            # Update layout
            fig.update_layout(
                title_text=f"Backtest Report - {timestamp}",
                showlegend=True,
                height=1200,
                width=1400,
            )

            # Save to HTML
            fig.write_html(report_path)

            logger.info(f"Interactive report saved: {report_path}")
            return report_path

        except Exception as e:
            logger.error(f"Error generating interactive report: {e}")
            return ""

    def generate_seaborn_report(self, output_dir: str = "backtest_reports") -> str:
        """
        Generate statistical reports with Seaborn

        Args:
            output_dir: Directory to save reports

        Returns:
            Path to generated report
        """
        try:
            os.makedirs(output_dir, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_path = f"{output_dir}/statistical_report_{timestamp}.png"

            # Set seaborn style
            sns.set_theme(style="darkgrid")

            # Create figure with subplots
            fig, axes = plt.subplots(2, 2, figsize=(16, 12))

            # 1. PnL Distribution with KDE
            if not self.trades_df.empty:
                sns.histplot(
                    data=self.trades_df,
                    x="pnl",
                    kde=True,
                    ax=axes[0, 0],
                    color="#0ea5e9",
                )
                axes[0, 0].set_title("Trade PnL Distribution")
                axes[0, 0].axvline(0, color="red", linestyle="--")

            # 2. Win/Loss Comparison
            if not self.trades_df.empty:
                win_loss = self.trades_df.copy()
                win_loss["result"] = win_loss["pnl"].apply(
                    lambda x: "Win" if x > 0 else "Loss"
                )
                sns.countplot(data=win_loss, x="result", ax=axes[0, 1], palette=["#ef4444", "#10b981"])
                axes[0, 1].set_title("Win/Loss Distribution")

            # 3. Trade Duration vs PnL
            if not self.trades_df.empty and "entry_time" in self.trades_df.columns:
                self.trades_df["duration_hours"] = (
                    self.trades_df["exit_time"] - self.trades_df["entry_time"]
                ).dt.total_seconds() / 3600

                sns.scatterplot(
                    data=self.trades_df,
                    x="duration_hours",
                    y="pnl",
                    ax=axes[1, 0],
                    hue="pnl",
                    palette="RdYlGn",
                    size="pnl",
                    sizes=(20, 200),
                )
                axes[1, 0].set_title("Trade Duration vs PnL")
                axes[1, 0].axhline(0, color="red", linestyle="--")

            # 4. Cumulative Returns
            if not self.equity_df.empty:
                returns = self.equity_df["equity"].pct_change()
                cumulative_returns = (1 + returns).cumprod() - 1

                sns.lineplot(
                    x=cumulative_returns.index,
                    y=cumulative_returns.values * 100,
                    ax=axes[1, 1],
                    color="#10b981",
                    linewidth=2,
                )
                axes[1, 1].set_title("Cumulative Returns (%)")
                axes[1, 1].axhline(0, color="gray", linestyle="--")

            plt.tight_layout()
            plt.savefig(report_path, dpi=150, bbox_inches="tight")
            plt.close()

            logger.info(f"Statistical report saved: {report_path}")
            return report_path

        except Exception as e:
            logger.error(f"Error generating seaborn report: {e}")
            return ""
