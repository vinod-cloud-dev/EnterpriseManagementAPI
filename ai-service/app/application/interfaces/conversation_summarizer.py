from abc import ABC, abstractmethod
from app.domain.models.conversation_message import ConversationMessage

class ConversationSummarizerInterface(ABC):
    @abstractmethod
    async def summarize(
        self,
        existing_summary: str | None,
        messages: list[ConversationMessage],
    ) -> str:
        pass