from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.interfaces.conversation_repository import (
    ConversationRepositoryInterface,
)
from app.infrastructure.database.database import get_db
from app.infrastructure.database.repositories.conversation_repository import (
    ConversationRepository,
)


def get_conversation_repository(
    session: AsyncSession = Depends(get_db),
) -> ConversationRepositoryInterface:

    return ConversationRepository(session)