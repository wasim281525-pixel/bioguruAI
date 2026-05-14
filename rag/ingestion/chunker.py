from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List, Dict
import re


class BiologyChunker:
    def __init__(self, chunk_size: int = 512, overlap: int = 64):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=overlap,
            separators=["\n\n", "\n", ". ", "? ", "! ", " "],
        )

    def chunk_document(self, text: str, metadata: Dict) -> List[Dict]:
        text = self._clean_biology_text(text)
        if not text.strip():
            return []

        chunks = self.splitter.split_text(text)
        return [
            {
                "text": chunk,
                "source": metadata.get("source", "NCERT"),
                "chapter": metadata.get("chapter", ""),
                "chapter_num": metadata.get("chapter_num", 0),
                "class": str(metadata.get("class", "11")),
                "page": metadata.get("page", 0),
                "type": metadata.get("type", "text"),
            }
            for chunk in chunks
            if chunk.strip()
        ]

    def _clean_biology_text(self, text: str) -> str:
        text = re.sub(r"\s+", " ", text)
        text = re.sub(r"Page \d+", "", text)
        text = re.sub(r"NCERT|©|\x0c", "", text)
        return text.strip()
