import pytest

from sjsu_cmpe180b_f25.client import Client
from sjsu_cmpe180b_f25.populate_db import populate_db


@pytest.mark.asyncio
async def test_populate_db(test_client: Client) -> None:
    """Test requesting a loan successfully."""

    await populate_db(test_client)
