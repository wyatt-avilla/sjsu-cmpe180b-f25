import asyncio
import logging
from collections.abc import Sequence

from .clap import parse_args
from .populate_db import populate_db


async def main(argv: Sequence[str] | None = None) -> None:
    cli_args = parse_args(argv)

    logging.basicConfig(
        level=cli_args.log_level,
        format="[%(levelname)s][%(asctime)s][%(name)s] %(message)s",
    )

    logging.getLogger(__name__).info(f"Utilizing log level '{cli_args.log_level}'")

    if cli_args.populate_db:
        logging.getLogger(__name__).info("Populating database...")
        await populate_db(cli_args.database_url)
        logging.getLogger(__name__).info("Database population complete.")
        return


def cli(argv: Sequence[str] | None = None) -> None:
    asyncio.run(main(argv))


if __name__ == "__main__":
    cli()
