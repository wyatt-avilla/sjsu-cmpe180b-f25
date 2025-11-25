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

    args = parser.parse_args(argv)

    return CommandLineArguments(
        database_url=args.database_url,
        log_level=args.log_level.upper(),
        populate_db=args.populate_db,
    )
