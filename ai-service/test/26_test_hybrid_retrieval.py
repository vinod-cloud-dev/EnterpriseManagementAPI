import asyncio
from datetime import datetime, timezone
from uuid import uuid4

from app.application.services.embedding_service import EmbeddingService
from app.application.services.semantic_retrieval_service import (
    SemanticRetrievalService,
)
from app.application.services.hybrid_retrieval_service import (
    HybridRetrievalService,
)
from app.application.services.relevant_message_retriever import (
    BasicRelevantMessageRetriever,
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
    user_id = 999997

    print("Creating database session...")

    async with AsyncSessionLocal() as session:

        # --------------------------------------------------
        # 1. Create repositories
        # --------------------------------------------------

        conversation_repository = ConversationRepository(
            session
        )

        embedding_repository = EmbeddingRepository(
            session
        )

        # --------------------------------------------------
        # 2. Create embedding provider
        # --------------------------------------------------

        embedding_provider = QwenEmbeddingProvider(
            model_name=MODEL_NAME
        )

        # --------------------------------------------------
        # 3. Create embedding service
        # --------------------------------------------------

        embedding_service = EmbeddingService(
            embedding_provider=embedding_provider,
            embedding_repository=embedding_repository,
            model_name=MODEL_NAME,
        )

        # --------------------------------------------------
        # 4. Create semantic retriever
        # --------------------------------------------------

        semantic_retriever = SemanticRetrievalService(
            embedding_provider=embedding_provider,
            embedding_repository=embedding_repository,
        )

        # --------------------------------------------------
        # 5. Create keyword retriever
        # --------------------------------------------------

        keyword_retriever = BasicRelevantMessageRetriever(
            repository=conversation_repository
        )

        # --------------------------------------------------
        # 6. Create hybrid retriever
        # --------------------------------------------------

        hybrid_retriever = HybridRetrievalService(
            semantic_retriever=semantic_retriever,
            keyword_retriever=keyword_retriever,
            semantic_weight=0.7,
            keyword_weight=0.3,
        )

        # --------------------------------------------------
        # 7. Create conversation
        # --------------------------------------------------

        print("\nCreating conversation...")

        await conversation_repository.create_conversation(
            conversation_id=conversation_id,
            user_id=user_id,
        )

        print("Conversation ID:")
        print(conversation_id)

        # --------------------------------------------------
        # 8. Create messages + embeddings
        # --------------------------------------------------

        messages = [
            "PostgreSQL is the source of truth for conversation data.",
            "Redis is used as a fast caching layer.",
            "FastAPI is used to build the AI service.",
            "JWT is used for authentication and authorization.",
        ]

        print("\nCreating messages and embeddings...")

        for sequence_number, content in enumerate(
            messages,
            start=1,
        ):

            message_id = uuid4()

            message = ConversationMessage(
                id=message_id,
                conversation_id=conversation_id,
                role="user",
                content=content,
                created_at=datetime.now(timezone.utc),
                sequence_number=sequence_number,
            )

            # Save message
            await conversation_repository.save_message(
                message
            )

            # Generate + save embedding
            await embedding_service.generate_and_save(
                message_id=message_id,
                conversation_id=conversation_id,
                content=content,
            )

            print(f"Saved: {content}")

        # --------------------------------------------------
        # 9. Query
        # --------------------------------------------------

        query = (
            "Where is our permanent conversation data stored?"
        )

        print("\n========================================")
        print("HYBRID SEARCH")
        print("========================================")

        print("\nQuery:")
        print(query)

        # --------------------------------------------------
        # 10. Execute hybrid retrieval
        # --------------------------------------------------

        results = await hybrid_retriever.retrieve(
            conversation_id=conversation_id,
            query=query,
            limit=3,
        )

        # --------------------------------------------------
        # 11. Display results
        # --------------------------------------------------

        print("\n========== HYBRID RESULTS ==========")

        for index, result in enumerate(
            results,
            start=1,
        ):

            print(f"\nResult {index}")

            print(
                "Message ID:",
                result.message.id,
            )

            print(
                "Conversation ID:",
                result.message.conversation_id,
            )

            print(
                "Content:",
                result.message.content,
            )

            print(
                "Role:",
                result.message.role,
            )

            print(
                "Relevance Score:",
                result.relevance_score,
            )

            print(
                "Retrieval Source:",
                result.retrieval_source,
            )

        # --------------------------------------------------
        # 12. Validation
        # --------------------------------------------------

        print("\n========== VALIDATION ==========")

        # No results
        if not results:

            print(
                "FAIL: Hybrid retrieval returned no results."
            )

            return

        print(
            "PASS: Hybrid retrieval returned results."
        )

        # --------------------------------------------------
        # 13. Check duplicates
        # --------------------------------------------------

        message_ids = [
            result.message.id
            for result in results
        ]

        unique_message_ids = set(message_ids)

        if len(message_ids) == len(unique_message_ids):

            print(
                "PASS: No duplicate messages."
            )

        else:

            print(
                "FAIL: Duplicate messages found."
            )

        # --------------------------------------------------
        # 14. Check retrieval sources
        # --------------------------------------------------

        retrieval_sources = {
            result.retrieval_source
            for result in results
        }

        print(
            "\nRetrieval sources:",
            retrieval_sources,
        )

        # --------------------------------------------------
        # 15. Check top result
        # --------------------------------------------------

        top_result = results[0]

        print("\nTop result:")
        print(top_result.message.content)

        if "PostgreSQL" in top_result.message.content:

            print(
                "\nPASS: PostgreSQL message ranked first."
            )

        else:

            print(
                "\nWARNING: PostgreSQL message was not ranked first."
            )


if __name__ == "__main__":
    asyncio.run(main())