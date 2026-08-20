from abc import ABC, abstractmethod
from uuid import UUID
from app.domain.models.conversation_message import ConversationMessage

class ConversationMemoryInterface(ABC):
    @abstractmethod
    async def get_history(self,conversation_id: UUID,) -> list[ConversationMessage]:
        pass

    @abstractmethod
    async def add_message(self,message: ConversationMessage,) -> None:
        pass