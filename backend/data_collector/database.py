"""
Database Module - SQLite Setup & Operations

File ini menangani semua operasi database menggunakan SQLAlchemy async.
Database digunakan untuk menyimpan:
- Data OHLCV (candlestick) dari Binance
- Berita crypto dan sentimen
- Sinyal trading
- Riwayat transaksi paper trading
- Posisi aktif

Untuk pemula:
- SQLAlchemy adalah ORM (Object-Relational Mapper) - kita bekerja dengan Python objects
- Async/await memungkinkan database operations tanpa blocking
- Database akan otomatis dibuat saat pertama kali dijalankan

Cara penggunaan:
    from data_collector.database import (
        init_db, save_ohlcv_data, get_ohlcv_data,
        save_news_data, get_recent_news
    )
    
    # Initialize database
    await init_db()
    
    # Save data
    await save_ohlcv_data("BTC/USDT", "1h", [candle_data])
    
    # Get data
    data = await get_ohlcv_data("BTC/USDT", "1h", limit=100)
"""

import os
from datetime import datetime, timedelta
from typing import List, Optional
from contextlib import asynccontextmanager

from sqlalchemy import (
    Column, Integer, Float, String, DateTime, Boolean, Text,
    Index, select
)
from sqlalchemy.ext.asyncio import (
    AsyncSession, create_async_engine, async_sessionmaker
)
from sqlalchemy.orm import DeclarativeBase
from loguru import logger

from data_collector.config import DATABASE_PATH, LOG_LEVEL


# ============================================
# DATABASE MODELS (Tabel)
# ============================================

class Base(DeclarativeBase):
    """Base class untuk semua model database"""
    pass


class OHLCVData(Base):
    """
    Tabel untuk menyimpan data candlestick (OHLCV) dari Binance.
    
    OHLCV = Open, High, Low, Close, Volume
    Ini adalah data harga dasar untuk analisis teknikal.
    
    Contoh data:
    - symbol: "BTC/USDT"
    - timeframe: "1h" (1 jam)
    - timestamp: 1642684522 (Unix timestamp)
    - open: 42000.50 (harga pembukaan)
    - high: 42500.00 (harga tertinggi)
    - low: 41800.00 (harga terendah)
    - close: 42300.75 (harga penutupan)
    - volume: 1234.56 (volume trading)
    """
    __tablename__ = "ohlcv_data"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String(20), nullable=False, index=True)
    timeframe = Column(String(5), nullable=False, index=True)
    timestamp = Column(Integer, nullable=False)  # Unix timestamp
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Composite index untuk query yang efisien
    __table_args__ = (
        Index('idx_symbol_timeframe_timestamp', 'symbol', 'timeframe', 'timestamp'),
    )
    
    def __repr__(self) -> str:
        return f"<OHLCV {self.symbol} {self.timeframe} {self.timestamp}>"


class NewsData(Base):
    """
    Tabel untuk menyimpan berita crypto dan analisis sentimen.
    
    Setiap berita akan dianalisis oleh FinBERT untuk menentukan sentimen:
    - sentiment_score: -1.0 (sangat negatif) sampai +1.0 (sangat positif)
    - sentiment_label: "bullish", "bearish", atau "neutral"
    """
    __tablename__ = "news_data"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(Text, nullable=False)
    source = Column(String(100), nullable=False)
    url = Column(Text, nullable=True)
    published_at = Column(DateTime, nullable=False)
    summary = Column(Text, nullable=True)
    
    # Sentiment analysis results
    sentiment_score = Column(Float, nullable=True)  # -1.0 to 1.0
    sentiment_label = Column(String(20), nullable=True)  # bullish, bearish, neutral
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        Index('idx_news_published', 'published_at'),
        Index('idx_news_sentiment', 'sentiment_label'),
    )
    
    def __repr__(self) -> str:
        return f"<News {self.source}: {self.title[:50]}...>"


class TradingSignal(Base):
    """
    Tabel untuk menyimpan sinyal trading yang dihasilkan oleh Analysis Engine.
    
    Setiap sinyal berisi:
    - signal: "BUY", "SELL", atau "HOLD"
    - confidence: 0.0 sampai 1.0 (0% sampai 100%)
    - reasons: JSON array berisi alasan-alasan sinyal
    - executed: apakah sinyal sudah dieksekusi atau tidak
    """
    __tablename__ = "trading_signals"
    
    id = Column(String(50), primary_key=True)
    symbol = Column(String(20), nullable=False, index=True)
    timeframe = Column(String(5), nullable=False)
    signal = Column(String(10), nullable=False)  # BUY, SELL, HOLD
    confidence = Column(Float, nullable=False)
    reasons = Column(Text, nullable=False)  # JSON string
    price = Column(Float, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    executed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        Index('idx_signal_symbol_time', 'symbol', 'timestamp'),
    )
    
    def __repr__(self) -> str:
        return f"<Signal {self.symbol} {self.signal} {self.confidence:.2%}>"


# ============================================
# DATABASE ENGINE & SESSION
# ============================================

# Create async engine
# DATABASE_PATH sudah Path object, convert ke string untuk URL
DATABASE_URL = f"sqlite+aiosqlite:///{DATABASE_PATH}"
engine = create_async_engine(
    DATABASE_URL,
    echo=False,  # Set True untuk debug SQL queries
    future=True,
)

