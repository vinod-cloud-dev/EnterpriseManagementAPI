from collections import defaultdict
from uuid import UUID
from app.application.interfaces.conversation_memory import (ConversationMemoryInterface,)
from app.domain.models.conversation_message import ConversationMessage

class InMemoryConversationMemory(ConversationMemoryInterface):
    def __init__(self) -> None:
        self._conversations: dict[UUID,list[ConversationMessage],] = defaultdict(list)

    async def get_history(self,conversation_id: UUID,) -> list[ConversationMessage]:
        return list(self._conversations[conversation_id])

    async def add_message(self,message: ConversationMessage,) -> None:
        self._conversations[message.conversation_id].append(message)