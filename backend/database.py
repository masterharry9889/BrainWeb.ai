import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from models import Base

from sqlalchemy.pool import NullPool
from pathlib import Path

def get_app_data_dir() -> Path:
    if os.name == 'nt':
        base_dir = os.environ.get('APPDATA', os.path.expanduser('~'))
    else:
        base_dir = os.path.expanduser('~')
    app_dir = Path(base_dir) / '.brainweb'
    app_dir.mkdir(parents=True, exist_ok=True)
    return app_dir

default_db_path = get_app_data_dir() / 'brainweb_data.db'
# Convert windows paths for sqlalchemy sqlite connection string
default_db_str = str(default_db_path).replace('\\', '/')
DATABASE_URL = os.environ.get(
    "DATABASE_URL", 
    f"sqlite+aiosqlite:///{default_db_str}"
)

engine = create_async_engine(DATABASE_URL, echo=False, poolclass=NullPool)

async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def init_db():
    async with engine.begin() as conn:
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
