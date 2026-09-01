from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.application.interfaces.conversation_memory import (ConversationMemoryInterface,)
from app.infrastructure.memory.in_memory_conversation_memory import (InMemoryConversationMemory,)
from app.infrastructure.memory.redis_conversation_memory import (RedisConversationMemory,)
from app.application.interfaces.conversation_repository import (ConversationRepositoryInterface,)
from app.infrastructure.database.database import get_db
from app.infrastructure.database.repositories.conversation_repository import (ConversationRepository,)

#For Inmemory storage, uncomment the following line and comment out the RedisConversationMemory line.
# _memory = InMemoryConversationMemory()

#For Redis storage, uncomment the following line and comment out the InMemoryConversationMemory line.
_memory = RedisConversationMemory()

def get_memory() -> ConversationMemoryInterface:
    return _memory

def get_conversation_repository(
    session: AsyncSession = Depends(get_db),
        ) -> ConversationRepositoryInterface:
    return ConversationRepository(session)