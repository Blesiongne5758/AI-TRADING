"""
Chat API Routes
Endpoints untuk XAI chat agent
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict
from loguru import logger
from data_collector.database import DatabaseManager
from xai.chat_agent import ChatAgent

router = APIRouter()

# Initialize components
db = DatabaseManager()
chat_agent = ChatAgent(db)


class ChatRequest(BaseModel):
    """Chat request model"""
    message: str


class ChatResponse(BaseModel):
    """Chat response model"""
    response: str
    intent: str = "unknown"
    confidence: float = 0.0


@router.post("/message", response_model=ChatResponse)
async def chat_message(request: ChatRequest) -> ChatResponse:
    """
    Send a message to the chat agent
    
    Args:
        request: Chat request with message
    
    Returns:
        Chat response
    """
    try:
        await db.initialize()
        
        # Process message
        response = await chat_agent.process_message(request.message)
        
        # Detect intent (simplified)
        intent = "unknown"
        if "rsi" in request.message.lower() or "macd" in request.message.lower():
            intent = "explain_indicator"
        elif "portfolio" in request.message.lower():
            intent = "portfolio_status"
        elif "market" in request.message.lower() or "btc" in request.message.lower():
            intent = "market_condition"
        elif "kenapa" in request.message.lower() or "mengapa" in request.message.lower():
            intent = "why_trade"
        elif "help" in request.message.lower():
            intent = "help"
        
        return ChatResponse(
            response=response,
            intent=intent,
            confidence=0.9,  # Simplified confidence
        )
    except Exception as e:
        logger.error(f"❌ Error processing chat message: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/intents")
async def get_intents() -> Dict:
    """
    Get list of supported intents
    
    Returns:
        Dictionary with intent descriptions
    """
    return {
        "greeting": "Salam dan perkenalan",
        "explain_indicator": "Penjelasan indikator teknikal (RSI, MACD, EMA, dll)",
        "explain_concept": "Penjelasan konsep trading (long, short, stop-loss, dll)",
        "why_trade": "Penjelasan keputusan bot",
        "portfolio_status": "Status portfolio dan P&L",
        "market_condition": "Kondisi market dan harga terbaru",
        "recent_trades": "Riwayat trade terakhir",
        "help": "Panduan penggunaan",
        "thanks": "Ucapan terima kasih",
    }


@router.get("/dictionary")
async def get_dictionary() -> Dict:
    """
    Get trading dictionary
    
    Returns:
        Dictionary with all trading terms
    """
    try:
        from xai.trading_dictionary import TradingDictionary
        
        dictionary = TradingDictionary()
        return {
            "terms": dictionary.terms,
            "count": len(dictionary.terms),
        }
    except Exception as e:
        logger.error(f"❌ Error getting dictionary: {e}")
        raise HTTPException(status_code=500, detail=str(e))
