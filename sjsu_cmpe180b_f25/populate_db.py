from datetime import datetime

from .client import Client
from .models import CopyStatus, LoanStatus


async def populate_db(database_url: str) -> None:
    client = Client(database_url)

    # Create tables
    await client.create_tables()

    # Create authors
    await client.create_author(id=1, name="George Orwell")

    # Create books
    await client.create_book(
        book_id=1,
        title="1984",
        isbn="9780451524935",
        published_year=1949,
        genre="Dystopian",
    )

    # Create book-author relationships
    await client.create_book_author(book_id=1, author_id=1)

    # Create members
    await client.create_member(
        member_id=1,
        name="Alice Smith",
        email="alice@gmail.com",
        joined_at=datetime(2023, 1, 15, 10, 0, 0),
    )

    # Create copies
    await client.create_copy(copy_id=1, book_id=1, status=CopyStatus.AVAILABLE)

    # Create loans
    await client.create_loan(
        loan_id=1,
        copy_id=1,
        member_id=1,
        loan_date=datetime(2023, 2, 1, 9, 0, 0),
        due_date=datetime(2023, 2, 15, 9, 0, 0),
        return_date=None,
        status=LoanStatus.ACTIVE,
    )

    # Create fines
    await client.create_fine(
        fine_id=1,
        member_id=1,
        loan_id=1,
        amount=5.0,
        assessed_at=datetime(2023, 2, 16, 12, 0, 0),
    )
