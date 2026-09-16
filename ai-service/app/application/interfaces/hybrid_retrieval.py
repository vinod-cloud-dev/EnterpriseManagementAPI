from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.models.relevant_message import RelevantMessage


class HybridRetrievalInterface(ABC):

    @abstractmethod
    async def retrieve(
        self,
        conversation_id: UUID,
        query: str,
        limit: int,
    ) -> list[RelevantMessage]:
        pass