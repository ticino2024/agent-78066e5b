"""Conversation schemas for API."""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel


class MessageBase(BaseModel):
    """Base message schema."""

    role: str
    content: str
    metadata: Optional[Dict[str, Any]] = None


class MessageCreate(MessageBase):
    """Message creation schema."""

    pass


class MessageResponse(MessageBase):
    """Message response schema."""

    id: int
    conversation_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class ConversationBase(BaseModel):
    """Base conversation schema."""

    title: Optional[str] = None


class ConversationCreate(ConversationBase):
    """Conversation creation schema."""

    pass


class ConversationResponse(ConversationBase):
    """Conversation response schema."""

    id: int
    user_id: int
    session_id: str
    created_at: datetime
    updated_at: datetime
    messages: List[MessageResponse] = []

    class Config:
        from_attributes = True


class ChatRequest(BaseModel):
    """Chat request schema."""

    message: str
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    """Chat response schema."""

    session_id: str
    message: str
    metadata: Optional[Dict[str, Any]] = None
