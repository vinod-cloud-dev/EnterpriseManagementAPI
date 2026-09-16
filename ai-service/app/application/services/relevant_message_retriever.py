import re
from uuid import UUID

from app.application.interfaces.conversation_repository import (
    ConversationRepositoryInterface,
)
from app.application.interfaces.relevant_message_retriever import (
    RelevantMessageRetriever,
)
from app.domain.models.retrieved_message import RetrievedMessage


class BasicRelevantMessageRetriever(RelevantMessageRetriever):

    STOPWORDS = {
        "a",
        "an",
        "and",
        "are",
        "as",
        "at",
        "be",
        "by",
        "for",
        "from",
        "has",
        "have",
        "in",
        "is",
        "it",
        "of",
        "on",
        "or",
        "that",
        "the",
        "this",
        "to",
        "was",
        "we",
        "what",
        "where",
        "with",
        "our",
        "about",
        "me",
        "tell",
        "how",
        "does",
        "do",
        "used",
        "use",
    }
    MIN_RELEVANCE_SCORE = 0.20

    def __init__(
        self,
        repository: ConversationRepositoryInterface,
    ) -> None:
        self._repository = repository

    def _normalize_text(self, text: str) -> list[str]:
        """
        Normalize text into meaningful keywords.

        Example:
        "Tell me about PostgreSQL and Redis!"
        ->
        ["postgresql", "redis"]
        """

        text = text.lower()

        # Keep only letters and numbers.
        text = re.sub(r"[^a-z0-9\s]", " ", text)

        words = text.split()

        return [
            word
            for word in words
            if word not in self.STOPWORDS
        ]

    async def retrieve(
        self,
        conversation_id: UUID,
        query: str,
        limit: int,
    ) -> list[RetrievedMessage]:

        history = await self._repository.get_history(
            conversation_id
        )

        if not history or not query.strip():
            return []

        query_words = set(
            self._normalize_text(query)
        )

        if not query_words:
            return []

        results: list[RetrievedMessage] = []

        for message in history:

            message_words = set(
                self._normalize_text(
                    message.content
                )
            )

            matching_words = (
                query_words.intersection(message_words)
            )

            if not matching_words:
                continue

            relevance_score = (len(matching_words)/ len(query_words))

            # Ignore weak keyword matches.
            if relevance_score < self.MIN_RELEVANCE_SCORE:
                continue

            results.append(
                RetrievedMessage(
                    message=message,
                    relevance_score=relevance_score,
                    retrieval_source="keyword",
                )
            )

        results.sort(
            key=lambda result: (
                result.relevance_score,
                result.message.sequence_number,
            ),
            reverse=True,
        )

        return results[:limit]