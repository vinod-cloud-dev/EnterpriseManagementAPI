from abc import ABC, abstractmethod
from uuid import UUID
from app.domain.models.retrieved_message import RetrievedMessage

class RelevantMessageRetriever(ABC):

    @abstractmethod
    async def retrieve(
        self,
        conversation_id: UUID,
        query: str,
        limit: int,
    ) -> list[RetrievedMessage]:
        pass