"""
Context Builder
Mengumpulkan konteks dari database untuk menjawab pertanyaan user
"""
from typing import Dict, List, Optional
from datetime import datetime
import aiosqlite
from data_collector.database import DatabaseManager


class ContextBuilder:
    """Membangun konteks dari berbagai sumber data"""

    def __init__(self, db: DatabaseManager):
        self.db = db

    async def build_portfolio_context(self) -> str:
        """Membangun konteks tentang portfolio saat ini"""
        positions = await self.db.get_open_positions()
        stats = await self.db.get_portfolio_stats()

        if not positions and stats["total_trades"] == 0:
            return "📊 Portfolio saat ini kosong. Belum ada trade yang dilakukan."

        context_parts = []

        # Posisi terbuka
        if positions:
            context_parts.append(f"\n📈 **Posisi Terbuka ({len(positions)}):**")
            for pos in positions:
                # Hitung PnL sederhana (butuh current_price dari ticker)
                ticker = await self.db.get_ticker(pos["symbol"])
                current_price = ticker["price"] if ticker else pos["entry_price"]

                if pos["side"] == "long":
                    pnl = (current_price - pos["entry_price"]) * pos["quantity"]
                else:
                    pnl = (pos["entry_price"] - current_price) * pos["quantity"]

                pnl_emoji = "💰" if pnl > 0 else "💸"
                context_parts.append(
                    f"  {pnl_emoji} {pos['symbol']} ({pos['side'].upper()})\n"
                    f"     Entry: ${pos['entry_price']:,.2f} → Current: ${current_price:,.2f}\n"
                    f"     PnL: ${pnl:+,.2f} | SL: ${pos['stop_loss']:,.2f} | TP: ${pos['take_profit']:,.2f}"
                )

        # Statistik historis
        if stats["total_trades"] > 0:
            context_parts.append(f"\n📊 **Statistik Trading:**")
            context_parts.append(
                f"  • Total trades: {stats['total_trades']}\n"
                f"  • Win rate: {stats['win_rate']:.1f}%\n"
                f"  • Profit factor: {stats['profit_factor']:.2f}\n"
                f"  • Total PnL: ${stats['total_pnl']:+,.2f}"
            )

        return "\n".join(context_parts)

    async def build_market_context(self, symbol: str = None) -> str:
        """Membangun konteks tentang kondisi pasar"""
        context_parts = []

        # Harga terbaru
        if symbol:
            ticker = await self.db.get_ticker(symbol)
            if ticker:
                context_parts.append(
                    f"\n💰 **{symbol}**: ${ticker['price']:,.2f} "
                    f"({ticker['price_change_24h']:+.2f}% dalam 24 jam)"
                )
        else:
            # Ambil semua ticker
            from data_collector.config import TRADING_SYMBOLS
            context_parts.append("\n💰 **Harga Terbaru:**")
            for sym in TRADING_SYMBOLS:
                ticker = await self.db.get_ticker(sym)
                if ticker:
                    context_parts.append(
                        f"  • {sym}: ${ticker['price']:,.2f} ({ticker['price_change_24h']:+.2f}%)"
                    )

        # Berita terbaru
        news = await self.db.get_latest_news(limit=5)
        if news:
            context_parts.append("\n📰 **Berita Terbaru:**")
            for n in news:
                context_parts.append(f"  • [{n['source']}] {n['title'][:70]}...")

        return "\n".join(context_parts)

    async def build_signal_context(self, symbol: str) -> str:
        """Membangun konteks tentang signal terakhir untuk simbol"""
        # Ambil candle terbaru untuk analisis cepat
        candles = await self.db.get_candles(symbol, "1h", limit=50)
        if not candles:
            return f"❌ Tidak ada data untuk {symbol}"

        # Hitung indikator sederhana
        from analysis.technical_indicators import TechnicalAnalyzer
        analyzer = TechnicalAnalyzer()
        result = analyzer.calculate_all(candles)

        if not result:
            return f"❌ Analisis gagal untuk {symbol}"

        context_parts = [f"\n📊 **Analisis {symbol}:**"]
        context_parts.append(f"  💰 Harga: ${result['latest_price']:,.2f}")

        for indicator, data in result["interpretation"].items():
            emoji = "🟢" if data["score"] > 20 else "🔴" if data["score"] < -20 else "⚪"
            context_parts.append(
                f"  {emoji} {indicator.upper()}: {data['signal']} (score: {data['score']:+.0f})"
            )

        return "\n".join(context_parts)

    async def get_recent_trades(self, limit: int = 5) -> str:
        """Mengambil trade terakhir untuk konteks"""
        async with aiosqlite.connect(self.db.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(
                """
                SELECT * FROM positions 
                WHERE status = 'CLOSED'
                ORDER BY close_time DESC
                LIMIT ?
                """,
                (limit,),
            )
            rows = await cursor.fetchall()

        if not rows:
            return "Belum ada trade yang ditutup."

        context_parts = ["\n📜 **Trade Terakhir:**"]
        for row in rows:
            pnl_emoji = "💰" if row["pnl"] > 0 else "💸"
            context_parts.append(
                f"  {pnl_emoji} {row['symbol']} ({row['side']})\n"
                f"     Entry: ${row['entry_price']:,.2f} → Exit: ${row['close_price']:,.2f}\n"
                f"     PnL: ${row['pnl']:+,.2f} ({row['pnl_percent']:+.2f}%) - {row['exit_reason']}"
            )

        return "\n".join(context_parts)
