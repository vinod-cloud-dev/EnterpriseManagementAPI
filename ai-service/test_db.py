import asyncio

from sqlalchemy import text

from app.infrastructure.database.database import engine


async def test_connection():
    async with engine.connect() as connection:
        result = await connection.execute(text("SELECT 1"))

        print("Database connection successful!")
        print("Result:", result.scalar())


asyncio.run(test_connection())