import uuid

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.database.db import Base
from app.database.db_depends import get_db
from app.main import app

TEST_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"


@pytest.fixture
async def test_engine():
    engine = create_async_engine(TEST_DATABASE_URL, future=True, echo=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    await engine.dispose()


@pytest.fixture
async def TestSessionLocal(test_engine):
    return sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture
async def override_get_db(TestSessionLocal):
    async def _override():
        async with TestSessionLocal() as session:
            yield session

    app.dependency_overrides[get_db] = _override
    yield
    app.dependency_overrides.clear()


@pytest.fixture
async def client(override_get_db):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def user_id():
    """Возвращает один и тот же user_id для всех тестов."""
    return str(uuid.uuid4())
