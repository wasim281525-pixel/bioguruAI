from typing import List, Dict, Optional


class SemanticRetriever:
    def __init__(self, embedder, vector_store):
        self.embedder = embedder
        self.vector_store = vector_store

    def retrieve(self, query: str, top_k: int = 5, where: Optional[Dict] = None) -> List[Dict]:
        query_vec = self.embedder.embed_query(query)
        return self.vector_store.query(
            query_embedding=query_vec.tolist(),
            top_k=top_k,
            where=where,
        )
