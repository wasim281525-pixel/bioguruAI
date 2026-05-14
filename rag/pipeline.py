import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag.embeddings.embedder import MultilingualEmbedder
from rag.vector_store.chroma_store import ChromaVectorStore
from rag.retrieval.hybrid_retriever import HybridRetriever
from rag.retrieval.reranker import CrossEncoderReranker
from typing import List, Dict, Optional
import re

SIMILARITY_THRESHOLD = float(os.environ.get("SIMILARITY_THRESHOLD", "0.5"))


class RAGPipeline:
    def __init__(self):
        model = os.environ.get("EMBEDDING_MODEL", "intfloat/multilingual-e5-large")
        chroma_host = os.environ.get("CHROMA_HOST", "chroma")
        chroma_port = int(os.environ.get("CHROMA_PORT", "8000"))

        self.embedder = MultilingualEmbedder(model=model)
        self.vector_store = ChromaVectorStore(host=chroma_host, port=chroma_port)
        self.retriever = HybridRetriever(
            embedder=self.embedder,
            vector_store=self.vector_store,
        )
        self.reranker = CrossEncoderReranker()

    async def retrieve(
        self,
        query: str,
        chapter_filter: Optional[str] = None,
        class_filter: Optional[str] = None,
        top_k: int = 5,
        lang: str = "en",
    ) -> List[Dict]:
        search_query = query
        if lang in ["hi", "hinglish", "ur"]:
            search_query = self._extract_biology_terms(query)

        candidates = await self.retriever.retrieve(
            query=search_query,
            filters={"chapter": chapter_filter, "class": class_filter},
            top_k=top_k * 3,
        )

        reranked = self.reranker.rerank(query=search_query, candidates=candidates, top_k=top_k)
        filtered = [c for c in reranked if c["score"] >= SIMILARITY_THRESHOLD]

        return filtered if filtered else reranked[:top_k]

    def _extract_biology_terms(self, text: str) -> str:
        words = text.split()
        english_words = [w for w in words if re.match(r"^[a-zA-Z\s]+$", w)]
        return " ".join(english_words) if english_words else text
