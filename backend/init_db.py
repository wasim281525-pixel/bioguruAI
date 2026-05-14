"""
Run once to create all database tables:
    docker-compose exec backend python init_db.py
"""
import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import all models so Base knows about them
from models.user import Base, User
from models.chat import ChatSession, ChatMessage
from models.progress import NEETSession, StudentProgress, Document, RetrievalLog
from models.database import engine


async def init():
    print("Creating database tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ All tables created successfully!")
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(init())
