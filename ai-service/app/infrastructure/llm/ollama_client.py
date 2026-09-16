
import time
import httpx
from app.application.interfaces.llm import LLMInterface

class OllamaClient(LLMInterface):

    def __init__(self, base_url: str, model: str) -> None:
        self.base_url = base_url
        self.model = model

    async def generate(self, prompt: str) -> str:

        print("\n========== OLLAMA DEBUG ==========")
        print(f"Model: {self.model}")
        print(f"Prompt characters: {len(prompt)}")
        print(f"Prompt preview: {prompt[:500]}")

        start_time = time.perf_counter()

        async with httpx.AsyncClient(timeout=300.0) as client:

            request_start = time.perf_counter()

            response = await client.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                },
            )

            request_end = time.perf_counter()

            print(
                f"HTTP request time: "
                f"{request_end - request_start:.2f} seconds"
            )

            response.raise_for_status()

            data = response.json()

        end_time = time.perf_counter()

        print(
            f"Total OllamaClient time: "
            f"{end_time - start_time:.2f} seconds"
        )

        print("==================================\n")

        return data["response"]

