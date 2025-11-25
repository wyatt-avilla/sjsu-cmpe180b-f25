from __future__ import annotations

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from .models import Author, Book, Member, Loan


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

    async def create_author(
        self,
        *,
        id: int,
        name: str,
    ) -> Author:
        async with self.__session_factory() as db:
            author = Author(
                id=id,
                name=name,
            )
            db.add(author)
            await db.commit()
            await db.refresh(author)
            return author

    async def create_book(
        self,
        *,
        id: int,
        title: str,
        author_id: int,
    ) -> Book:
        async with self.__session_factory() as db:
            book = Book(
                id=id,
                title=title,
                author_id=author_id,
            )
            db.add(book)
            await db.commit()
            await db.refresh(book)
            return book

    async def create_member(
        self,
        *,
        id: int,
        name: str,
        email: str,
    ) -> Member:
        async with self.__session_factory() as db:
            member = Member(
                id=id,
                name=name,
                email=email,
            )
            db.add(member)
            await db.commit()
            await db.refresh(member)
            return member

    async def create_loan(
        self,
        *,
        id: int,
        book_id: int,
        member_id: int,
        loan_date: str,
        return_date: str | None = None,
    ) -> Loan:
        async with self.__session_factory() as db:
            loan = Loan(
                id=id,
                book_id=book_id,
                member_id=member_id,
                loan_date=loan_date,
                return_date=return_date,
            )
            db.add(loan)
            await db.commit()
            await db.refresh(loan)
            return loan
