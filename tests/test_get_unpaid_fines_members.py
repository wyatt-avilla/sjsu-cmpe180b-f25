from datetime import datetime

import pytest

from sjsu_cmpe180b_f25.client import Client
from sjsu_cmpe180b_f25.models import CopyStatus, LoanStatus


@pytest.mark.asyncio
async def test_get_unpaid_fines_members(test_client: Client) -> None:
    """Test retrieving members with unpaid fines."""

    now = datetime.now(tz=None)

    await test_client.create_member(
        member_id=1,
        name="Fine Member",
        email="member1@email.com",
        joined_at=now,
    )

    await test_client.create_member(
        member_id=2,
        name="No Fine Member",
        email="member2@email.com",
        joined_at=now,
    )

    await test_client.create_book(book_id=1, title="Fined Book")
    await test_client.create_copy(copy_id=10, book_id=1, status=CopyStatus.AVAILABLE)

    loan = await test_client.create_loan(
        loan_id=1,
        copy_id=10,
        member_id=1,
        loan_date=now,
        due_date=now,
        status=LoanStatus.ACTIVE,
    )

    assert loan is not None

    await test_client.create_fine(
        fine_id=1,
        member_id=1,
        loan_id=loan.loan_id,
        amount=15.00,
        assessed_at=now,
        paid=False,
    )

    results = await test_client.get_unpaid_fines_members()
    assert len(results) == 1
    assert [tuple(row) for row in results] == [
        (1, "Fine Member", "member1@email.com", 15.00, 1),
    ]
