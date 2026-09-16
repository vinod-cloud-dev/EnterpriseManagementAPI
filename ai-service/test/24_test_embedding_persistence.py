import asyncio
from datetime import datetime, timezone
from uuid import uuid4

from app.application.services.embedding_service import EmbeddingService
from app.infrastructure.database.database import AsyncSessionLocal
from app.infrastructure.database.repositories.embedding_repository import (
    EmbeddingRepository,
)
from app.infrastructure.database.repositories.conversation_repository import (
    ConversationRepository,
)
from app.infrastructure.embeddings.qwen_embedding_provider import (
    QwenEmbeddingProvider,
)


async def main():

    conversation_id = uuid4()
    message_id = uuid4()
    user_id = 999999

    print("Creating database session...")

    async with AsyncSessionLocal() as session:

        conversation_repository = ConversationRepository(session)

        embedding_repository = EmbeddingRepository(session)

        embedding_provider = QwenEmbeddingProvider(
            model_name="Qwen/Qwen3-Embedding-0.6B"
        )

        embedding_service = EmbeddingService(
            embedding_provider=embedding_provider,
            embedding_repository=embedding_repository,
            model_name="Qwen/Qwen3-Embedding-0.6B",
        )

        # --------------------------------------------------
        # 1. Create conversation
        # --------------------------------------------------

        print("\nCreating conversation...")

        await conversation_repository.create_conversation(
            conversation_id=conversation_id,
            user_id=user_id,
        )

        print("Conversation created:")
        print(conversation_id)

        # --------------------------------------------------
        # 2. Create message
        # --------------------------------------------------

        message = {
            "id": message_id,
            "conversation_id": conversation_id,
            "role": "user",
            "content": "PostgreSQL is the source of truth for conversation data.",
            "created_at": datetime.now(timezone.utc),
            "sequence_number": 1,
        }

        from app.domain.models.conversation_message import ConversationMessage

        domain_message = ConversationMessage(**message)

        await conversation_repository.save_message(domain_message)

        print("\nMessage created:")
        print(message_id)

        # --------------------------------------------------
        # 3. Generate embedding + save
        # --------------------------------------------------

        print("\nGenerating embedding...")

        saved_embedding = await embedding_service.generate_and_save(
            message_id=message_id,
            conversation_id=conversation_id,
            content=domain_message.content,
        )

        print("\n========== EMBEDDING SAVED ==========")

        print("Embedding ID:", saved_embedding.id)
        print("Message ID:", saved_embedding.message_id)
        print("Conversation ID:", saved_embedding.conversation_id)
        print("Model:", saved_embedding.model_name)
        print("Vector dimensions:", len(saved_embedding.embedding))

        # --------------------------------------------------
        # 4. Read embedding back from PostgreSQL
        # --------------------------------------------------

        print("\nReading embedding from PostgreSQL...")

        stored_embedding = await embedding_service.get_by_message_id(
            message_id
        )

        # --------------------------------------------------
        # 5. Validate
        # --------------------------------------------------

        print("\n========== VALIDATION ==========")

        if stored_embedding is None:
            print("FAIL: Embedding was not found.")
            return

        print("Embedding found in PostgreSQL.")

        if len(stored_embedding.embedding) != 1024:
            print(
                "FAIL: Unexpected vector dimensions:",
                len(stored_embedding.embedding),
            )
            return

        if stored_embedding.message_id != message_id:
            print("FAIL: Message ID mismatch.")
            return

        if stored_embedding.conversation_id != conversation_id:
            print("FAIL: Conversation ID mismatch.")
            return

        print("PASS: Embedding persistence test successful.")


if __name__ == "__main__":
    asyncio.run(main())