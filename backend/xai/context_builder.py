"""
Context Builder
Membangun konteks dari database untuk penjelasan yang lebih kaya
"""
from typing import Dict, List, Optional
from datetime import datetime
from loguru import logger
from data_collector.database import DatabaseManager


class ContextBuilder:
    """
    Membangun konteks dari database untuk XAI
    
    Mengambil data historis dan statistik untuk memberikan penjelasan yang lebih mendalam
    """

    def __init__(self, db: DatabaseManager):
        """
        Initialize context builder
        
        Args:
            db: DatabaseManager instance
        """
        self.db = db
        logger.info("🏗️  Context Builder initialized")

    async def build_symbol_context(self, symbol: str, timeframe: str = "1h") -> Dict:
        """
        Bangun konteks lengkap untuk satu symbol
        
        Args:
            symbol: Trading pair (e.g., "BTC/USDT")
            timeframe: Timeframe (e.g., "1h")
        
        Returns:
            Dictionary dengan konteks lengkap
        """
        context = {
            "symbol": symbol,
            "timeframe": timeframe,
            "timestamp": datetime.now().isoformat(),
        }
        
        # 1. Current price dan ticker
        ticker = await self.db.get_latest_ticker(symbol)
        if ticker:
            context["current_price"] = ticker["price"]
            context["price_change_24h"] = ticker.get("price_change_24h", 0)
            context["volume_24h"] = ticker.get("volume_24h", 0)
        
        # 2. Recent candles (last 24)
        candles = await self.db.get_candles(symbol, timeframe, limit=24)
        if candles:
            context["recent_candles"] = candles
            context["price_high_24h"] = max(c["high"] for c in candles)
            context["price_low_24h"] = min(c["low"] for c in candles)
            
            # Calculate simple statistics
            closes = [c["close"] for c in candles]
            context["price_avg_24h"] = sum(closes) / len(closes)
            
            # Price movement
            if len(closes) >= 2:
                context["price_movement"] = closes[-1] - closes[0]
                context["price_movement_percent"] = (context["price_movement"] / closes[0]) * 100
        
        # 3. Recent news
        news = await self.db.get_latest_news(limit=10)
        if news:
            context["recent_news"] = news
            context["news_count"] = len(news)
        
        # 4. Trading history untuk symbol ini
        positions = await self.db.get_open_positions(symbol)
        context["open_positions"] = positions
        context["open_positions_count"] = len(positions)
        
        # 5. Portfolio stats
        stats = await self.db.get_portfolio_stats()
        context["portfolio_stats"] = stats
        
        return context

    async def build_trade_context(self, position_id: int) -> Dict:
        """
        Bangun konteks untuk satu trade/posisi
        
        Args:
            position_id: Position ID
        
        Returns:
            Dictionary dengan konteks trade
        """
        # Get position details
        positions = await self.db.get_open_positions()
        position = next((p for p in positions if p["id"] == position_id), None)
        
        if not position:
            # Try closed positions
            logger.warning(f"Position {position_id} not found in open positions")
            return {"error": "Position not found"}
        
        context = {
            "position_id": position_id,
            "symbol": position["symbol"],
            "side": position["side"],
            "entry_price": position["entry_price"],
            "quantity": position["quantity"],
            "stop_loss": position["stop_loss"],
            "take_profit": position["take_profit"],
            "entry_time": position["entry_time"],
        }
        
        # Get current price
        ticker = await self.db.get_latest_ticker(position["symbol"])
        if ticker:
            current_price = ticker["price"]
            context["current_price"] = current_price
            
            # Calculate unrealized PnL
            if position["side"] == "long":
                pnl = (current_price - position["entry_price"]) * position["quantity"]
            else:
                pnl = (position["entry_price"] - current_price) * position["quantity"]
            
            context["unrealized_pnl"] = pnl
            context["unrealized_pnl_percent"] = (pnl / (position["entry_price"] * position["quantity"])) * 100
            
            # Distance to SL/TP
            if position["side"] == "long":
                context["distance_to_sl"] = current_price - position["stop_loss"]
                context["distance_to_tp"] = position["take_profit"] - current_price
            else:
                context["distance_to_sl"] = position["stop_loss"] - current_price
                context["distance_to_tp"] = current_price - position["take_profit"]
        
        return context

    async def build_performance_context(self, days: int = 7) -> Dict:
        """
        Bangun konteks performance untuk periode tertentu
        
        Args:
            days: Number of days to analyze (default 7)
        
        Returns:
            Dictionary dengan performance context
        """
        context = {
            "period_days": days,
            "timestamp": datetime.now().isoformat(),
        }
        
        # Get portfolio stats
        stats = await self.db.get_portfolio_stats()
        context["stats"] = stats
        
        # Get portfolio snapshots
        snapshots = await self.db.get_portfolio_snapshots(limit=100)
        if snapshots:
            context["snapshots"] = snapshots
            
            # Calculate performance over period
            if len(snapshots) >= 2:
                oldest = snapshots[-1]
                newest = snapshots[0]
                
                context["period_start_balance"] = oldest["total_balance"]
                context["period_end_balance"] = newest["total_balance"]
                context["period_pnl"] = newest["total_balance"] - oldest["total_balance"]
                context["period_return_percent"] = (
                    (context["period_pnl"] / oldest["total_balance"]) * 100
                    if oldest["total_balance"] > 0 else 0
                )
        
        # Get trade history
        trades = await self.db.get_trade_history(limit=100)
        if trades:
            context["recent_trades"] = trades
            context["trade_count"] = len(trades)
            
            # Calculate win/loss
            closed_trades = [t for t in trades if t["action"] in ["STOP_LOSS", "TAKE_PROFIT"]]
            if closed_trades:
                # Extract PnL from notes
                wins = 0
                losses = 0
                for trade in closed_trades:
                    notes = trade.get("notes", "")
                    if "PnL: $+" in notes:
                        wins += 1
                    elif "PnL: $-" in notes:
                        losses += 1
                
                context["wins"] = wins
                context["losses"] = losses
                context["win_rate"] = (wins / len(closed_trades) * 100) if closed_trades else 0
        
        return context

    def format_context_summary(self, context: Dict) -> str:
        """
        Format context summary untuk ditampilkan
        
        Args:
            context: Context dictionary
        
        Returns:
            Formatted summary string
        """
        lines = []
        lines.append("=" * 70)
        lines.append("📊 KONTEKS MARKET")
        lines.append("=" * 70)
        lines.append("")
        
        # Symbol info
        if "symbol" in context:
            lines.append(f"📈 Symbol: {context['symbol']} [{context.get('timeframe', 'N/A')}]")
            
            if "current_price" in context:
                lines.append(f"💰 Current Price: ${context['current_price']:,.2f}")
            
            if "price_change_24h" in context:
                change = context["price_change_24h"]
                emoji = "🟢" if change >= 0 else "🔴"
                lines.append(f"{emoji} 24h Change: {change:+.2f}%")
            
            if "price_high_24h" in context and "price_low_24h" in context:
                lines.append(f"📊 24h Range: ${context['price_low_24h']:,.2f} - ${context['price_high_24h']:,.2f}")
        
        # Portfolio stats
        if "portfolio_stats" in context:
            stats = context["portfolio_stats"]
            lines.append("")
            lines.append("💼 Portfolio Stats:")
            lines.append(f"   Total Trades: {stats.get('total_trades', 0)}")
            lines.append(f"   Win Rate: {stats.get('win_rate', 0):.1f}%")
            lines.append(f"   Profit Factor: {stats.get('profit_factor', 0):.2f}")
            lines.append(f"   Total PnL: ${stats.get('total_pnl', 0):+,.2f}")
        
        # Open positions
        if "open_positions" in context:
            positions = context["open_positions"]
            lines.append("")
            lines.append(f"📂 Open Positions: {len(positions)}")
            for pos in positions[:3]:  # Show max 3
                lines.append(f"   • {pos['symbol']} {pos['side'].upper()} @ ${pos['entry_price']:,.2f}")
        
        lines.append("")
        lines.append("=" * 70)
        
        return "\n".join(lines)
