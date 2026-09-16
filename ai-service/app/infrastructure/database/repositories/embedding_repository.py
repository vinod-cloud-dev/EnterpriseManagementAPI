from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.interfaces.embedding_repository import (
    EmbeddingRepositoryInterface,
)
from app.domain.models.message_embedding import MessageEmbedding as DomainMessageEmbedding
from app.infrastructure.database.models.message_embedding import (
    MessageEmbedding as MessageEmbeddingModel,
)
from app.domain.models.relevant_message import RelevantMessage
from app.infrastructure.database.models.conversation_message import (
    ConversationMessage,
)
from app.domain.models.retrieved_message import RetrievedMessage

class EmbeddingRepository(EmbeddingRepositoryInterface):

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, embedding: DomainMessageEmbedding) -> None:
        """
        Save or update an embedding for a message.

        message_id is unique, so re-embedding the same message
        updates the existing record instead of creating duplicates.
        """

        result = await self._session.execute(
            select(MessageEmbeddingModel).where(
                MessageEmbeddingModel.message_id == embedding.message_id
            )
        )

        existing = result.scalar_one_or_none()

        if existing is None:
            db_embedding = MessageEmbeddingModel(
                id=embedding.id,
                message_id=embedding.message_id,
                conversation_id=embedding.conversation_id,
                embedding=embedding.embedding,
                model_name=embedding.model_name,
                created_at=embedding.created_at,
                updated_at=embedding.updated_at,
            )

            self._session.add(db_embedding)

        else:
            existing.embedding = embedding.embedding
            existing.model_name = embedding.model_name
            existing.updated_at = embedding.updated_at

        await self._session.commit()

    async def get_by_message_id(
        self,
        message_id: UUID,
    ) -> DomainMessageEmbedding | None:

        result = await self._session.execute(
            select(MessageEmbeddingModel).where(
                MessageEmbeddingModel.message_id == message_id
            )
        )

        db_embedding = result.scalar_one_or_none()

        if db_embedding is None:
            return None

        return self._to_domain(db_embedding)

    async def delete_by_message_id(
        self,
        message_id: UUID,
    ) -> None:

        await self._session.execute(
            delete(MessageEmbeddingModel).where(
                MessageEmbeddingModel.message_id == message_id
            )
        )

        await self._session.commit()

    async def search_similar(
        self,
        conversation_id: UUID,
        query_embedding: list[float],
        limit: int,
    ) -> list[RelevantMessage]:

        distance = MessageEmbeddingModel.embedding.cosine_distance(
            query_embedding
        )

        result = await self._session.execute(
            select(
                MessageEmbeddingModel.message_id,
                MessageEmbeddingModel.conversation_id,
                ConversationMessage.content,
                ConversationMessage.role,
                distance.label("distance"),
            )
            .join(
                ConversationMessage,
                MessageEmbeddingModel.message_id
                == ConversationMessage.id,
            )
            .where(
                MessageEmbeddingModel.conversation_id == conversation_id
            )
            .order_by(distance)
            .limit(limit)
        )

        rows = result.all()

        return [
            RetrievedMessage(
                message=ConversationMessage(
                    id=message_id,
                    conversation_id=conversation_id,
                    role=role,
                    content=content,
                    created_at=None,
                    sequence_number=0,
                ),
                relevance_score=1.0 - float(distance_value),
                retrieval_source="semantic",
            )
            for (
                message_id,
                conversation_id,
                content,
                role,
                distance_value,
            ) in rows
        ]

    @staticmethod
    def _to_domain(
        db_embedding: MessageEmbeddingModel,
    ) -> DomainMessageEmbedding:

        return DomainMessageEmbedding(
            id=db_embedding.id,
            message_id=db_embedding.message_id,
            conversation_id=db_embedding.conversation_id,
            embedding=list(db_embedding.embedding),
            model_name=db_embedding.model_name,
            created_at=db_embedding.created_at,
            updated_at=db_embedding.updated_at,
        )