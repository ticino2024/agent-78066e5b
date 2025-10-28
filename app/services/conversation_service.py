"""Conversation service."""

from typing import List, Optional
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.conversation import Conversation, Message
from app.schemas.conversation import ConversationCreate, MessageCreate
from app.core.logging import get_logger

logger = get_logger(__name__)


class ConversationService:
    """Conversation service."""

    @staticmethod
    async def create_conversation(
        db: AsyncSession, user_id: int, conversation_data: ConversationCreate
    ) -> Conversation:
        """Create a new conversation."""
        session_id = str(uuid.uuid4())
        conversation = Conversation(
            user_id=user_id,
            session_id=session_id,
            title=conversation_data.title,
        )
        db.add(conversation)
        await db.commit()
        await db.refresh(conversation)
        logger.info(f"Created new conversation: {session_id}")
        return conversation

    @staticmethod
    async def get_conversation_by_session_id(
        db: AsyncSession, session_id: str
    ) -> Optional[Conversation]:
        """Get conversation by session ID."""
        result = await db.execute(
            select(Conversation)
            .options(selectinload(Conversation.messages))
            .where(Conversation.session_id == session_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_conversations(
        db: AsyncSession, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Conversation]:
        """Get all conversations for a user."""
        result = await db.execute(
            select(Conversation)
            .where(Conversation.user_id == user_id)
            .order_by(Conversation.updated_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    @staticmethod
    async def add_message(
        db: AsyncSession, conversation_id: int, message_data: MessageCreate
    ) -> Message:
        """Add a message to a conversation."""
        message = Message(
            conversation_id=conversation_id,
            role=message_data.role,
            content=message_data.content,
            metadata=message_data.metadata,
        )
        db.add(message)
        await db.commit()
        await db.refresh(message)
        return message

    @staticmethod
    async def delete_conversation(db: AsyncSession, conversation_id: int) -> bool:
        """Delete a conversation."""
        result = await db.execute(
            select(Conversation).where(Conversation.id == conversation_id)
        )
        conversation = result.scalar_one_or_none()
        if conversation:
            await db.delete(conversation)
            await db.commit()
            logger.info(f"Deleted conversation: {conversation_id}")
            return True
        return False
