import os
import pytest
import asyncio
from unittest.mock import Mock
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.backend.db_model import Base

@pytest.fixture(scope="session")
def even_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
async def test_db():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    AsyncSessionTest = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with AsyncSessionTest() as session:
        yield session

    await engine.dispose()


