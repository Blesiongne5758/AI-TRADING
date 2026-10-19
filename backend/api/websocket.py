"""
WebSocket for Real-time Updates
"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List
from loguru import logger
import asyncio
import json

router = APIRouter()


class ConnectionManager:
    """Manage WebSocket connections"""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        """Accept new connection"""
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"✅ WebSocket connected. Total: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket):
        """Remove connection"""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        logger.info(f"❌ WebSocket disconnected. Total: {len(self.active_connections)}")
    
    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """Send message to specific client"""
        try:
            await websocket.send_json(message)
        except Exception as e:
            logger.error(f"❌ Error sending message: {e}")
    
    async def broadcast(self, message: dict):
        """Broadcast message to all clients"""
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"❌ Error broadcasting: {e}")


manager = ConnectionManager()


@router.websocket("/updates")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time updates
    
    Sends:
    - Price updates
    - Signal updates
    - Portfolio updates
    """
    await manager.connect(websocket)
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            
            # Parse command
            try:
                command = json.loads(data)
                cmd_type = command.get("type", "")
                
                if cmd_type == "ping":
                    await manager.send_personal_message({"type": "pong"}, websocket)
                elif cmd_type == "subscribe":
                    # Subscribe to specific updates
                    await manager.send_personal_message(
                        {"type": "subscribed", "data": command.get("channels", [])},
                        websocket
                    )
            except json.JSONDecodeError:
                await manager.send_personal_message(
                    {"type": "error", "message": "Invalid JSON"},
                    websocket
                )
    
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"❌ WebSocket error: {e}")
        manager.disconnect(websocket)


async def broadcast_price_update(symbol: str, price: float, change: float):
    """Broadcast price update to all clients"""
    await manager.broadcast({
        "type": "price_update",
        "data": {
            "symbol": symbol,
            "price": price,
            "change": change,
        }
    })


async def broadcast_signal_update(signal: dict):
    """Broadcast signal update to all clients"""
    await manager.broadcast({
        "type": "signal_update",
        "data": signal
    })


async def broadcast_portfolio_update(portfolio: dict):
    """Broadcast portfolio update to all clients"""
    await manager.broadcast({
        "type": "portfolio_update",
        "data": portfolio
    })
