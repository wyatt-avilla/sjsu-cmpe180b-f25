import random
from datetime import datetime, timedelta

from .client import Client
from .models import CopyStatus, LoanStatus


async def populate_db(database_url: str) -> None:
    client = Client(database_url)

    # Create tables
    await client.create_tables()

    # Create authors
    authors = [
        (1, "George Orwell"),
        (2, "J.K. Rowling"),
        (3, "Haruki Murakami"),
        (4, "Agatha Christie"),
        (5, "Leo Tolstoy"),
        (6, "Jane Austen"),
        (7, "Mark Twain"),
        (8, "Yuval Noah Harari"),
        (9, "Isaac Asimov"),
        (10, "Ernest Hemingway"),
    ]

    for author_id, name in authors:
        await client.create_author(id=author_id, name=name)

    # Create books
    books = [
        (1, "1984", "978-0451524935", 1949, "Dystopian", [1]),
        (2, "Animal Farm", "978-0451526342", 1945, "Political Satire", [1]),
        (
            3,
            "Harry Potter and the Sorcerer’s Stone",
            "978-0590353427",
            1997,
            "Fantasy",
            [2],
        ),
        (4, "Kafka on the Shore", "978-1400079278", 2002, "Magical Realism", [3]),
        (5, "Murder on the Orient Express", "978-0062693662", 1934, "Mystery", [4]),
        (6, "War and Peace", "978-0199232765", 1869, "Historical", [5]),
        (7, "Pride and Prejudice", "978-1503290563", 1813, "Romance", [6]),
        (8, "The Adventures of Tom Sawyer", "978-0143039563", 1876, "Adventure", [7]),
        (9, "Sapiens", "978-0062316110", 2011, "History", [8]),
        (10, "Foundation", "978-0553293357", 1951, "Science Fiction", [9]),
    ]

    for book_id, title, isbn, year, genre, author_ids in books:
        await client.create_book(
            book_id=book_id,
            title=title,
            isbn=isbn,
            published_year=year,
            genre=genre,
        )

        # Create book-author relationships
        for a_id in author_ids:
            await client.create_book_author(book_id=book_id, author_id=a_id)

    # Create members
    for member_id in range(1, 31):
        await client.create_member(
            member_id=member_id,
            name=f"Member {member_id}",
            email=f"member{member_id}@example.com",
            joined_at=datetime(2023, random.randint(1, 12), random.randint(1, 28)),
        )

    # Create copies
    copy_id = 1
    copy_map: dict[int, list[int]] = {}  # key: book_id, value: list of copy_ids

    for book_id in range(1, 11):
        copy_map[book_id] = []
        num_copies = random.randint(1, 3)

        for _ in range(num_copies):
            await client.create_copy(
                copy_id=copy_id,
                book_id=book_id,
                status=CopyStatus.AVAILABLE,
            )
            copy_map[book_id].append(copy_id)
            copy_id += 1

    # Create loans
    loan_id = 1
    fine_id = 1

    for member_id in range(1, 21):  # Only 20 members borrow books
        # Randomly choose a book
        book_id = random.randint(1, 10)
        possible_copies = copy_map[book_id]
        copy_id_selected = random.choice(possible_copies)

        # Generate realistic loan dates
        loan_date = datetime.now() - timedelta(days=random.randint(1, 60))
        due_date = loan_date + timedelta(days=14)

        # Random loan status
        if random.random() < 0.7:
            # returned on time or late
            return_date = loan_date + timedelta(days=random.randint(5, 25))
            if return_date > due_date:
                status = LoanStatus.OVERDUE
            else:
                status = LoanStatus.RETURNED
        else:
            # still active
            return_date = None
            status = LoanStatus.ACTIVE

        await client.create_loan(
            loan_id=loan_id,
            copy_id=copy_id_selected,
            member_id=member_id,
            loan_date=loan_date,
            due_date=due_date,
            return_date=return_date,
            status=status,
        )
        # Create fines
        if status == LoanStatus.OVERDUE and return_date is not None:
            days_late = (return_date - due_date).days
            amount = round(days_late * 0.5, 2)  # 50 cents/day

            await client.create_fine(
                fine_id=fine_id,
                member_id=member_id,
                loan_id=loan_id,
                amount=amount,
                assessed_at=return_date,
                paid=False,
                paid_at=None,
            )
            fine_id += 1

        loan_id += 1
