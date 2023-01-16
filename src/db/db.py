from typing import AsyncIterator

from sqlalchemy.ext.asyncio import (AsyncSession,  # type: ignore
                                    create_async_engine)
from sqlalchemy.orm import sessionmaker

from config.config import settings

engine = create_async_engine(settings.DB_URL, echo=True, future=True)
async_session = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def get_session() -> AsyncIterator[AsyncSession]:
    async with async_session() as session:
        yield session
