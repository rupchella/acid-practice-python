import asyncio

from psycopg import AsyncConnection

from app.core.config import get_settings


async def main() -> None:
    settings = get_settings()

    conn = await AsyncConnection.connect(settings.database_url)

    async with conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT 1;")
            result = await cur.fetchone()

    print(f"Database connection is OK: {result}")

if __name__ == "__main__":
    asyncio.run(
        main(),
        loop_factory=asyncio.SelectorEventLoop,
    )