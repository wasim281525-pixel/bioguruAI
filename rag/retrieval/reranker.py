from typing import List, Dict


class CrossEncoderReranker:
    """
    Simple score-based reranker.
    Optionally loads a cross-encoder model for true reranking if available.
    """

    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"):
        self.model = None
        try:
            from sentence_transformers import CrossEncoder
            self.model = CrossEncoder(model_name)
            print(f"[Reranker] Loaded cross-encoder: {model_name}")
        except Exception as e:
            print(f"[Reranker] CrossEncoder not available, using score passthrough: {e}")

    def rerank(self, query: str, candidates: List[Dict], top_k: int = 5) -> List[Dict]:
        if not candidates:
            return []

        if self.model is None:
            # Passthrough: already sorted by hybrid score
            return sorted(candidates, key=lambda x: x["score"], reverse=True)[:top_k]

        try:
            pairs = [(query, c["text"]) for c in candidates]
            scores = self.model.predict(pairs)
            for i, c in enumerate(candidates):
                c["rerank_score"] = float(scores[i])
            candidates.sort(key=lambda x: x["rerank_score"], reverse=True)
        except Exception as e:
            print(f"[Reranker] Reranking failed: {e}")

        return candidates[:top_k]
