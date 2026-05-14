from embeddings.embedder import MultilingualEmbedder
from typing import List, Dict
import numpy as np


def batch_embed_chunks(
    chunks: List[Dict],
    embedder: MultilingualEmbedder,
    batch_size: int = 32,
) -> List[np.ndarray]:
    """Embed all chunks in batches, return list of embedding arrays."""
    all_embeddings = []
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i: i + batch_size]
        texts = [c["text"] for c in batch]
        embeddings = embedder.embed(texts)
        all_embeddings.extend(embeddings)
        print(f"[BatchEmbed] {i + len(batch)}/{len(chunks)}")
    return all_embeddings
