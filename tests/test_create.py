import pytest

from sjsu_cmpe180b_f25.client import Client


@pytest.mark.asyncio
async def test_create_author(test_client: Client) -> None:
    """Test that an active loan can be ended successfully."""

    author = await test_client.create_author(id=1, name="Benjamin Reichwald")

    assert author is not None
