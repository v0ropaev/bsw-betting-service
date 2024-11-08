from contextvars import ContextVar

from db import container
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker


db_session: ContextVar[AsyncSession | None] = ContextVar("db_session", default=None)


class Transaction:
    async def __aenter__(self) -> None:
        session_maker = container.resolve(sessionmaker)
        self.session: AsyncSession = session_maker()
        self.token = db_session.set(self.session)

    async def __aexit__(self, exception_type, exception, traceback) -> None:
        if exception:
            await self.session.rollback()
        else:
            await self.session.commit()
        await self.session.close()
        db_session.reset(self.token)
