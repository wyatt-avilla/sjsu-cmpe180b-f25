from datetime import datetime

import pytest

from sjsu_cmpe180b_f25.client import Client
from sjsu_cmpe180b_f25.models import CopyStatus, LoanStatus


@pytest.mark.asyncio
async def test_get_genre_fine_stats(test_client: Client) -> None:
    """Test retrieving genre fine statistics."""

    await test_client.create_book(book_id=1, title="Book One", genre="Fiction")
    await test_client.create_book(book_id=2, title="Book Two", genre="Non-Fiction")
    await test_client.create_book(book_id=3, title="Book Three", genre="Fiction")

    await test_client.create_copy(copy_id=10, book_id=1, status=CopyStatus.AVAILABLE)
    await test_client.create_copy(copy_id=20, book_id=2, status=CopyStatus.AVAILABLE)
    await test_client.create_copy(copy_id=30, book_id=3, status=CopyStatus.AVAILABLE)

    now = datetime.now(tz=None)

    await test_client.create_member(
        member_id=1,
        name="Member One",
        email="member1@email.com",
        joined_at=now,
    )

    await test_client.create_loan(
        loan_id=1,
        copy_id=10,
        member_id=1,
        loan_date=now,
        due_date=now,
        status=LoanStatus.RETURNED,
        return_date=now,
    )

    await test_client.create_loan(
        loan_id=2,
        copy_id=20,
        member_id=1,
        loan_date=now,
        due_date=now,
        status=LoanStatus.RETURNED,
        return_date=now,
    )

    await test_client.create_loan(
        loan_id=3,
        copy_id=30,
        member_id=1,
        loan_date=now,
        due_date=now,
        status=LoanStatus.RETURNED,
        return_date=now,
    )

    await test_client.create_fine(
        fine_id=1,
        member_id=1,
        loan_id=1,
        amount=10.00,
        assessed_at=now,
        paid=True,
    )

    await test_client.create_fine(
        fine_id=2,
        member_id=1,
        loan_id=2,
        amount=5.00,
        assessed_at=now,
        paid=False,
    )

    await test_client.create_fine(
        fine_id=3,
        member_id=1,
        loan_id=3,
        amount=15.00,
        assessed_at=now,
        paid=True,
    )

    result = await test_client.get_genre_fine_statistics()
    assert [tuple(row) for row in result] == [
        ("Fiction", 2, 25.0),
        ("Non-Fiction", 1, 5.0),
    ]
