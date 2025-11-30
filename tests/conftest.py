from collections.abc import AsyncGenerator

import pytest_asyncio

from sjsu_cmpe180b_f25.client import Client


@pytest_asyncio.fixture
async def test_client() -> AsyncGenerator[Client]:
    """Create a client with an in-memory SQLite database for testing."""
    database_url = "sqlite+aiosqlite:///:memory:"
    client = Client(database_url)
    await client.create_tables()
    yield client
