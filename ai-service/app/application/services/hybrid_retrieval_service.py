from uuid import UUID

from app.application.interfaces.relevant_message_retriever import (
    RelevantMessageRetriever,
)
from app.domain.models.retrieved_message import RetrievedMessage


class HybridRetrievalService:
    def __init__(
        self,
        semantic_retriever: RelevantMessageRetriever,
        keyword_retriever: RelevantMessageRetriever,
        semantic_weight: float,
        keyword_weight: float,
    ) -> None:
        self._semantic_retriever = semantic_retriever
        self._keyword_retriever = keyword_retriever
        self._semantic_weight = semantic_weight
        self._keyword_weight = keyword_weight

    async def retrieve(
        self,
        conversation_id: UUID,
        query: str,
        limit: int,
    ) -> list[RetrievedMessage]:

        semantic_results = await self._semantic_retriever.retrieve(
            conversation_id=conversation_id,
            query=query,
            limit=limit,
        )

        keyword_results = await self._keyword_retriever.retrieve(
            conversation_id=conversation_id,
            query=query,
            limit=limit,
        )

        combined: dict[UUID, dict] = {}

        # Add semantic results
        for result in semantic_results:
            combined[result.message.id] = {
                "message": result.message,
                "semantic_score": result.relevance_score,
                "keyword_score": 0.0,
            }

        # Add keyword results
        for result in keyword_results:
            existing = combined.get(result.message.id)

            if existing is None:
                combined[result.message.id] = {
                    "message": result.message,
                    "semantic_score": 0.0,
                    "keyword_score": result.relevance_score,
                }
            else:
                existing["keyword_score"] = result.relevance_score

        # Calculate weighted hybrid score
        results: list[RetrievedMessage] = []

        for item in combined.values():
            hybrid_score = (
                item["semantic_score"] * self._semantic_weight
                + item["keyword_score"] * self._keyword_weight
            )

            results.append(
                RetrievedMessage(
                    message=item["message"],
                    relevance_score=hybrid_score,
                    retrieval_source="hybrid",
                )
            )

        # Highest score first
        results.sort(
            key=lambda result: (
                result.relevance_score,
                result.message.sequence_number,
            ),
            reverse=True,
        )

        return results[:limit]