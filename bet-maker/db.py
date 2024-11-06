from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from config import Settings

engine = create_async_engine(Settings.DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)


@asynccontextmanager
async def get_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session

Base = declarative_base()
