from __future__ import annotations

import logging
from datetime import datetime
from typing import TypeVar

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
            pool_size=10,
            max_overflow=20,
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
                logging.getLogger(__name__).warn(f"Unable to create '{model}' {(e)}")
                await db.rollback()
                return None

    async def create_tables(self) -> None:
        async with self.__engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def create_author(
        self,
        *,
        id: int,
        name: str,
    ) -> Author | None:
        """Creates an author, returning the author or None if it exists."""
        author = Author(
            id=id,
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
            member_id=id,
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
        id: int,
        member_id: int,
        amount: float,
        paid: bool = False,
    ) -> Fine | None:
        """Creates a fine, returning the fine or None if it exists."""
        fine = Fine(
            id=id,
            member_id=member_id,
            amount=amount,
            paid=paid,
        )
        return await self.__generic_create(fine)
