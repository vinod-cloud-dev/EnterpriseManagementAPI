import httpx
from app.application.interfaces.llm import LLMInterface

class OllamaClient(LLMInterface):
    def __init__(self,base_url: str ,model: str ,) -> None:
        self.base_url = base_url
        self.model = model
        
    async def generate(self, prompt: str) -> str:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                },
            )
            response.raise_for_status()
            data = response.json()
            return data["response"]