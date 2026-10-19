"""
Binance WebSocket & REST Collector
Mengambil data real-time via WebSocket dan data historis via REST API

File ini bertanggung jawab untuk:
1. Mengambil data candlestick historis dari Binance REST API
2. Mengambil data ticker real-time setiap 10 detik
3. Menyimpan semua data ke database

Untuk pemula:
- REST API = Request-response (ambil data sekali)
- WebSocket = Real-time stream (data terus mengalir)
- CCXT = Library universal untuk semua crypto exchange
- Testnet = Environment testing (tidak pakai uang asli)

Alur kerja:
1. Initialize koneksi ke Binance
2. Fetch historical candles (sekali saat startup)
3. Loop fetch real-time tickers (setiap 10 detik)
4. Save semua data ke database
"""

import asyncio
import ccxt.async_support as ccxt
from datetime import datetime
from typing import List, Dict
from loguru import logger
from data_collector.config import (
    TRADING_SYMBOLS,
    TIMEFRAMES,
    HISTORICAL_CANDLE_LIMIT,
    BINANCE_API_KEY,
    BINANCE_API_SECRET,
    USE_TESTNET,
)
from data_collector.database import DatabaseManager


class BinanceCollector:
    """
    Mengumpulkan data harga dari Binance.
    
    Class ini menangani:
    - Koneksi ke Binance (testnet atau mainnet)
    - Fetch historical candlestick data
    - Fetch real-time ticker data
    - Save data ke database
    
    Attributes:
        db: DatabaseManager instance untuk save data
        exchange: CCXT exchange instance
        running: Boolean flag untuk kontrol loop
    """

    def __init__(self, db: DatabaseManager):
        """
        Initialize BinanceCollector.
        
        Args:
            db: DatabaseManager instance untuk save data
        """
        self.db = db
        self.exchange = None
        self.running = False

    async def initialize(self) -> None:
        """
        Inisialisasi koneksi ke Binance.
        
        Membuat CCXT exchange instance dan load markets.
        Menggunakan testnet jika USE_TESTNET=True (recommended untuk testing).
        """
        self.exchange = ccxt.binance(
            {
                "apiKey": BINANCE_API_KEY,
                "secret": BINANCE_API_SECRET,
                "enableRateLimit": True,
                "options": {"defaultType": "spot"},
            }
        )

        # Gunakan testnet untuk testing
        if USE_TESTNET:
            self.exchange.set_sandbox_mode(True)
            logger.info("🧪 Menggunakan Binance TESTNET (aman untuk testing)")
        else:
            logger.warning("⚠️  Menggunakan Binance PRODUCTION (uang asli!)")

        await self.exchange.load_markets()
        logger.info(f"✅ Connected to Binance. Markets loaded: {len(self.exchange.markets)}")

    async def fetch_historical_candles(self) -> None:
        """
        Mengambil data candlestick historis untuk semua simbol & timeframe.
        
        Ini dijalankan sekali saat startup untuk mengisi database dengan data historis.
        Data ini akan digunakan untuk analisis teknikal di Fase 2.
        
        Note:
            - Ada jeda 0.5 detik antara setiap request untuk menghindari rate limit
            - Jika symbol tidak tersedia di Binance, akan di-skip
            - Error pada 1 symbol tidak akan menghentikan proses untuk symbol lain
        """
        logger.info("📊 Fetching historical candles...")

        for symbol in TRADING_SYMBOLS:
            for timeframe in TIMEFRAMES:
                try:
                    # Validasi simbol ada di Binance
                    if symbol not in self.exchange.markets:
                        logger.warning(f"⚠️  Symbol {symbol} tidak tersedia, skip")
                        continue

                    # Fetch OHLCV data dari Binance
                    ohlcv = await self.exchange.fetch_ohlcv(
                        symbol, timeframe, limit=HISTORICAL_CANDLE_LIMIT
                    )

                    # Format data ke struktur standar
                    candles = [
                        {
                            "timestamp": candle[0],
                            "open": float(candle[1]),
                            "high": float(candle[2]),
                            "low": float(candle[3]),
                            "close": float(candle[4]),
                            "volume": float(candle[5]),
                        }
                        for candle in ohlcv
                    ]

                    # Save ke database
                    await self.db.save_candles(symbol, timeframe, candles)
                    logger.info(
                        f"✅ {symbol} [{timeframe}]: {len(candles)} candles loaded"
                    )

                    # Jeda untuk menghindari rate limit Binance
                    await asyncio.sleep(0.5)

                except Exception as e:
                    logger.error(f"❌ Error fetching {symbol} [{timeframe}]: {e}")

    async def fetch_realtime_tickers(self) -> None:
        """
        Loop untuk mengambil harga terbaru setiap 10 detik.
        
        Ini berjalan terus-menerus selama collector running.
        Data ticker akan di-save ke database untuk monitoring real-time.
        
        Note:
            - Update setiap 10 detik (bisa di-adjust)
            - Error pada 1 symbol tidak akan menghentikan loop
            - Loop akan berhenti jika self.running = False
        """
        logger.info("🔄 Starting real-time ticker loop...")

        while self.running:
            try:
                for symbol in TRADING_SYMBOLS:
                    try:
                        # Fetch ticker data
                        ticker = await self.exchange.fetch_ticker(symbol)
                        
                        # Save ke database
                        await self.db.save_ticker(symbol, ticker)
                        
                        # Log harga terbaru
                        logger.debug(
                            f"💹 {symbol}: ${ticker['last']:,.2f} "
                            f"({ticker['percentage']:+.2f}%)"
                        )
                    except Exception as e:
                        logger.error(f"❌ Ticker error {symbol}: {e}")

                # Tunggu 10 detik sebelum update berikutnya
                await asyncio.sleep(10)

            except asyncio.CancelledError:
                # Loop dibatalkan (shutdown)
                break
            except Exception as e:
                logger.error(f"❌ Ticker loop error: {e}")
                await asyncio.sleep(5)

    async def start(self) -> None:
        """
        Menjalankan collector secara penuh.
        
        Alur:
        1. Initialize koneksi ke Binance
        2. Fetch historical candles (sekali saja)
        3. Start loop real-time tickers
        """
        self.running = True
        await self.initialize()

        # 1. Ambil data historis dulu (sekali saja saat startup)
        await self.fetch_historical_candles()

        # 2. Mulai loop real-time
        await self.fetch_realtime_tickers()

    async def stop(self) -> None:
        """
        Menghentikan collector dengan aman.
        
        Set running = False dan close exchange connection.
        """
        self.running = False
        if self.exchange:
            await self.exchange.close()
            logger.info("🛑 Binance collector stopped")


