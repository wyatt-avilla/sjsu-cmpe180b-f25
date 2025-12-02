from __future__ import annotations

import argparse
import os
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence


@dataclass(slots=True)
class CommandLineArguments:
    database_url: str
    log_level: str
    populate_db: bool = False
    request_loan: tuple[int, int] | None = None
    end_loan: int | None = None
    pay_fine: int | None = None

    top_books: int | None = None
    overdue_members: bool = False
    unpaid_fines_members: float | None = None
    copies_on_loans: int | None = None
    genre_fine_stats: bool = False
    member_history: int | None = None
    create_indexes: bool = False
    drop_indexes: bool = False
    explain: str | None = None
    explain_member_history: int | None = None


def parse_args(argv: Sequence[str] | None = None) -> CommandLineArguments:
    parser = argparse.ArgumentParser(
        description="CMPE-180b Project Command Line Interface",
    )
    parser.add_argument(
        "--database-url",
        default=os.getenv("DATABASE_URL"),
        required=os.getenv("DATABASE_URL") is None,
        help="URL for the database. Takes priority over the `DATABASE_URL` environment variable. Required if DATABASE_URL is not set.",
    )
    parser.add_argument(
        "--populate-db",
        action="store_true",
        help="Populate the database with initial data.",
    )
    parser.add_argument(
        "--log-level",
        default="info",
        choices=("critical", "error", "warning", "info", "debug"),
        help="Logging verbosity. Defaults to info.",
    )

    parser.add_argument(
        "--request-loan",
        nargs=2,
        type=int,
        metavar=("COPY_ID", "MEMBER_ID"),
        help="Create a new loan for the specified copy ID and member ID.",
    )
    parser.add_argument(
        "--end-loan",
        type=int,
        metavar="LOAN_ID",
        help="End the loan with the specified loan ID.",
    )
    parser.add_argument(
        "--pay-fine",
        type=int,
        metavar="FINE_ID",
        help="Pay the fine with the specified ID.",
    )

    parser.add_argument(
        "--top-books",
        type=int,
        metavar="N",
        help="Show the top N most loaned books.",
    )

    parser.add_argument(
        "--overdue-members",
        action="store_true",
        help="List members who currently have overdue loans.",
    )

    parser.add_argument(
        "--unpaid-fines-members",
        type=float,
        metavar="AMOUNT",
        help="List members whose unpaid fines total with optional minimum amount.",
    )

    parser.add_argument(
        "--copies-on-loans",
        type=int,
        metavar="N",
        help="Show the top N books based on copies on loans.",
    )

    parser.add_argument(
        "--genre-fine-stats",
        action="store_true",
        help="Show fine statistics grouped by book genre.",
    )

    parser.add_argument(
        "--member-history",
        nargs=1,
        type=int,
        metavar="MEMBER_ID",
        help="Show loan history for the given member_id"
    )

    parser.add_argument(
        "--create-indexes",
        action="store_true",
        help="Create indexes that optimize the complex queries.",
    )

    parser.add_argument(
        "--drop-indexes", action="store_true", help="Drop all created indexes."
    )

    parser.add_argument(
        "--explain",
        choices=["top-books", "overdue-members", "unpaid-fines"],
        help="Run EXPLAIN ANALYZE on a complex query.",
    )

    parser.add_argument(
        "--explain-member-history",
        type=int,
        help="Run EXPLAIN ANALYZE loan history query for the given member_id"
    )

    args = parser.parse_args(argv)

    return CommandLineArguments(
        database_url=args.database_url,
        log_level=args.log_level.upper(),
        populate_db=args.populate_db,
        request_loan=tuple(args.request_loan) if args.request_loan else None,
        end_loan=args.end_loan,
        pay_fine=args.pay_fine,
        top_books=args.top_books,
        overdue_members=args.overdue_members,
        unpaid_fines_members=args.unpaid_fines_members,
        copies_on_loans=args.copies_on_loans,
        genre_fine_stats=args.genre_fine_stats,
        member_history=args.member_history,
        create_indexes=args.create_indexes,
        drop_indexes=args.drop_indexes,
        explain=args.explain,
        explain_member_history=args.explain_member_history,
    )
