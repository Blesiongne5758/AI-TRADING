"""
Performance Metrics
Menghitung metrik performa profesional (Sharpe, Sortino, Calmar, dll)
"""
import pandas as pd
import numpy as np
from typing import Dict, List
from .strategy_runner import BacktestResult
from loguru import logger


class PerformanceMetrics:
    """Menghitung metrik performa backtest"""

    def calculate_all(self, result: BacktestResult, risk_free_rate: float = 0.05) -> Dict:
        """
        Menghitung SEMUA metrik performa
        
        Args:
            result: BacktestResult dari strategy runner
            risk_free_rate: Risk-free rate tahunan (default 5% = US Treasury)
            
        Returns:
            Dictionary dengan semua metrik
        """
        if not result.trades:
            return self._empty_metrics()

        # Konversi trades ke DataFrame
        trades_df = pd.DataFrame([t.__dict__ for t in result.trades])
        equity_df = pd.DataFrame(result.equity_curve)

        # === RETURN METRICS ===
        total_return = (result.final_balance / result.initial_balance) - 1
        
        # Annualized return
        days = (result.end_date - result.start_date).days
        years = days / 365.25
        annualized_return = ((1 + total_return) ** (1 / years)) - 1 if years > 0 else 0

        # === TRADE STATISTICS ===
        winning_trades = trades_df[trades_df["pnl"] > 0]
        losing_trades = trades_df[trades_df["pnl"] < 0]
        
        total_trades = len(trades_df)
        winning_count = len(winning_trades)
        losing_count = len(losing_trades)
        win_rate = (winning_count / total_trades * 100) if total_trades > 0 else 0

        avg_win = winning_trades["pnl"].mean() if len(winning_trades) > 0 else 0
        avg_loss = abs(losing_trades["pnl"].mean()) if len(losing_trades) > 0 else 0
        profit_factor = (avg_win / avg_loss) if avg_loss > 0 else float("inf")

        largest_win = trades_df["pnl"].max()
        largest_loss = trades_df["pnl"].min()

        # === DRAWDOWN METRICS ===
        equity_df["peak"] = equity_df["balance"].cummax()
        equity_df["drawdown"] = (equity_df["balance"] - equity_df["peak"]) / equity_df["peak"]
        
        max_drawdown = abs(equity_df["drawdown"].min())
        max_drawdown_usd = (equity_df["peak"] - equity_df["balance"]).max()

        # Calmar Ratio = Annualized Return / Max Drawdown
        calmar_ratio = annualized_return / max_drawdown if max_drawdown > 0 else 0

        # === RISK METRICS ===
        # Daily returns
        equity_df["daily_return"] = equity_df["balance"].pct_change()
        daily_returns = equity_df["daily_return"].dropna()

        # Volatility (annualized)
        daily_volatility = daily_returns.std()
        annualized_volatility = daily_volatility * np.sqrt(365)

        # Sharpe Ratio = (Return - Risk Free) / Volatility
        excess_return = annualized_return - risk_free_rate
        sharpe_ratio = excess_return / annualized_volatility if annualized_volatility > 0 else 0

        # Sortino Ratio (hanya hitung downside deviation)
        downside_returns = daily_returns[daily_returns < 0]
        downside_deviation = downside_returns.std() * np.sqrt(365) if len(downside_returns) > 0 else 0
        sortino_ratio = excess_return / downside_deviation if downside_deviation > 0 else 0

        # === HOLDING PERIOD ===
        avg_holding_hours = trades_df["holding_period"].mean() if "holding_period" in trades_df else 0

        # === EXIT REASON DISTRIBUTION ===
        exit_reasons = trades_df["exit_reason"].value_counts().to_dict() if "exit_reason" in trades_df else {}

        # === LONG VS SHORT PERFORMANCE ===
        long_trades = trades_df[trades_df["side"] == "long"]
        short_trades = trades_df[trades_df["side"] == "short"]
        
        long_win_rate = (len(long_trades[long_trades["pnl"] > 0]) / len(long_trades) * 100) if len(long_trades) > 0 else 0
        short_win_rate = (len(short_trades[short_trades["pnl"] > 0]) / len(short_trades) * 100) if len(short_trades) > 0 else 0

        # === EXPECTANCY (harapan matematis per trade) ===
        expectancy = (
            (win_rate / 100 * avg_win) - ((1 - win_rate / 100) * avg_loss)
        )

        # === PAYOFF RATIO ===
        payoff_ratio = avg_win / avg_loss if avg_loss > 0 else 0

        # === KELLY CRITERION (optimal position sizing) ===
        kelly_fraction = (win_rate / 100) - ((1 - win_rate / 100) / payoff_ratio) if payoff_ratio > 0 else 0

        return {
            # Return
            "total_return_percent": round(total_return * 100, 2),
            "annualized_return_percent": round(annualized_return * 100, 2),
            "initial_balance": result.initial_balance,
            "final_balance": round(result.final_balance, 2),
            "net_profit": round(result.final_balance - result.initial_balance, 2),
            
            # Trade stats
            "total_trades": total_trades,
            "winning_trades": winning_count,
            "losing_trades": losing_count,
            "win_rate_percent": round(win_rate, 2),
            "avg_win_usd": round(avg_win, 2),
            "avg_loss_usd": round(avg_loss, 2),
            "largest_win_usd": round(largest_win, 2),
            "largest_loss_usd": round(largest_loss, 2),
            "profit_factor": round(profit_factor, 2),
            "expectancy_usd": round(expectancy, 2),
            "payoff_ratio": round(payoff_ratio, 2),
            
            # Risk
            "max_drawdown_percent": round(max_drawdown * 100, 2),
            "max_drawdown_usd": round(max_drawdown_usd, 2),
            "annualized_volatility_percent": round(annualized_volatility * 100, 2),
            "sharpe_ratio": round(sharpe_ratio, 2),
            "sortino_ratio": round(sortino_ratio, 2),
            "calmar_ratio": round(calmar_ratio, 2),
            "kelly_criterion_percent": round(max(kelly_fraction * 100, 0), 2),
            
            # Timing
            "avg_holding_hours": round(avg_holding_hours, 2),
            "backtest_days": days,
            
            # Breakdown
            "long_win_rate_percent": round(long_win_rate, 2),
            "short_win_rate_percent": round(short_win_rate, 2),
            "long_trades": len(long_trades),
            "short_trades": len(short_trades),
            
            # Exit reasons
            "exit_reasons": exit_reasons,
            
            # Data untuk plotting
            "equity_curve": result.equity_curve,
        }

    def _empty_metrics(self) -> Dict:
        """Return empty metrics jika tidak ada trade"""
        return {
            "total_return_percent": 0,
            "total_trades": 0,
            "win_rate_percent": 0,
            "sharpe_ratio": 0,
            "max_drawdown_percent": 0,
            "profit_factor": 0,
        }

    def grade_strategy(self, metrics: Dict) -> Dict:
        """
        Memberi grade pada strategi berdasarkan metrik
        A+ (Excellent) sampai F (Fail)
        """
        scores = []
        grades = {}

        # Sharpe Ratio
        sharpe = metrics.get("sharpe_ratio", 0)
        if sharpe >= 2.0:
            grades["sharpe"] = ("A+", "Sangat excellent")
            scores.append(100)
        elif sharpe >= 1.5:
            grades["sharpe"] = ("A", "Excellent")
            scores.append(90)
        elif sharpe >= 1.0:
            grades["sharpe"] = ("B", "Bagus")
            scores.append(75)
        elif sharpe >= 0.5:
            grades["sharpe"] = ("C", "Cukup")
            scores.append(60)
        elif sharpe >= 0:
            grades["sharpe"] = ("D", "Kurang")
            scores.append(40)
        else:
            grades["sharpe"] = ("F", "Buruk - di bawah risk-free rate")
            scores.append(0)

        # Max Drawdown
        mdd = metrics.get("max_drawdown_percent", 100)
        if mdd <= 10:
            grades["drawdown"] = ("A+", "Drawdown sangat kecil")
            scores.append(100)
        elif mdd <= 20:
            grades["drawdown"] = ("A", "Drawdown kecil")
            scores.append(90)
        elif mdd <= 30:
            grades["drawdown"] = ("B", "Drawdown moderat")
            scores.append(75)
        elif mdd <= 40:
            grades["drawdown"] = ("C", "Drawdown besar")
            scores.append(60)
        else:
            grades["drawdown"] = ("F", "Drawdown sangat besar - berbahaya!")
            scores.append(20)

        # Win Rate
        wr = metrics.get("win_rate_percent", 0)
        if wr >= 60:
            grades["win_rate"] = ("A", "Win rate tinggi")
            scores.append(90)
        elif wr >= 50:
            grades["win_rate"] = ("B", "Win rate cukup")
            scores.append(75)
        elif wr >= 40:
            grades["win_rate"] = ("C", "Win rate rendah tapi masih OK jika PF bagus")
            scores.append(60)
        else:
            grades["win_rate"] = ("D", "Win rate sangat rendah")
            scores.append(30)

        # Profit Factor
        pf = metrics.get("profit_factor", 0)
        if pf >= 2.0:
            grades["profit_factor"] = ("A+", "Profit factor excellent")
            scores.append(100)
        elif pf >= 1.5:
            grades["profit_factor"] = ("A", "Profit factor bagus")
            scores.append(90)
        elif pf >= 1.2:
            grades["profit_factor"] = ("B", "Profit factor cukup")
            scores.append(75)
        elif pf >= 1.0:
            grades["profit_factor"] = ("C", "Profit factor tipis")
            scores.append(50)
        else:
            grades["profit_factor"] = ("F", "Profit factor < 1 = sistem rugi!")
            scores.append(0)

        # Overall grade
        avg_score = sum(scores) / len(scores) if scores else 0
        if avg_score >= 90:
            overall = "A+ (STRATEGI EXCELLENT - siap live trading)"
        elif avg_score >= 75:
            overall = "A (STRATEGI BAGUS - layak dipertimbangkan)"
        elif avg_score >= 60:
            overall = "B (STRATEGI CUKUP - perlu optimasi)"
        elif avg_score >= 40:
            overall = "C (STRATEGI KURANG - perlu revisi besar)"
        else:
            overall = "D/F (STRATEGI BURUK - jangan dipakai live!)"

        return {
            "grades": grades,
            "overall_score": round(avg_score, 1),
            "overall_grade": overall,
            "recommendation": self._get_recommendation(avg_score, metrics),
        }

    def _get_recommendation(self, score: float, metrics: Dict) -> str:
        """Memberikan rekomendasi berdasarkan score"""
        if score >= 75:
            return (
                "✅ STRATEGI LAYAK untuk live trading dengan modal kecil. "
                "Mulai dengan 10-20% dari modal yang direncanakan, lalu scale up "
                "setelah 3 bulan performa konsisten."
            )
        elif score >= 60:
            return (
                "⚠️ STRATEGI BUTUH OPTIMASI. Coba parameter berbeda atau "
                "tambahkan filter (misal: hanya trade saat sentimen positif). "
                "Jangan live trading dulu."
            )
        else:
            return (
                "❌ STRATEGI TIDAK LAYAK. Kemungkinan besar akan rugi di live trading. "
                "Evaluasi ulang logika strategi, pertimbangkan indikator lain, "
                "atau ganti timeframe."
            )
