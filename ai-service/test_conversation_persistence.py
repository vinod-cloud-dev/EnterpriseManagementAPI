import asyncio
from uuid import UUID

from app.infrastructure.redis.redis_client import redis_client
from app.infrastructure.memory.redis_conversation_memory import (
    RedisConversationMemory,
)
from app.infrastructure.database.database import AsyncSessionLocal
from app.infrastructure.database.repositories.conversation_repository import (
    ConversationRepository,
)


CONVERSATION_ID = UUID(
    "550e8400-e29b-41d4-a716-446655440012"
)


async def test_persistence():

    print("\n========================================")
    print("   CONVERSATION PERSISTENCE TEST")
    print("========================================")

    memory = RedisConversationMemory()

    # -------------------------------------------------
    # 1. Check Redis
    # -------------------------------------------------

    print("\n[1] Checking Redis...")

    redis_history = await memory.get_history(
        CONVERSATION_ID
    )

    if redis_history:

        print(
            f"[REDIS] History found: "
            f"{len(redis_history)} messages"
        )

        for message in redis_history:
            print(
                f"   [REDIS] "
                f"{message.role}: {message.content}"
            )

        print("\nResult: History came from REDIS.")

    else:

        print("[REDIS] No history found.")

        # -------------------------------------------------
        # 2. Check PostgreSQL
        # -------------------------------------------------

        print("\n[2] Checking PostgreSQL...")

        async with AsyncSessionLocal() as session:

            repository = ConversationRepository(
                session
            )

            db_history = await repository.get_history(
                CONVERSATION_ID
            )

        if db_history:

            print(
                f"[DB] History found: "
                f"{len(db_history)} messages"
            )

            for message in db_history:
                print(
                    f"   [DB] "
                    f"{message.role}: {message.content}"
                )

            print("\nResult: History came from DATABASE.")

        else:

            print(
                "[DB] No history found."
            )

            print(
                "\nResult: No conversation exists "
                "in Redis or PostgreSQL."
            )

    print("\n========================================")
    print("             TEST COMPLETE")
    print("========================================\n")


async def main():

    try:
        await test_persistence()

    finally:
        await redis_client.aclose()


if __name__ == "__main__":
    asyncio.run(main())