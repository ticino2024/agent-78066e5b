"""Chat API routes for AI agent interaction."""

from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.schemas.conversation import ChatRequest, ChatResponse, ConversationResponse
from app.services.conversation_service import ConversationService
from app.schemas.conversation import ConversationCreate, MessageCreate
from app.agents.social_media_agent import agent_manager
from app.core.security import get_current_user
from app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/message", response_model=ChatResponse)
async def send_message(
    request: ChatRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ChatResponse:
    """Send a message to the AI agent and get a response."""
    try:
        user_id = int(current_user["user_id"])
        
        # Get or create conversation
        if request.session_id:
            conversation = await ConversationService.get_conversation_by_session_id(
                db, request.session_id
            )
            if not conversation or conversation.user_id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Conversation not found",
                )
        else:
            # Create new conversation
            conversation = await ConversationService.create_conversation(
                db, user_id, ConversationCreate(title="New Chat")
            )
        
        # Save user message
        await ConversationService.add_message(
            db,
            conversation.id,
            MessageCreate(role="user", content=request.message),
        )
        
        # Get or create agent
        agent = agent_manager.get_or_create_agent(conversation.session_id, user_id)
        
        # Process message with agent
        response = await agent.process_message(request.message)
        
        # Save assistant message
        await ConversationService.add_message(
            db,
            conversation.id,
            MessageCreate(
                role="assistant",
                content=response["message"],
                metadata=response.get("metadata"),
            ),
        )
        
        return ChatResponse(
            session_id=conversation.session_id,
            message=response["message"],
            metadata=response.get("metadata"),
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing chat message: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing message",
        )


@router.get("/conversations", response_model=list[ConversationResponse])
async def get_conversations(
    skip: int = 0,
    limit: int = 100,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[ConversationResponse]:
    """Get all conversations for the current user."""
    user_id = int(current_user["user_id"])
    conversations = await ConversationService.get_user_conversations(db, user_id, skip, limit)
    return conversations


@router.get("/conversations/{session_id}", response_model=ConversationResponse)
async def get_conversation(
    session_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ConversationResponse:
    """Get a specific conversation by session ID."""
    user_id = int(current_user["user_id"])
    conversation = await ConversationService.get_conversation_by_session_id(db, session_id)
    
    if not conversation or conversation.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )
    
    return conversation


@router.delete("/conversations/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_conversation(
    session_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    """Delete a conversation."""
    user_id = int(current_user["user_id"])
    conversation = await ConversationService.get_conversation_by_session_id(db, session_id)
    
    if not conversation or conversation.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )
    
    await ConversationService.delete_conversation(db, conversation.id)
    
    # Remove agent from memory
    agent_manager.remove_agent(session_id)
