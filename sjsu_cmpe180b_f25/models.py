from datetime import datetime
from enum import Enum

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class CopyStatus(str, Enum):
    AVAILABLE = "available"
    ON_LOAN = "on_loan"
    LOST = "lost"


class LoanStatus(str, Enum):
    ACTIVE = "active"
    RETURNED = "returned"
    OVERDUE = "overdue"


class Author(Base):
    __tablename__ = "authors"
    author_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False)


class Book(Base):
    __tablename__ = "books"
    book_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(nullable=False)
    isbn: Mapped[str | None] = mapped_column(unique=True, nullable=True)
    published_year: Mapped[int | None] = mapped_column(nullable=True)
    genre: Mapped[str | None] = mapped_column(nullable=True)


class BookAuthor(Base):
    __tablename__ = "book_authors"
    book_id: Mapped[int] = mapped_column(ForeignKey("books.book_id"), primary_key=True)
    author_id: Mapped[int] = mapped_column(
        ForeignKey("authors.author_id"), primary_key=True
    )


class Member(Base):
    __tablename__ = "members"
    member_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    joined_at: Mapped[datetime] = mapped_column(nullable=False)


class Copy(Base):
    __tablename__ = "copies"
    copy_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.book_id"), nullable=False)
    status: Mapped[CopyStatus] = mapped_column(nullable=False)


class Loan(Base):
    __tablename__ = "loans"
    loan_id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
        autoincrement=True,
    )
    copy_id: Mapped[int] = mapped_column(
        ForeignKey("copies.copy_id"), nullable=False, unique=True
    )
    member_id: Mapped[int] = mapped_column(
        ForeignKey("members.member_id"), nullable=False
    )
    loan_date: Mapped[datetime] = mapped_column(nullable=False)
    due_date: Mapped[datetime] = mapped_column(nullable=False)
    return_date: Mapped[datetime | None] = mapped_column(nullable=True)
    status: Mapped[LoanStatus] = mapped_column(nullable=False)


class Fine(Base):
    __tablename__ = "fines"
    fine_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    member_id: Mapped[int] = mapped_column(
        ForeignKey("members.member_id"), nullable=False
    )
    loan_id: Mapped[int | None] = mapped_column(
        ForeignKey("loans.loan_id"), nullable=True
    )
    amount: Mapped[float] = mapped_column(nullable=False)
    assessed_at: Mapped[datetime] = mapped_column(nullable=False)
    paid: Mapped[bool] = mapped_column(nullable=False, default=False)
    paid_at: Mapped[datetime | None] = mapped_column(nullable=True)
