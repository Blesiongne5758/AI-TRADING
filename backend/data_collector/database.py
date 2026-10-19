"""
Database Manager - Mengelola SQLite untuk menyimpan data harga dan berita

File ini menangani semua operasi database menggunakan aiosqlite (async SQLite).
Database digunakan untuk menyimpan:
- Data OHLCV (candlestick) dari Binance
- Data ticker real-time (harga terbaru)
- Berita crypto dari RSS feeds

Untuk pemula:
- aiosqlite = async version dari SQLite
- Kita tulis SQL langsung (tidak pakai ORM)
- Lebih mudah di-debug dan dipahami
- INSERT OR REPLACE = update jika sudah ada, insert jika belum

Cara penggunaan:
    from data_collector.database import DatabaseManager
    
    db = DatabaseManager()
    await db.initialize()
    await db.save_candles("BTC/USDT", "1h", candles_data)
    candles = await db.get_candles("BTC/USDT", "1h", limit=100)
"""

import aiosqlite
from datetime import datetime
from typing import List, Dict, Optional
from loguru import logger
from data_collector.config import DATABASE_PATH


class DatabaseManager:
    """
    Mengelola semua operasi database secara asynchronous.
    
    Class ini menangani:
    - Inisialisasi database (create tables)
    - Save data (candles, ticker, news)
    - Get data untuk analisis
    
    Attributes:
        db_path: Path ke file database SQLite
    """

    def __init__(self, db_path: str = str(DATABASE_PATH)):
        """
        Initialize DatabaseManager.
        
        Args:
            db_path: Path ke file database. Default dari config.
        """
        self.db_path = db_path

    async def initialize(self) -> None:
        """
        Membuat tabel-tabel yang dibutuhkan saat startup.
        
        Tabel yang dibuat:
        - candles: Data candlestick (OHLCV)
        - ticker: Data ticker real-time
        - news: Berita crypto
        
        Dipanggil sekali saat aplikasi dimulai.
        """
        async with aiosqlite.connect(self.db_path) as db:
            # Tabel untuk data candlestick (OHLCV)
            await db.execute("""
                CREATE TABLE IF NOT EXISTS candles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol TEXT NOT NULL,
                    timeframe TEXT NOT NULL,
                    timestamp INTEGER NOT NULL,
                    open REAL NOT NULL,
                    high REAL NOT NULL,
                    low REAL NOT NULL,
                    close REAL NOT NULL,
                    volume REAL NOT NULL,
                    UNIQUE(symbol, timeframe, timestamp)
                )
            """)

            # Tabel untuk data ticker real-time (harga terbaru)
            await db.execute("""
                CREATE TABLE IF NOT EXISTS ticker (
                    symbol TEXT PRIMARY KEY,
                    price REAL NOT NULL,
                    bid REAL,
                    ask REAL,
                    volume_24h REAL,
                    price_change_24h REAL,
                    last_update INTEGER NOT NULL
                )
            """)

            # Tabel untuk berita
            await db.execute("""
                CREATE TABLE IF NOT EXISTS news (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source TEXT NOT NULL,
                    title TEXT NOT NULL,
                    link TEXT UNIQUE NOT NULL,
                    published_date INTEGER,
                    summary TEXT,
                    category TEXT,
                    fetched_at INTEGER NOT NULL
                )
            """)

            # Index untuk mempercepat query
            await db.execute("""
                CREATE INDEX IF NOT EXISTS idx_candles_symbol_timeframe
                ON candles(symbol, timeframe, timestamp)
            """)

            await db.commit()
            logger.info(f"✅ Database initialized at {self.db_path}")

    async def save_candles(self, symbol: str, timeframe: str, candles: List[Dict]) -> None:
        """
        Menyimpan data candlestick ke database.
        
        Args:
            symbol: Trading pair (e.g., "BTC/USDT")
            timeframe: Time interval (e.g., "1h")
            candles: List of candle dictionaries
        
        Contoh candles:
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
        
        Note:
            Menggunakan INSERT OR REPLACE untuk menghindari duplikasi.
            Jika data dengan (symbol, timeframe, timestamp) yang sama sudah ada,
            akan di-update dengan data baru.
        """
        async with aiosqlite.connect(self.db_path) as db:
            data_to_insert = [
                (
                    symbol,
                    timeframe,
                    candle["timestamp"],
                    candle["open"],
                    candle["high"],
                    candle["low"],
                    candle["close"],
                    candle["volume"],
                )
                for candle in candles
            ]

            await db.executemany(
                """
                INSERT OR REPLACE INTO candles 
                (symbol, timeframe, timestamp, open, high, low, close, volume)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                data_to_insert,
            )
            await db.commit()
            logger.debug(f"💾 Saved {len(candles)} candles for {symbol} [{timeframe}]")

    async def save_ticker(self, symbol: str, ticker: Dict) -> None:
        """
        Menyimpan/update data ticker real-time.
        
        Args:
            symbol: Trading pair (e.g., "BTC/USDT")
            ticker: Ticker dictionary dari CCXT
        
        Contoh ticker:
            {
                "last": 42300.75,      # Harga terakhir
                "bid": 42300.50,       # Harga beli tertinggi
                "ask": 42301.00,       # Harga jual terendah
                "baseVolume": 1234.56, # Volume 24h
                "percentage": 2.5      # Perubahan harga 24h (%)
            }
        
        Note:
            Menggunakan INSERT OR REPLACE karena hanya ada 1 row per symbol.
            Data akan selalu di-update dengan harga terbaru.
        """
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                """
                INSERT OR REPLACE INTO ticker 
                (symbol, price, bid, ask, volume_24h, price_change_24h, last_update)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    symbol,
                    ticker.get("last", 0),
                    ticker.get("bid", 0),
                    ticker.get("ask", 0),
                    ticker.get("baseVolume", 0),
                    ticker.get("percentage", 0),
                    int(datetime.now().timestamp() * 1000),
                ),
            )
            await db.commit()

    async def save_news(self, news_items: List[Dict]) -> int:
        """
        Menyimpan berita baru (hindari duplikasi).
        
        Args:
            news_items: List of news dictionaries
        
        Contoh news_items:
            [
                {
                    "source": "CoinDesk",
                    "title": "Bitcoin reaches new high",
                    "link": "https://coindesk.com/...",
                    "published_date": 1642684522,
                    "summary": "Bitcoin price surged...",
                    "category": "crypto"
                },
                ...
            ]
        
        Returns:
            Jumlah berita yang berhasil disimpan
        
        Note:
            Menggunakan UNIQUE constraint pada 'link' untuk menghindari duplikasi.
            Jika berita dengan link yang sama sudah ada, akan di-skip.
        """
        async with aiosqlite.connect(self.db_path) as db:
            saved_count = 0
            for item in news_items:
                try:
                    await db.execute(
                        """
                        INSERT INTO news 
                        (source, title, link, published_date, summary, category, fetched_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            item["source"],
                            item["title"],
                            item["link"],
                            item.get("published_date"),
                            item.get("summary"),
                            item.get("category"),
                            int(datetime.now().timestamp() * 1000),
                        ),
                    )
                    saved_count += 1
                except aiosqlite.IntegrityError:
                    # Berita sudah ada (link duplikat), skip
                    pass

            await db.commit()
            if saved_count > 0:
                logger.info(f"📰 Saved {saved_count} new articles")
            
            return saved_count

    async def get_candles(
        self, symbol: str, timeframe: str, limit: int = 100
    ) -> List[Dict]:
        """
        Mengambil data candlestick untuk analisis.
        
        Args:
            symbol: Trading pair (e.g., "BTC/USDT")
            timeframe: Time interval (e.g., "1h")
            limit: Jumlah candle maksimum (default 100)
        
        Returns:
            List of candle dictionaries, sorted by timestamp ascending
        
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
        
        Note:
            Data di-return dalam urutan kronologis (oldest first).
            Query di-sort DESC lalu di-reverse untuk efisiensi.
        """
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(
                """
                SELECT timestamp, open, high, low, close, volume
                FROM candles
                WHERE symbol = ? AND timeframe = ?
                ORDER BY timestamp DESC
                LIMIT ?
                """,
                (symbol, timeframe, limit),
            )
            rows = await cursor.fetchall()
            return [dict(row) for row in reversed(rows)]

    async def get_latest_ticker(self, symbol: str) -> Optional[Dict]:
        """
        Mengambil data ticker terbaru untuk sebuah symbol.
        
        Args:
            symbol: Trading pair (e.g., "BTC/USDT")
        
        Returns:
            Ticker dictionary atau None jika tidak ada
        """
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(
                """
                SELECT symbol, price, bid, ask, volume_24h, price_change_24h, last_update
                FROM ticker
                WHERE symbol = ?
                """,
                (symbol,),
            )
            row = await cursor.fetchone()
            return dict(row) if row else None

    async def get_latest_news(self, limit: int = 20) -> List[Dict]:
        """
        Mengambil berita terbaru untuk analisis sentimen.
        
        Args:
            limit: Jumlah berita maksimum (default 20)
        
        Returns:
            List of news dictionaries, sorted by published_date descending
        """
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(
                """
                SELECT source, title, link, published_date, summary, category
                FROM news
                ORDER BY published_date DESC
                LIMIT ?
                """,
                (limit,),
            )
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]

    async def get_all_tickers(self) -> List[Dict]:
        """
        Mengambil semua ticker terbaru.
        
        Returns:
            List of ticker dictionaries
        """
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(
                """
                SELECT symbol, price, bid, ask, volume_24h, price_change_24h, last_update
                FROM ticker
                ORDER BY symbol
                """
            )
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]

    async def get_candle_count(self, symbol: str, timeframe: str) -> int:
        """
        Menghitung jumlah candle yang tersimpan untuk symbol/timeframe.
        
        Args:
            symbol: Trading pair
            timeframe: Time interval
        
        Returns:
            Jumlah candle
        """
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                """
                SELECT COUNT(*) as count
                FROM candles
                WHERE symbol = ? AND timeframe = ?
                """,
                (symbol, timeframe),
            )
            row = await cursor.fetchone()
            return row[0] if row else 0

    async def get_news_count(self) -> int:
        """
        Menghitung total berita yang tersimpan.
        
        Returns:
            Jumlah berita
        """
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute("SELECT COUNT(*) as count FROM news")
            row = await cursor.fetchone()
            return row[0] if row else 0


# ============================================
# STANDALONE TESTING
# ============================================

async def test_database():
    """
    Test database operations.
    
    Cara menjalankan:
        python -m data_collector.database
    """
    logger.info("Testing database operations...")
    
    # Initialize
    db = DatabaseManager()
    await db.initialize()
    
    # Test save candles
    test_candles = [
        {
            "timestamp": 1642684522,
            "open": 42000.50,
            "high": 42500.00,
            "low": 41800.00,
            "close": 42300.75,
            "volume": 1234.56,
        }
    ]
    await db.save_candles("BTC/USDT", "1h", test_candles)
    
    # Test get candles
    candles = await db.get_candles("BTC/USDT", "1h", limit=10)
    logger.info(f"Retrieved {len(candles)} candles")
    
    # Test save ticker
    test_ticker = {
        "last": 42300.75,
        "bid": 42300.50,
        "ask": 42301.00,
        "baseVolume": 1234.56,
        "percentage": 2.5,
    }
    await db.save_ticker("BTC/USDT", test_ticker)
    
    # Test get ticker
    ticker = await db.get_latest_ticker("BTC/USDT")
    logger.info(f"Retrieved ticker: {ticker}")
    
    # Test save news
    test_news = [
        {
            "source": "CoinDesk",
            "title": "Bitcoin reaches new high",
            "link": "https://coindesk.com/test1",
            "published_date": 1642684522,
            "summary": "Bitcoin price surged...",
            "category": "crypto",
        }
    ]
    saved = await db.save_news(test_news)
    logger.info(f"Saved {saved} news articles")
    
    # Test get news
    news = await db.get_latest_news(limit=10)
    logger.info(f"Retrieved {len(news)} news articles")
    
    # Test counts
    candle_count = await db.get_candle_count("BTC/USDT", "1h")
    news_count = await db.get_news_count()
    logger.info(f"Candle count: {candle_count}, News count: {news_count}")
    
    logger.info("✅ Database test completed successfully")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_database())
