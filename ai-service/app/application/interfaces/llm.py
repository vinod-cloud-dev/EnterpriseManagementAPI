from abc import ABC, abstractmethod

class LLMInterface(ABC):
    @abstractmethod
    async def generate(self, prompt: str) -> str:
        pass