"""Database initialization script."""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.db.base import engine, Base
from app.models import User, Conversation, Message, SocialMediaPost, EngagementMetric
from app.core.logging import setup_logging, get_logger

setup_logging()
logger = get_logger(__name__)


async def init_db() -> None:
    """Initialize database tables."""
    logger.info("Initializing database...")
    
    async with engine.begin() as conn:
        # Drop all tables (use with caution!)
        # await conn.run_sync(Base.metadata.drop_all)
        
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)
    
    logger.info("Database initialized successfully!")


if __name__ == "__main__":
    asyncio.run(init_db())
