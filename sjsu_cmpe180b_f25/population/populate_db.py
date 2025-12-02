import logging
import random
from datetime import datetime, timedelta

from sjsu_cmpe180b_f25.client import Client
from sjsu_cmpe180b_f25.models import CopyStatus, LoanStatus

from .data import book_title_parts, first_names, genres, last_names


async def populate_db(
    client: Client,
    *,
    num_authors: int = 1000,
    num_books: int = 1000,
    num_members: int = 1000,
    copies_per_book: int = 3,
    num_loans: int = 1000,
    fine_probability: float = 0.2,
) -> None:
    """
    Generates synthetic library data.

    Args:
        client: Database client with create methods
        num_authors: Number of authors to create
        num_books: Number of books to create
        num_members: Number of library members to create
        copies_per_book: Average number of copies per book
        num_loans: Number of loan records to create
        fine_probability: Probability that an overdue loan has a fine (0.0 to 1.0)
    """

    await client.create_tables()
    logger = logging.getLogger(__name__)

    logger.info("Creating authors...")
    author_ids = []
    for i in range(1, num_authors + 1):
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        author = await client.create_author(id=i, name=name)
        if author:
            author_ids.append(i)
    logger.info(f"Created {len(author_ids)} authors")

    logger.info("Creating books...")
    book_ids = []
    for i in range(1, num_books + 1):
        title = " ".join(random.choice(part) for part in book_title_parts)
        isbn = f"{random.randint(100, 999)}-{random.randint(1, 9)}-{random.randint(10, 99)}-{random.randint(100000, 999999)}-{random.randint(0, 9)}"
        year = random.randint(1950, 2024)
        genre = random.choice(genres)

        book = await client.create_book(
            book_id=i, title=title, isbn=isbn, published_year=year, genre=genre
        )
        if book:
            book_ids.append(i)

            num_book_authors = random.randint(1, min(3, len(author_ids)))
            selected_authors = random.sample(author_ids, num_book_authors)
            for author_id in selected_authors:
                await client.create_book_author(book_id=i, author_id=author_id)

    logger.info(f"Created {len(book_ids)} books with author relationships")

    logger.info("Creating members...")
    member_ids = []
    base_date = datetime(2020, 1, 1)
    for i in range(1, num_members + 1):
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        email = f"{name.lower().replace(' ', '.')}@example.com"
        joined_at = base_date + timedelta(days=random.randint(0, 1800))

        member = await client.create_member(
            member_id=i, name=name, email=email, joined_at=joined_at
        )
        if member:
            member_ids.append(i)
    logger.info(f"Created {len(member_ids)} members")

    logger.info("Creating book copies...")
    copy_ids = []
    copy_id = 1
    for book_id in book_ids:
        num_copies = random.randint(1, copies_per_book * 2)
        for _ in range(num_copies):
            copy_status = random.choice(
                [
                    CopyStatus.AVAILABLE,
                    CopyStatus.AVAILABLE,
                    CopyStatus.AVAILABLE,
                    CopyStatus.ON_LOAN,
                    CopyStatus.LOST,
                ]
            )

            copy = await client.create_copy(
                copy_id=copy_id, book_id=book_id, status=copy_status
            )
            if copy:
                copy_ids.append(copy_id)
            copy_id += 1
    logger.info(f"Created {len(copy_ids)} book copies")

    logger.info("Creating loans...")
    loan_ids = []
    fine_id = 1
    current_date = datetime.now()

    for i in range(1, num_loans + 1):
        if not copy_ids or not member_ids:
            break

        copy_id = random.choice(copy_ids)
        member_id = random.choice(member_ids)

        loan_date = current_date - timedelta(days=random.randint(1, 365))
        due_date = loan_date + timedelta(days=14)

        is_overdue = current_date > due_date
        is_returned = random.random() < 0.7

        if is_returned:
            return_date = loan_date + timedelta(days=random.randint(1, 30))
            loan_status = LoanStatus.RETURNED
        elif is_overdue:
            return_date = None
            loan_status = LoanStatus.OVERDUE
        else:
            return_date = None
            loan_status = LoanStatus.ACTIVE

        loan = await client.create_loan(
            copy_id=copy_id,
            member_id=member_id,
            loan_date=loan_date,
            due_date=due_date,
            status=loan_status,
            return_date=return_date,
        )

        if loan:
            loan_ids.append(i)

            if loan_status == LoanStatus.OVERDUE and random.random() < fine_probability:
                days_overdue = (current_date - due_date).days
                amount = days_overdue * 0.50
                paid = random.random() < 0.3

                assessed_at = due_date + timedelta(days=1)
                paid_at = (
                    assessed_at + timedelta(days=random.randint(1, 30))
                    if paid
                    else None
                )

                await client.create_fine(
                    fine_id=fine_id,
                    member_id=member_id,
                    loan_id=i,
                    amount=round(amount, 2),
                    assessed_at=assessed_at,
                    paid=paid,
                    paid_at=paid_at,
                )
                fine_id += 1

    logger.info(f"Created {len(loan_ids)} loans and {fine_id - 1} fines")

    logger.info("Synthetic data generation complete!")
