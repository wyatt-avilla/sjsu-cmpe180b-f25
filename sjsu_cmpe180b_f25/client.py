from __future__ import annotations

import logging
from collections.abc import Sequence
from datetime import datetime, timedelta
from typing import TypeVar

from sqlalchemy import Float, Integer, Row, case, desc, func, select, type_coerce
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from .models import (
    Author,
    Base,
    Book,
    BookAuthor,
    Copy,
    CopyStatus,
    Fine,
    Loan,
    LoanStatus,
    Member,
)

M = TypeVar("M", Author, Book, BookAuthor, Copy, Fine, Loan, Member)


class Client:
    def __init__(self, database_url: str) -> None:
        self.__engine = create_async_engine(
            database_url,
            pool_pre_ping=True,
            echo=False,
        )

        self.__session_factory = async_sessionmaker(
            bind=self.__engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def __generic_create(self, model: M) -> M | None:
        async with self.__session_factory() as db:
            db.add(model)
            try:
                await db.commit()
                await db.refresh(model)
                return model
            except IntegrityError as e:
                logging.getLogger(__name__).warning(f"Unable to create '{model}' {(e)}")
                await db.rollback()
                return None

    async def create_tables(self) -> None:
        async with self.__engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def dispose(self) -> None:
        await self.__engine.dispose()

    async def create_author(
        self,
        *,
        id: int,
        name: str,
    ) -> Author | None:
        """Creates an author, returning the author or None if it exists."""
        author = Author(
            author_id=id,
            name=name,
        )
        return await self.__generic_create(author)

    async def create_book(
        self,
        *,
        book_id: int,
        title: str,
        isbn: str | None = None,
        published_year: int | None = None,
        genre: str | None = None,
    ) -> Book | None:
        """Creates a book, returning the book or None if it exists."""
        book = Book(
            book_id=book_id,
            title=title,
            isbn=isbn,
            published_year=published_year,
            genre=genre,
        )
        return await self.__generic_create(book)

    async def create_book_author(
        self,
        *,
        book_id: int,
        author_id: int,
    ) -> BookAuthor | None:
        """Creates a book-author relationship, returning it or None if it exists."""
        book_author = BookAuthor(
            book_id=book_id,
            author_id=author_id,
        )
        return await self.__generic_create(book_author)

    async def create_member(
        self,
        *,
        member_id: int,
        name: str,
        email: str,
        joined_at: datetime,
    ) -> Member | None:
        """Creates a member, returning the member or None if it exists."""
        member = Member(
            member_id=member_id,
            name=name,
            email=email,
            joined_at=joined_at,
        )
        return await self.__generic_create(member)

    async def create_copy(
        self,
        *,
        copy_id: int,
        book_id: int,
        status: CopyStatus,
    ) -> Copy | None:
        """Creates a copy, returning the copy or None if it exists."""
        copy = Copy(
            copy_id=copy_id,
            book_id=book_id,
            status=status,
        )
        return await self.__generic_create(copy)

    async def create_loan(
        self,
        *,
        loan_id: int,
        copy_id: int,
        member_id: int,
        loan_date: datetime,
        due_date: datetime,
        status: LoanStatus,
        return_date: datetime | None = None,
    ) -> Loan | None:
        """Creates a loan, returning the loan or None if it exists."""
        loan = Loan(
            loan_id=loan_id,
            copy_id=copy_id,
            member_id=member_id,
            loan_date=loan_date,
            due_date=due_date,
            return_date=return_date,
            status=status,
        )
        return await self.__generic_create(loan)

    async def create_fine(
        self,
        *,
        fine_id: int,
        member_id: int,
        loan_id: int,
        amount: float,
        assessed_at: datetime,
        paid: bool = False,
        paid_at: datetime | None = None,
    ) -> Fine | None:
        """Creates a fine, returning the fine or None if it exists."""
        fine = Fine(
            fine_id=fine_id,
            member_id=member_id,
            loan_id=loan_id,
            amount=amount,
            assessed_at=assessed_at,
            paid=paid,
            paid_at=paid_at,
        )
        return await self.__generic_create(fine)

    async def request_loan(
        self,
        *,
        copy_id: int,
        member_id: int,
    ) -> Loan | None:
        """Requests a loan for a copy by a member, returning the loan or None if not possible."""
        async with self.__session_factory() as db:
            stmt = select(Copy).where(Copy.copy_id == copy_id).with_for_update()
            result = await db.execute(stmt)
            copy = result.scalar_one_or_none()

            if not copy or copy.status != CopyStatus.AVAILABLE:
                logging.getLogger(__name__).warning(
                    f"Copy '{copy_id}' is not available for loan."
                )
                return None

            now = datetime.now(tz=None)
            loan = Loan(
                copy_id=copy_id,
                member_id=member_id,
                loan_date=now,
                due_date=now + timedelta(days=14),
                status=LoanStatus.ACTIVE,
            )
            db.add(loan)
            copy.status = CopyStatus.ON_LOAN

            try:
                await db.commit()
                await db.refresh(loan)
                return loan
            except IntegrityError as e:
                logging.getLogger(__name__).warning(
                    f"Unable to create loan for copy '{copy_id}' to member '{member_id}': {e}"
                )
                await db.rollback()
                return None

    async def end_loan(
        self,
        *,
        loan_id: int,
    ) -> bool:
        """Ends a loan, returning True if successful, False otherwise."""
        async with self.__session_factory() as db:
            loan_result = await db.execute(
                select(Loan).where(Loan.loan_id == loan_id).with_for_update()
            )
            loan = loan_result.scalar_one_or_none()

            if not loan or loan.status != LoanStatus.ACTIVE:
                logging.getLogger(__name__).warning(
                    f"Loan '{loan_id}' is not active and cannot be ended."
                )
                return False

            copy_result = await db.execute(
                select(Copy).where(Copy.copy_id == loan.copy_id).with_for_update()
            )
            copy = copy_result.scalar_one_or_none()

            if not copy:
                logging.getLogger(__name__).error(
                    f"Copy '{loan.copy_id}' associated with loan '{loan_id}' not found."
                )
                return False

            loan.return_date = datetime.now(tz=None)
            loan.status = LoanStatus.RETURNED
            copy.status = CopyStatus.AVAILABLE

            try:
                await db.commit()
                return True
            except IntegrityError as e:
                logging.getLogger(__name__).error(
                    f"Unable to end loan '{loan_id}': {e}"
                )
                await db.rollback()
                return False

    async def pay_fine(
        self,
        *,
        fine_id: int,
    ) -> bool:
        """Pays a fine, returning True if successful, False otherwise."""
        async with self.__session_factory() as db:
            stmt = select(Fine).where(Fine.fine_id == fine_id).with_for_update()
            result = await db.execute(stmt)
            fine = result.scalar_one_or_none()

            if not fine or fine.paid:
                logging.getLogger(__name__).warning(
                    f"Fine '{fine_id}' is either not found or already paid."
                )
                return False

            fine.paid = True
            fine.paid_at = datetime.now(tz=None)

            try:
                await db.commit()
                return True
            except IntegrityError as e:
                logging.getLogger(__name__).error(
                    f"Unable to pay fine '{fine_id}': {e}"
                )
                await db.rollback()
                return False

    async def get_top_books(
        self, limit: int = 10
    ) -> Sequence[Row[tuple[int, str, int]]]:
        """Return the top N most loaned books"""
        async with self.__session_factory() as db:
            stmt = (
                select(
                    Book.book_id,
                    Book.title,
                    func.count(Loan.loan_id).label("total_loans"),
                )
                .join(Copy, Copy.book_id == Book.book_id)
                .join(Loan, Loan.copy_id == Copy.copy_id)
                .group_by(Book.book_id, Book.title)
                .order_by(desc("total_loans"), Book.title)
                .limit(limit)
            )

            result = await db.execute(stmt)
            return result.all()

    async def get_overdue_members(
        self,
    ) -> Sequence[Row[tuple[int, str, str, int, datetime]]]:
        """Return members who currently have overdue loans"""
        async with self.__session_factory() as db:
            stmt = (
                select(
                    Member.member_id,
                    Member.name,
                    Member.email,
                    func.count(Loan.loan_id).label("overdue_count"),
                    func.min(Loan.due_date).label("earliest_due_date"),
                )
                .join(Loan, Loan.member_id == Member.member_id)
                .where(
                    Loan.status == LoanStatus.ACTIVE,
                    Loan.return_date.is_(None),
                    Loan.due_date < datetime.now(tz=None),
                )
                .group_by(
                    Member.member_id,
                    Member.name,
                    Member.email,
                )
                .order_by(
                    desc("overdue_count"),
                    func.min(Loan.due_date),
                )
            )

            result = await db.execute(stmt)
            return result.all()

    async def get_unpaid_fines_members(
        self,
        min_total: float = 0.0,
    ) -> Sequence[Row[tuple[int, str, str, float, int]]]:
        """Return members with unpaid fines with optional min threshold"""
        async with self.__session_factory() as db:
            total_unpaid = func.sum(Fine.amount).label("total_unpaid")
            fine_count = func.count(Fine.fine_id).label("unpaid_fine_count")

            stmt = (
                select(
                    Member.member_id,
                    Member.name,
                    Member.email,
                    total_unpaid,
                    fine_count,
                )
                .join(Fine, Fine.member_id == Member.member_id)
                .where(Fine.paid.is_(False))
                .group_by(
                    Member.member_id,
                    Member.name,
                    Member.email,
                )
            )

            if min_total > 0:
                stmt = stmt.having(total_unpaid >= min_total)

            stmt = stmt.order_by(desc("total_unpaid"), desc("unpaid_fine_count"))

            result = await db.execute(stmt)
            return result.all()

    async def get_copies_on_loan(
        self,
        limit: int = 20,
    ) -> Sequence[Row[tuple[int, str, int, int, float]]]:
        """Return loan stats per book title"""
        async with self.__session_factory() as db:
            total_copies = func.count(Copy.copy_id)
            copies_on_loan = func.sum(
                case((Copy.status == CopyStatus.ON_LOAN, 1), else_=0)
            )

            stmt = (
                select(
                    Book.book_id,
                    Book.title,
                    type_coerce(total_copies, Integer).label("total_copies"),
                    type_coerce(copies_on_loan, Integer).label("copies_on_loan"),
                    type_coerce(
                        copies_on_loan * 100.0 / func.nullif(total_copies, 0), Float
                    ).label("utilization_percent"),
                )
                .join(Copy, Copy.book_id == Book.book_id)
                .group_by(Book.book_id, Book.title)
                .order_by(
                    desc("utilization_percent"),
                    desc("total_copies"),
                )
                .limit(limit)
            )

            result = await db.execute(stmt)
            return result.all()

    async def get_genre_fine_statistics(
        self,
    ) -> Sequence[Row[tuple[str | None, int, float]]]:
        """Return fine stats aggregated by book genre"""
        async with self.__session_factory() as db:
            stmt = (
                select(
                    Book.genre,
                    func.count(Fine.fine_id).label("fine_count"),
                    func.sum(Fine.amount).label("total_fines"),
                )
                .join(Loan, Loan.loan_id == Fine.loan_id)
                .join(Copy, Copy.copy_id == Loan.copy_id)
                .join(Book, Book.book_id == Copy.book_id)
                .group_by(Book.genre)
                .order_by(desc("total_fines"))
            )

            result = await db.execute(stmt)
            return result.all()
