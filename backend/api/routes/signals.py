"""
Signal Routes
Endpoints untuk analisis dan sinyal trading
"""
from fastapi import APIRouter, Request, HTTPException
from typing import Optional
from analysis.technical_indicators import TechnicalAnalyzer
from analysis.sentiment_analysis import SentimentAnalyzer
from analysis.signal_generator import SignalGenerator

router = APIRouter()


@router.get("/analyze/{symbol}")
async def analyze_symbol(
    request: Request,
    symbol: str,
    timeframe: str = "1h",
):
    """Menganalisis satu simbol dan generate signal"""
    db = request.app.state.db
    tech_analyzer = request.app.state.tech_analyzer
    sentiment_analyzer = request.app.state.sentiment_analyzer
    signal_generator = request.app.state.signal_generator
    
    # Validasi timeframe
    valid_timeframes = ["1m", "5m", "15m", "1h", "4h", "1d"]
    if timeframe not in valid_timeframes:
        raise HTTPException(status_code=400, detail=f"Invalid timeframe. Use: {valid_timeframes}")
    
    # Ambil data candle
    candles = await db.get_candles(symbol, timeframe, limit=250)
    if not candles:
        raise HTTPException(status_code=404, detail=f"No data for {symbol}")
    
    # Analisis teknikal
    tech_result = tech_analyzer.calculate_all(candles)
    if not tech_result:
        raise HTTPException(status_code=500, detail="Technical analysis failed")
    
    # Analisis sentimen
    news_items = await db.get_latest_news(limit=15)
    sentiment_result = sentiment_analyzer.analyze_news_batch(news_items)
    
    # Generate signal
    signal = signal_generator.generate_signal(
        symbol=symbol,
        timeframe=timeframe,
        technical_analysis=tech_result,
        sentiment_analysis=sentiment_result,
    )
    
    return {
        "signal": signal,
        "technical_analysis": tech_result,
        "sentiment_analysis": sentiment_result,
    }


@router.get("/active")
async def get_active_signals(request: Request):
    """Mengambil sinyal aktif untuk semua simbol"""
    db = request.app.state.db
    tech_analyzer = request.app.state.tech_analyzer
    sentiment_analyzer = request.app.state.sentiment_analyzer
    signal_generator = request.app.state.signal_generator
    
    from data_collector.config import TRADING_SYMBOLS
    
    active_signals = []
    
    for symbol in TRADING_SYMBOLS:
        try:
            candles = await db.get_candles(symbol, "1h", limit=250)
            if not candles:
                continue
            
            tech_result = tech_analyzer.calculate_all(candles)
            if not tech_result:
                continue
            
            news_items = await db.get_latest_news(limit=15)
            sentiment_result = sentiment_analyzer.analyze_news_batch(news_items)
            
            signal = signal_generator.generate_signal(
                symbol=symbol,
                timeframe="1h",
                technical_analysis=tech_result,
                sentiment_analysis=sentiment_result,
            )
            
            active_signals.append(signal)
            
        except Exception as e:
            continue
    
    return {"signals": active_signals, "count": len(active_signals)}


@router.get("/history")
async def get_signal_history(request: Request, limit: int = 20):
    """Mengambil riwayat sinyal (dari trades)"""
    db = request.app.state.db
    
    import aiosqlite
    async with aiosqlite.connect(db.db_path) as conn:
        conn.row_factory = aiosqlite.Row
        cursor = await conn.execute(
            """
            SELECT t.*, p.entry_price, p.stop_loss, p.take_profit, p.pnl, p.exit_reason
            FROM trades t
            LEFT JOIN positions p ON t.position_id = p.id
            ORDER BY t.timestamp DESC
            LIMIT ?
            """,
            (limit,),
        )
        rows = await cursor.fetchall()
        history = [dict(row) for row in rows]
    
    return {"history": history, "count": len(history)}
