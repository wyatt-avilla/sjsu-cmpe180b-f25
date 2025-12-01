from datetime import datetime

import pytest

from sjsu_cmpe180b_f25.client import Client
from sjsu_cmpe180b_f25.models import CopyStatus, LoanStatus


@pytest.mark.asyncio
async def test_get_overdue_members(test_client: Client) -> None:
    """Test retrieving members with overdue loans."""

    now = datetime.now(tz=None)

    await test_client.create_member(
        member_id=1,
        name="Overdue Member",
        email="overdue@email.com",
        joined_at=now,
    )

    await test_client.create_member(
        member_id=2,
        name="Other Member",
        email="other@email.com",
        joined_at=now,
    )

    await test_client.create_book(book_id=1, title="Overdue Book")
    await test_client.create_book(book_id=2, title="On-time Book")
    await test_client.create_copy(copy_id=10, book_id=1, status=CopyStatus.AVAILABLE)
    await test_client.create_copy(copy_id=20, book_id=2, status=CopyStatus.AVAILABLE)

    year_back = now.replace(year=now.year - 1).year

    await test_client.create_loan(
        loan_id=1,
        copy_id=10,
        member_id=1,
        loan_date=now,
        due_date=now.replace(year_back),
        status=LoanStatus.ACTIVE,
    )

    results = await test_client.get_overdue_members()
    assert len(results) == 1
    assert [tuple(row) for row in results] == [
        (1, "Overdue Member", "overdue@email.com", 1, now.replace(year_back)),
    ]
