import chromadb
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Optional
from config import settings
import numpy as np


class RAGService:
    """
    Connects to ChromaDB and performs hybrid retrieval.
    Falls back gracefully if the collection is empty.
    """

    def __init__(self):
        self._client = None
        self._embedder = None
        self._collection = None

    def _init(self):
        if self._client is None:
            try:
                self._client = chromadb.HttpClient(
                    host=settings.CHROMA_HOST, port=settings.CHROMA_PORT
                )
                self._embedder = SentenceTransformer(settings.EMBEDDING_MODEL)
                self._collection = self._client.get_or_create_collection(
                    name="bioguru_ncert",
                    metadata={"hnsw:space": "cosine"},
                )
            except Exception as e:
                print(f"[RAGService] ChromaDB init failed: {e}. Falling back to empty context.")
                self._client = None

    def _embed_query(self, query: str) -> List[float]:
        if "e5" in settings.EMBEDDING_MODEL.lower():
            query = f"query: {query}"
        vec = self._embedder.encode([query], normalize_embeddings=True)[0]
        return vec.tolist()

    async def retrieve(
        self,
        query: str,
        chapter_filter: Optional[str] = None,
        top_k: int = 5,
        lang: str = "en",
    ) -> List[Dict]:
        self._init()
        if self._client is None or self._collection is None:
            return []

        try:
            # Extract English biology terms for non-English queries
            search_query = query
            if lang in ["hi", "hinglish", "ur"]:
                import re
                words = query.split()
                eng = [w for w in words if re.match(r"^[a-zA-Z]+$", w)]
                if eng:
                    search_query = " ".join(eng)

            query_vec = self._embed_query(search_query)
            where = {"class": {"$in": ["11", "12"]}}
            if chapter_filter:
                where["chapter"] = {"$eq": chapter_filter}

            results = self._collection.query(
                query_embeddings=[query_vec],
                n_results=min(top_k, self._collection.count() or 1),
                where=where if self._collection.count() > 0 else None,
                include=["documents", "metadatas", "distances"],
            )

            chunks = []
            for doc, meta, dist in zip(
                results["documents"][0],
                results["metadatas"][0],
                results["distances"][0],
            ):
                score = 1.0 - dist  # cosine distance → similarity
                if score >= settings.SIMILARITY_THRESHOLD:
                    chunks.append({
                        "text": doc,
                        "source": meta.get("source", "NCERT"),
                        "chapter": meta.get("chapter", "General"),
                        "class": meta.get("class", "11"),
                        "page": meta.get("page", 0),
                        "score": round(score, 4),
                    })
            return chunks

        except Exception as e:
            print(f"[RAGService] Retrieval error: {e}")
            return []
