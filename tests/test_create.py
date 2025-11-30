import pytest

from sjsu_cmpe180b_f25.client import Client


@pytest.mark.asyncio
async def test_create_author(test_client: Client) -> None:
    """Test that an active loan can be ended successfully."""

    author = await test_client.create_author(id=1, name="Benjamin Reichwald")

    assert author is not None


@pytest.mark.asyncio
async def test_create_author_duplicate_id(test_client: Client) -> None:
    """Test that creating an author with a duplicate ID fails."""

    author1 = await test_client.create_author(id=1, name="Benjamin Reichwald")
    author2 = await test_client.create_author(id=1, name="Zak Arogundade")

    assert author1 is not None
    assert author2 is None
