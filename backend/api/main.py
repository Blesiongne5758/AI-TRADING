"""
FastAPI Main Application
Menghubungkan semua modul backend dengan frontend
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from loguru import logger
import asyncio
import json
from datetime import datetime

from data_collector.database import DatabaseManager
from data_collector.config import TRADING_SYMBOLS
from paper_trading.portfolio_manager import PortfolioManager
from paper_trading.risk_manager import RiskManager
from analysis.technical_indicators import TechnicalAnalyzer
from analysis.sentiment_analysis import SentimentAnalyzer
from analysis.signal_generator import SignalGenerator
from xai.chat_agent import ChatAgent
from .routes import portfolio, signals, market, chat


# Global instances
db = DatabaseManager()
portfolio_manager = PortfolioManager(initial_balance=10000.0, db=db)
risk_manager = RiskManager(portfolio_manager)
tech_analyzer = TechnicalAnalyzer()
sentiment_analyzer = SentimentAnalyzer(use_finbert=False)
signal_generator = SignalGenerator()
chat_agent = ChatAgent(db)

# WebSocket connections
connected_clients = []


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup & shutdown events"""
    logger.info("🚀 Starting AI Trading Agent API...")
    await db.initialize()
    await portfolio_manager.initialize()
    logger.info("✅ API ready")
    yield
    logger.info("🛑 Shutting down API...")


app = FastAPI(
    title="AI Trading Agent API",
    description="API untuk AI Trading Agent - Fase 1 MVP",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite & CRA
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(portfolio.router, prefix="/api/portfolio", tags=["portfolio"])
app.include_router(signals.router, prefix="/api/signals", tags=["signals"])
app.include_router(market.router, prefix="/api/market", tags=["market"])
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])


@app.get("/")
async def root():
    """Health check"""
    return {
        "status": "ok",
        "service": "AI Trading Agent API",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
    }


@app.get("/api/status")
async def get_status():
    """Get overall system status"""
    portfolio_summary = portfolio_manager.get_portfolio_summary()
    stats = await db.get_portfolio_stats()
    
    return {
        "portfolio": portfolio_summary,
        "stats": stats,
        "monitoring_symbols": TRADING_SYMBOLS,
        "connected_clients": len(connected_clients),
    }


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket untuk real-time updates"""
    await websocket.accept()
    connected_clients.append(websocket)
    logger.info(f"🔌 WebSocket connected. Total clients: {len(connected_clients)}")

    try:
        while True:
            # Keep connection alive
            data = await websocket.receive_text()
            
            # Handle client messages (jika ada)
            if data == "ping":
                await websocket.send_text("pong")
                
    except WebSocketDisconnect:
        connected_clients.remove(websocket)
        logger.info(f"🔌 WebSocket disconnected. Total clients: {len(connected_clients)}")


async def broadcast_update(update_type: str, data: dict):
    """Broadcast update ke semua connected clients"""
    message = {
        "type": update_type,
        "data": data,
        "timestamp": datetime.now().isoformat(),
    }
    
    disconnected = []
    for client in connected_clients:
        try:
            await client.send_text(json.dumps(message))
        except:
            disconnected.append(client)
    
    # Remove disconnected clients
    for client in disconnected:
        if client in connected_clients:
            connected_clients.remove(client)


# Export untuk digunakan di route lain
app.state.db = db
app.state.portfolio_manager = portfolio_manager
app.state.risk_manager = risk_manager
app.state.tech_analyzer = tech_analyzer
app.state.sentiment_analyzer = sentiment_analyzer
app.state.signal_generator = signal_generator
app.state.chat_agent = chat_agent
app.state.broadcast_update = broadcast_update


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
