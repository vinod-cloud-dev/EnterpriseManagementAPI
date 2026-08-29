from abc import ABC, abstractmethod
from uuid import UUID
from app.domain.models.conversation_message import ConversationMessage

class ConversationRepositoryInterface(ABC):
    @abstractmethod
    async def save_message(self,message: ConversationMessage,) -> None:
        pass

    @abstractmethod
    async def get_history(self,conversation_id: UUID,) -> list[ConversationMessage]:
        pass