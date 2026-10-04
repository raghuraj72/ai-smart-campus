from typing import List, Optional, Dict, Any
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query, status
from jose import JWTError, jwt
from sqlmodel import select

from app.core.config import settings
from app.core.database import get_session, engine
from app.models.domain import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

router = APIRouter(tags=["WebSockets"])

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: Dict[str, Any]):
        for connection in list(self.active_connections):
            try:
                await connection.send_json(message)
            except Exception:
                self.disconnect(connection)

manager = ConnectionManager()

async def get_ws_user(token: Optional[str]) -> Optional[User]:
    if not token:
        print("[WS AUTH] Missing token")
        return None

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        user_id = payload.get("sub")

        if not user_id:
            print("[WS AUTH] Token missing sub claim")
            return None

        async_session = sessionmaker(
            engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

        async with async_session() as session:
            stmt = select(User).where(User.id == int(user_id))
            result = await session.execute(stmt)

            user = result.scalars().first()

            if not user:
                print(f"[WS AUTH] User ID '{user_id}' not found")

            return user

    except Exception as e:
        print(f"[WS AUTH] Error decoding token: {e}")
        return None


@router.websocket("/ws")
@router.websocket("/ws/complaints")
async def websocket_endpoint(
    websocket: WebSocket,
    token: Optional[str] = Query(None),
):
    await websocket.accept()

    user = await get_ws_user(token)

    if not user or not user.is_active:
        print("[WS] Auth rejected for token. Closing socket.")
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await manager.connect(websocket)

    print(f"[WS] Client connected: {user.email}")

    try:
        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print(f"[WS] Client disconnected: {user.email}")