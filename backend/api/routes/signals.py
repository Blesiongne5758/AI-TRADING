"""
Signals API Routes
Endpoints untuk trading signals
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Dict, List, Optional
from loguru import logger
from data_collector.database import DatabaseManager
from data_collector.config import TRADING_SYMBOLS
from analysis.technical_indicators import TechnicalAnalyzer
from analysis.sentiment_analysis import SentimentAnalyzer
from analysis.signal_generator import SignalGenerator

router = APIRouter()

# Initialize components
db = DatabaseManager()
tech_analyzer = TechnicalAnalyzer()
sentiment_analyzer = SentimentAnalyzer(use_finbert=False)
signal_generator = SignalGenerator()


@router.get("/analyze/{symbol}")
async def analyze_symbol(
    symbol: str,
    timeframe: str = Query(default="1h", enum=["1m", "5m", "15m", "1h", "4h", "1d"])
) -> Dict:
    """
    Analyze a symbol and generate trading signal
    
    Args:
        symbol: Trading pair (e.g., "BTC/USDT")
        timeframe: Timeframe for analysis
    
    Returns:
        Trading signal with analysis
    """
    try:
        await db.initialize()
        
        # Get candle data
        candles = await db.get_candles(symbol, timeframe, limit=250)
        if not candles or len(candles) < 200:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient data for {symbol} ({len(candles) if candles else 0} candles)"
            )
        
        # Technical analysis
        tech_result = tech_analyzer.calculate_all(candles)
        if not tech_result:
            raise HTTPException(status_code=500, detail="Technical analysis failed")
        
        # Sentiment analysis
        news_items = await db.get_latest_news(limit=15)
        sentiment_result = sentiment_analyzer.analyze_news_batch(news_items)
        
        # Generate signal
        signal = signal_generator.generate_signal(
            symbol=symbol,
            timeframe=timeframe,
            technical_analysis=tech_result,
            sentiment_analysis=sentiment_result,
        )
        
        return signal
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error analyzing {symbol}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analyze-all")
async def analyze_all_symbols(
    timeframe: str = Query(default="1h", enum=["1m", "5m", "15m", "1h", "4h", "1d"])
) -> List[Dict]:
    """
    Analyze all symbols and generate trading signals
    
    Args:
        timeframe: Timeframe for analysis
    
    Returns:
        List of trading signals
    """
    try:
        await db.initialize()
        
        signals = []
        for symbol in TRADING_SYMBOLS:
            try:
                # Get candle data
                candles = await db.get_candles(symbol, timeframe, limit=250)
                if not candles or len(candles) < 200:
                    continue
                
                # Technical analysis
                tech_result = tech_analyzer.calculate_all(candles)
                if not tech_result:
                    continue
                
                # Sentiment analysis
                news_items = await db.get_latest_news(limit=15)
                sentiment_result = sentiment_analyzer.analyze_news_batch(news_items)
                
                # Generate signal
                signal = signal_generator.generate_signal(
                    symbol=symbol,
                    timeframe=timeframe,
                    technical_analysis=tech_result,
                    sentiment_analysis=sentiment_result,
                )
                
                signals.append(signal)
            except Exception as e:
                logger.error(f"❌ Error analyzing {symbol}: {e}")
                continue
        
        return signals
    except Exception as e:
        logger.error(f"❌ Error analyzing all symbols: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history")
async def get_signal_history(limit: int = Query(default=50, ge=1, le=100)) -> List[Dict]:
    """
    Get signal history
    
    Args:
        limit: Maximum number of signals to return
    
    Returns:
        List of historical signals
    """
    try:
        await db.initialize()
        # TODO: Implement signal history in database
        return []
    except Exception as e:
        logger.error(f"❌ Error getting signal history: {e}")
        raise HTTPException(status_code=500, detail=str(e))