# ============================================
# STANDALONE TESTING
# ============================================

async def test_collector():
    """
    Test BinanceCollector secara standalone.
    
    Cara menjalankan:
        python -m data_collector.binance_ws
    """
    logger.info("Testing BinanceCollector...")
    
    # Initialize database
    db = DatabaseManager()
    await db.initialize()
    
    # Create collector
    collector = BinanceCollector(db)
    
    try:
        # Initialize
        await collector.initialize()
        
        # Fetch historical data (only 1 symbol & timeframe for testing)
        logger.info("Fetching test data...")
        ohlcv = await collector.exchange.fetch_ohlcv("BTC/USDT", "1h", limit=10)
        
        candles = [
            {
                "timestamp": candle[0],
                "open": float(candle[1]),
                "high": float(candle[2]),
                "low": float(candle[3]),
                "close": float(candle[4]),
                "volume": float(candle[5]),
            }
            for candle in ohlcv
        ]
        
        await db.save_candles("BTC/USDT", "1h", candles)
        logger.info(f"✅ Saved {len(candles)} test candles")
        
        # Fetch ticker
        ticker = await collector.exchange.fetch_ticker("BTC/USDT")
        await db.save_ticker("BTC/USDT", ticker)
        logger.info(f"✅ Saved ticker: ${ticker['last']:,.2f}")
        
        # Get data from database
        candles = await db.get_candles("BTC/USDT", "1h", limit=10)
        logger.info(f"✅ Retrieved {len(candles)} candles from database")
        
        ticker = await db.get_latest_ticker("BTC/USDT")
        logger.info(f"✅ Retrieved ticker from database: {ticker}")
        
    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
    finally:
        await collector.stop()
    
    logger.info("✅ Test completed")


if __name__ == "__main__":
    asyncio.run(test_collector())
