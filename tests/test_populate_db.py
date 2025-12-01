import pytest

from sjsu_cmpe180b_f25.client import Client
from sjsu_cmpe180b_f25.population import populate_db


@pytest.mark.asyncio
async def test_populate_db(test_client: Client) -> None:
    """Test requesting a loan successfully."""

    await populate_db(
        test_client,
        num_authors=10,
        num_books=10,
        num_members=10,
        copies_per_book=2,
        num_loans=10,
    )
