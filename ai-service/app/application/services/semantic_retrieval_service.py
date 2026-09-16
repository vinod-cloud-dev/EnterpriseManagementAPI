from uuid import UUID

from app.application.interfaces.embedding_provider import (
    EmbeddingProviderInterface,
)
from app.application.interfaces.embedding_repository import (
    EmbeddingRepositoryInterface,
)
from app.domain.models.retrieved_message import RetrievedMessage

class SemanticRetrievalService:

    def __init__(
        self,
        embedding_provider: EmbeddingProviderInterface,
        embedding_repository: EmbeddingRepositoryInterface,
    ) -> None:
        self._embedding_provider = embedding_provider
        self._embedding_repository = embedding_repository

    async def retrieve(
        self,
        conversation_id: UUID,
        query: str,
        limit: int,
    ) -> list[RetrievedMessage]:

        query_embedding = await self._embedding_provider.embed(
            query
        )

        return await self._embedding_repository.search_similar(
            conversation_id=conversation_id,
            query_embedding=query_embedding,
            limit=limit,
        )