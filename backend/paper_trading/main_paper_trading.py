"""
Main Paper Trading - Orchestrator untuk auto-trade loop
"""
import asyncio
import sys
from pathlib import Path
from datetime import datetime
from loguru import logger

# Tambahkan parent directory ke path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from data_collector.database import DatabaseManager
from data_collector.config import TRADING_SYMBOLS, INITIAL_BALANCE
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


class PaperTradingEngine:
    """Orchestrator untuk paper trading engine"""

    def __init__(self, initial_balance: float = INITIAL_BALANCE):
        """
        Initialize paper trading engine
        
        Args:
            initial_balance: Saldo awal virtual
        """
        # Initialize components
        self.db = DatabaseManager()
        self.portfolio = PortfolioManager(initial_balance=initial_balance)
        self.risk_manager = RiskManager()
        self.executor = OrderExecutor(self.portfolio, self.risk_manager)
        
        # Analysis components
        self.tech_analyzer = TechnicalAnalyzer()
        self.sentiment_analyzer = SentimentAnalyzer(use_finbert=False)
        self.signal_generator = SignalGenerator()
        
        # Trading parameters
        self.symbols = TRADING_SYMBOLS
        self.timeframe = "1h"
        self.check_interval = 300  # 5 minutes
        
        logger.info("🚀 Paper Trading Engine initialized")

    async def initialize(self):
        """Initialize semua components"""
        await self.db.initialize()
        await self.portfolio.initialize()
        logger.info("✅ All components initialized")

    async def analyze_and_trade(self, symbol: str) -> bool:
        """
        Analisis symbol dan execute trade jika ada signal
        
        Args:
            symbol: Trading pair
            
        Returns:
            True jika trade dieksekusi, False jika tidak
        """
        logger.info(f"\n{'='*70}")
        logger.info(f"🔍 Analyzing {symbol} [{self.timeframe}]")
        logger.info(f"{'='*70}")
        
        # 1. Get candle data
        candles = await self.db.get_candles(symbol, self.timeframe, limit=250)
        if not candles or len(candles) < 200:
            logger.warning(f"⚠️  Insufficient data for {symbol}: {len(candles) if candles else 0} candles")
            return False
        
        # 2. Technical analysis
        tech_result = self.tech_analyzer.calculate_all(candles)
        if not tech_result:
            logger.error("❌ Technical analysis failed")
            return False
        
        # 3. Sentiment analysis
        news_items = await self.db.get_latest_news(limit=15)
        sentiment_result = self.sentiment_analyzer.analyze_news_batch(news_items)
        
        # 4. Generate signal
        signal = self.signal_generator.generate_signal(
            symbol=symbol,
            timeframe=self.timeframe,
            technical_analysis=tech_result,
            sentiment_analysis=sentiment_result
        )
        
        # 5. Display signal
        logger.info(f"\n🎯 Signal: {signal['signal']} (Confidence: {signal['confidence']:.1f}%)")
        logger.info(f"   Score: {signal['final_score']:+.2f}")
        
        # 6. Execute if actionable
        if signal['signal'] in ['STRONG_BUY', 'BUY', 'STRONG_SELL', 'SELL']:
            result = await self.executor.execute_signal(signal)
            return result is not None
        else:
            logger.info(f"⏭️  No actionable signal for {symbol}")
            return False

    async def run_cycle(self):
        """Jalankan satu cycle trading"""
        logger.info(f"\n{'='*70}")
        logger.info(f"🔄 Starting trading cycle @ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info(f"{'='*70}")
        
        # 1. Get current prices untuk check SL/TP
        current_prices = {}
        for symbol in self.symbols:
            ticker = await self.db.get_latest_ticker(symbol)
            if ticker:
                current_prices[symbol] = ticker['price']
        
        # 2. Check existing positions for SL/TP
        if self.portfolio.positions:
            await self.executor.check_and_close_positions(current_prices)
        
        # 3. Analyze each symbol
        trades_executed = 0
        for symbol in self.symbols:
            try:
                executed = await self.analyze_and_trade(symbol)
                if executed:
                    trades_executed += 1
            except Exception as e:
                logger.error(f"❌ Error analyzing {symbol}: {e}")
        
        # 4. Print summary
        logger.info(f"\n{'='*70}")
        logger.info(f"📊 Cycle Summary: {trades_executed} trades executed")
        logger.info(f"{'='*70}")
        await self.executor.print_execution_summary()

    async def run_continuous(self):
        """Jalankan continuous trading loop"""
        logger.info(f"\n🚀 Starting continuous paper trading...")
        logger.info(f"   Symbols: {', '.join(self.symbols)}")
        logger.info(f"   Timeframe: {self.timeframe}")
        logger.info(f"   Check interval: {self.check_interval}s")
        logger.info(f"   Press Ctrl+C to stop\n")
        
        cycle_count = 0
        while True:
            try:
                cycle_count += 1
                logger.info(f"\n{'#'*70}")
                logger.info(f"# CYCLE #{cycle_count}")
                logger.info(f"{'#'*70}")
                
                await self.run_cycle()
                
                logger.info(f"\n⏰ Next cycle in {self.check_interval}s...")
                await asyncio.sleep(self.check_interval)
                
            except KeyboardInterrupt:
                logger.info("\n\n⚠️  Stopping paper trading engine...")
                break
            except Exception as e:
                logger.error(f"❌ Error in trading cycle: {e}")
                logger.info(f"⏰ Retrying in {self.check_interval}s...")
                await asyncio.sleep(self.check_interval)
        
        # Final summary
        logger.info("\n" + "="*70)
        logger.info("📊 FINAL PORTFOLIO SUMMARY")
        logger.info("="*70)
        await self.executor.print_execution_summary()

    async def run_once(self):
        """Jalankan satu cycle saja (untuk testing)"""
        await self.run_cycle()


async def main():
    """Main entry point"""
    # Initialize engine
    engine = PaperTradingEngine(initial_balance=INITIAL_BALANCE)
    await engine.initialize()
    
    # Run mode
    mode = "once"  # Change to "continuous" for auto-trading
    
    if mode == "once":
        # Run one cycle
        await engine.run_once()
    else:
        # Run continuous
        await engine.run_continuous()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("\n⚠️  Paper trading stopped by user")
    except Exception as e:
        logger.exception(f"💥 Fatal error: {e}")
