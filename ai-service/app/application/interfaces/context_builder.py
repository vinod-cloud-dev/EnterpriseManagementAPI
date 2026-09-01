from abc import ABC, abstractmethod
from app.domain.models.conversation_message import ConversationMessage

class ContextBuilderInterface(ABC):
    @abstractmethod
    def build(
        self,
        history: list[ConversationMessage],
        current_message: str,
    ) -> str:
        pass