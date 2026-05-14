from rank_bm25 import BM25Okapi
from typing import List, Dict, Optional
import numpy as np


class HybridRetriever:
    """Combines dense (semantic) and sparse (BM25) retrieval."""

    def __init__(self, embedder, vector_store):
        self.embedder = embedder
        self.vector_store = vector_store

    async def retrieve(
        self,
        query: str,
        filters: Optional[Dict] = None,
        top_k: int = 10,
    ) -> List[Dict]:
        # Dense retrieval
        query_vec = self.embedder.embed_query(query)
        where = self._build_where(filters)

        try:
            dense_results = self.vector_store.query(
                query_embedding=query_vec.tolist(),
                top_k=top_k,
                where=where,
            )
        except Exception as e:
            print(f"[HybridRetriever] Dense retrieval error: {e}")
            dense_results = []

        if not dense_results:
            return []

        # BM25 re-scoring on the dense candidates
        corpus = [r["text"] for r in dense_results]
        tokenized = [doc.lower().split() for doc in corpus]

        if tokenized:
            bm25 = BM25Okapi(tokenized)
            bm25_scores = bm25.get_scores(query.lower().split())

            for i, result in enumerate(dense_results):
                bm25_score = float(bm25_scores[i]) if i < len(bm25_scores) else 0.0
                # Hybrid: 70% dense + 30% BM25 (normalized)
                max_bm25 = max(bm25_scores) if bm25_scores.any() else 1.0
                norm_bm25 = bm25_score / max_bm25 if max_bm25 > 0 else 0.0
                result["score"] = round(0.7 * result["score"] + 0.3 * norm_bm25, 4)

            dense_results.sort(key=lambda x: x["score"], reverse=True)

        return dense_results[:top_k]

    def _build_where(self, filters: Optional[Dict]) -> Optional[Dict]:
        if not filters:
            return None
        conditions = {}
        if filters.get("chapter"):
            conditions["chapter"] = {"$eq": filters["chapter"]}
        if filters.get("class"):
            conditions["class"] = {"$eq": str(filters["class"])}
        return conditions if conditions else None
