"""
Portfolio Manager
Mengelola saldo virtual, posisi terbuka, dan menghitung PnL real-time
"""
from typing import Dict, List, Optional
from datetime import datetime
from loguru import logger
from data_collector.database import DatabaseManager


class PortfolioManager:
    """Mengelola portfolio virtual untuk paper trading"""

    def __init__(self, initial_balance: float = 10000.0, db: DatabaseManager = None):
        """
        Args:
            initial_balance: Saldo awal virtual (default $10,000)
            db: DatabaseManager instance
        """
        self.initial_balance = initial_balance
        self.available_balance = initial_balance
        self.db = db
        
        # Cache untuk posisi terbuka
        self.open_positions: Dict[int, Dict] = {}
        
        # Statistik
        self.total_realized_pnl = 0.0
        self.peak_balance = initial_balance
        self.max_drawdown = 0.0

    async def initialize(self):
        """Load data dari database saat startup"""
        if not self.db:
            logger.warning("⚠️  No database provided, using in-memory only")
            return

        # Load posisi terbuka dari database
        positions = await self.db.get_open_positions()
        for pos in positions:
            self.open_positions[pos["id"]] = pos
        
        logger.info(f"✅ Portfolio loaded: {len(self.open_positions)} open positions")

    def get_portfolio_summary(self) -> Dict:
        """Mengambil ringkasan portfolio"""
        unrealized_pnl = self._calculate_unrealized_pnl()
        total_balance = self.available_balance + self._get_total_position_value()
        
        # Update peak balance dan drawdown
        if total_balance > self.peak_balance:
            self.peak_balance = total_balance
        
        current_drawdown = ((self.peak_balance - total_balance) / self.peak_balance) * 100
        if current_drawdown > self.max_drawdown:
            self.max_drawdown = current_drawdown

        return {
            "initial_balance": self.initial_balance,
            "available_balance": round(self.available_balance, 2),
            "unrealized_pnl": round(unrealized_pnl, 2),
            "realized_pnl": round(self.total_realized_pnl, 2),
            "total_balance": round(total_balance, 2),
            "total_return_percent": round(
                ((total_balance - self.initial_balance) / self.initial_balance) * 100, 2
            ),
            "open_positions": len(self.open_positions),
            "peak_balance": round(self.peak_balance, 2),
            "max_drawdown_percent": round(self.max_drawdown, 2),
        }

    def _calculate_unrealized_pnl(self) -> float:
        """Menghitung PnL belum terealisasi dari posisi terbuka"""
        total = 0.0
        for pos in self.open_positions.values():
            # Untuk paper trading, kita butuh harga terbaru dari external source
            # Di sini kita asumsikan entry_price (akan di-update oleh order executor)
            current_price = pos.get("current_price", pos["entry_price"])
            
            if pos["side"] == "long":
                pnl = (current_price - pos["entry_price"]) * pos["quantity"]
            else:  # short
                pnl = (pos["entry_price"] - current_price) * pos["quantity"]
            
            total += pnl
        
        return total

    def _get_total_position_value(self) -> float:
        """Menghitung total nilai posisi terbuka"""
        total = 0.0
        for pos in self.open_positions.values():
            position_value = pos["entry_price"] * pos["quantity"]
            total += position_value
        return total

    def can_open_position(self, required_margin: float) -> bool:
        """Cek apakah ada cukup saldo untuk membuka posisi"""
        return self.available_balance >= required_margin

    def reserve_margin(self, amount: float) -> bool:
        """Reserve saldo untuk posisi baru"""
        if self.available_balance >= amount:
            self.available_balance -= amount
            return True
        return False

    def release_margin(self, amount: float, pnl: float = 0):
        """Release saldo setelah posisi ditutup"""
        self.available_balance += amount + pnl
        self.total_realized_pnl += pnl

    def add_position(self, position_id: int, position_data: Dict):
        """Tambahkan posisi ke cache"""
        self.open_positions[position_id] = position_data

    def remove_position(self, position_id: int):
        """Hapus posisi dari cache"""
        if position_id in self.open_positions:
            del self.open_positions[position_id]

    def update_position_price(self, position_id: int, current_price: float):
        """Update harga terbaru untuk posisi (untuk kalkulasi PnL real-time)"""
        if position_id in self.open_positions:
            self.open_positions[position_id]["current_price"] = current_price
