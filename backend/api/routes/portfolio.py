"""
Portfolio API Routes
Endpoints untuk portfolio management
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, List
from loguru import logger
from data_collector.database import DatabaseManager
from paper_trading.portfolio_manager import PortfolioManager

router = APIRouter()

# Initialize database manager
db = DatabaseManager()


@router.get("/summary")
async def get_portfolio_summary() -> Dict:
    """
    Get portfolio summary
    
    Returns:
        Dictionary dengan summary portfolio
    """
    try:
        await db.initialize()
        stats = await db.get_portfolio_stats()
        
        # Get open positions
        positions = await db.get_open_positions()
        
        # Calculate current balance
        balance = await db.get_current_balance()
        
        return {
            "balance": balance,
            "stats": stats,
            "open_positions": len(positions),
            "positions": positions,
        }
    except Exception as e:
        logger.error(f"❌ Error getting portfolio summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/positions")
async def get_positions(status: str = "OPEN") -> List[Dict]:
    """
    Get positions by status
    
    Args:
        status: OPEN or CLOSED
    
    Returns:
        List of positions
    """
    try:
        await db.initialize()
        
        if status == "OPEN":
            positions = await db.get_open_positions()
        else:
            # Get closed positions from trades
            positions = []  # TODO: Implement get_closed_positions
        
        return positions
    except Exception as e:
        logger.error(f"❌ Error getting positions: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/trades")
async def get_trades(limit: int = 50) -> List[Dict]:
    """
    Get trade history
    
    Args:
        limit: Maximum number of trades to return
    
    Returns:
        List of trades
    """
    try:
        await db.initialize()
        trades = await db.get_trade_history(limit=limit)
        return trades
    except Exception as e:
        logger.error(f"❌ Error getting trades: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats")
async def get_portfolio_stats() -> Dict:
    """
    Get portfolio statistics
    
    Returns:
        Dictionary dengan statistics
    """
    try:
        await db.initialize()
        stats = await db.get_portfolio_stats()
        return stats
    except Exception as e:
        logger.error(f"❌ Error getting portfolio stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/snapshots")
async def get_portfolio_snapshots(limit: int = 100) -> List[Dict]:
    """
    Get portfolio snapshots for equity curve
    
    Args:
        limit: Maximum number of snapshots
    
    Returns:
        List of snapshots
    """
    try:
        await db.initialize()
        snapshots = await db.get_portfolio_snapshots(limit=limit)
        return snapshots
    except Exception as e:
        logger.error(f"❌ Error getting snapshots: {e}")
        raise HTTPException(status_code=500, detail=str(e))
