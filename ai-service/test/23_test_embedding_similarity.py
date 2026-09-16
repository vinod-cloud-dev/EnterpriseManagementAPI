import asyncio
import math

from app.infrastructure.embeddings.qwen_embedding_provider import (
    QwenEmbeddingProvider,
)


def cosine_similarity(vector_a: list[float], vector_b: list[float]) -> float:
    dot_product = sum(a * b for a, b in zip(vector_a, vector_b))

    magnitude_a = math.sqrt(sum(a * a for a in vector_a))
    magnitude_b = math.sqrt(sum(b * b for b in vector_b))

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)


async def main():
    provider = QwenEmbeddingProvider(
    model_name="Qwen/Qwen3-Embedding-0.6B"
        )

    text_1 = "I forgot my password"
    text_2 = "I cannot remember my password"
    text_3 = "The weather is very nice today"

    print("Generating embeddings...\n")

    embedding_1 = await provider.embed(text_1)
    embedding_2 = await provider.embed(text_2)
    embedding_3 = await provider.embed(text_3)

    similarity_1_2 = cosine_similarity(embedding_1, embedding_2)
    similarity_1_3 = cosine_similarity(embedding_1, embedding_3)

    print("========== RESULTS ==========")

    print(f"\nText 1: {text_1}")
    print(f"Text 2: {text_2}")
    print(f"Text 3: {text_3}")

    print(f"\nSimilarity (Text 1 ↔ Text 2): {similarity_1_2:.4f}")
    print(f"Similarity (Text 1 ↔ Text 3): {similarity_1_3:.4f}")

    print("\n========== VALIDATION ==========")

    if similarity_1_2 > similarity_1_3:
        print("PASS: Similar sentences have higher similarity.")
    else:
        print("FAIL: Similarity result is unexpected.")


if __name__ == "__main__":
    asyncio.run(main())