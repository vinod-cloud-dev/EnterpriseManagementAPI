from app.application.interfaces.context_builder import (
    ContextBuilderInterface,
)
from app.domain.models.conversation_message import ConversationMessage
from app.domain.models.retrieved_message import RetrievedMessage


class ContextBuilder(ContextBuilderInterface):

    def build(
        self,
        history: list[ConversationMessage],
        current_message: str,
        summary: str | None = None,
        relevant_messages: list[RetrievedMessage] | None = None,
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
        if relevant_messages:
            relevant_context = "\n".join(
                f"{result.message.role}: {result.message.content}"
                for result in relevant_messages
            )

            parts.append(
                f"relevant conversation:\n{relevant_context}"
            )
        parts.append(f"user: {current_message}")
        parts.append("assistant:")

        return "\n".join(parts)