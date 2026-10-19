"""
Order Executor
Eksekusi order berdasarkan trading signals
"""
from typing import Dict, Optional
from loguru import logger

from .portfolio_manager import PortfolioManager
from .risk_manager import RiskManager


class OrderExecutor:
    """Mengeksekusi order berdasarkan trading signals"""

    def __init__(self, portfolio_manager: PortfolioManager, risk_manager: RiskManager):
        """
        Initialize order executor
        
        Args:
            portfolio_manager: Portfolio manager instance
            risk_manager: Risk manager instance
        """
        self.portfolio = portfolio_manager
        self.risk_manager = risk_manager
        
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
        
        # Get portfolio summary
        portfolio_summary = await self.portfolio.get_portfolio_summary()
        
        # Validate signal with risk manager
        validation = self.risk_manager.validate_signal(signal, portfolio_summary)
        
        if not validation['valid']:
            logger.warning(f"❌ Signal validation failed: {validation['reason']}")
            return None
        
        # Determine side
        side = "LONG" if signal_type in ['STRONG_BUY', 'BUY'] else "SHORT"
        
        # Get execution parameters
        entry_price = suggested_actions.get('entry', 0)
        stop_loss = suggested_actions.get('stop_loss', 0)
        take_profit = suggested_actions.get('take_profit', 0)
        adjusted_quantity = validation['adjusted_quantity']
        
        if entry_price <= 0 or stop_loss <= 0 or take_profit <= 0:
            logger.error("❌ Invalid execution parameters")
            return None
        
        # Execute trade
        position = await self.portfolio.open_position(
            symbol=symbol,
            side=side,
            entry_price=entry_price,
            quantity=adjusted_quantity,
            stop_loss=stop_loss,
            take_profit=take_profit,
            signal_id=signal.get('timestamp', '')
        )
        
        if not position:
            logger.error("❌ Failed to open position")
            return None
        
        # Return execution result
        result = {
            "symbol": symbol,
            "side": side,
            "entry_price": entry_price,
            "quantity": adjusted_quantity,
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "position_value": entry_price * adjusted_quantity,
            "position_size_percent": validation['adjusted_position_size'],
            "confidence": confidence,
            "signal_type": signal_type,
            "position_id": position.get('id')
        }
        
        logger.info(
            f"✅ Order executed: {side} {symbol} @ ${entry_price:,.2f} "
            f"(Qty: {adjusted_quantity:.6f}, Value: ${result['position_value']:,.2f})"
        )
        
        return result

    async def check_and_close_positions(self, current_prices: Dict[str, float]):
        """
        Check semua posisi dan close jika trigger SL/TP
        
        Args:
            current_prices: Dict symbol -> current price
        """
        logger.info(f"\n🔍 Checking {len(self.portfolio.positions)} open positions for SL/TP...")
        await self.portfolio.check_stop_loss_take_profit(current_prices)

    async def print_execution_summary(self):
        """Print execution summary"""
        await self.portfolio.print_portfolio_summary()
        self.risk_manager.print_risk_summary(
            await self.portfolio.get_portfolio_summary()
        )
