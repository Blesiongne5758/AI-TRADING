"""
Portfolio Routes
Endpoints untuk mengelola portfolio
"""
from fastapi import APIRouter, Depends, Request
from typing import List, Dict

router = APIRouter()


@router.get("/summary")
async def get_portfolio_summary(request: Request):
    """Mengambil ringkasan portfolio"""
    portfolio_manager = request.app.state.portfolio_manager
    db = request.app.state.db
    
    summary = portfolio_manager.get_portfolio_summary()
    stats = await db.get_portfolio_stats()
    
    return {
        "summary": summary,
        "stats": stats,
    }


@router.get("/positions")
async def get_open_positions(request: Request):
    """Mengambil semua posisi terbuka"""
    db = request.app.state.db
    positions = await db.get_open_positions()
    
    # Tambahkan current price & PnL
    enriched_positions = []
    for pos in positions:
        ticker = await db.get_ticker(pos["symbol"])
        current_price = ticker["price"] if ticker else pos["entry_price"]
        
        if pos["side"] == "long":
            pnl = (current_price - pos["entry_price"]) * pos["quantity"]
        else:
            pnl = (pos["entry_price"] - current_price) * pos["quantity"]
        
        pnl_percent = (pnl / (pos["entry_price"] * pos["quantity"])) * 100
        
        enriched_positions.append({
            **pos,
            "current_price": current_price,
            "pnl": pnl,
            "pnl_percent": pnl_percent,
        })
    
    return {"positions": enriched_positions}


@router.get("/history")
async def get_trade_history(request: Request, limit: int = 50):
    """Mengambil riwayat trade"""
    db = request.app.state.db
    
    import aiosqlite
    async with aiosqlite.connect(db.db_path) as conn:
        conn.row_factory = aiosqlite.Row
        cursor = await conn.execute(
            """
            SELECT * FROM positions 
            WHERE status = 'CLOSED'
            ORDER BY close_time DESC
            LIMIT ?
            """,
            (limit,),
        )
        rows = await cursor.fetchall()
        trades = [dict(row) for row in rows]
    
    return {"trades": trades, "count": len(trades)}


@router.get("/equity-curve")
async def get_equity_curve(request: Request, hours: int = 24):
    """Mengambil data equity curve"""
    db = request.app.state.db
    
    import aiosqlite
    from datetime import datetime, timedelta
    
    async with aiosqlite.connect(db.db_path) as conn:
        conn.row_factory = aiosqlite.Row
        
        cutoff_time = int((datetime.now() - timedelta(hours=hours)).timestamp() * 1000)
        
        cursor = await conn.execute(
            """
            SELECT timestamp, total_balance, unrealized_pnl, realized_pnl
            FROM portfolio_snapshots
            WHERE timestamp > ?
            ORDER BY timestamp ASC
            """,
            (cutoff_time,),
        )
        rows = await cursor.fetchall()
        snapshots = [dict(row) for row in rows]
    
    return {"snapshots": snapshots}
