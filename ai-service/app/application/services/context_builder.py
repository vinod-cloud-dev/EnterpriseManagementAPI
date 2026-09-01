from app.application.interfaces.context_builder import (ContextBuilderInterface,)
from app.domain.models.conversation_message import ConversationMessage

class ContextBuilder(ContextBuilderInterface):

    def build(
        self,
        history: list[ConversationMessage],
        current_message: str,
    ) -> str:

        conversation = "\n".join(
            f"{message.role}: {message.content}"
            for message in history
        )

        return (
            f"{conversation}\n"
            f"user: {current_message}\n"
            f"assistant:"
        )