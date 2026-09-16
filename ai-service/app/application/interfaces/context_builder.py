from abc import ABC, abstractmethod
from app.domain.models.conversation_message import ConversationMessage
from app.domain.models.retrieved_message import RetrievedMessage

class ContextBuilderInterface(ABC):

    @abstractmethod
    def build(
        self,
        history: list[ConversationMessage],
        current_message: str,
        summary: str | None = None,
        relevant_messages: list[RetrievedMessage] | None = None,
    ) -> str:
        pass