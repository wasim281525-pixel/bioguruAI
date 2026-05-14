import chromadb
import numpy as np
import uuid
from typing import List, Dict, Optional


class ChromaVectorStore:
    COLLECTION_NAME = "bioguru_ncert"

    def __init__(self, host: str = "chroma", port: int = 8000):
        self.client = chromadb.HttpClient(host=host, port=port)
        self.collection = self.client.get_or_create_collection(
            name=self.COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},
        )

    async def add_documents(self, chunks: List[Dict], embeddings: np.ndarray):
        ids = [str(uuid.uuid4()) for _ in chunks]
        documents = [c["text"] for c in chunks]
        metadatas = [
            {
                "source": c.get("source", "NCERT"),
                "chapter": c.get("chapter", ""),
                "class": str(c.get("class", "11")),
                "page": str(c.get("page", 0)),
                "type": c.get("type", "text"),
            }
            for c in chunks
        ]

        self.collection.add(
            ids=ids,
            embeddings=embeddings.tolist() if isinstance(embeddings, np.ndarray) else [e.tolist() for e in embeddings],
            documents=documents,
            metadatas=metadatas,
        )

    def query(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        where: Optional[Dict] = None,
    ) -> List[Dict]:
        kwargs = {
            "query_embeddings": [query_embedding],
            "n_results": top_k,
            "include": ["documents", "metadatas", "distances"],
        }
        if where:
            kwargs["where"] = where

        results = self.collection.query(**kwargs)

        chunks = []
        for doc, meta, dist in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        ):
            chunks.append({
                "text": doc,
                "source": meta.get("source", "NCERT"),
                "chapter": meta.get("chapter", ""),
                "class": meta.get("class", "11"),
                "page": meta.get("page", 0),
                "score": round(1.0 - dist, 4),
            })
        return chunks

    def count(self) -> int:
        return self.collection.count()
