"""
Main Paper Trading Orchestrator
Menghubungkan Analysis Engine (Modul B) dengan Paper Trading Engine (Modul C)
"""
import asyncio
import sys
from pathlib import Path
from datetime import datetime
from loguru import logger

# Tambahkan parent directory ke path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from data_collector.config import TRADING_SYMBOLS
from data_collector.database import DatabaseManager
from analysis.technical_indicators import TechnicalAnalyzer
from analysis.sentiment_analysis import SentimentAnalyzer
from analysis.signal_generator import SignalGenerator
from .portfolio_manager import PortfolioManager
from .risk_manager import RiskManager
from .order_executor import OrderExecutor


# Setup logging
logger.remove()
logger.add(
    sys.stdout,
    level="INFO",
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | {message}",
)


class PaperTradingService:
    """Service utama untuk paper trading otomatis"""

    def __init__(self, initial_balance: float = 10000.0):
        self.db = DatabaseManager()
        self.portfolio = PortfolioManager(initial_balance, self.db)
        self.risk_manager = RiskManager(self.portfolio)
        self.executor = OrderExecutor(self.portfolio, self.risk_manager, self.db)
        
        # Analysis components
        self.tech_analyzer = TechnicalAnalyzer()
        self.sentiment_analyzer = SentimentAnalyzer(use_finbert=False)
        self.signal_generator = SignalGenerator()
        
        # Control
        self.running = False
        self.analysis_interval = 300  # Analisis setiap 5 menit
        self.price_check_interval = 10  # Cek SL/TP setiap 10 detik

    async def initialize(self):
        """Inisialisasi semua komponen"""
        logger.info("🚀 Initializing Paper Trading Service...")
        
        await self.db.initialize()
        await self.portfolio.initialize()
        
        logger.info(f"💰 Initial balance: ${self.portfolio.initial_balance:,.2f}")
        logger.info(f"📊 Max open positions: {self.risk_manager.max_open_positions}")
        logger.info(f"⚠️  Max risk per trade: {self.risk_manager.max_risk_per_trade_percent}%")

    async def analyze_and_trade(self, symbol: str, timeframe: str = "1h"):
        """Analisis satu simbol dan eksekusi trade jika ada signal"""
        try:
            # 1. Ambil data candle
            candles = await self.db.get_candles(symbol, timeframe, limit=250)
            if not candles:
                return

            # 2. Analisis teknikal
            tech_result = self.tech_analyzer.calculate_all(candles)
            if not tech_result:
                return

            # 3. Analisis sentimen
            news_items = await self.db.get_latest_news(limit=15)
            sentiment_result = self.sentiment_analyzer.analyze_news_batch(news_items)

            # 4. Generate signal
            signal = self.signal_generator.generate_signal(
                symbol=symbol,
                timeframe=timeframe,
                technical_analysis=tech_result,
                sentiment_analysis=sentiment_result,
            )

            # 5. Eksekusi jika ada signal BUY/SELL
            if signal["signal"] in ["BUY", "STRONG_BUY", "SELL", "STRONG_SELL"]:
                current_price = tech_result["latest_price"]
                await self.executor.execute_signal(signal, current_price)

        except Exception as e:
            logger.error(f"❌ Error analyzing {symbol}: {e}")

    async def check_exit_conditions_all(self):
        """Cek SL/TP untuk semua posisi terbuka"""
        open_positions = await self.db.get_open_positions()
        
        for position in open_positions:
            symbol = position["symbol"]
            
            # Ambil harga terbaru
            try:
                ticker = await self.db.get_latest_ticker(symbol)
                if not ticker:
                    continue
                
                current_price = ticker["price"]
                await self.executor.check_exit_conditions(symbol, current_price)
                
            except Exception as e:
                logger.error(f"❌ Error checking exits for {symbol}: {e}")

    async def save_portfolio_snapshot(self):
        """Simpan snapshot portfolio untuk equity curve"""
        summary = self.portfolio.get_portfolio_summary()
        snapshot = {
            "timestamp": int(datetime.now().timestamp() * 1000),
            "total_balance": summary["total_balance"],
            "available_balance": summary["available_balance"],
            "unrealized_pnl": summary["unrealized_pnl"],
            "realized_pnl": summary["realized_pnl"],
            "total_positions": summary["open_positions"],
        }
        await self.db.save_portfolio_snapshot(snapshot)

    async def print_portfolio_status(self):
        """Cetak status portfolio"""
        summary = self.portfolio.get_portfolio_summary()
        stats = await self.db.get_portfolio_stats()

        logger.info("\n" + "=" * 70)
        logger.info("💼 PORTFOLIO STATUS")
        logger.info("=" * 70)
        logger.info(f"  Initial Balance:    ${summary['initial_balance']:>12,.2f}")
        logger.info(f"  Total Balance:      ${summary['total_balance']:>12,.2f}")
        logger.info(f"  Available Balance:  ${summary['available_balance']:>12,.2f}")
        logger.info(f"  Unrealized PnL:     ${summary['unrealized_pnl']:>+12,.2f}")
        logger.info(f"  Realized PnL:       ${summary['realized_pnl']:>+12,.2f}")
        logger.info(f"  Total Return:       {summary['total_return_percent']:>+11.2f}%")
        logger.info(f"  Max Drawdown:       {summary['max_drawdown_percent']:>11.2f}%")
        logger.info(f"  Open Positions:     {summary['open_positions']:>12}")
        
        if stats["total_trades"] > 0:
            logger.info(f"\n📊 TRADING STATISTICS")
            logger.info(f"  Total Trades:       {stats['total_trades']:>12}")
            logger.info(f"  Win Rate:           {stats['win_rate']:>11.2f}%")
            logger.info(f"  Profit Factor:      {stats['profit_factor']:>11.2f}")
            logger.info(f"  Avg Win:            ${stats['avg_win']:>12,.2f}")
            logger.info(f"  Avg Loss:           ${stats['avg_loss']:>12,.2f}")
        logger.info("=" * 70 + "\n")

    async def run(self):
        """Main loop untuk paper trading"""
        self.running = True
        await self.initialize()

        logger.info("🚀 Paper Trading Service started")
        logger.info(f"📈 Monitoring {len(TRADING_SYMBOLS)} symbols: {', '.join(TRADING_SYMBOLS)}")

        last_analysis_time = 0
        last_snapshot_time = 0

        while self.running:
            try:
                current_time = datetime.now().timestamp()

                # Analisis & trading setiap 5 menit
                if current_time - last_analysis_time >= self.analysis_interval:
                    logger.info("\n🔍 Starting analysis cycle...")
                    
                    for symbol in TRADING_SYMBOLS:
                        await self.analyze_and_trade(symbol)
                    
                    last_analysis_time = current_time
                    
                    # Print status setiap analisis
                    await self.print_portfolio_status()

                # Cek SL/TP setiap 10 detik
                await self.check_exit_conditions_all()

                # Snapshot setiap 1 jam
                if current_time - last_snapshot_time >= 3600:
                    await self.save_portfolio_snapshot()
                    last_snapshot_time = current_time

                # Sleep sebelum loop berikutnya
                await asyncio.sleep(self.price_check_interval)

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Main loop error: {e}")
                await asyncio.sleep(30)

    async def stop(self):
        """Hentikan service"""
        self.running = False
        logger.info("🛑 Paper Trading Service stopped")


async def main():
    """Entry point"""
    service = PaperTradingService(initial_balance=10000.0)
    
    try:
        await service.run()
    except KeyboardInterrupt:
        logger.info("\n⚠️  Service stopped by user")
    finally:
        await service.stop()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logger.exception(f"💥 Fatal error: {e}")
        sys.exit(1)
