from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.models.message_embedding import MessageEmbedding
from app.domain.models.retrieved_message import RetrievedMessage

class EmbeddingRepositoryInterface(ABC):

    @abstractmethod
    async def save(
        self,
        embedding: MessageEmbedding,
    ) -> None:
        pass

    @abstractmethod
    async def get_by_message_id(
        self,
        message_id: UUID,
    ) -> MessageEmbedding | None:
        pass

    @abstractmethod
    async def delete_by_message_id(
        self,
        message_id: UUID,
    ) -> None:
        pass

    @abstractmethod
    async def search_similar(
        self,
        conversation_id: UUID,
        query_embedding: list[float],
        limit: int,
    ) -> list[RetrievedMessage]:
        pass