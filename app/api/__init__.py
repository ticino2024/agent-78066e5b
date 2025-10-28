"""API routes package."""

from fastapi import APIRouter
from app.api import auth, chat, analytics

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(chat.router)
api_router.include_router(analytics.router)

__all__ = ["api_router"]
