"""
Portfolio Manager
Mengelola saldo virtual, posisi terbuka, dan riwayat trading
"""
import asyncio
from datetime import datetime
from typing import Dict, List, Optional
from loguru import logger

from data_collector.database import DatabaseManager


class PortfolioManager:
    """Mengelola portfolio virtual untuk paper trading"""

    def __init__(self, initial_balance: float = 10000.0):
        """
        Initialize portfolio manager
        
        Args:
            initial_balance: Saldo awal virtual (default $10,000)
        """
        self.db = DatabaseManager()
        self.initial_balance = initial_balance
        self.current_balance = initial_balance
        self.positions: Dict[str, Dict] = {}  # symbol -> position data
        self.trade_history: List[Dict] = []
        
    async def initialize(self):
        """Initialize database dan load portfolio state"""
        await self.db.initialize()
        await self._load_portfolio_state()
        logger.info(f"💼 Portfolio initialized with ${self.current_balance:,.2f}")

    async def _load_portfolio_state(self):
        """Load portfolio state dari database"""
        # Load open positions
        positions = await self.db.get_open_positions()
        self.positions = {pos['symbol']: pos for pos in positions}
        
        # Load trade history
        history = await self.db.get_trade_history(limit=100)
        self.trade_history = history
        
        # Calculate current balance
        self.current_balance = await self.db.get_current_balance()
        
        logger.info(f"📊 Loaded {len(self.positions)} open positions")
        logger.info(f"📜 Loaded {len(self.trade_history)} trade history")

    async def open_position(
        self,
        symbol: str,
        side: str,  # "LONG" or "SHORT"
        entry_price: float,
        quantity: float,
        stop_loss: float,
        take_profit: float,
        signal_id: str
    ) -> Dict:
        """
        Buka posisi baru
        
        Args:
            symbol: Trading pair (e.g., "BTC/USDT")
            side: "LONG" or "SHORT"
            entry_price: Harga entry
            quantity: Jumlah asset
            stop_loss: Stop loss price
            take_profit: Take profit price
            signal_id: ID dari signal yang trigger trade
            
        Returns:
            Dict dengan position data
        """
        # Calculate position value
        position_value = entry_price * quantity
        
        # Check if we have enough balance
        if position_value > self.current_balance:
            logger.error(f"❌ Insufficient balance: ${self.current_balance:,.2f} < ${position_value:,.2f}")
            return None
        
        # Create position record
        position = {
            "symbol": symbol,
            "side": side,
            "entry_price": entry_price,
            "quantity": quantity,
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "status": "OPEN"
        }
        
        # Save to database
        position_id = await self.db.create_position(position)
        position['id'] = position_id
        position['entry_time'] = int(datetime.now().timestamp() * 1000)
        
        # Update local state
        self.positions[symbol] = position
        
        # Deduct from balance
        self.current_balance -= position_value
        await self.db.update_balance(self.current_balance)
        
        # Record trade
        trade = {
            "position_id": position_id,
            "symbol": symbol,
            "side": side,
            "action": "OPEN",
            "price": entry_price,
            "quantity": quantity,
            "notes": f"Opened from signal {signal_id}" if signal_id else None
        }
        await self.db.create_trade(trade)
        self.trade_history.append(trade)
        
        logger.info(
            f"✅ Opened {side} position: {symbol} @ ${entry_price:,.2f} "
            f"(Qty: {quantity:.6f}, Value: ${position_value:,.2f})"
        )
        
        return position

    async def close_position(
        self,
        symbol: str,
        exit_price: float,
        reason: str = "MANUAL"
    ) -> Optional[Dict]:
        """
        Tutup posisi
        
        Args:
            symbol: Trading pair
            exit_price: Harga exit
            reason: Alasan close (MANUAL, STOP_LOSS, TAKE_PROFIT, SIGNAL)
            
        Returns:
            Dict dengan P&L data atau None jika posisi tidak ada
        """
        if symbol not in self.positions:
            logger.warning(f"⚠️  No open position for {symbol}")
            return None
        
        position = self.positions[symbol]
        
        # Calculate P&L
        if position['side'] == 'LONG':
            pnl = (exit_price - position['entry_price']) * position['quantity']
            pnl_percent = ((exit_price - position['entry_price']) / position['entry_price']) * 100
        else:  # SHORT
            pnl = (position['entry_price'] - exit_price) * position['quantity']
            pnl_percent = ((position['entry_price'] - exit_price) / position['entry_price']) * 100
        
        # Calculate exit value
        exit_value = exit_price * position['quantity']
        
        # Update position in database
        await self.db.close_position(
            position_id=position['id'],
            exit_price=exit_price,
            pnl=pnl,
            pnl_percent=pnl_percent,
            reason=reason
        )
        
        # Return capital to balance
        self.current_balance += exit_value
        await self.db.update_balance(self.current_balance)
        
        # Record close trade (action sesuai reason)
        action_map = {
            "MANUAL": "CLOSE",
            "STOP_LOSS": "STOP_LOSS",
            "TAKE_PROFIT": "TAKE_PROFIT",
            "SIGNAL": "CLOSE"
        }
        
        trade = {
            "position_id": position['id'],
            "symbol": symbol,
            "side": position['side'],
            "action": action_map.get(reason, "CLOSE"),
            "price": exit_price,
            "quantity": position['quantity'],
            "notes": f"Closed by {reason} | P&L: ${pnl:+,.2f} ({pnl_percent:+.2f}%)"
        }
        await self.db.create_trade(trade)
        self.trade_history.append(trade)
        
        # Remove from local state
        del self.positions[symbol]
        
        emoji = "🟢" if pnl > 0 else "🔴"
        logger.info(
            f"{emoji} Closed {position['side']} position: {symbol} @ ${exit_price:,.2f} "
            f"(P&L: ${pnl:+,.2f} / {pnl_percent:+.2f}%, Reason: {reason})"
        )
        
        return {
            "symbol": symbol,
            "entry_price": position['entry_price'],
            "exit_price": exit_price,
            "pnl": pnl,
            "pnl_percent": pnl_percent,
            "reason": reason
        }

    async def check_stop_loss_take_profit(self, current_prices: Dict[str, float]):
        """
        Check semua posisi untuk trigger stop loss atau take profit
        
        Args:
            current_prices: Dict symbol -> current price
        """
        for symbol, position in list(self.positions.items()):
            if symbol not in current_prices:
                continue
            
            current_price = current_prices[symbol]
            
            # Check stop loss
            if position['side'] == 'LONG' and current_price <= position['stop_loss']:
                await self.close_position(symbol, current_price, reason="STOP_LOSS")
            elif position['side'] == 'SHORT' and current_price >= position['stop_loss']:
                await self.close_position(symbol, current_price, reason="STOP_LOSS")
            
            # Check take profit
            elif position['side'] == 'LONG' and current_price >= position['take_profit']:
                await self.close_position(symbol, current_price, reason="TAKE_PROFIT")
            elif position['side'] == 'SHORT' and current_price <= position['take_profit']:
                await self.close_position(symbol, current_price, reason="TAKE_PROFIT")

    async def get_portfolio_summary(self) -> Dict:
        """
        Get ringkasan portfolio lengkap dengan statistik
        
        Returns:
            Dict dengan summary data dan statistik trading
        """
        # Calculate unrealized P&L
        unrealized_pnl = 0.0
        for symbol, position in self.positions.items():
            # Get current price from database
            ticker = await self.db.get_latest_ticker(symbol)
            if ticker:
                current_price = ticker['price']
                if position['side'] == 'LONG':
                    unrealized_pnl += (current_price - position['entry_price']) * position['quantity']
                else:
                    unrealized_pnl += (position['entry_price'] - current_price) * position['quantity']
        
        # Get portfolio stats from database
        stats = await self.db.get_portfolio_stats()
        
        # Calculate totals
        realized_pnl = stats['total_pnl']
        total_pnl = realized_pnl + unrealized_pnl
        total_pnl_percent = (total_pnl / self.initial_balance) * 100
        
        return {
            "initial_balance": self.initial_balance,
            "current_balance": self.current_balance,
            "available_balance": self.current_balance,
            "unrealized_pnl": unrealized_pnl,
            "realized_pnl": realized_pnl,
            "total_pnl": total_pnl,
            "total_pnl_percent": total_pnl_percent,
            "open_positions": len(self.positions),
            "total_trades": stats['total_trades'],
            "winning_trades": stats['wins'],
            "losing_trades": stats['losses'],
            "win_rate": stats['win_rate'],
            "avg_win": stats['avg_win'],
            "avg_loss": stats['avg_loss'],
            "profit_factor": stats['profit_factor'],
            "max_loss": stats['max_loss'],
            "positions": list(self.positions.values())
        }

    async def save_snapshot(self):
        """Simpan snapshot portfolio untuk tracking equity curve"""
        summary = await self.get_portfolio_summary()
        
        snapshot = {
            "total_balance": summary['current_balance'] + summary['unrealized_pnl'],
            "available_balance": summary['available_balance'],
            "unrealized_pnl": summary['unrealized_pnl'],
            "realized_pnl": summary['realized_pnl'],
            "total_positions": summary['open_positions']
        }
        
        await self.db.save_portfolio_snapshot(snapshot)
        logger.debug(f"📸 Portfolio snapshot saved: ${snapshot['total_balance']:,.2f}")

    async def print_portfolio_summary(self):
        """Print ringkasan portfolio ke console dengan statistik lengkap"""
        summary = await self.get_portfolio_summary()
        
        logger.info("\n" + "="*70)
        logger.info("💼 PORTFOLIO SUMMARY")
        logger.info("="*70)
        
        # Balance Info
        logger.info("\n💰 BALANCE:")
        logger.info(f"   Initial Balance: ${summary['initial_balance']:,.2f}")
        logger.info(f"   Current Balance: ${summary['current_balance']:,.2f}")
        logger.info(f"   Available Balance: ${summary['available_balance']:,.2f}")
        
        # P&L Info
        logger.info("\n📈 PROFIT & LOSS:")
        logger.info(f"   Unrealized P&L: ${summary['unrealized_pnl']:+,.2f}")
        logger.info(f"   Realized P&L: ${summary['realized_pnl']:+,.2f}")
        logger.info(f"   Total P&L: ${summary['total_pnl']:+,.2f} ({summary['total_pnl_percent']:+.2f}%)")
        
        # Trading Stats
        logger.info("\n📊 TRADING STATISTICS:")
        logger.info(f"   Total Trades: {summary['total_trades']}")
        logger.info(f"   Winning Trades: {summary['winning_trades']}")
        logger.info(f"   Losing Trades: {summary['losing_trades']}")
        logger.info(f"   Win Rate: {summary['win_rate']:.1f}%")
        logger.info(f"   Average Win: ${summary['avg_win']:,.2f}")
        logger.info(f"   Average Loss: ${summary['avg_loss']:,.2f}")
        logger.info(f"   Profit Factor: {summary['profit_factor']:.2f}")
        logger.info(f"   Max Loss: ${summary['max_loss']:,.2f}")
        
        # Open Positions
        logger.info(f"\n📂 OPEN POSITIONS: {summary['open_positions']}")
        if summary['positions']:
            for pos in summary['positions']:
                # Calculate current P&L for this position
                ticker = await self.db.get_latest_ticker(pos['symbol'])
                if ticker:
                    current_price = ticker['price']
                    if pos['side'] == 'LONG':
                        pos_pnl = (current_price - pos['entry_price']) * pos['quantity']
                    else:
                        pos_pnl = (pos['entry_price'] - current_price) * pos['quantity']
                    
                    pnl_percent = (pos_pnl / (pos['entry_price'] * pos['quantity'])) * 100
                    emoji = "🟢" if pos_pnl >= 0 else "🔴"
                    
                    logger.info(
                        f"   {emoji} {pos['symbol']} {pos['side']} @ ${pos['entry_price']:,.2f} "
                        f"(Qty: {pos['quantity']:.6f}) | P&L: ${pos_pnl:+,.2f} ({pnl_percent:+.2f}%)"
                    )
        else:
            logger.info("   (No open positions)")
        
        logger.info("\n" + "="*70 + "\n")