# Create async session factory
async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# ============================================
# DATABASE INITIALIZATION
# ============================================

async def init_db() -> None:
    """
    Initialize database - create all tables.
    
    Dipanggil saat aplikasi dimulai.
    Jika tabel sudah ada, tidak akan membuat ulang.
    """
    try:
        async with engine.begin() as conn:
            # Create all tables
            await conn.run_sync(Base.metadata.create_all)
            logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise


async def close_db() -> None:
    """
    Close database connections.
    
    Dipanggil saat aplikasi shutdown.
    """
    try:
        await engine.dispose()
        logger.info("Database connections closed")
    except Exception as e:
        logger.error(f"Failed to close database: {e}")


# ============================================
# DATABASE OPERATIONS (CRUD)
# ============================================

@asynccontextmanager
async def get_session():
    """
    Context manager untuk mendapatkan database session.
    
    Penggunaan:
        async with get_session() as session:
            # Do database operations
            await session.commit()
    """
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            await session.close()


# ============================================
# OHLCV DATA OPERATIONS
# ============================================

async def save_ohlcv_data(
    symbol: str,
    timeframe: str,
    data: List[dict]
) -> int:
    """
    Simpan data OHLCV ke database.
    
    Args:
        symbol: Trading pair (e.g., "BTC/USDT")
        timeframe: Time interval (e.g., "1h")
        data: List of OHLCV dictionaries
    
    Returns:
        Jumlah data yang berhasil disimpan
    
    Contoh data:
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
    saved_count = 0
    
    try:
        async with get_session() as session:
            for item in data:
                # Check if data already exists
                stmt = select(OHLCVData).where(
                    OHLCVData.symbol == symbol,
                    OHLCVData.timeframe == timeframe,
                    OHLCVData.timestamp == item["timestamp"]
                )
                result = await session.execute(stmt)
                existing = result.scalar_one_or_none()
                
                if not existing:
                    # Create new record
                    ohlcv = OHLCVData(
                        symbol=symbol,
                        timeframe=timeframe,
                        timestamp=item["timestamp"],
                        open=item["open"],
                        high=item["high"],
                        low=item["low"],
                        close=item["close"],
                        volume=item["volume"]
                    )
                    session.add(ohlcv)
                    saved_count += 1
            
            logger.info(f"Saved {saved_count} OHLCV records for {symbol} {timeframe}")
            return saved_count
            
    except Exception as e:
        logger.error(f"Failed to save OHLCV data: {e}")
        raise


async def get_ohlcv_data(
    symbol: str,
    timeframe: str,
    limit: int = 500
) -> List[OHLCVData]:
    """
    Ambil data OHLCV dari database.
    
    Args:
        symbol: Trading pair
        timeframe: Time interval
        limit: Jumlah data maksimum (default 500)
    
    Returns:
        List of OHLCVData objects, sorted by timestamp descending
    """
    try:
        async with get_session() as session:
            stmt = (
                select(OHLCVData)
                .where(
                    OHLCVData.symbol == symbol,
                    OHLCVData.timeframe == timeframe
                )
                .order_by(OHLCVData.timestamp.desc())
                .limit(limit)
            )
            result = await session.execute(stmt)
            data = result.scalars().all()
            
            # Reverse to get chronological order
            return list(reversed(data))
            
    except Exception as e:
        logger.error(f"Failed to get OHLCV data: {e}")
        raise


# ============================================
# NEWS DATA OPERATIONS
# ============================================

async def save_news_data(
    title: str,
    source: str,
    url: str,
    published_at: datetime,
    summary: Optional[str] = None,
    sentiment_score: Optional[float] = None,
    sentiment_label: Optional[str] = None
) -> bool:
    """
    Simpan data berita ke database.
    
    Returns:
        True jika berhasil disimpan, False jika sudah ada
    """
    try:
        async with get_session() as session:
            # Check if news already exists
            stmt = select(NewsData).where(NewsData.url == url)
            result = await session.execute(stmt)
            existing = result.scalar_one_or_none()
            
            if existing:
                logger.debug(f"News already exists: {url}")
                return False
            
            # Create new record
            news = NewsData(
                title=title,
                source=source,
                url=url,
                published_at=published_at,
                summary=summary,
                sentiment_score=sentiment_score,
                sentiment_label=sentiment_label
            )
            session.add(news)
            logger.info(f"Saved news: {title[:50]}...")
            return True
            
    except Exception as e:
        logger.error(f"Failed to save news: {e}")
        raise


async def get_recent_news(
    limit: int = 50,
    hours: int = 24
) -> List[NewsData]:
    """
    Ambil berita terbaru dari database.
    
    Args:
        limit: Jumlah berita maksimum
        hours: Ambil berita dari X jam terakhir
    
    Returns:
        List of NewsData objects
    """
    try:
        async with get_session() as session:
            cutoff_time = datetime.utcnow() - timedelta(hours=hours)
            
            stmt = (
                select(NewsData)
                .where(NewsData.published_at >= cutoff_time)
                .order_by(NewsData.published_at.desc())
                .limit(limit)
            )
            result = await session.execute(stmt)
            return list(result.scalars().all())
            
    except Exception as e:
        logger.error(f"Failed to get recent news: {e}")
        raise
