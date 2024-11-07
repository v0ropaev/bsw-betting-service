import punq
from config import settings
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_async_engine(settings.database_uri_async, echo=False)
session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


Base = declarative_base()


class SessionMaker:
    def __new__(cls):
        return sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


container = punq.Container()
container.register(sessionmaker, SessionMaker)
