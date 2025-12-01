from datetime import datetime

import pytest

from sjsu_cmpe180b_f25.client import Client
from sjsu_cmpe180b_f25.models import CopyStatus


@pytest.mark.asyncio
async def test_get_copies_on_loan(test_client: Client) -> None:
    """Test retrieving copies currently on loan."""

    now = datetime.now(tz=None)

    await test_client.create_member(
        member_id=1,
        name="Loan Member",
        email="member@email.com",
        joined_at=now,
    )

    await test_client.create_book(book_id=1, title="Loaned Book")
    await test_client.create_book(book_id=2, title="Partially Loaned Book")
    await test_client.create_book(book_id=3, title="Available Book")

    await test_client.create_copy(copy_id=10, book_id=1, status=CopyStatus.ON_LOAN)
    await test_client.create_copy(copy_id=11, book_id=1, status=CopyStatus.ON_LOAN)
    await test_client.create_copy(copy_id=12, book_id=1, status=CopyStatus.ON_LOAN)

    await test_client.create_copy(copy_id=20, book_id=2, status=CopyStatus.ON_LOAN)
    await test_client.create_copy(copy_id=21, book_id=2, status=CopyStatus.ON_LOAN)
    await test_client.create_copy(copy_id=22, book_id=2, status=CopyStatus.AVAILABLE)
    await test_client.create_copy(copy_id=23, book_id=2, status=CopyStatus.AVAILABLE)

    await test_client.create_copy(copy_id=30, book_id=3, status=CopyStatus.AVAILABLE)
    await test_client.create_copy(copy_id=31, book_id=3, status=CopyStatus.AVAILABLE)
    await test_client.create_copy(copy_id=32, book_id=3, status=CopyStatus.AVAILABLE)

    result = await test_client.get_copies_on_loan(limit=2)
    assert len(result) == 2
    assert result == [
        (1, "Loaned Book", 3, 3, 100.0),
        (2, "Partially Loaned Book", 4, 2, 50.0),
    ]
