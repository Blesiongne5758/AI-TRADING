"""
Risk Manager
Memvalidasi setiap trade sebelum dieksekusi untuk mencegah risiko berlebihan
"""
from typing import Dict, Optional
from loguru import logger


class RiskManager:
    """Mengelola risiko dan memvalidasi trade"""

    def __init__(self, portfolio_manager):
        self.portfolio = portfolio_manager
        
        # Parameter risiko (bisa disesuaikan)
        self.max_risk_per_trade_percent = 2.0  # Max 2% dari portfolio per trade
        self.max_open_positions = 5  # Max 5 posisi terbuka bersamaan
        self.max_position_size_percent = 20.0  # Max 20% dari portfolio per posisi
        self.max_daily_loss_percent = 5.0  # Stop trading jika loss > 5% per hari
        self.min_confidence_threshold = 55.0  # Minimum confidence untuk trade

        # Tracking harian
        self.daily_pnl = 0.0
        self.daily_trades = 0

    def validate_trade(self, signal: Dict, current_price: float) -> Dict:
        """
        Validasi apakah trade boleh dieksekusi
        
        Returns:
            {
                "approved": bool,
                "reason": str,
                "adjusted_quantity": float (jika ada penyesuaian),
                "position_size_usd": float
            }
        """
        # === 1. Cek Confidence ===
        if signal["confidence"] < self.min_confidence_threshold:
            return {
                "approved": False,
                "reason": f"Confidence terlalu rendah: {signal['confidence']:.1f}% < {self.min_confidence_threshold}%",
            }

        # === 2. Cek Max Open Positions ===
        if len(self.portfolio.open_positions) >= self.max_open_positions:
            return {
                "approved": False,
                "reason": f"Max open positions tercapai: {len(self.portfolio.open_positions)}/{self.max_open_positions}",
            }

        # === 3. Cek Duplicate Symbol ===
        for pos in self.portfolio.open_positions.values():
            if pos["symbol"] == signal["symbol"]:
                return {
                    "approved": False,
                    "reason": f"Sudah ada posisi terbuka untuk {signal['symbol']}",
                }

        # === 4. Cek Daily Loss Limit ===
        portfolio_summary = self.portfolio.get_portfolio_summary()
        daily_loss_limit = self.portfolio.initial_balance * (self.max_daily_loss_percent / 100)
        
        if self.daily_pnl < -daily_loss_limit:
            return {
                "approved": False,
                "reason": f"Daily loss limit tercapai: ${self.daily_pnl:.2f} (limit: -${daily_loss_limit:.2f})",
            }

        # === 5. Hitung Position Size ===
        suggested_actions = signal["suggested_actions"]
        position_size_percent = suggested_actions["position_size_percent"]
        
        # Batasi max position size
        if position_size_percent > self.max_position_size_percent:
            position_size_percent = self.max_position_size_percent
            logger.warning(
                f"⚠️  Position size dibatasi ke {self.max_position_size_percent}%"
            )

        # Hitung jumlah USD yang akan digunakan
        position_size_usd = portfolio_summary["total_balance"] * (position_size_percent / 100)

        # === 6. Cek Risk per Trade ===
        max_risk_usd = portfolio_summary["total_balance"] * (self.max_risk_per_trade_percent / 100)
        sl_distance_percent = suggested_actions["sl_distance_percent"]
        risk_usd = position_size_usd * (sl_distance_percent / 100)

        if risk_usd > max_risk_usd:
            # Adjust position size agar sesuai max risk
            adjusted_position_size_usd = max_risk_usd / (sl_distance_percent / 100)
            logger.warning(
                f"⚠️  Risk terlalu besar (${risk_usd:.2f} > ${max_risk_usd:.2f}), "
                f"adjust position size ke ${adjusted_position_size_usd:.2f}"
            )
            position_size_usd = adjusted_position_size_usd

        # === 7. Cek Available Balance ===
        if not self.portfolio.can_open_position(position_size_usd):
            return {
                "approved": False,
                "reason": f"Saldo tidak cukup: butuh ${position_size_usd:.2f}, tersedia ${self.portfolio.available_balance:.2f}",
            }

        # === 8. Hitung Quantity ===
        quantity = position_size_usd / current_price

        # === APPROVED ===
        return {
            "approved": True,
            "reason": "Trade approved",
            "position_size_usd": round(position_size_usd, 2),
            "quantity": round(quantity, 8),
            "risk_usd": round(risk_usd, 2),
            "risk_percent": round((risk_usd / portfolio_summary["total_balance"]) * 100, 2),
        }

    def record_trade_result(self, pnl: float):
        """Catat hasil trade untuk tracking harian"""
        self.daily_pnl += pnl
        self.daily_trades += 1

    def reset_daily_stats(self):
        """Reset statistik harian (panggil setiap hari)"""
        logger.info(f"📊 Daily stats reset. PnL: ${self.daily_pnl:.2f}, Trades: {self.daily_trades}")
        self.daily_pnl = 0.0
        self.daily_trades = 0
