from abc import ABC, abstractmethod

class EmbeddingProviderInterface(ABC):

    @abstractmethod
    async def embed(self, text: str) -> list[float]:
        pass