from __future__ import annotations

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


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
