from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from app.database import get_db
from app.schemas.chat import ChatRequest, ChatResponse, ChatHistoryResponse
from app.models.chat import ChatMessage
from app.services.chat_service import process_chat_message
from app.services.default_user import get_default_user

router = APIRouter(prefix="/api/chat", tags=["Chatbot"])


@router.post("", response_model=ChatResponse)
async def chat(
    body: ChatRequest,
    db: AsyncSession = Depends(get_db),
):
    user = await get_default_user(db)
    reply, _ = await process_chat_message(db, user.id, body.message)
    return ChatResponse(reply=reply, created_at=datetime.utcnow())


@router.get("/history", response_model=ChatHistoryResponse)
async def get_chat_history(
    db: AsyncSession = Depends(get_db),
):
    user = await get_default_user(db)
    result = await db.execute(
        select(ChatMessage)
        .where(ChatMessage.user_id == user.id)
        .order_by(ChatMessage.created_at.asc())
    )
    messages = [
        {"role": m.role, "content": m.content, "created_at": m.created_at.isoformat()}
        for m in result.scalars().all()
    ]
    return ChatHistoryResponse(messages=messages)
