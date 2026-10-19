"""
FastAPI Main Application
REST API untuk AI Trading Agent
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
import sys

from .routes import portfolio, signals, market, chat
from .websocket import router as websocket_router

# Setup logging
logger.remove()
logger.add(
    sys.stdout,
    level="INFO",
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | {message}",
)

# Create FastAPI app
app = FastAPI(
    title="AI Trading Agent API",
    description="REST API untuk AI Trading Agent dengan XAI capabilities",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(portfolio.router, prefix="/api/portfolio", tags=["Portfolio"])
app.include_router(signals.router, prefix="/api/signals", tags=["Signals"])
app.include_router(market.router, prefix="/api/market", tags=["Market"])
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(websocket_router, prefix="/ws", tags=["WebSocket"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "🤖 AI Trading Agent API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": "ok"}


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"❌ Error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": str(exc), "type": type(exc).__name__},
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
