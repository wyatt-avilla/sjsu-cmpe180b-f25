from datetime import UTC, datetime

import pytest

from sjsu_cmpe180b_f25.client import Client
from sjsu_cmpe180b_f25.models import CopyStatus, LoanStatus


@pytest.mark.asyncio
async def test_request_loan_success(test_client: Client) -> None:
    """Test requesting a loan successfully."""

    await test_client.create_book(book_id=1, title="Test Book")
    await test_client.create_copy(copy_id=1, book_id=1, status=CopyStatus.AVAILABLE)
    await test_client.create_member(
        member_id=1,
        name="John Doe",
        email="johndoe@gmail.com",
        joined_at=datetime.now(tz=None),
    )

    loan = await test_client.request_loan(copy_id=1, member_id=1)

    assert loan is not None
    assert loan.copy_id == 1
    assert loan.member_id == 1
    assert loan.status == LoanStatus.ACTIVE


@pytest.mark.asyncio
async def test_request_loan_unavailable_copy(test_client: Client) -> None:
    """Test that a loan cannot be requested for a copy that's already on loan."""

    await test_client.create_book(book_id=1, title="Test Book")
    await test_client.create_copy(copy_id=1, book_id=1, status=CopyStatus.ON_LOAN)
    await test_client.create_member(
        member_id=1,
        name="Test Member",
        email="test@example.com",
        joined_at=datetime.now(tz=UTC),
    )

    loan = await test_client.request_loan(copy_id=1, member_id=1)

    assert loan is None
