from db.db import create_sessionmaker
from models import Base, HistoryModel, UrlModel

import asyncio
from asyncio import AbstractEventLoop
from dataclasses import dataclass
from functools import cached_property
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from sqlalchemy import text
from sqlalchemy.engine import URL, make_url
from sqlalchemy.ext.asyncio import (AsyncConnection, AsyncEngine, AsyncTransaction,
                                    create_async_engine)
from sqlalchemy.orm import DeclarativeMeta

from config.config import settings


@dataclass
class DBUtils:
    url: str

    @cached_property
    def postgres_engine(self) -> AsyncEngine:
        url_params = self._parsed_url._asdict()
        url_params['database'] = 'postgres'
        url_with_postgres_db = URL.create(**url_params)
        return create_async_engine(url_with_postgres_db, isolation_level='AUTOCOMMIT')

    @cached_property
    def db_engine(self) -> AsyncEngine:
        return create_async_engine(self.url, isolation_level='AUTOCOMMIT')

    async def create_database(self) -> None:
        query = text(f'CREATE DATABASE {self._parsed_url.database} ENCODING "utf8";')
        async with self.postgres_engine.connect() as conn:
            await conn.execute(query)

    async def create_extensions(self) -> None:
        query = text('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
        async with self.db_engine.begin() as conn:
            await conn.execute(query)

    async def create_tables(self, base: DeclarativeMeta) -> None:
        async with self.db_engine.begin() as conn:
            await conn.run_sync(base.metadata.create_all)

    async def drop_database(self) -> None:
        query = text(f'DROP DATABASE {self._parsed_url.database}')
        async with self.postgres_engine.begin() as conn:
            await conn.execute(query)

    async def database_exists(self) -> bool:
        query = text('SELECT 1 FROM pg_database WHERE datname = :database')
        async with self.postgres_engine.connect() as conn:
            query_result = await conn.execute(query, {'database': self._parsed_url.database})
        result = query_result.scalar()
        return bool(result)

    @cached_property
    def _parsed_url(self) -> URL:
        return make_url(self.url)


def create_engine_test() -> AsyncEngine:
    db_utils = DBUtils(url=settings.TEST_DB_URL)

    return db_utils.db_engine


async_session_test = create_sessionmaker(create_engine_test())


async def override_get_db_session():
    try:
        db = async_session_test()
        yield db
    finally:
        db.close()


async def create_db(url: str, base: DeclarativeMeta) -> None:
    db_utils = DBUtils(url=url)

    try:
        if await db_utils.database_exists():
            await db_utils.drop_database()

        await db_utils.create_database()
        await db_utils.create_extensions()
        await db_utils.create_tables(base)
    finally:
        await db_utils.postgres_engine.dispose()
        await db_utils.db_engine.dispose()


async def drop_db(url: str, base: DeclarativeMeta) -> None:
    db_utils = DBUtils(url=url)

    await db_utils.drop_database()


@pytest.fixture(scope='session')
def event_loop() -> Generator[AbstractEventLoop, None, None]:
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


# @pytest.fixture(scope='session')
# def event_loop():
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()


@pytest_asyncio.fixture(scope='session', autouse=True)
async def _create_db() -> None:
    yield await create_db(url=settings.TEST_DB_URL, base=Base)
    await drop_db(url=settings.TEST_DB_URL, base=Base)


@pytest_asyncio.fixture()
async def engine_test() -> AsyncGenerator[AsyncEngine, None]:
    engine = create_engine_test()
    try:
        yield engine
    finally:
        await engine.dispose()


@pytest_asyncio.fixture()
async def db_test_connection(engine_test: AsyncEngine) -> AsyncGenerator[AsyncConnection, None]:
    async with engine_test.connect() as test_connection:
        yield test_connection


@pytest_asyncio.fixture(autouse=True)
async def db_transaction(
        db_test_connection: AsyncConnection
) -> AsyncGenerator[AsyncTransaction, None]:
    """
    Recipe for using transaction rollback in tests
    https://docs.sqlalchemy.org/en/14/orm/session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites  # noqa
    """
    async with db_test_connection.begin() as transaction:
        yield transaction
        await transaction.rollback()


@pytest_asyncio.fixture()
async def url_items() -> AsyncGenerator[UrlModel, None]:
    async with async_session_test() as session, session.begin():
        url1 = UrlModel(
            url='http://httpbin.org/uuid',
            is_delete=False,
        )
        url2 = UrlModel(
            url='https://www.google.ru/',
            is_delete=True,
        )
        session.add_all([url1, url2])
    yield [url1, url2]


@pytest_asyncio.fixture()
async def history_items(url_items) -> AsyncGenerator[HistoryModel, None]:
    url_obj, deleted_url_obj = url_items
    async with async_session_test() as session, session.begin():
        history = HistoryModel(
            url_id=url_obj.id,
            method='GET',
            domen='',
        )
        session.add(history)
    yield history
