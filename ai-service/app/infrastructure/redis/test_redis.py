## You can delete this if you want to test the Redis connection. This is just a simple test script to check if the Redis client is working properly.

import asyncio
from app.infrastructure.redis.redis_client import redis_client

async def main() -> None:
    response = await redis_client.ping()
    print(f"Redis response: {response}")

asyncio.run(main())