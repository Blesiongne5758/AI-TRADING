"""
Backtest API Routes
Endpoints untuk menjalankan backtesting strategies
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import datetime
import pandas as pd
import asyncio
from loguru import logger

from backtesting.backtest_engine import BacktestEngine
from analysis.custom_strategies import StrategyFactory

router = APIRouter()


class BacktestRequest(BaseModel):
    """Request model untuk backtest"""
    symbol: str
    timeframe: str = "1h"
    start_date: str
    end_date: str
    strategy: str
    strategy_params: Dict = {}
    initial_balance: float = 10000.0
    commission: float = 0.001  # 0.1%


class BacktestResponse(BaseModel):
    """Response model untuk backtest"""
    id: str
    status: str
    symbol: str
    timeframe: str
    strategy: str
    start_date: str
    end_date: str
    initial_balance: float
    final_balance: float
    total_return: float
    total_return_pct: float
    max_drawdown: float
    max_drawdown_pct: float
    sharpe_ratio: float
    win_rate: float
    total_trades: int
    winning_trades: int
    losing_trades: int
    avg_win: float
    avg_loss: float
    profit_factor: float
    created_at: str


class StrategyInfo(BaseModel):
    """Info model untuk strategy"""
    name: str
    description: str
    parameters: Dict
    default_params: Dict


class OptimizeRequest(BaseModel):
    """Request model untuk optimization"""
    symbol: str
    timeframe: str = "1h"
    start_date: str
    end_date: str
    strategy: str
    param_ranges: Dict[str, List]
    optimization_metric: str = "sharpe_ratio"
    initial_balance: float = 10000.0


# In-memory storage untuk backtest results (production should use database)
backtest_results = {}


@router.post("/run", response_model=BacktestResponse)
async def run_backtest(request: BacktestRequest):
    """
    Menjalankan backtest dengan parameter tertentu
    
    Args:
        request: BacktestRequest dengan symbol, timeframe, dates, strategy, dll
        
    Returns:
        BacktestResponse dengan hasil backtest
    """
    try:
        logger.info(f"Starting backtest: {request.symbol} {request.timeframe} with {request.strategy}")
        
        # Validate strategy
        if request.strategy not in StrategyFactory.list_strategies():
            raise HTTPException(
                status_code=400,
                detail=f"Unknown strategy: {request.strategy}. Available: {StrategyFactory.list_strategies()}"
            )
        
        # Create backtest engine
        engine = BacktestEngine(
            symbol=request.symbol,
            timeframe=request.timeframe,
            start_date=request.start_date,
            end_date=request.end_date,
            strategy_name=request.strategy,
            strategy_params=request.strategy_params,
            initial_balance=request.initial_balance,
            commission=request.commission
        )
        
        # Run backtest
        result = await engine.run()
        
        # Generate unique ID
        backtest_id = f"bt_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{request.symbol.replace('/', '_')}"
        
        # Store result
        backtest_results[backtest_id] = {
            "id": backtest_id,
            "status": "completed",
            "request": request.dict(),
            "result": result,
            "created_at": datetime.now().isoformat()
        }
        
        # Create response
        response = BacktestResponse(
            id=backtest_id,
            status="completed",
            symbol=request.symbol,
            timeframe=request.timeframe,
            strategy=request.strategy,
            start_date=request.start_date,
            end_date=request.end_date,
            initial_balance=result["initial_balance"],
            final_balance=result["final_balance"],
            total_return=result["total_return"],
            total_return_pct=result["total_return_pct"],
            max_drawdown=result["max_drawdown"],
            max_drawdown_pct=result["max_drawdown_pct"],
            sharpe_ratio=result["sharpe_ratio"],
            win_rate=result["win_rate"],
            total_trades=result["total_trades"],
            winning_trades=result["winning_trades"],
            losing_trades=result["losing_trades"],
            avg_win=result["avg_win"],
            avg_loss=result["avg_loss"],
            profit_factor=result["profit_factor"],
            created_at=datetime.now().isoformat()
        )
        
        logger.info(f"Backtest completed: {backtest_id} - Return: {result['total_return_pct']:.2f}%")
        
        return response
        
    except Exception as e:
        logger.error(f"Backtest error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/strategies", response_model=List[StrategyInfo])
async def get_strategies():
    """
    Mendapatkan daftar strategies yang tersedia
    
    Returns:
        List of StrategyInfo dengan nama, deskripsi, dan parameters
    """
    try:
        strategies = []
        
        for strategy_name in StrategyFactory.list_strategies():
            info = StrategyFactory.get_strategy_info(strategy_name)
            strategies.append(StrategyInfo(
                name=strategy_name,
                description=info["description"],
                parameters=info["parameters"],
                default_params=info["default_params"]
            ))
        
        return strategies
        
    except Exception as e:
        logger.error(f"Error getting strategies: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/results/{backtest_id}")
async def get_backtest_result(backtest_id: str):
    """
    Mendapatkan hasil backtest tertentu
    
    Args:
        backtest_id: ID backtest
        
    Returns:
        Dictionary dengan detail hasil backtest
    """
    try:
        if backtest_id not in backtest_results:
            raise HTTPException(status_code=404, detail=f"Backtest not found: {backtest_id}")
        
        return backtest_results[backtest_id]
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting backtest result: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/results")
async def list_backtest_results(limit: int = 10, offset: int = 0):
    """
    Mendapatkan daftar hasil backtest
    
    Args:
        limit: Jumlah results per page
        offset: Offset untuk pagination
        
    Returns:
        List of backtest results
    """
    try:
        results = list(backtest_results.values())
        
        # Sort by created_at descending
        results.sort(key=lambda x: x["created_at"], reverse=True)
        
        # Apply pagination
        paginated = results[offset:offset + limit]
        
        return {
            "total": len(results),
            "limit": limit,
            "offset": offset,
            "results": paginated
        }
        
    except Exception as e:
        logger.error(f"Error listing backtest results: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/results/{backtest_id}")
async def delete_backtest_result(backtest_id: str):
    """
    Menghapus hasil backtest tertentu
    
    Args:
        backtest_id: ID backtest
        
    Returns:
        Success message
    """
    try:
        if backtest_id not in backtest_results:
            raise HTTPException(status_code=404, detail=f"Backtest not found: {backtest_id}")
        
        del backtest_results[backtest_id]
        
        return {"status": "deleted", "id": backtest_id}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting backtest result: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/optimize")
async def optimize_strategy(request: OptimizeRequest):
    """
    Optimasi parameter strategy
    
    Args:
        request: OptimizeRequest dengan param_ranges dan optimization_metric
        
    Returns:
        Dictionary dengan best parameters dan results
    """
    try:
        logger.info(f"Starting optimization: {request.symbol} with {request.strategy}")
        
        # Validate strategy
        if request.strategy not in StrategyFactory.list_strategies():
            raise HTTPException(
                status_code=400,
                detail=f"Unknown strategy: {request.strategy}"
            )
        
        # Import optimizer
        from backtesting.optimizer import ParameterOptimizer
        
        # Create optimizer
        optimizer = ParameterOptimizer(
            symbol=request.symbol,
            timeframe=request.timeframe,
            start_date=request.start_date,
            end_date=request.end_date,
            strategy_name=request.strategy,
            initial_balance=request.initial_balance
        )
        
        # Run optimization
        result = await optimizer.optimize(
            param_ranges=request.param_ranges,
            optimization_metric=request.optimization_metric
        )
        
        # Generate unique ID
        optimize_id = f"opt_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{request.symbol.replace('/', '_')}"
        
        logger.info(f"Optimization completed: {optimize_id} - Best {request.optimization_metric}: {result['best_score']:.2f}")
        
        return {
            "id": optimize_id,
            "status": "completed",
            "strategy": request.strategy,
            "optimization_metric": request.optimization_metric,
            "best_params": result["best_params"],
            "best_score": result["best_score"],
            "total_combinations": result["total_combinations"],
            "created_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Optimization error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/strategy/{strategy_name}")
async def get_strategy_details(strategy_name: str):
    """
    Mendapatkan detail strategy tertentu
    
    Args:
        strategy_name: Nama strategy
        
    Returns:
        Dictionary dengan detail strategy
    """
    try:
        if strategy_name not in StrategyFactory.list_strategies():
            raise HTTPException(
                status_code=404,
                detail=f"Unknown strategy: {strategy_name}"
            )
        
        info = StrategyFactory.get_strategy_info(strategy_name)
        
        return {
            "name": strategy_name,
            "description": info["description"],
            "parameters": info["parameters"],
            "default_params": info["default_params"],
            "available": True
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting strategy details: {e}")
        raise HTTPException(status_code=500, detail=str(e))
