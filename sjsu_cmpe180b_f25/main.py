import asyncio
import logging
import sys
from collections.abc import Sequence

from .clap import parse_args
from .client import Client
from .population import populate_db


async def main(argv: Sequence[str] | None = None) -> None:
    cli_args = parse_args(argv)

    logging.basicConfig(
        level=cli_args.log_level,
        format="[%(levelname)s][%(asctime)s][%(name)s] %(message)s",
    )

    logging.getLogger(__name__).info(f"Utilizing log level '{cli_args.log_level}'")

    client = Client(cli_args.database_url)

    if cli_args.populate_db:
        logging.getLogger(__name__).info("Populating database...")
        await populate_db(client)
        logging.getLogger(__name__).info("Database population complete.")

    if cli_args.request_loan is not None:
        copy_id, member_id = cli_args.request_loan
        logging.getLogger(__name__).info(
            f"Requesting loan for copy ID '{copy_id}' by member ID '{member_id}'..."
        )
        loan = await client.request_loan(copy_id=copy_id, member_id=member_id)
        if loan is not None:
            logging.getLogger(__name__).info(
                f"Loan requested successfully with loan ID '{loan.loan_id}'."
            )
        else:
            logging.getLogger(__name__).error("Loan request failed.")
            sys.exit(1)

    if cli_args.end_loan is not None:
        loan_id = cli_args.end_loan
        logging.getLogger(__name__).info(f"Ending loan ID '{loan_id}'...")
        success = await client.end_loan(loan_id=loan_id)
        if success:
            logging.getLogger(__name__).info(f"Loan ID '{loan_id}' ended successfully.")
        else:
            logging.getLogger(__name__).error(f"Failed to end loan ID '{loan_id}'.")
            sys.exit(1)

    if cli_args.pay_fine is not None:
        fine_id = cli_args.pay_fine
        logging.getLogger(__name__).info(f"Paying fine ID '{fine_id}'...")
        success = await client.pay_fine(fine_id=fine_id)
        if success:
            logging.getLogger(__name__).info(f"Fine ID '{fine_id}' paid successfully.")
        else:
            logging.getLogger(__name__).error(f"Failed to pay fine ID '{fine_id}'.")
            sys.exit(1)


def cli(argv: Sequence[str] | None = None) -> None:
    asyncio.run(main(argv))


if __name__ == "__main__":
    cli()
