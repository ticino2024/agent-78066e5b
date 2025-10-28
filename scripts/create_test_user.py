"""Script to create a test user."""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.db.base import AsyncSessionLocal
from app.services.auth_service import AuthService
from app.schemas.user import UserCreate
from app.core.logging import setup_logging, get_logger

setup_logging()
logger = get_logger(__name__)


async def create_test_user() -> None:
    """Create a test user."""
    async with AsyncSessionLocal() as db:
        # Check if user exists
        existing = await AuthService.get_user_by_username(db, "demo")
        if existing:
            logger.info("Test user already exists!")
            return
        
        # Create user
        user_data = UserCreate(
            username="demo",
            email="demo@example.com",
            password="Demo123!"
        )
        
        user = await AuthService.create_user(db, user_data)
        logger.info(f"Created test user: {user.username} (ID: {user.id})")
        logger.info("Login credentials: username=demo, password=Demo123!")


if __name__ == "__main__":
    asyncio.run(create_test_user())
