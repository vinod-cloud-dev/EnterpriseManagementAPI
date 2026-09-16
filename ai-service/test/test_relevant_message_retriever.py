import asyncio
from datetime import datetime, timezone
from uuid import uuid4

from app.infrastructure.database.database import AsyncSessionLocal
from app.infrastructure.database.repositories.conversation_repository import (
    ConversationRepository,
)
from app.application.services.relevant_message_retriever import (
    BasicRelevantMessageRetriever,
)
from app.domain.models.conversation_message import ConversationMessage


async def main():

    print("Creating dependencies...")

    async with AsyncSessionLocal() as session:

        repository = ConversationRepository(session)

        conversation_id = uuid4()
        user_id = 1

        print("\nConversation ID:")
        print(conversation_id)

        # -------------------------------------------------
        # Create conversation
        # -------------------------------------------------

        await repository.create_conversation(
            conversation_id=conversation_id,
            user_id=user_id,
        )

        # -------------------------------------------------
        # Create test messages
        # -------------------------------------------------

        messages = [
            ConversationMessage(
                id=uuid4(),
                conversation_id=conversation_id,
                role="user",
                content=(
                    "I am building an AI service using "
                    "FastAPI and PostgreSQL."
                ),
                sequence_number=1,
                created_at=datetime.now(timezone.utc),
            ),

            ConversationMessage(
                id=uuid4(),
                conversation_id=conversation_id,
                role="assistant",
                content=(
                    "FastAPI is a good choice for building "
                    "the AI service API."
                ),
                sequence_number=2,
                created_at=datetime.now(timezone.utc),
            ),

            ConversationMessage(
                id=uuid4(),
                conversation_id=conversation_id,
                role="user",
                content=(
                    "I want to use Redis for "
                    "conversation caching."
                ),
                sequence_number=3,
                created_at=datetime.now(timezone.utc),
            ),

            ConversationMessage(
                id=uuid4(),
                conversation_id=conversation_id,
                role="assistant",
                content=(
                    "Redis can be used as a fast cache "
                    "while PostgreSQL remains the source of truth."
                ),
                sequence_number=4,
                created_at=datetime.now(timezone.utc),
            ),

            ConversationMessage(
                id=uuid4(),
                conversation_id=conversation_id,
                role="user",
                content=(
                    "Later I want to add RAG and "
                    "vector search."
                ),
                sequence_number=5,
                created_at=datetime.now(timezone.utc),
            ),
        ]

        # -------------------------------------------------
        # Save messages
        # -------------------------------------------------

        for message in messages:
            await repository.save_message(message)

        print("\nTest messages inserted.")

        # -------------------------------------------------
        # Create retriever
        # -------------------------------------------------

        retriever = BasicRelevantMessageRetriever(
            repository=repository
        )

        # -------------------------------------------------
        # Test query
        # -------------------------------------------------

        query = "How can I use Redis for caching?"

        print("\nQuery:")
        print(query)

        # -------------------------------------------------
        # Retrieve relevant messages
        # -------------------------------------------------

        results = await retriever.retrieve(
            conversation_id=conversation_id,
            query=query,
            limit=3,
        )

        # -------------------------------------------------
        # Display results
        # -------------------------------------------------

        print("\n========== RETRIEVED MESSAGES ==========")

        if not results:
            print("No relevant messages found.")

        for result in results:

            print("\nScore:", result.relevance_score)
            print("Source:", result.retrieval_source)
            print("Role:", result.message.role)
            print("Message:", result.message.content)


if __name__ == "__main__":
    asyncio.run(main())