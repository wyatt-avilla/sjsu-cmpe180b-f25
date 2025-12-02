from __future__ import annotations

import logging

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

INDEX_STATEMENTS: list[str] = [
    # Complex Query 1 – Top N most-loaned books
    # Speeds up joins books -> copies -> loans
    "CREATE INDEX IF NOT EXISTS idx_copies_book_id ON copies (book_id)",
    "CREATE INDEX IF NOT EXISTS idx_loans_copy_id ON loans (copy_id)",
    # Complex Query 2 – Members with overdue loans
    # Helps filter by status and due_date when looking for overdue loans
    "CREATE INDEX IF NOT EXISTS idx_loans_status_due_date ON loans (status, due_date)",
    "CREATE INDEX IF NOT EXISTS idx_loans_member_id ON loans (member_id)",
    # Complex Query 3 – Members with large unpaid fines
    # Supports grouping and filtering by member on unpaid fines
    "CREATE INDEX IF NOT EXISTS idx_fines_member_id ON fines (member_id)",
    # Partial index: only unpaid fines, smaller & more selective
    "CREATE INDEX IF NOT EXISTS idx_fines_unpaid_member "
    "ON fines (member_id) WHERE paid = FALSE",
]

INDEX_NAMES = [
    "idx_copies_book_id",
    "idx_loans_copy_id",
    "idx_loans_status_due_date",
    "idx_loans_member_id",
    "idx_fines_member_id",
    "idx_fines_unpaid_member",
]

logger = logging.getLogger(__name__)


async def create_indexes(database_url: str) -> None:
    """Create indexes that optimize the complex queries"""
    logger.info("Creating indexes on database...")
    engine = create_async_engine(database_url, pool_pre_ping=True)

    async with engine.begin() as conn:
        for sql in INDEX_STATEMENTS:
            logger.info("Running: %s", sql)
            await conn.execute(text(sql))

    await engine.dispose()
    logger.info("Index creation complete.")


async def drop_indexes(database_url: str) -> None:
    """Drop all indexes if they exist."""
    logger.info("Dropping indexes...")
    engine = create_async_engine(database_url)

    async with engine.begin() as conn:
        for name in INDEX_NAMES:
            stmt = text(f"DROP INDEX IF EXISTS {name}")
            logger.info("Running: %s", stmt.text)
            await conn.execute(stmt)

    logger.info("Index drop complete.")
