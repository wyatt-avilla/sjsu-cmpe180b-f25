from datetime import datetime

import pytest

from sjsu_cmpe180b_f25.client import Client
from sjsu_cmpe180b_f25.models import CopyStatus, LoanStatus


@pytest.mark.asyncio
async def test_get_top_books(test_client: Client) -> None:
    """Test retrieving the top borrowed books."""

    now = datetime.now(tz=None)

    await test_client.create_member(
        member_id=1,
        name="Test Member",
        email="test@email.com",
        joined_at=datetime.now(tz=None),
    )

    await test_client.create_book(book_id=1, title="Book One")
    await test_client.create_book(book_id=2, title="Book Two")
    await test_client.create_book(book_id=3, title="Book Three")

    await test_client.create_copy(copy_id=10, book_id=1, status=CopyStatus.AVAILABLE)
    await test_client.create_copy(copy_id=11, book_id=1, status=CopyStatus.AVAILABLE)
    await test_client.create_copy(copy_id=12, book_id=1, status=CopyStatus.AVAILABLE)
    await test_client.create_copy(copy_id=20, book_id=2, status=CopyStatus.AVAILABLE)
    await test_client.create_copy(copy_id=21, book_id=2, status=CopyStatus.AVAILABLE)
    await test_client.create_copy(copy_id=22, book_id=2, status=CopyStatus.AVAILABLE)
    await test_client.create_copy(copy_id=30, book_id=3, status=CopyStatus.AVAILABLE)
    await test_client.create_copy(copy_id=31, book_id=3, status=CopyStatus.AVAILABLE)
    await test_client.create_copy(copy_id=32, book_id=3, status=CopyStatus.AVAILABLE)

    await test_client.create_loan(
        loan_id=1,
        copy_id=20,
        member_id=1,
        loan_date=now,
        due_date=now,
        status=LoanStatus.ACTIVE,
    )
    await test_client.create_loan(
        loan_id=2,
        copy_id=21,
        member_id=1,
        loan_date=now,
        due_date=now,
        status=LoanStatus.ACTIVE,
    )
    await test_client.create_loan(
        loan_id=3,
        copy_id=10,
        member_id=1,
        loan_date=now,
        due_date=now,
        status=LoanStatus.ACTIVE,
    )

    results = await test_client.get_top_books(limit=2)
    assert [tuple(row) for row in results] == [
        (2, "Book Two", 2),
        (1, "Book One", 1),
    ]
