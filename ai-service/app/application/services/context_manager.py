from datetime import datetime, timezone
from uuid import UUID

from app.application.interfaces.context_manager import (
    ContextManagerInterface,
)
from app.application.interfaces.context_builder import (
    ContextBuilderInterface,
)
from app.application.interfaces.token_counter import (
    TokenCounterInterface,
)
from app.application.interfaces.conversation_repository import (
    ConversationRepositoryInterface,
)
from app.application.interfaces.conversation_summarizer import (
    ConversationSummarizerInterface,
)
from app.domain.models.conversation_message import ConversationMessage
from app.domain.models.conversation_summary import ConversationSummary
from app.application.interfaces.relevant_message_retriever import (
    RelevantMessageRetriever,
)

class ContextManager(ContextManagerInterface):

    def __init__(
        self,
        context_builder: ContextBuilderInterface,
        token_counter: TokenCounterInterface,
        repository: ConversationRepositoryInterface,
        summarizer: ConversationSummarizerInterface,
        relevant_message_retriever: RelevantMessageRetriever,
        max_context_tokens: int,
        max_output_tokens: int,
        relevant_message_limit: int,
    ) -> None:
        self._context_builder = context_builder
        self._token_counter = token_counter
        self._repository = repository
        self._summarizer = summarizer
        self._relevant_message_retriever = relevant_message_retriever
        self._max_context_tokens = max_context_tokens
        self._max_output_tokens = max_output_tokens
        self._relevant_message_limit = relevant_message_limit
        

    async def build_context(
        self,
        conversation_id: UUID,
        history: list[ConversationMessage],
        current_message: str,
    ) -> str:

        current_message_tokens = self._token_counter.count_text(
            current_message
        )

        available_tokens = (
            self._max_context_tokens
            - self._max_output_tokens
            - current_message_tokens
        )
         # 1. Select recent messages first
        selected_history: list[ConversationMessage] = []
        used_tokens = 0

        for message in reversed(history):
            message_tokens = self._token_counter.count_text(
                message.content
            )

            if used_tokens + message_tokens > available_tokens:
                break

            selected_history.insert(0, message)
            used_tokens += message_tokens
        # 2. Retrieve relevant messages
        relevant_messages = await self._relevant_message_retriever.retrieve(
            conversation_id=conversation_id,
            query=current_message,
               limit=self._relevant_message_limit,

        )
        
    # 3. Remove duplicates
    #    Recent history has priority
    # ---------------------------------------------------------

        recent_message_ids = {
            message.id
            for message in selected_history
        }

        deduplicated_relevant_messages = [
            result
            for result in relevant_messages
            if result.message.id not in recent_message_ids
        ]
        
        print("\n========== AFTER DEDUP ==========")

        for result in deduplicated_relevant_messages:
            print(
                result.message.sequence_number,
                result.message.id
            )

        print("=================================\n")
            # 4. Allocate remaining token budget to relevant messages
            # ---------------------------------------------------------

        remaining_tokens = available_tokens - used_tokens

        selected_relevant_messages = []

        for result in deduplicated_relevant_messages:

            message_tokens = self._token_counter.count_text(
                result.message.content
            )

            if message_tokens > remaining_tokens:
                continue

            selected_relevant_messages.append(result)
            remaining_tokens -= message_tokens
            
        print("\n========== DEDUP DEBUG ==========")

        print("Recent message IDs:")
        for message in selected_history:
            print(message.id)

        print("\nRelevant message IDs:")
        for result in deduplicated_relevant_messages:
            print(result.message.id)

        print("=================================\n")
        summary = await self._repository.get_summary(
            conversation_id
        
        )

        unsummarized_messages: list[ConversationMessage] = []

        summarized_until = (
            summary.summarized_until_sequence
            if summary
            else 0
        )

        selected_history_ids = {
            message.id
            for message in selected_history
        }

        for message in history:
            if (
                message.sequence_number > summarized_until
                and message.id not in selected_history_ids
            ):
                unsummarized_messages.append(message)
                
        # 6. Update summary if required
        if unsummarized_messages:

            existing_summary = (
                summary.summary
                if summary
                else None
            )

            updated_summary = await self._summarizer.summarize(
                existing_summary,
                unsummarized_messages,
            )

            latest_sequence = max(
                message.sequence_number
                for message in unsummarized_messages
            )

            now = datetime.now(timezone.utc)

            summary = ConversationSummary(
                conversation_id=conversation_id,
                summary=updated_summary,
                summarized_until_sequence=latest_sequence,
                created_at=(
                    summary.created_at
                    if summary
                    else now
                ),
                updated_at=now,
            )

            await self._repository.save_summary(summary)

        return self._context_builder.build(
            selected_history,
            current_message,
            summary.summary if summary else None,
            selected_relevant_messages,
        )