from abc import ABC, abstractmethod

class TokenCounterInterface(ABC):
    @abstractmethod
    def count_text(self, text: str) -> int:
        pass