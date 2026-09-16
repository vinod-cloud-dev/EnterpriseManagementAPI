from sentence_transformers import SentenceTransformer

from app.application.interfaces.embedding_provider import (
    EmbeddingProviderInterface,
)

class QwenEmbeddingProvider(EmbeddingProviderInterface):

    def __init__(self, model_name: str) -> None:
        self._model = SentenceTransformer(model_name)

    async def embed(self, text: str) -> list[float]:
        embedding = self._model.encode(
            text,
            normalize_embeddings=True,
        )

        return embedding.tolist()