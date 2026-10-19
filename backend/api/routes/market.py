"""
Market Data API Routes
Endpoints untuk market data
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Dict, List, Optional
from loguru import logger
from data_collector.database import DatabaseManager
from data_collector.config import TRADING_SYMBOLS

router = APIRouter()

# Initialize database manager
db = DatabaseManager()


@router.get("/ticker/{symbol}")
async def get_ticker(symbol: str) -> Dict:
    """
    Get latest ticker data for a symbol
    
    Args:
        symbol: Trading pair (e.g., "BTC/USDT")
    
    Returns:
        Ticker data
    """
    try:
        await db.initialize()
        ticker = await db.get_ticker(symbol)
        
        if not ticker:
            raise HTTPException(status_code=404, detail=f"Ticker not found for {symbol}")
        
        return ticker
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error getting ticker for {symbol}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tickers")
async def get_all_tickers() -> List[Dict]:
    """
    Get latest ticker data for all symbols
    
    Returns:
        List of ticker data
    """
    try:
        await db.initialize()
        
        tickers = []
        for symbol in TRADING_SYMBOLS:
            ticker = await db.get_ticker(symbol)
            if ticker:
                tickers.append(ticker)
        
        return tickers
    except Exception as e:
        logger.error(f"❌ Error getting all tickers: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/candles/{symbol}")
async def get_candles(
    symbol: str,
    timeframe: str = Query(default="1h", enum=["1m", "5m", "15m", "1h", "4h", "1d"]),
    limit: int = Query(default=100, ge=1, le=1000)
) -> List[Dict]:
    """
    Get candlestick data for a symbol
    
    Args:
        symbol: Trading pair (e.g., "BTC/USDT")
        timeframe: Timeframe (1m, 5m, 15m, 1h, 4h, 1d)
        limit: Number of candles to return
    
    Returns:
        List of candlestick data
    """
    try:
        await db.initialize()
        candles = await db.get_candles(symbol, timeframe, limit=limit)
        
        if not candles:
            raise HTTPException(status_code=404, detail=f"No candle data found for {symbol}")
        
        return candles
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error getting candles for {symbol}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/news")
async def get_news(limit: int = Query(default=20, ge=1, le=100)) -> List[Dict]:
    """
    Get latest news
    
    Args:
        limit: Maximum number of news articles to return
    
    Returns:
        List of news articles
    """
    try:
        await db.initialize()
        news = await db.get_latest_news(limit=limit)
        return news
    except Exception as e:
        logger.error(f"❌ Error getting news: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/symbols")
async def get_symbols() -> List[str]:
    """
    Get list of trading symbols
    
    Returns:
        List of trading symbols
    """
    return TRADING_SYMBOLS


@router.get("/timeframes")
async def get_timeframes() -> List[str]:
    """
    Get list of available timeframes
    
    Returns:
        List of timeframes
    """
    return ["1m", "5m", "15m", "1h", "4h", "1d"]
