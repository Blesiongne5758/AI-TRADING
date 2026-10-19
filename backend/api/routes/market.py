"""
Market Routes
Endpoints untuk data market
"""
from fastapi import APIRouter, Request
from typing import List

router = APIRouter()


@router.get("/tickers")
async def get_all_tickers(request: Request):
    """Mengambil semua ticker terbaru"""
    db = request.app.state.db
    from data_collector.config import TRADING_SYMBOLS
    
    tickers = []
    for symbol in TRADING_SYMBOLS:
        ticker = await db.get_ticker(symbol)
        if ticker:
            tickers.append(ticker)
    
    return {"tickers": tickers}


@router.get("/candles/{symbol}")
async def get_candles(
    request: Request,
    symbol: str,
    timeframe: str = "1h",
    limit: int = 100,
):
    """Mengambil data candlestick"""
    db = request.app.state.db
    candles = await db.get_candles(symbol, timeframe, limit)
    
    return {
        "symbol": symbol,
        "timeframe": timeframe,
        "candles": candles,
        "count": len(candles),
    }


@router.get("/news")
async def get_news(request: Request, limit: int = 20):
    """Mengambil berita terbaru"""
    db = request.app.state.db
    news = await db.get_latest_news(limit)
    
    return {"news": news, "count": len(news)}
