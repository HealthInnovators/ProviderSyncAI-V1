"""Database connection and session management."""
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager
from typing import AsyncGenerator
import os
from ..settings import settings


class Database:
    """Database connection manager."""
    
    def __init__(self):
        # Use SQLite for simplicity, can be switched to PostgreSQL
        db_url = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./providersync.db")
        if db_url.startswith("sqlite"):
            # Ensure async SQLite support
            self.engine = create_async_engine(
                db_url,
                echo=False,
                connect_args={"check_same_thread": False} if "aiosqlite" in db_url else {},
            )
        else:
            self.engine = create_async_engine(db_url, echo=False)
        
        self.async_session = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
    
    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Get database session."""
        async with self.async_session() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()
    
    async def init_db(self):
        """Initialize database tables."""
        from .models import Base
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)


# Global database instance
_db = Database()


def get_db() -> Database:
    """Get database instance."""
    return _db


async def init_db():
    """Initialize database."""
    await _db.init_db()

