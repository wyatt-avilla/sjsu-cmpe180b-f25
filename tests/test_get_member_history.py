from datetime import datetime, timedelta

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

    ten_before = now - timedelta(days=10)
    fifteen_before = now - timedelta(days=15)
    twenty_before = now - timedelta(days=20)

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
        loan_date=ten_before,
        due_date=now,
        status=LoanStatus.RETURNED,
        return_date=now,
    )

    await test_client.create_loan(
        loan_id=2,
        copy_id=20,
        member_id=1,
        loan_date=twenty_before,
        due_date=now,
        status=LoanStatus.RETURNED,
        return_date=now,
    )

    await test_client.create_loan(
        loan_id=3,
        copy_id=30,
        member_id=1,
        loan_date=fifteen_before,
        due_date=now,
        status=LoanStatus.RETURNED,
        return_date=now,
    )

    res = await test_client.get_member_history(member_id=1)

    assert [tuple(row) for row in res] == [
        (1, 10, ten_before, now, LoanStatus.RETURNED),
        (3, 30, fifteen_before, now, LoanStatus.RETURNED),
        (2, 20, twenty_before, now, LoanStatus.RETURNED),
    ]
