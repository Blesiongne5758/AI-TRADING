"""
AI Trading Agent - FastAPI Main Application

Ini adalah entry point utama untuk backend AI Trading Agent.
FastAPI menyediakan REST API untuk komunikasi dengan frontend.

Untuk pemula:
- FastAPI adalah web framework modern untuk Python (seperti Flask tapi lebih cepat)
- Async/await memungkinkan handling banyak request secara concurrent
- API endpoints bisa diakses via HTTP (GET, POST, dll)
- Swagger UI otomatis tersedia di /docs untuk testing API

Alur kerja aplikasi:
1. Startup: Initialize database, start data collectors
2. Running: Serve API requests, collect data continuously
3. Shutdown: Stop collectors, close connections
"""

import asyncio
from contextlib import asynccontextmanager
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from loguru import logger
import sys

from config import settings
from database import (
    init_db, close_db, get_session,
    get_ohlcv_data, get_recent_news,
    OHLCVData, NewsData
)
from data_collector import BinanceDataCollector, NewsScraper


# ============================================
# LOGGING SETUP
# ============================================

# Remove default logger
logger.remove()

# Add console logger
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level=settings.LOG_LEVEL
)

# Add file logger
logger.add(
    "logs/api.log",
    rotation="10 MB",
    retention="7 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}"
)


# ============================================
# GLOBAL STATE
# ============================================

class AppState:
    """
    Global application state.
    
    Menyimpan instances dari semua services.
    """
    binance_collector: Optional[BinanceDataCollector] = None
    news_scraper: Optional[NewsScraper] = None
    background_tasks: List[asyncio.Task] = []


app_state = AppState()


