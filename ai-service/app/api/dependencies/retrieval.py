from fastapi import Depends

from app.application.interfaces.relevant_message_retriever import (
    RelevantMessageRetriever,
)
from app.application.services.hybrid_retrieval_service import (
    HybridRetrievalService,
)
from app.application.services.relevant_message_retriever import (
    BasicRelevantMessageRetriever,
)
from app.application.services.semantic_retrieval_service import (
    SemanticRetrievalService,
)
from app.core.config.settings import get_settings
from app.infrastructure.database.database import get_db
from app.infrastructure.database.repositories.conversation_repository import (
    ConversationRepository,
)
from app.infrastructure.database.repositories.embedding_repository import (
    EmbeddingRepository,
)
from app.infrastructure.embeddings.qwen_embedding_provider import (
    QwenEmbeddingProvider,
)
from sqlalchemy.ext.asyncio import AsyncSession


def get_semantic_retriever(
    session: AsyncSession = Depends(get_db),
) -> RelevantMessageRetriever:
    settings = get_settings()

    embedding_provider = QwenEmbeddingProvider(
        model_name=settings.embedding_model
    )

    embedding_repository = EmbeddingRepository(session)

    return SemanticRetrievalService(
        embedding_provider=embedding_provider,
        embedding_repository=embedding_repository,
    )


def get_keyword_retriever(
    session: AsyncSession = Depends(get_db),
) -> RelevantMessageRetriever:
    repository = ConversationRepository(session)

    return BasicRelevantMessageRetriever(
        repository=repository
    )


def get_hybrid_retriever(
    semantic_retriever: RelevantMessageRetriever = Depends(
        get_semantic_retriever
    ),
    keyword_retriever: RelevantMessageRetriever = Depends(
        get_keyword_retriever
    ),
) -> HybridRetrievalService:

    settings = get_settings()

    return HybridRetrievalService(
        semantic_retriever=semantic_retriever,
        keyword_retriever=keyword_retriever,
        semantic_weight=settings.hybrid_semantic_weight,
        keyword_weight=settings.hybrid_keyword_weight,
    )