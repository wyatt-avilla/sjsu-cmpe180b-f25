from .client import Client


async def populate_db(database_url: str) -> None:
    client = Client(database_url)

    # Create authors
    await client.create_author(id=1, name="George Orwell")

    # Create books
    await client.create_book(id=1, title="1984", author_id=1)
