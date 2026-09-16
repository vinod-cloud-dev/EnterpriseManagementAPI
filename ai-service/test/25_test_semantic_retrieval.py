import asyncio
from datetime import datetime, timezone
from uuid import uuid4

from app.application.services.embedding_service import EmbeddingService
from app.application.services.semantic_retrieval_service import (
    SemanticRetrievalService,
)
from app.domain.models.conversation_message import ConversationMessage
from app.infrastructure.database.database import AsyncSessionLocal
from app.infrastructure.database.repositories.conversation_repository import (
    ConversationRepository,
)
from app.infrastructure.database.repositories.embedding_repository import (
    EmbeddingRepository,
)
from app.infrastructure.embeddings.qwen_embedding_provider import (
    QwenEmbeddingProvider,
)


MODEL_NAME = "Qwen/Qwen3-Embedding-0.6B"


async def main():

    conversation_id = uuid4()
    user_id = 999998

    print("Creating database session...")

    async with AsyncSessionLocal() as session:

        conversation_repository = ConversationRepository(session)
        embedding_repository = EmbeddingRepository(session)

        embedding_provider = QwenEmbeddingProvider(
            model_name=MODEL_NAME
        )

        embedding_service = EmbeddingService(
            embedding_provider=embedding_provider,
            embedding_repository=embedding_repository,
            model_name=MODEL_NAME,
        )

        retrieval_service = SemanticRetrievalService(
            embedding_provider=embedding_provider,
            embedding_repository=embedding_repository,
        )

        print("\nCreating conversation...")

        await conversation_repository.create_conversation(
            conversation_id=conversation_id,
            user_id=user_id,
        )

        messages = [
            "PostgreSQL is the source of truth for conversation data.",
            "Redis is used as a fast caching layer.",
            "FastAPI is used to build the AI service.",
            "JWT is used for authentication and authorization.",
        ]

        print("\nCreating messages and embeddings...")

        for sequence_number, content in enumerate(messages, start=1):

            message_id = uuid4()

            message = ConversationMessage(
                id=message_id,
                conversation_id=conversation_id,
                role="user",
                content=content,
                created_at=datetime.now(timezone.utc),
                sequence_number=sequence_number,
            )

            await conversation_repository.save_message(message)

            await embedding_service.generate_and_save(
                message_id=message_id,
                conversation_id=conversation_id,
                content=content,
            )

            print(f"Saved: {content}")

        query = "Where is our permanent conversation data stored?"

        print("\n========================================")
        print("SEMANTIC SEARCH")
        print("========================================")

        print("\nQuery:")
        print(query)

        results = await retrieval_service.retrieve(
            conversation_id=conversation_id,
            query=query,
            limit=3,
        )

        print("\n========== RESULTS ==========")

        for index, result in enumerate(results, start=1):

                print(f"\nResult {index}")
                print("Message ID:", result.message.id)
                print("Conversation ID:", result.message.conversation_id)
                print("Content:", result.message.content)
                print("Role:", result.message.role)
                print("Relevance Score:", result.relevance_score)
                print("Retrieval Source:", result.retrieval_source)

        print("\n========== VALIDATION ==========")

        if not results:
            print("FAIL: No semantic results returned.")
            return

        top_result = results[0]

        print("\nTop result:")
        print(top_result.message.content)

        if "PostgreSQL" in top_result.message.content:
            print(
                "\nPASS: Semantic retrieval found the relevant message."
            )
        else:
            print(
                "\nWARNING: Top result was not the expected PostgreSQL message."
            )


if __name__ == "__main__":
    asyncio.run(main())