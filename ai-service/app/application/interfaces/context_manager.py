from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.models.conversation_message import ConversationMessage


class ContextManagerInterface(ABC):

    @abstractmethod
    async def build_context(
        self,
        conversation_id: UUID,
        history: list[ConversationMessage],
        current_message: str,
    ) -> str:
        pass