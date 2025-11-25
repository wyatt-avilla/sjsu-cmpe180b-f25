from __future__ import annotations

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from .models import Author, Book


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
