from app.application.interfaces.context_builder import (
    ContextBuilderInterface,
)
from app.domain.models.conversation_message import ConversationMessage


class ContextBuilder(ContextBuilderInterface):

    def build(
        self,
        history: list[ConversationMessage],
        current_message: str,
        summary: str | None = None,
    ) -> str:

        parts: list[str] = []

        if summary:
            parts.append(
                f"conversation summary:\n{summary}"
            )

        if history:
            conversation = "\n".join(
                f"{message.role}: {message.content}"
                for message in history
            )
            parts.append(conversation)

        parts.append(f"user: {current_message}")
        parts.append("assistant:")

        return "\n".join(parts)