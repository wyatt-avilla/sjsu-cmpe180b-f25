import pytest

from sjsu_cmpe180b_f25.populate_db import populate_db


@pytest.mark.asyncio
async def test_populate_db() -> None:
    """Test requesting a loan successfully."""

    await populate_db("sqlite+aiosqlite:///:memory:")
