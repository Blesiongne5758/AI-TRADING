"""
Backtesting Data Loader
Memuat data historis dengan perlindungan dari lookahead bias
"""
import pandas as pd
import ccxt.async_support as ccxt
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from loguru import logger
import asyncio


class BacktestDataLoader:
    """Memuat data historis untuk backtesting dengan integritas tinggi"""

    def __init__(self):
        self.exchange = None

    async def initialize(self):
        """Inisialisasi exchange (public data, tidak perlu API key)"""
        self.exchange = ccxt.binance({
            "enableRateLimit": True,
            "options": {"defaultType": "spot"},
        })
        await self.exchange.load_markets()
        logger.info("✅ Backtest data loader initialized")

    async def load_historical_data(
        self,
        symbol: str,
        timeframe: str = "1h",
        start_date: str = "2023-01-01",
        end_date: str = None,
    ) -> pd.DataFrame:
        """
        Memuat data historis lengkap (bisa ribuan candle)
        
        Args:
            symbol: Trading pair (misal: "BTC/USDT")
            timeframe: Interval candle (1m, 5m, 15m, 1h, 4h, 1d)
            start_date: Tanggal mulai (YYYY-MM-DD)
            end_date: Tanggal akhir (default: sekarang)
            
        Returns:
            DataFrame dengan kolom: timestamp, open, high, low, close, volume
        """
        if end_date is None:
            end_date = datetime.now().strftime("%Y-%m-%d")

        start_ts = int(datetime.strptime(start_date, "%Y-%m-%d").timestamp() * 1000)
        end_ts = int(datetime.strptime(end_date, "%Y-%m-%d").timestamp() * 1000)

        all_candles = []
        current_ts = start_ts
        batch_size = 1000  # Binance limit per request

        logger.info(f"📥 Loading {symbol} [{timeframe}] from {start_date} to {end_date}")

        while current_ts < end_ts:
            try:
                ohlcv = await self.exchange.fetch_ohlcv(
                    symbol, timeframe, since=current_ts, limit=batch_size
                )

                if not ohlcv:
                    break

                all_candles.extend(ohlcv)
                current_ts = ohlcv[-1][0] + 1  # Next candle

                # Rate limit
                await asyncio.sleep(0.3)

                # Progress log
                if len(all_candles) % 5000 == 0:
                    logger.info(f"   Loaded {len(all_candles)} candles...")

            except Exception as e:
                logger.error(f"❌ Error loading data: {e}")
                break

        # Konversi ke DataFrame
        df = pd.DataFrame(
            all_candles,
            columns=["timestamp", "open", "high", "low", "close", "volume"],
        )

        # Konversi tipe data
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df.set_index("timestamp", inplace=True)

        # Filter range tanggal
        df = df[(df.index >= start_date) & (df.index <= end_date)]

        # Hapus duplikat
        df = df[~df.index.duplicated(keep="first")]

        logger.info(f"✅ Loaded {len(df)} candles ({df.index[0]} → {df.index[-1]})")

        return df

    async def load_multi_timeframe(
        self, symbol: str, timeframes: List[str], start_date: str
    ) -> Dict[str, pd.DataFrame]:
        """Memuat data untuk multiple timeframe (untuk multi-timeframe analysis)"""
        data = {}
        for tf in timeframes:
            data[tf] = await self.load_historical_data(symbol, tf, start_date)
        return data

    async def close(self):
        """Tutup koneksi exchange"""
        if self.exchange:
            await self.exchange.close()
