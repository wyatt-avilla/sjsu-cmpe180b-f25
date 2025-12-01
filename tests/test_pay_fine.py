from datetime import datetime

import pytest

from sjsu_cmpe180b_f25.client import Client
from sjsu_cmpe180b_f25.models import CopyStatus


@pytest.mark.asyncio
async def test_pay_fine_success(test_client: Client) -> None:
    """Test that an unpaid fine can be paid."""

    now = datetime.now(tz=None)

    await test_client.create_member(
        member_id=1,
        name="Test Member",
        email="test@example. com",
        joined_at=now,
    )
    await test_client.create_book(book_id=1, title="Test Book")
    await test_client.create_copy(copy_id=1, book_id=1, status=CopyStatus.AVAILABLE)
    loan = await test_client.request_loan(copy_id=1, member_id=1)

    assert loan is not None

    await test_client.create_fine(
        fine_id=1,
        member_id=1,
        loan_id=loan.loan_id,
        amount=5.00,
        assessed_at=now,
        paid=False,
    )

    result = await test_client.pay_fine(fine_id=1)

    assert result is True


@pytest.mark.asyncio
async def test_pay_fine_already_paid(test_client: Client) -> None:
    """Test that an already paid fine cannot be paid again."""

    now = datetime.now(tz=None)

    await test_client.create_member(
        member_id=1,
        name="Test Member",
        email="test@example.com",
        joined_at=now,
    )
    await test_client.create_book(book_id=1, title="Test Book")
    await test_client.create_copy(copy_id=1, book_id=1, status=CopyStatus.AVAILABLE)
    loan = await test_client.request_loan(copy_id=1, member_id=1)

    assert loan is not None

    await test_client.create_fine(
        fine_id=1,
        member_id=1,
        loan_id=loan.loan_id,
        amount=5.00,
        assessed_at=now,
        paid=True,
    )

    result = await test_client.pay_fine(fine_id=1)

    assert result is False
