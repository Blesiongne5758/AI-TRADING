"""
Order Executor
Mengeksekusi order berdasarkan signal dari Analysis Engine
"""
from typing import Dict, Optional
from datetime import datetime
from loguru import logger
from data_collector.database import DatabaseManager
from .portfolio_manager import PortfolioManager
from .risk_manager import RiskManager


class OrderExecutor:
    """Mengeksekusi order paper trading"""

    # Fee simulasi (0.1% seperti Binance)
    TRADING_FEE_PERCENT = 0.1

    def __init__(
        self,
        portfolio: PortfolioManager,
        risk_manager: RiskManager,
        db: DatabaseManager,
    ):
        self.portfolio = portfolio
        self.risk_manager = risk_manager
        self.db = db

    async def execute_signal(self, signal: Dict, current_price: float) -> Optional[Dict]:
        """
        Eksekusi signal trading
        
        Args:
            signal: Output dari SignalGenerator
            current_price: Harga terbaru untuk eksekusi
            
        Returns:
            Dict dengan detail eksekusi, atau None jika ditolak
        """
        symbol = signal["symbol"]
        suggested_action = signal["suggested_actions"]["action"]

        # Skip jika HOLD
        if suggested_action == "HOLD":
            logger.debug(f"⏸️  {symbol}: HOLD signal, skip execution")
            return None

        # === 1. Validasi dengan Risk Manager ===
        validation = self.risk_manager.validate_trade(signal, current_price)
        
        if not validation["approved"]:
            logger.warning(f"❌ {symbol}: Trade ditolak - {validation['reason']}")
            return None

        logger.info(f"✅ {symbol}: Trade approved - {validation['reason']}")

        # === 2. Tentukan Side & Quantity ===
        if suggested_action == "OPEN_LONG":
            side = "long"
        elif suggested_action == "OPEN_SHORT":
            side = "short"
        else:
            logger.error(f"❌ {symbol}: Unknown action {suggested_action}")
            return None

        quantity = validation["quantity"]
        position_size_usd = validation["position_size_usd"]

        # === 3. Reserve Margin ===
        if not self.portfolio.reserve_margin(position_size_usd):
            logger.error(f"❌ {symbol}: Gagal reserve margin")
            return None

        # === 4. Hitung Fee ===
        fee = position_size_usd * (self.TRADING_FEE_PERCENT / 100)

        # === 5. Buat Position di Database ===
        position_data = {
            "symbol": symbol,
            "side": side,
            "entry_price": current_price,
            "quantity": quantity,
            "stop_loss": signal["suggested_actions"]["stop_loss"],
            "take_profit": signal["suggested_actions"]["take_profit"],
            "entry_time": int(datetime.now().timestamp() * 1000),
        }

        position_id = await self.db.create_position(position_data)

        # === 6. Simpan Trade Log ===
        trade_data = {
            "position_id": position_id,
            "symbol": symbol,
            "side": side,
            "action": "OPEN",
            "price": current_price,
            "quantity": quantity,
            "timestamp": int(datetime.now().timestamp() * 1000),
            "fee": fee,
            "notes": f"Confidence: {signal['confidence']:.1f}%, Score: {signal['final_score']:+.2f}",
        }
        await self.db.save_trade(trade_data)

        # === 7. Update Portfolio Cache ===
        position_data["id"] = position_id
        position_data["current_price"] = current_price
        self.portfolio.add_position(position_id, position_data)

        # === 8. Log Eksekusi ===
        logger.info(
            f"🎯 {symbol}: {side.upper()} executed @ ${current_price:,.2f} | "
            f"Qty: {quantity:.6f} | Value: ${position_size_usd:.2f} | Fee: ${fee:.2f}"
        )
        logger.info(
            f"   SL: ${signal['suggested_actions']['stop_loss']:,.2f} | "
            f"TP: ${signal['suggested_actions']['take_profit']:,.2f}"
        )

        return {
            "position_id": position_id,
            "symbol": symbol,
            "side": side,
            "entry_price": current_price,
            "quantity": quantity,
            "position_size_usd": position_size_usd,
            "fee": fee,
            "stop_loss": signal["suggested_actions"]["stop_loss"],
            "take_profit": signal["suggested_actions"]["take_profit"],
        }

    async def check_exit_conditions(self, symbol: str, current_price: float) -> Optional[Dict]:
        """
        Cek apakah ada posisi yang harus ditutup (SL/TP hit)
        
        Returns:
            Dict dengan detail exit, atau None jika tidak ada exit
        """
        open_positions = await self.db.get_open_positions(symbol)
        
        for position in open_positions:
            position_id = position["id"]
            side = position["side"]
            entry_price = position["entry_price"]
            sl = position["stop_loss"]
            tp = position["take_profit"]

            exit_reason = None
            exit_price = current_price

            # Cek Stop Loss
            if side == "long" and current_price <= sl:
                exit_reason = "STOP_LOSS"
                exit_price = sl  # Asumsi slippage minimal
            elif side == "short" and current_price >= sl:
                exit_reason = "STOP_LOSS"
                exit_price = sl

            # Cek Take Profit
            elif side == "long" and current_price >= tp:
                exit_reason = "TAKE_PROFIT"
                exit_price = tp
            elif side == "short" and current_price <= tp:
                exit_reason = "TAKE_PROFIT"
                exit_price = tp

            # Jika ada exit condition
            if exit_reason:
                return await self._close_position(
                    position=position,
                    exit_price=exit_price,
                    exit_reason=exit_reason,
                )

        return None

    async def _close_position(
        self, position: Dict, exit_price: float, exit_reason: str
    ) -> Dict:
        """Menutup posisi dan hitung PnL"""
        position_id = position["id"]
        entry_price = position["entry_price"]
        quantity = position["quantity"]
        side = position["side"]

        # Hitung PnL
        if side == "long":
            pnl = (exit_price - entry_price) * quantity
        else:  # short
            pnl = (entry_price - exit_price) * quantity

        # Hitung fee exit
        exit_value = exit_price * quantity
        fee = exit_value * (self.TRADING_FEE_PERCENT / 100)
        pnl_after_fee = pnl - fee

        # Hitung PnL percent
        entry_value = entry_price * quantity
        pnl_percent = (pnl_after_fee / entry_value) * 100

        # Update database
        await self.db.close_position(
            position_id=position_id,
            close_price=exit_price,
            pnl=pnl_after_fee,
            pnl_percent=pnl_percent,
            exit_reason=exit_reason,
        )

        # Simpan trade log
        trade_data = {
            "position_id": position_id,
            "symbol": position["symbol"],
            "side": side,
            "action": exit_reason,
            "price": exit_price,
            "quantity": quantity,
            "timestamp": int(datetime.now().timestamp() * 1000),
            "fee": fee,
            "notes": f"PnL: ${pnl_after_fee:.2f} ({pnl_percent:+.2f}%)",
        }
        await self.db.save_trade(trade_data)

        # Release margin dan update PnL
        self.portfolio.release_margin(entry_value, pnl_after_fee)
        self.portfolio.remove_position(position_id)
        self.risk_manager.record_trade_result(pnl_after_fee)

        # Log
        emoji = "💰" if pnl_after_fee > 0 else "💸"
        logger.info(
            f"{emoji} {position['symbol']}: Position closed ({exit_reason}) | "
            f"Entry: ${entry_price:,.2f} → Exit: ${exit_price:,.2f} | "
            f"PnL: ${pnl_after_fee:+.2f} ({pnl_percent:+.2f}%)"
        )

        return {
            "position_id": position_id,
            "symbol": position["symbol"],
            "exit_price": exit_price,
            "exit_reason": exit_reason,
            "pnl": pnl_after_fee,
            "pnl_percent": pnl_percent,
        }

    async def close_position_manual(self, position_id: int, current_price: float, reason: str = "MANUAL") -> Optional[Dict]:
        """Tutup posisi secara manual (untuk testing atau override)"""
        positions = await self.db.get_open_positions()
        position = next((p for p in positions if p["id"] == position_id), None)
        
        if not position:
            logger.error(f"❌ Position {position_id} not found")
            return None

        return await self._close_position(position, current_price, reason)
