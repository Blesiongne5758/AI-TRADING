"""
Chat Routes
Endpoints untuk chat agent
"""
from fastapi import APIRouter, Request
from pydantic import BaseModel

router = APIRouter()


class ChatMessage(BaseModel):
    message: str


@router.post("/message")
async def send_message(request: Request, chat_message: ChatMessage):
    """Mengirim pesan ke chat agent"""
    chat_agent = request.app.state.chat_agent
    
    response = await chat_agent.process_message(chat_message.message)
    
    return {
        "response": response,
        "timestamp": request.state.timestamp if hasattr(request.state, 'timestamp') else None,
    }


@router.get("/suggestions")
async def get_suggestions():
    """Mengambil saran pertanyaan"""
    return {
        "suggestions": [
            "Apa itu RSI?",
            "Kenapa bot beli BTC?",
            "Status portfolio saya",
            "Jelaskan MACD",
            "Apa artinya stop-loss?",
            "Bagaimana kondisi market?",
        ]
    }
