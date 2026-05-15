from pydantic import BaseModel
from datetime import datetime


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str
    created_at: datetime


class ChatHistoryResponse(BaseModel):
    messages: list[dict]
