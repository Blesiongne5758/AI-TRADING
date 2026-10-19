"""
Test Database Module

Unit tests untuk database operations.

Cara menjalankan:
    pytest tests/test_database.py -v
"""

import pytest
import asyncio
from datetime import datetime, timedelta

from database import (
    init_db, close_db, get_session,
    save_ohlcv_data, get_ohlcv_data,
    save_news_data, get_recent_news,
    OHLCVData, NewsData
)


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def setup_database():
    """Initialize database before tests."""
    await init_db()
    yield
    await close_db()


class TestOHLCVData:
    """Test OHLCV data operations."""
    
    @pytest.mark.asyncio
    async def test_save_ohlcv_data(self):
        """Test saving OHLCV data to database."""
        # Test data
        data = [
            {
                "timestamp": 1642684522,
                "open": 42000.50,
                "high": 42500.00,
                "low": 41800.00,
                "close": 42300.75,
                "volume": 1234.56
            },
            {
                "timestamp": 1642688122,
                "open": 42300.75,
                "high": 42800.00,
                "low": 42200.00,
                "close": 42650.25,
                "volume": 1456.78
            }
        ]
        
        # Save data
        saved_count = await save_ohlcv_data("BTC/USDT", "1h", data)
        
        # Verify
        assert saved_count == 2
        
        # Retrieve data
        retrieved = await get_ohlcv_data("BTC/USDT", "1h", limit=10)
        
        # Verify
        assert len(retrieved) >= 2
        assert retrieved[0].symbol == "BTC/USDT"
        assert retrieved[0].timeframe == "1h"
    
    @pytest.mark.asyncio
    async def test_save_duplicate_ohlcv(self):
        """Test that duplicate data is not saved."""
        data = [
            {
                "timestamp": 1642691722,
                "open": 42500.00,
                "high": 43000.00,
                "low": 42400.00,
                "close": 42800.00,
                "volume": 1500.00
            }
        ]
        
        # Save first time
        saved_count1 = await save_ohlcv_data("ETH/USDT", "1h", data)
        assert saved_count1 == 1
        
        # Save same data again
        saved_count2 = await save_ohlcv_data("ETH/USDT", "1h", data)
        assert saved_count2 == 0  # Should not save duplicate
    
    @pytest.mark.asyncio
    async def test_get_ohlcv_data_limit(self):
        """Test limit parameter in get_ohlcv_data."""
        # Save multiple records
        data = []
        for i in range(10):
            data.append({
                "timestamp": 1642700000 + i,
                "open": 42000.0 + i,
                "high": 42500.0 + i,
                "low": 41800.0 + i,
                "close": 42300.0 + i,
                "volume": 1000.0 + i
            })
        
        await save_ohlcv_data("SOL/USDT", "1h", data)
        
        # Get with limit
        retrieved = await get_ohlcv_data("SOL/USDT", "1h", limit=5)
        
        # Verify
        assert len(retrieved) == 5


class TestNewsData:
    """Test news data operations."""
    
    @pytest.mark.asyncio
    async def test_save_news_data(self):
        """Test saving news data to database."""
        # Save news
        success = await save_news_data(
            title="Bitcoin reaches new all-time high",
            source="CoinDesk",
            url="https://coindesk.com/test1",
            published_at=datetime.utcnow(),
            summary="Bitcoin price surged to new heights today.",
            sentiment_score=0.85,
            sentiment_label="bullish"
        )
        
        # Verify
        assert success is True
    
    @pytest.mark.asyncio
    async def test_save_duplicate_news(self):
        """Test that duplicate news is not saved."""
        url = "https://coindesk.com/test2"
        
        # Save first time
        success1 = await save_news_data(
            title="Ethereum upgrade announced",
            source="CoinTelegraph",
            url=url,
            published_at=datetime.utcnow(),
            sentiment_score=0.72,
            sentiment_label="bullish"
        )
        assert success1 is True
        
        # Save same URL again
        success2 = await save_news_data(
            title="Ethereum upgrade announced",
            source="CoinTelegraph",
            url=url,
            published_at=datetime.utcnow(),
            sentiment_score=0.72,
            sentiment_label="bullish"
        )
        assert success2 is False  # Should not save duplicate
    
    @pytest.mark.asyncio
    async def test_get_recent_news(self):
        """Test getting recent news."""
        # Save some news
        for i in range(5):
            await save_news_data(
                title=f"Test news {i}",
                source="TestSource",
                url=f"https://test.com/news{i}",
                published_at=datetime.utcnow() - timedelta(hours=i),
                sentiment_score=0.5,
                sentiment_label="neutral"
            )
        
        # Get recent news
        news = await get_recent_news(limit=10, hours=24)
        
        # Verify
        assert len(news) >= 5
        assert all(isinstance(n, NewsData) for n in news)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
