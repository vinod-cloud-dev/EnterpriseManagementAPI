from app.application.interfaces.conversation_summarizer import (
    ConversationSummarizerInterface,
)
from app.application.interfaces.llm import LLMInterface
from app.domain.models.conversation_message import ConversationMessage


class ConversationSummarizer(ConversationSummarizerInterface):

    def __init__(self, llm: LLMInterface) -> None:
        self._llm = llm

    async def summarize(
        self,
        existing_summary: str | None,
        messages: list[ConversationMessage],
    ) -> str:

        if not messages:
            return existing_summary or ""

        conversation_text = "\n".join(
            f"{message.role}: {message.content}"
            for message in messages
        )

        existing_summary_text = (
            existing_summary
            if existing_summary
            else "No previous summary exists."
        )

        prompt = f"""
Update the existing conversation summary using the new conversation messages.

Existing Summary:
{existing_summary_text}

New Conversation Messages:
{conversation_text}

Create an updated summary.

Preserve:
- Important facts
- User requirements
- Decisions made
- Important technical details
- Unresolved questions
- Relevant context needed for future messages

Rules:
- Preserve important information from the existing summary.
- Incorporate important information from the new messages.
- Remove information only if it is clearly outdated or contradicted.
- Do not invent information.
- Keep the summary concise and useful for future conversation context.

Updated Summary:
""".strip()

        return await self._llm.generate(prompt)