from typing import AsyncGenerator

import pytest_asyncio
from sqlmodel import text

from app.kit.postgres import create_async_engine
from app.models import RecordModel


@pytest_asyncio.fixture(scope="session", loop_scope="session", autouse=True)
async def initialize_test_database() -> AsyncGenerator[None, None]:
    asyncengine = create_async_engine("app")
    async with asyncengine.begin() as cnx:
        await cnx.execute(text("DROP SCHEMA IF EXISTS public CASCADE"))
        await cnx.execute(text("CREATE SCHEMA public"))
        await cnx.run_sync(RecordModel.metadata.drop_all)
        await cnx.run_sync(RecordModel.metadata.create_all)
    yield
    await asyncengine.dispose()
