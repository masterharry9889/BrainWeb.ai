import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from .models import Base

DATABASE_URL = os.environ.get(
    "DATABASE_URL", 
    "postgresql+asyncpg://ingot:password@127.0.0.1:5432/ingot_db"
)

engine = create_async_engine(DATABASE_URL, echo=False)

async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def init_db():
    async with engine.begin() as conn:
        # Create pgvector extension if it doesn't exist
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        await conn.run_sync(Base.metadata.create_all)
        
        # Safely migrate existing tables
        try:
            await conn.execute(text("ALTER TABLE nodes ADD COLUMN IF NOT EXISTS project_id VARCHAR NOT NULL DEFAULT 'default'"))
            await conn.execute(text("CREATE INDEX IF NOT EXISTS ix_nodes_project_id ON nodes (project_id)"))
            
            await conn.execute(text("ALTER TABLE edges ADD COLUMN IF NOT EXISTS project_id VARCHAR NOT NULL DEFAULT 'default'"))
            await conn.execute(text("CREATE INDEX IF NOT EXISTS ix_edges_project_id ON edges (project_id)"))
        except Exception as e:
            # Column might already exist, safe to ignore
            pass

async def get_db():
    async with async_session() as session:
        yield session
