from __future__ import annotations

import logging

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

logger = logging.getLogger(__name__)

EXPLAIN_QUERIES = {
    "top_books": """
        EXPLAIN ANALYZE
        SELECT
            b.book_id,
            b.title,
            COUNT(*) AS loan_count
        FROM books b
        JOIN copies c ON c.book_id = b.book_id
        JOIN loans l ON l.copy_id = c.copy_id
        GROUP BY b.book_id, b.title
        ORDER BY loan_count DESC
        LIMIT 10;
    """,
    "overdue_members": """
        EXPLAIN ANALYZE
        SELECT DISTINCT
            m.member_id,
            m.name,
            m.email
        FROM members m
        JOIN loans l ON m.member_id = l.member_id
        WHERE l.status = 'OVERDUE'::loanstatus;
    """,
    "unpaid_fines": """
        EXPLAIN ANALYZE
        SELECT
            m.member_id,
            m.name,
            SUM(f.amount) AS total_unpaid
        FROM members m
        JOIN fines f ON m.member_id = f.member_id
        WHERE f.paid = FALSE
        GROUP BY m.member_id, m.name
        HAVING SUM(f.amount) > 20.0;
    """,
}


async def run_explain(database_url: str, query_name: str) -> None:
    if query_name not in EXPLAIN_QUERIES:
        raise ValueError(f"Unknown query name '{query_name}'")

    logging.info(f"Running EXPLAIN ANALYZE for: {query_name}")

    engine = create_async_engine(database_url, pool_pre_ping=True)

    async with engine.begin() as conn:
        result = await conn.execute(text(EXPLAIN_QUERIES[query_name]))
        plan = "\n".join(row[0] for row in result.fetchall())

    await engine.dispose()

    logger.info("\n===== EXPLAIN ANALYZE plan =====")
    logger.info(plan)
    logger.info("================================\n")
