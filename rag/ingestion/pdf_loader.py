import fitz  # PyMuPDF
import pdfplumber
from typing import List
import os


class PDFLoader:
    def load(self, filepath: str) -> List[str]:
        """Load PDF and return list of page texts"""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"PDF not found: {filepath}")

        pages = []
        try:
            # Primary: PyMuPDF (fast, good for text-based PDFs)
            doc = fitz.open(filepath)
            for page in doc:
                text = page.get_text("text")
                if text.strip():
                    pages.append(text)
            doc.close()

            # Fallback to pdfplumber for pages with no text (scanned)
            if not any(pages):
                with pdfplumber.open(filepath) as pdf:
                    for page in pdf.pages:
                        text = page.extract_text() or ""
                        pages.append(text)
        except Exception as e:
            print(f"[PDFLoader] Error loading {filepath}: {e}")

        return pages
