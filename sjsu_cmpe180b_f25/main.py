import logging
from collections.abc import Sequence

from .clap import parse_args


def main(argv: Sequence[str] | None = None) -> None:
    cli_args = parse_args(argv)

    logging.basicConfig(
        level=cli_args.log_level,
        format="[%(levelname)s][%(asctime)s][%(name)s] %(message)s",
    )

    logging.getLogger(__name__).info(f"Utilizing log level '{cli_args.log_level}'")


def cli(argv: Sequence[str] | None = None) -> None:
    main(argv)


if __name__ == "__main__":
    cli()
