import pytest

from sjsu_cmpe180b_f25.client import Client


@pytest.mark.asyncio
async def test_create_author(test_client: Client) -> None:
    """Test that an author can be created successfully."""

    author = await test_client.create_author(id=1, name="Benjamin Reichwald")

    assert author is not None


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
