from typing import AsyncGenerator, AsyncIterator

import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from app.kit.postgres import AsyncSession, create_async_engine, get_async_db_session
from app.main import app as _app

TEST_BASE_URL = "http://testserver:8001"


@pytest_asyncio.fixture
async def session() -> AsyncIterator[AsyncSession]:
    engine = create_async_engine(process_name="app")
    connection = await engine.connect()
    transaction = await connection.begin()
    session = AsyncSession(bind=connection, expire_on_commit=False)
    yield session
    await transaction.rollback()
    await connection.close()
    await engine.dispose()


@pytest_asyncio.fixture
async def app(session: AsyncSession) -> AsyncGenerator[FastAPI, None]:
    _app.dependency_overrides[get_async_db_session] = lambda: session
    yield _app
    _app.dependency_overrides.pop(get_async_db_session)


@pytest_asyncio.fixture
async def client(app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    # async with LifespanManager(app) as manager:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url=TEST_BASE_URL
    ) as client:
        yield client
