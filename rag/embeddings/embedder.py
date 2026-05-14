from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List


class MultilingualEmbedder:
    """
    Supports:
    - intfloat/multilingual-e5-large (768 dims, 100+ languages)
    - BAAI/bge-m3 (1024 dims, state-of-art multilingual)
    - sentence-transformers/paraphrase-multilingual-mpnet-base-v2
    """

    def __init__(self, model: str = "intfloat/multilingual-e5-large"):
        print(f"[Embedder] Loading model: {model}")
        self.model = SentenceTransformer(model)
        self.model_name = model

    def embed(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings with E5 instruction prefix if needed"""
        if "e5" in self.model_name.lower():
            texts = [f"passage: {t}" for t in texts]
        return self.model.encode(texts, normalize_embeddings=True, show_progress_bar=False)

    def embed_query(self, query: str) -> np.ndarray:
        if "e5" in self.model_name.lower():
            query = f"query: {query}"
        return self.model.encode([query], normalize_embeddings=True)[0]
