import logging

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s][%(asctime)s][%(name)s] %(message)s",
)

logger = logging.getLogger(__name__)


def extra_unused_function():
    pass


def main() -> None:
    logger.info("hello world")


if __name__ == "__main__":
    main()
