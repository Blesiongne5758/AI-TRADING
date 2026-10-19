"""
Order Executor
Eksekusi order berdasarkan trading signals
"""
from typing import Dict, Optional
from datetime import datetime
from loguru import logger

from data_collector.database import DatabaseManager
from .portfolio_manager import PortfolioManager
from .risk_manager import RiskManager


class OrderExecutor:
    """Mengeksekusi order berdasarkan trading signals"""

    def __init__(
        self,
        portfolio_manager: PortfolioManager,
        risk_manager: RiskManager,
        db: DatabaseManager
    ):
        """
        Initialize order executor
        
        Args:
            portfolio_manager: Portfolio manager instance
            risk_manager: Risk manager instance
            db: Database manager instance
        """
        self.portfolio = portfolio_manager
        self.risk_manager = risk_manager
        self.db = db
        
        logger.info("⚡ Order Executor initialized")

    async def execute_signal(self, signal: Dict) -> Optional[Dict]:
        """
        Eksekusi trading signal
        
        Args:
            signal: Trading signal dari analysis engine
            
        Returns:
            Dict dengan execution result atau None jika gagal
        """
        symbol = signal.get('symbol', '')
        signal_type = signal.get('signal', 'NEUTRAL')
        confidence = signal.get('confidence', 0)
        suggested_actions = signal.get('suggested_actions', {})
        
        logger.info(f"\n⚡ Executing signal: {symbol} {signal_type} (Confidence: {confidence:.1f}%)")
        
        # Check if signal is actionable
        if signal_type not in ['STRONG_BUY', 'BUY', 'STRONG_SELL', 'SELL']:
            logger.info(f"⏭️  Skipping non-actionable signal: {signal_type}")
            return None
        
        # Get portfolio summary (synchronous)
        portfolio_summary = self.portfolio.get_portfolio_summary()
        
        # Validate signal with risk manager
        validation = self.risk_manager.validate_signal(signal, portfolio_summary)
        
        if not validation['valid']:
            logger.warning(f"❌ Signal validation failed: {validation['reason']}")
            return None
        
        # Determine side
        side = "long" if signal_type in ['STRONG_BUY', 'BUY'] else "short"
        
        # Get execution parameters
        entry_price = suggested_actions.get('entry', 0)
        stop_loss = suggested_actions.get('stop_loss', 0)
        take_profit = suggested_actions.get('take_profit', 0)
        adjusted_quantity = validation['adjusted_quantity']
        
        if entry_price <= 0 or stop_loss <= 0 or take_profit <= 0:
            logger.error("❌ Invalid execution parameters")
            return None
        
        # Calculate position value
        position_value = entry_price * adjusted_quantity
        
        # Check if we have enough balance
        if not self.portfolio.can_open_position(position_value):
            logger.error(f"❌ Insufficient balance: ${self.portfolio.available_balance:,.2f} < ${position_value:,.2f}")
            return None
        
        # Reserve margin
        if not self.portfolio.reserve_margin(position_value):
            logger.error("❌ Failed to reserve margin")
            return None
        
        # Create position in database
        entry_time = int(datetime.now().timestamp() * 1000)
        position_data = {
            "symbol": symbol,
            "side": side,
            "entry_price": entry_price,
            "quantity": adjusted_quantity,
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "entry_time": entry_time
        }
        
        position_id = await self.db.create_position(position_data)
        
        if not position_id:
            logger.error("❌ Failed to create position in database")
            # Release margin
            self.portfolio.release_margin(position_value)
            return None
        
        # Add position to portfolio cache
        position_data["id"] = position_id
        position_data["current_price"] = entry_price
        self.portfolio.add_position(position_id, position_data)
        
        # Save trade log
        trade_data = {
            "position_id": position_id,
            "symbol": symbol,
            "side": side,
            "action": "OPEN",
            "price": entry_price,
            "quantity": adjusted_quantity,
            "timestamp": entry_time,
            "fee": 0,
            "notes": f"Opened from signal {signal_type} (confidence: {confidence:.1f}%)"
        }
        await self.db.save_trade(trade_data)
        
        # Return execution result
        result = {
            "symbol": symbol,
            "side": side,
            "entry_price": entry_price,
            "quantity": adjusted_quantity,
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "position_value": position_value,
            "position_size_percent": validation['adjusted_position_size'],
            "confidence": confidence,
            "signal_type": signal_type,
            "position_id": position_id
        }
        
        logger.info(
            f"✅ Order executed: {side.upper()} {symbol} @ ${entry_price:,.2f} "
            f"(Qty: {adjusted_quantity:.6f}, Value: ${position_value:,.2f})"
        )
        
        return result

    async def check_and_close_positions(self, current_prices: Dict[str, float]):
        """
        Check semua posisi dan close jika trigger SL/TP
        
        Args:
            current_prices: Dict symbol -> current price
        """
        logger.info(f"\n🔍 Checking {len(self.portfolio.open_positions)} open positions for SL/TP...")
        
        # Update current prices untuk semua posisi
        for position_id, pos in self.portfolio.open_positions.items():
            symbol = pos["symbol"]
            if symbol in current_prices:
                self.portfolio.update_position_price(position_id, current_prices[symbol])
        
        # Check SL/TP untuk setiap posisi
        positions_to_close = []
        
        for position_id, pos in self.portfolio.open_positions.items():
            symbol = pos["symbol"]
            if symbol not in current_prices:
                continue
            
            current_price = current_prices[symbol]
            side = pos["side"]
            stop_loss = pos["stop_loss"]
            take_profit = pos["take_profit"]
            
            # Check stop loss
            if side == "long" and current_price <= stop_loss:
                positions_to_close.append((position_id, current_price, "STOP_LOSS"))
            elif side == "short" and current_price >= stop_loss:
                positions_to_close.append((position_id, current_price, "STOP_LOSS"))
            
            # Check take profit
            elif side == "long" and current_price >= take_profit:
                positions_to_close.append((position_id, current_price, "TAKE_PROFIT"))
            elif side == "short" and current_price <= take_profit:
                positions_to_close.append((position_id, current_price, "TAKE_PROFIT"))
        
        # Close positions
        for position_id, close_price, reason in positions_to_close:
            await self._close_position(position_id, close_price, reason)

    async def _close_position(self, position_id: int, close_price: float, reason: str):
        """
        Close posisi dan update portfolio
        
        Args:
            position_id: Position ID
            close_price: Harga close
            reason: Alasan close (STOP_LOSS, TAKE_PROFIT, MANUAL)
        """
        if position_id not in self.portfolio.open_positions:
            logger.warning(f"⚠️  Position {position_id} not found in cache")
            return
        
        pos = self.portfolio.open_positions[position_id]
        
        # Calculate PnL
        if pos["side"] == "long":
            pnl = (close_price - pos["entry_price"]) * pos["quantity"]
        else:
            pnl = (pos["entry_price"] - close_price) * pos["quantity"]
        
        pnl_percent = (pnl / (pos["entry_price"] * pos["quantity"])) * 100
        
        # Close position in database
        success = await self.db.close_position(
            position_id=position_id,
            close_price=close_price,
            pnl=pnl,
            pnl_percent=pnl_percent,
            exit_reason=reason
        )
        
        if not success:
            logger.error(f"❌ Failed to close position {position_id} in database")
            return
        
        # Release margin dan update PnL
        position_value = pos["entry_price"] * pos["quantity"]
        self.portfolio.release_margin(position_value, pnl)
        
        # Remove position from cache
        self.portfolio.remove_position(position_id)
        
        # Save trade log
        close_time = int(datetime.now().timestamp() * 1000)
        trade_data = {
            "position_id": position_id,
            "symbol": pos["symbol"],
            "side": pos["side"],
            "action": reason,
            "price": close_price,
            "quantity": pos["quantity"],
            "timestamp": close_time,
            "fee": 0,
            "notes": f"Closed by {reason} | P&L: ${pnl:+,.2f} ({pnl_percent:+.2f}%)"
        }
        await self.db.save_trade(trade_data)
        
        emoji = "🟢" if pnl > 0 else "🔴"
        logger.info(
            f"{emoji} Position closed: {pos['symbol']} {pos['side'].upper()} | "
            f"Entry: ${pos['entry_price']:,.2f} → Exit: ${close_price:,.2f} | "
            f"P&L: ${pnl:+,.2f} ({pnl_percent:+.2f}%) | Reason: {reason}"
        )

    def print_execution_summary(self):
        """Print execution summary"""
        summary = self.portfolio.get_portfolio_summary()
        
        logger.info("\n" + "="*70)
        logger.info("💼 PORTFOLIO SUMMARY")
        logger.info("="*70)
        logger.info(f"   Initial Balance: ${summary['initial_balance']:,.2f}")
        logger.info(f"   Available Balance: ${summary['available_balance']:,.2f}")
        logger.info(f"   Total Balance: ${summary['total_balance']:,.2f}")
        logger.info(f"   Total Return: {summary['total_return_percent']:+.2f}%")
        logger.info(f"   Unrealized P&L: ${summary['unrealized_pnl']:+,.2f}")
        logger.info(f"   Realized P&L: ${summary['realized_pnl']:+,.2f}")
        logger.info(f"   Open Positions: {summary['open_positions']}")
        logger.info(f"   Peak Balance: ${summary['peak_balance']:,.2f}")
        logger.info(f"   Max Drawdown: {summary['max_drawdown_percent']:.2f}%")
        logger.info("="*70 + "\n")
