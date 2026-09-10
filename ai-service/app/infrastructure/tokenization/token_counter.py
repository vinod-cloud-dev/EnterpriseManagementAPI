from app.application.interfaces.token_counter import (
    TokenCounterInterface,
)

class TokenCounter(TokenCounterInterface):

    def count_text(self, text: str) -> int:
        # Temporary implementation.
        # This will be replaced with the actual model tokenizer.
        return len(text.split())