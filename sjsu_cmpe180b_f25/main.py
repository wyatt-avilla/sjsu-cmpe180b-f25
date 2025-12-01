import asyncio
import logging
import sys
from collections.abc import Sequence

from .clap import parse_args
from .client import Client
from .population import populate_db
from .index import create_indexes, drop_indexes
from .explain import run_explain

async def main(argv: Sequence[str] | None = None) -> None:
    cli_args = parse_args(argv)

    logging.basicConfig(
        level=cli_args.log_level,
        format="[%(levelname)s][%(asctime)s][%(name)s] %(message)s",
    )

    logger = logging.getLogger(__name__)
    logger.info(f"Utilizing log level '{cli_args.log_level}'")

    client = Client(cli_args.database_url)

    if cli_args.populate_db:
        logging.getLogger(__name__).info("Populating database...")
        await populate_db(client)
        logging.getLogger(__name__).info("Database population complete.")

    if cli_args.request_loan is not None:
        copy_id, member_id = cli_args.request_loan
        logger.info(
            f"Requesting loan for copy ID '{copy_id}' by member ID '{member_id}'..."
        )
        loan = await client.request_loan(copy_id=copy_id, member_id=member_id)
        if loan is not None:
            logger.info(f"Loan requested successfully with loan ID '{loan.loan_id}'.")
        else:
            logger.error("Loan request failed.")
            sys.exit(1)

    if cli_args.end_loan is not None:
        loan_id = cli_args.end_loan
        logger.info(f"Ending loan ID '{loan_id}'...")
        success = await client.end_loan(loan_id=loan_id)
        if success:
            logger.info(f"Loan ID '{loan_id}' ended successfully.")
        else:
            logger.error(f"Failed to end loan ID '{loan_id}'.")
            sys.exit(1)

    if cli_args.pay_fine is not None:
        fine_id = cli_args.pay_fine
        logger.info(f"Paying fine ID '{fine_id}'...")
        success = await client.pay_fine(fine_id=fine_id)
        if success:
            logger.info(f"Fine ID '{fine_id}' paid successfully.")
        else:
            logger.error(f"Failed to pay fine ID '{fine_id}'.")
            sys.exit(1)

    # Top N most-loaned books
    if cli_args.top_books is not None:
        limit = cli_args.top_books
        logger.info(f"Fetching top {limit} most-loaned books...")
        top_books = await client.get_top_books(limit=limit)

        header = [
            f"\nTop {limit} books by total loans:\n",
            f"{'ID':>5}  {'Title':40}  {'Loans':>5}",
            "-" * 60,
        ]
        formatted_books = [
            f"{book_id:5}  {title[:40]:40}  {total_loans:5}"
            for book_id, title, total_loans in top_books
        ]

        logger.info("\n".join(header + formatted_books))

    # Members with currently overdue loans
    if cli_args.overdue_members:
        logger.info("Fetching members with currently overdue loans...")
        overdue_members = await client.get_overdue_members()

        header = [
            "\nMembers with currently overdue loans:\n",
            f"{'ID':>5}  {'Name':25}  {'Email':30}  {'Overdue':>7}  {'Earliest Due':>12}",
            "-" * 90,
        ]
        formatted_members = [
            f"{member_id:5}  {name[:25]:25}  {email[:30]:30}  "
            f"{overdue_count:7}  {earliest_due.strftime('%Y-%m-%d'):>12}"
            for member_id, name, email, overdue_count, earliest_due in overdue_members
        ]

        logger.info("\n".join(header + formatted_members))

    # Members with highest unpaid fines (with optional minimum)
    if cli_args.unpaid_fines_members is not None:
        min_total = cli_args.unpaid_fines_members
        logger.info(f"Fetching members with unpaid fines >= {min_total:.2f}...")
        members_with_unpaid_fines = await client.get_unpaid_fines_members(
            min_total=min_total
        )

        header = [
            f"\nMembers with unpaid fines >= {min_total:.2f}:\n",
            f"{'ID':>5}  {'Name':25}  {'Email':30}  {'Total Unpaid':>12}  {'Count':>5}",
            "-" * 95,
        ]
        formatted_members = [
            f"{member_id:5}  {name[:25]:25}  {email[:30]:30}  "
            f"{total_unpaid:12.2f}  {fine_count:5}"
            for member_id, name, email, total_unpaid, fine_count in members_with_unpaid_fines
        ]
        logger.info("\n".join(header + formatted_members))

    # Copies on loan per book
    if cli_args.copies_on_loans is not None:
        limit = cli_args.copies_on_loans
        logger.info(f"Fetching top {limit} books by utilization...")
        collection_utilization = await client.get_copies_on_loan(limit=limit)

        header = [
            f"\nTop {limit} books by copy utilization:\n",
            f"{'ID':>5}  {'Title':40}  {'Copies':>6}  {'On Loan':>7}  {'Util %':>7}",
            "-" * 80,
        ]
        formatted_copies = [
            f"{book_id:5}  {title[:40]:40}  {total_copies:6}  "
            f"{copies_on_loan:7}  {util if util is not None else 0.0:7.2f}"
            for book_id, title, total_copies, copies_on_loan, util in collection_utilization
        ]
        logger.info("\n".join(header + formatted_copies))

    # Fine statistics by genre
    if cli_args.genre_fine_stats:
        logger.info("Fetching fine statistics grouped by genre...")
        fine_statistics = await client.get_genre_fine_statistics()
        header = [
            "\nFine statistics by genre:\n",
            f"{'Genre':20}  {'Fine Count':>10}  {'Total Fines':>12}",
            "-" * 50,
        ]
        formatted_stats = [
            f"{genre or 'UNKNOWN':20}  {fine_count:10}  {total_fines:12.2f}"
            for genre, fine_count, total_fines in fine_statistics
        ]
        logger.info("\n".join(header + formatted_stats))

    if cli_args.create_indexes:
        await create_indexes(cli_args.database_url)
        return
    
    if cli_args.drop_indexes:
        await drop_indexes(cli_args.database_url)
        return
    
    if cli_args.explain:
        await run_explain(cli_args.database_url, cli_args.explain)
        return
    
def cli(argv: Sequence[str] | None = None) -> None:
    asyncio.run(main(argv))


if __name__ == "__main__":
    cli()
