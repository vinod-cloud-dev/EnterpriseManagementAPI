from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.application.interfaces.embedding_provider import EmbeddingProviderInterface
from app.application.interfaces.embedding_repository import (
    EmbeddingRepositoryInterface,
)
from app.domain.models.message_embedding import MessageEmbedding


class EmbeddingService:

    def __init__(
        self,
        embedding_provider: EmbeddingProviderInterface,
        embedding_repository: EmbeddingRepositoryInterface,
        model_name: str,
    ) -> None:
        self._embedding_provider = embedding_provider
        self._embedding_repository = embedding_repository
        self._model_name = model_name

    async def generate_and_save(
        self,
        message_id: UUID,
        conversation_id: UUID,
        content: str,
    ) -> MessageEmbedding:

        vector = await self._embedding_provider.embed(content)

        now = datetime.now(timezone.utc)

        embedding = MessageEmbedding(
            id=uuid4(),
            message_id=message_id,
            conversation_id=conversation_id,
            embedding=vector,
            model_name=self._model_name,
            created_at=now,
            updated_at=now,
        )

        await self._embedding_repository.save(embedding)

        return embedding

    async def get_by_message_id(
        self,
        message_id: UUID,
    ) -> MessageEmbedding | None:

        return await self._embedding_repository.get_by_message_id(
            message_id
        )