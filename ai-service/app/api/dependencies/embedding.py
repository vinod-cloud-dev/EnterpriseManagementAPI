from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.interfaces.embedding_provider import (
    EmbeddingProviderInterface,
)
from app.application.interfaces.embedding_repository import (
    EmbeddingRepositoryInterface,
)
from app.application.services.embedding_service import EmbeddingService
from app.core.config.settings import get_settings
from app.infrastructure.database.database import get_db
from app.infrastructure.database.repositories.embedding_repository import (
    EmbeddingRepository,
)
from app.infrastructure.embeddings.qwen_embedding_provider import (
    QwenEmbeddingProvider,
)


def get_embedding_provider() -> EmbeddingProviderInterface:
    settings = get_settings()

    return QwenEmbeddingProvider(
        model_name=settings.embedding_model,
    )


def get_embedding_repository(
    session: AsyncSession = Depends(get_db),
) -> EmbeddingRepositoryInterface:
    return EmbeddingRepository(session)


def get_embedding_service(
    embedding_provider: EmbeddingProviderInterface = Depends(
        get_embedding_provider
    ),
    embedding_repository: EmbeddingRepositoryInterface = Depends(
        get_embedding_repository
    ),
) -> EmbeddingService:

    settings = get_settings()

    return EmbeddingService(
        embedding_provider=embedding_provider,
        embedding_repository=embedding_repository,
        model_name=settings.embedding_model,
    )