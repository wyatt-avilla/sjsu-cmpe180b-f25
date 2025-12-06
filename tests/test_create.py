import asyncio
from datetime import datetime

import pytest

from sjsu_cmpe180b_f25.client import Client
from sjsu_cmpe180b_f25.models import CopyStatus, LoanStatus, Member


@pytest.mark.asyncio
async def test_create_author(test_client: Client) -> None:
    """Test that an author can be created successfully."""

    author = await test_client.create_author(id=1, name="Benjamin Reichwald")

    assert author is not None
    assert author.author_id == 1
    assert author.name == "Benjamin Reichwald"


@pytest.mark.asyncio
async def test_create_author_duplicate_id(test_client: Client) -> None:
    """Test that creating an author with a duplicate ID fails."""

    author1 = await test_client.create_author(id=1, name="Benjamin Reichwald")
    author2 = await test_client.create_author(id=1, name="Zak Arogundade")

    assert author1 is not None
    assert author2 is None


@pytest.mark.asyncio
async def test_create_book(test_client: Client) -> None:
    """Test that a book can be created successfully."""

    book = await test_client.create_book(
        book_id=1,
        title="Introduction to Software Engineering",
        isbn="978-3-16-148410-0",
        published_year=2024,
        genre="Education",
    )

    assert book is not None
    assert book.book_id == 1
    assert book.title == "Introduction to Software Engineering"
    assert book.isbn == "978-3-16-148410-0"
    assert book.published_year == 2024
    assert book.genre == "Education"


@pytest.mark.asyncio
async def test_create_book_author(test_client: Client) -> None:
    """Test that a book with an author can be created successfully."""

    author = await test_client.create_author(id=1, name="Benjamin Reichwald")
    assert author is not None

    book = await test_client.create_book(
        book_id=1,
        title="Introduction to Software Engineering",
        isbn="978-3-16-148410-0",
        published_year=2024,
        genre="Education",
    )
    assert book is not None

    book_author = await test_client.create_book_author(book_id=1, author_id=1)

    assert book_author is not None

    assert book_author.book_id == book.book_id
    assert book_author.author_id == author.author_id


@pytest.mark.asyncio
async def test_create_member(test_client: Client) -> None:
    """Test that a member can be created successfully."""

    member = await test_client.create_member(
        member_id=1,
        name="Tatiana Schwaninger",
        email="tati@nbb.com",
        joined_at=datetime.now(tz=None),
    )

    assert member is not None
    assert member.member_id == 1
    assert member.name == "Tatiana Schwaninger"
    assert member.email == "tati@nbb.com"


@pytest.mark.asyncio
async def test_create_copy(test_client: Client) -> None:
    """Test that a copy can be created successfully."""

    await test_client.create_book(book_id=1, title="Test Book")

    copy = await test_client.create_copy(
        copy_id=1,
        book_id=1,
        status=CopyStatus.AVAILABLE,
    )

    assert copy is not None
    assert copy.copy_id == 1
    assert copy.book_id == 1
    assert copy.status == CopyStatus.AVAILABLE


@pytest.mark.asyncio
async def test_create_loan(test_client: Client) -> None:
    """Test that a loan can be created successfully."""

    await test_client.create_book(book_id=1, title="Test Book")
    await test_client.create_copy(copy_id=1, book_id=1, status=CopyStatus.AVAILABLE)
    await test_client.create_member(
        member_id=1,
        name="Graham Perez",
        email="graham@nbb.com",
        joined_at=datetime.now(tz=None),
    )

    now = datetime.now(tz=None)

    loan = await test_client.create_loan(
        loan_id=1,
        copy_id=1,
        member_id=1,
        loan_date=now,
        due_date=now,
        return_date=None,
        status=LoanStatus.ACTIVE,
    )

    assert loan is not None
    assert loan.loan_id == 1
    assert loan.copy_id == 1
    assert loan.member_id == 1
    assert loan.loan_date == now
    assert loan.due_date == now
    assert loan.return_date is None
    assert loan.status == LoanStatus.ACTIVE


@pytest.mark.asyncio
async def test_create_fine(test_client: Client) -> None:
    """Test that a fine can be created successfully."""

    now = datetime.now(tz=None)

    member = await test_client.create_member(
        member_id=1,
        name="Test Name",
        email="test@email.com",
        joined_at=now,
    )
    assert member is not None

    copy = await test_client.create_copy(
        copy_id=1,
        book_id=1,
        status=CopyStatus.AVAILABLE,
    )
    assert copy is not None

    loan = await test_client.create_loan(
        loan_id=1,
        copy_id=1,
        member_id=1,
        loan_date=now,
        due_date=now,
        return_date=None,
        status=LoanStatus.ACTIVE,
    )
    assert loan is not None

    fine = await test_client.create_fine(
        fine_id=1,
        member_id=1,
        loan_id=1,
        amount=10.0,
        assessed_at=now,
        paid=False,
        paid_at=None,
    )
    assert fine is not None

    assert fine.fine_id == 1
    assert fine.member_id == 1
    assert fine.loan_id == 1
    assert fine.amount == 10.0
    assert fine.assessed_at == now
    assert fine.paid is False
    assert fine.paid_at is None


@pytest.mark.asyncio
async def test_concurrent_create_member(test_client: Client) -> None:
    """Test only a single attempt to create a member with the same ID succeeds."""

    async def create_member_attempt() -> None | Member:
        return await test_client.create_member(
            member_id=1,
            name="Concurrent User",
            email="email@gmail.com",
            joined_at=datetime.now(tz=None),
        )

    tasks = [create_member_attempt() for _ in range(5)]

    results = await asyncio.gather(*tasks, return_exceptions=True)
    assert len([res for res in results if res is not None]) == 1


@pytest.mark.asyncio
async def test_concurrent_create_book(test_client: Client) -> None:
    """Test only a single attempt to create a book with the same ID succeeds."""

    async def create_book_attempt() -> None | object:
        return await test_client.create_book(
            book_id=1,
            title="Concurrent Book",
            isbn="123-4-56-789012-3",
            published_year=2024,
            genre="Fiction",
        )

    tasks = [create_book_attempt() for _ in range(5)]

    results = await asyncio.gather(*tasks, return_exceptions=True)
    assert len([res for res in results if res is not None]) == 1
