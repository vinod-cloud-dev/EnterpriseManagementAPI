from app.application.interfaces.conversation_memory import (
    ConversationMemoryInterface,
)
from app.infrastructure.memory.in_memory_conversation_memory import (
    InMemoryConversationMemory,
)
_memory = InMemoryConversationMemory()

def get_memory() -> ConversationMemoryInterface:
    return _memory