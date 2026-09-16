import asyncio

from app.infrastructure.embeddings.qwen_embedding_provider import (
    QwenEmbeddingProvider,
)


async def main():

    provider = QwenEmbeddingProvider(
        model_name="Qwen/Qwen3-Embedding-0.6B"
    )

    text = (
        "PostgreSQL is the source of truth "
        "for conversation data."
    )

    embedding = await provider.embed(text)

    print("\nEmbedding generated successfully!")
    print("Vector dimensions:", len(embedding))
    print("First 10 values:", embedding[:10])


if __name__ == "__main__":
    asyncio.run(main())