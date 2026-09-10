from app.application.interfaces.conversation_memory import (
    ConversationMemoryInterface,
)
from app.infrastructure.memory.redis_conversation_memory import (
    RedisConversationMemory,
)

# For InMemory storage, uncomment the following line
# and comment out the RedisConversationMemory line.
# _memory = InMemoryConversationMemory()

# For Redis storage, uncomment the following line
# and comment out the InMemoryConversationMemory line.
_memory = RedisConversationMemory()


def get_memory() -> ConversationMemoryInterface:
    return _memory