# ============================================
# LIFESPAN (STARTUP & SHUTDOWN)
# ============================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan handler.
    
    Dipanggil saat aplikasi start dan shutdown.
    """
    # STARTUP
    logger.info("=" * 60)
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info("=" * 60)
    
    try:
        # Initialize database
        logger.info("Initializing database...")
        await init_db()
        
        # Initialize Binance collector
        logger.info("Initializing Binance data collector...")
        app_state.binance_collector = BinanceDataCollector()
        await app_state.binance_collector.initialize()
        
        # Initialize news scraper
        logger.info("Initializing news scraper...")
        app_state.news_scraper = NewsScraper()
        await app_state.news_scraper.initialize()
        
        # Start background tasks
        logger.info("Starting background tasks...")
        
        # Task 1: Fetch historical data
        task1 = asyncio.create_task(fetch_initial_data())
        app_state.background_tasks.append(task1)
        
        # Task 2: Start real-time data collection
        task2 = asyncio.create_task(app_state.binance_collector.start())
        app_state.background_tasks.append(task2)
        
        # Task 3: Start news scraping
        task3 = asyncio.create_task(app_state.news_scraper.start())
        app_state.background_tasks.append(task3)
        
        logger.info("Application started successfully")
        
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        raise
    
    yield  # Application runs here
    
    # SHUTDOWN
    logger.info("Shutting down application...")
    
    try:
        # Stop background tasks
        for task in app_state.background_tasks:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
        
        # Stop collectors
        if app_state.binance_collector:
            await app_state.binance_collector.stop()
        
        if app_state.news_scraper:
            await app_state.news_scraper.stop()
        
        # Close database
        await close_db()
        
        logger.info("Application shutdown complete")
        
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")


# ============================================
# FASTAPI APP
# ============================================

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI Trading Agent Backend API",
    lifespan=lifespan
)

# CORS middleware (allow frontend to access API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================
# BACKGROUND TASKS
# ============================================

async def fetch_initial_data():
    """
    Fetch initial historical data for all symbols and timeframes.
    
    Ini dijalankan sekali saat startup untuk mengisi database.
    """
    logger.info("Fetching initial historical data...")
    
    try:
        for symbol in settings.TRADING_SYMBOLS:
            for timeframe in settings.TIMEFRAMES:
                try:
                    # Fetch historical data
                    data = await app_state.binance_collector.fetch_historical_ohlcv(
                        symbol=symbol,
                        timeframe=timeframe,
                        limit=500
                    )
                    
                    # Save to database
                    from database import save_ohlcv_data
                    saved = await save_ohlcv_data(symbol, timeframe, data)
                    
                    logger.info(f"Fetched {saved} candles for {symbol} {timeframe}")
                    
                    # Small delay to avoid rate limiting
                    await asyncio.sleep(1)
                    
                except Exception as e:
                    logger.error(f"Failed to fetch {symbol} {timeframe}: {e}")
                    continue
        
        logger.info("Initial data fetch complete")
        
    except Exception as e:
        logger.error(f"Error in initial data fetch: {e}")


# ============================================
# PYDANTIC MODELS (Request/Response schemas)
# ============================================

class OHLCVResponse(BaseModel):
    """Response model for OHLCV data"""
    timestamp: int
    open: float
    high: float
    low: float
    close: float
    volume: float


class NewsResponse(BaseModel):
    """Response model for news data"""
    id: int
    title: str
    source: str
    url: str
    published_at: datetime
    summary: Optional[str]
    sentiment_score: Optional[float]
    sentiment_label: Optional[str]


class StatusResponse(BaseModel):
    """Response model for system status"""
    status: str
    version: str
    timestamp: datetime
    services: Dict[str, Any]


# ============================================
# API ENDPOINTS
# ============================================

@app.get("/")
async def root():
    """
    Root endpoint - API information.
    
    GET /
    """
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    
    GET /health
    
    Digunakan untuk monitoring dan load balancer.
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/status", response_model=StatusResponse)
async def get_status():
    """
    Get system status and statistics.
    
    GET /status
    
    Returns:
        System status including all services
    """
    services = {}
    
    if app_state.binance_collector:
        services['binance_collector'] = app_state.binance_collector.get_stats()
    
    if app_state.news_scraper:
        services['news_scraper'] = app_state.news_scraper.get_stats()
    
    return StatusResponse(
        status="running",
        version=settings.APP_VERSION,
        timestamp=datetime.utcnow(),
        services=services
    )


@app.get("/ohlcv/{symbol}/{timeframe}", response_model=List[OHLCVResponse])
async def get_ohlcv(
    symbol: str,
    timeframe: str,
    limit: int = 500
):
    """
    Get OHLCV data for a symbol and timeframe.
    
    GET /ohlcv/BTC/USDT/1h?limit=500
    
    Args:
        symbol: Trading pair (e.g., "BTC/USDT")
        timeframe: Time interval (e.g., "1h")
        limit: Number of candles (default 500, max 1000)
    
    Returns:
        List of OHLCV data points
    """
    # Validate inputs
    if symbol not in settings.TRADING_SYMBOLS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid symbol. Available: {settings.TRADING_SYMBOLS}"
        )
    
    if timeframe not in settings.TIMEFRAMES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid timeframe. Available: {settings.TIMEFRAMES}"
        )
    
    limit = min(limit, 1000)  # Cap at 1000
    
    try:
        data = await get_ohlcv_data(symbol, timeframe, limit)
        
        return [
            OHLCVResponse(
                timestamp=candle.timestamp,
                open=candle.open,
                high=candle.high,
                low=candle.low,
                close=candle.close,
                volume=candle.volume
            )
            for candle in data
        ]
        
    except Exception as e:
        logger.error(f"Failed to get OHLCV data: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/news", response_model=List[NewsResponse])
async def get_news(
    limit: int = 50,
    hours: int = 24
):
    """
    Get recent news with sentiment analysis.
    
    GET /news?limit=50&hours=24
    
    Args:
        limit: Number of news items (default 50)
        hours: Time range in hours (default 24)
    
    Returns:
        List of news with sentiment scores
    """
    try:
        news = await get_recent_news(limit=limit, hours=hours)
        
        return [
            NewsResponse(
                id=item.id,
                title=item.title,
                source=item.source,
                url=item.url,
                published_at=item.published_at,
                summary=item.summary,
                sentiment_score=item.sentiment_score,
                sentiment_label=item.sentiment_label
            )
            for item in news
        ]
        
    except Exception as e:
        logger.error(f"Failed to get news: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/price/{symbol}")
async def get_current_price(symbol: str):
    """
    Get current price for a symbol.
    
    GET /price/BTC/USDT
    
    Args:
        symbol: Trading pair
    
    Returns:
        Current price
    """
    if not app_state.binance_collector:
        raise HTTPException(status_code=503, detail="Binance collector not initialized")
    
    try:
        price = await app_state.binance_collector.fetch_current_price(symbol)
        
        return {
            "symbol": symbol,
            "price": price,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to get price: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================
# MAIN ENTRY POINT
# ============================================

def main():
    """
    Main entry point untuk menjalankan server.
    
    Cara menjalankan:
        python main.py
    
    Atau dengan uvicorn langsung:
        uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    """
    import uvicorn
    
    logger.info(f"Starting server on {settings.API_HOST}:{settings.API_PORT}")
    
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )


if __name__ == "__main__":
    main()
