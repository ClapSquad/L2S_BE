from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config.environments import SUPABASE_DB_URL

ASYNC_DB_URL = SUPABASE_DB_URL.replace("postgresql+psycopg2", "postgresql+asyncpg")

engine = create_async_engine(
    ASYNC_DB_URL,
    pool_pre_ping=True,
    pool_size=15,
    max_overflow=15,
    connect_args={
        "statement_cache_size": 0,
        "prepared_statement_cache_size": 0,
    }
)

AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()