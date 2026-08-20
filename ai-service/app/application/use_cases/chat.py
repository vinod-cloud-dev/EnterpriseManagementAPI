from app.application.interfaces.llm import LLMInterface

class ChatUseCase:
    def __init__(self, llm: LLMInterface) -> None:
        self.llm = llm

    async def execute(self, message: str) -> str:
        return await self.llm.generate(message)