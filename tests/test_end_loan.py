import asyncio
from datetime import datetime

import pytest

from sjsu_cmpe180b_f25.client import Client
from sjsu_cmpe180b_f25.models import CopyStatus


@pytest.mark.asyncio
async def test_end_loan_success(test_client: Client) -> None:
    """Test that an active loan can be ended successfully."""

    await test_client.create_book(book_id=1, title="Test Book")
    await test_client.create_copy(copy_id=1, book_id=1, status=CopyStatus.AVAILABLE)
    await test_client.create_member(
        member_id=1,
        name="Test Member",
        email="test@example.com",
        joined_at=datetime.now(tz=None),
    )
    loan = await test_client.request_loan(copy_id=1, member_id=1)

    assert loan is not None

    result = await test_client.end_loan(loan_id=loan.loan_id)

    assert result is True


@pytest.mark.asyncio
async def test_concurrent_end_loan(test_client: Client) -> None:
    """Test that ending a loan concurrently is handled properly."""

    await test_client.create_book(book_id=1, title="Test Book")
    await test_client.create_copy(copy_id=1, book_id=1, status=CopyStatus.AVAILABLE)
    await test_client.create_member(
        member_id=1,
        name="Concurrent Member",
        email="member@member.member",
        joined_at=datetime.now(tz=None),
    )
    loan = await test_client.request_loan(copy_id=1, member_id=1)
    assert loan is not None

    tasks = [test_client.end_loan(loan_id=loan.loan_id) for _ in range(5)]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    assert len([res for res in results if res is True]) == 1
