"""
Binance WebSocket Data Collector

Modul ini bertanggung jawab untuk:
1. Koneksi real-time ke Binance WebSocket
2. Menarik data OHLCV (candlestick) untuk multiple symbols dan timeframes
3. Menyimpan data ke database

Untuk pemula:
- WebSocket adalah protokol komunikasi dua arah yang memungkinkan data real-time
- Binance menyediakan WebSocket gratis untuk data market
- Kita menggunakan library ccxt yang sudah handle semua kompleksitas koneksi
- Data disimpan ke database untuk analisis lebih lanjut

Alur kerja:
1. Connect ke Binance WebSocket
2. Subscribe ke candlestick streams untuk setiap symbol/timeframe
3. Terima data real-time setiap ada candle baru
4. Simpan ke database
5. Reconnect otomatis jika koneksi terputus
"""

import asyncio
import ccxt.async_support as ccxt
from typing import List, Dict, Any, Optional
from datetime import datetime
import json
from loguru import logger

from data_collector.config import (
    BINANCE_API_KEY,
    BINANCE_API_SECRET,
    USE_TESTNET,
    TRADING_SYMBOLS,
    TIMEFRAMES,
    HISTORICAL_CANDLE_LIMIT,
)
from data_collector.database import DatabaseManager


class BinanceDataCollector:
    """
    Data collector untuk menarik data OHLCV dari Binance.
    
    Class ini menangani:
    - Koneksi WebSocket ke Binance
    - Subscribe ke multiple symbols dan timeframes
    - Error handling dan auto-reconnect
    - Penyimpanan data ke database
    
    Attributes:
        exchange: CCXT exchange instance untuk Binance
        symbols: List of trading pairs (e.g., ["BTC/USDT", "ETH/USDT"])
        timeframes: List of time intervals (e.g., ["1m", "5m", "1h"])
        running: Boolean flag untuk kontrol loop
    """
    
    def __init__(
        self,
        symbols: Optional[List[str]] = None,
        timeframes: Optional[List[str]] = None,
        db: Optional[DatabaseManager] = None
    ):
        """
        Initialize BinanceDataCollector.
        
        Args:
            symbols: List of trading pairs. Default dari config.
            timeframes: List of time intervals. Default dari config.
            db: DatabaseManager instance. Default akan dibuat baru.
        """
        self.symbols = symbols or TRADING_SYMBOLS
        self.timeframes = timeframes or TIMEFRAMES
        self.db = db or DatabaseManager()
        self.running = False
        self.exchange: Optional[ccxt.binance] = None
        
        # Statistics
        self.messages_received = 0
        self.errors_count = 0
        self.last_message_time: Optional[datetime] = None
        
        logger.info(
            f"BinanceDataCollector initialized: "
            f"{len(self.symbols)} symbols, {len(self.timeframes)} timeframes"
        )
    
    async def initialize(self) -> None:
        """
        Initialize exchange connection.
        
        Membuat instance CCXT exchange dan load markets.
        Harus dipanggil sebelum start().
        """
        try:
            # Create exchange instance
            self.exchange = ccxt.binance({
                'apiKey': BINANCE_API_KEY if not USE_TESTNET else '',
                'secret': BINANCE_API_SECRET if not USE_TESTNET else '',
                'enableRateLimit': True,
                'options': {
                    'defaultType': 'spot',
                    'test': USE_TESTNET,  # Use testnet if enabled
                }
            })
            
            # Load markets (required before trading)
            await self.exchange.load_markets()
            
            # Validate symbols
            for symbol in self.symbols:
                if symbol not in self.exchange.markets:
                    logger.warning(f"Symbol {symbol} not available on Binance")
            
            logger.info("Exchange initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize exchange: {e}")
            raise
    
    async def fetch_historical_ohlcv(
        self,
        symbol: str,
        timeframe: str,
        limit: int = 500
    ) -> List[Dict[str, Any]]:
        """
        Fetch historical OHLCV data from Binance.
        
        Ini digunakan untuk mengisi database dengan data historis
        sebelum memulai real-time collection.
        
        Args:
            symbol: Trading pair (e.g., "BTC/USDT")
            timeframe: Time interval (e.g., "1h")
            limit: Number of candles to fetch (max 1000)
        
        Returns:
            List of OHLCV dictionaries
        
        Contoh return:
            [
                {
                    "timestamp": 1642684522,
                    "open": 42000.50,
                    "high": 42500.00,
                    "low": 41800.00,
                    "close": 42300.75,
                    "volume": 1234.56
                },
                ...
            ]
        """
        if not self.exchange:
            raise RuntimeError("Exchange not initialized. Call initialize() first.")
        
        try:
            logger.info(f"Fetching {limit} historical candles for {symbol} {timeframe}")
            
            # Fetch OHLCV data from Binance
            ohlcv = await self.exchange.fetch_ohlcv(
                symbol=symbol,
                timeframe=timeframe,
                limit=limit
            )
            
            # Convert to dictionary format
            data = []
            for candle in ohlcv:
                data.append({
                    "timestamp": candle[0],  # Unix timestamp in milliseconds
                    "open": float(candle[1]),
                    "high": float(candle[2]),
                    "low": float(candle[3]),
                    "close": float(candle[4]),
                    "volume": float(candle[5])
                })
            
            logger.info(f"Fetched {len(data)} candles for {symbol} {timeframe}")
            return data
            
        except Exception as e:
            logger.error(f"Failed to fetch historical OHLCV: {e}")
            raise
    
    async def fetch_current_price(self, symbol: str) -> float:
        """
        Fetch current price for a symbol.
        
        Args:
            symbol: Trading pair (e.g., "BTC/USDT")
        
        Returns:
            Current price as float
        """
        if not self.exchange:
            raise RuntimeError("Exchange not initialized")
        
        try:
            ticker = await self.exchange.fetch_ticker(symbol)
            return float(ticker['last'])
        except Exception as e:
            logger.error(f"Failed to fetch price for {symbol}: {e}")
            raise
    
    async def watch_ohlcv_for_symbol(
        self,
        symbol: str,
        timeframe: str
    ) -> None:
        """
        Watch OHLCV data for a specific symbol and timeframe.
        
        Ini adalah WebSocket stream yang berjalan terus-menerus.
        Setiap ada candle baru atau update, data akan diproses.
        
        Args:
            symbol: Trading pair
            timeframe: Time interval
        """
        if not self.exchange:
            raise RuntimeError("Exchange not initialized")
        
        retry_count = 0
        max_retries = 5
        
        while self.running:
            try:
                logger.debug(f"Starting watch_ohlcv for {symbol} {timeframe}")
                
                # Watch OHLCV stream
                while self.running:
                    ohlcv = await self.exchange.watch_ohlcv(symbol, timeframe)
                    
                    if ohlcv:
                        # Get the latest candle
                        latest_candle = ohlcv[-1]
                        
                        # Convert to dictionary
                        candle_data = [{
                            "timestamp": latest_candle[0],
                            "open": float(latest_candle[1]),
                            "high": float(latest_candle[2]),
                            "low": float(latest_candle[3]),
                            "close": float(latest_candle[4]),
                            "volume": float(latest_candle[5])
                        }]
                        
                        # Save to database
                        await self.db.save_candles(symbol, timeframe, candle_data)
                        
                        # Update statistics
                        self.messages_received += 1
                        self.last_message_time = datetime.utcnow()
                        
                        logger.debug(
                            f"Received candle for {symbol} {timeframe}: "
                            f"Close={candle_data[0]['close']}"
                        )
                
            except ccxt.NetworkError as e:
                retry_count += 1
                logger.warning(
                    f"Network error for {symbol} {timeframe}: {e}. "
                    f"Retry {retry_count}/{max_retries}"
                )
                
                if retry_count >= max_retries:
                    logger.error(f"Max retries reached for {symbol} {timeframe}")
                    break
                
                # Wait before retry (exponential backoff)
                await asyncio.sleep(min(2 ** retry_count, 60))
                
            except ccxt.ExchangeError as e:
                logger.error(f"Exchange error for {symbol} {timeframe}: {e}")
                self.errors_count += 1
                await asyncio.sleep(5)
                
            except Exception as e:
                logger.error(f"Unexpected error for {symbol} {timeframe}: {e}")
                self.errors_count += 1
                await asyncio.sleep(5)
    
    async def start(self) -> None:
        """
        Start data collection for all symbols and timeframes.
        
        Ini akan membuat task terpisah untuk setiap symbol/timeframe combination.
        Semua tasks berjalan secara concurrent menggunakan asyncio.
        """
        if not self.exchange:
            await self.initialize()
        
        self.running = True
        logger.info("Starting Binance data collection...")
        
        # Create tasks for each symbol/timeframe
        tasks = []
        for symbol in self.symbols:
            for timeframe in self.timeframes:
                task = asyncio.create_task(
                    self.watch_ohlcv_for_symbol(symbol, timeframe)
                )
                tasks.append(task)
                logger.info(f"Started watching {symbol} {timeframe}")
        
        # Wait for all tasks
        try:
            await asyncio.gather(*tasks, return_exceptions=True)
        except Exception as e:
            logger.error(f"Error in data collection: {e}")
        finally:
            self.running = False
    
    async def stop(self) -> None:
        """
        Stop data collection and close connections.
        """
        logger.info("Stopping Binance data collection...")
        self.running = False
        
        if self.exchange:
            await self.exchange.close()
            logger.info("Exchange connection closed")
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get collection statistics.
        
        Returns:
            Dictionary with statistics
        """
        return {
            "running": self.running,
            "symbols": self.symbols,
            "timeframes": self.timeframes,
            "messages_received": self.messages_received,
            "errors_count": self.errors_count,
            "last_message_time": self.last_message_time.isoformat() if self.last_message_time else None
        }


# ============================================
# STANDALONE RUNNER
# ============================================

async def main():
    """
    Main function untuk standalone testing.
    
    Cara menjalankan:
        python binance_ws.py
    """
    # Setup logging
    logger.add(
        "logs/binance_ws.log",
        rotation="10 MB",
        retention="7 days",
        level="INFO"
    )
    
    # Create collector
    collector = BinanceDataCollector()
    
    try:
        # Fetch historical data first
        logger.info("Fetching historical data...")
        for symbol in collector.symbols[:2]:  # Only first 2 for testing
            for timeframe in ["1h", "1d"]:  # Only 2 timeframes for testing
                data = await collector.fetch_historical_ohlcv(
                    symbol=symbol,
                    timeframe=timeframe,
                    limit=100
                )
                await collector.db.save_candles(symbol, timeframe, data)
                logger.info(f"Saved {len(data)} historical candles for {symbol} {timeframe}")
        
        # Start real-time collection
        logger.info("Starting real-time data collection...")
        await collector.start()
        
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt")
    except Exception as e:
        logger.error(f"Error in main: {e}")
    finally:
        await collector.stop()
        logger.info("Data collector stopped")


if __name__ == "__main__":
    asyncio.run(main())
