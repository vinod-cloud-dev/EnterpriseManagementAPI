
import asyncio
import time

from app.infrastructure.llm.ollama_client import OllamaClient


async def main() -> None:

    client = OllamaClient(
        base_url="http://localhost:11434",
        model="qwen3:1.7b",
    )

    print("Testing Ollama...")
    print("Model: qwen3:1.7b")
    print("URL: http://localhost:11434")
    print()

    start_time = time.perf_counter()

    response = await client.generate("Are you working?")

    end_time = time.perf_counter()

    elapsed_time = end_time - start_time

    print("\nAI Response:")
    print(response)

    print(f"\nResponse time: {elapsed_time:.2f} seconds")


if __name__ == "__main__":
    asyncio.run(main())
