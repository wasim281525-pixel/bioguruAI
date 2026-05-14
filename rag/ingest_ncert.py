"""
Usage:
    python rag/ingest_ncert.py --source data/ncert/class11 --class 11
    python rag/ingest_ncert.py --source data/ncert/class12 --class 12
"""
import asyncio
import argparse
import os
import sys

# Ensure local imports resolve
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag.ingestion.pdf_loader import PDFLoader
from rag.ingestion.chunker import BiologyChunker
from rag.ingestion.metadata_extractor import extract_metadata_from_filename
from rag.embeddings.embedder import MultilingualEmbedder
from rag.vector_store.chroma_store import ChromaVectorStore
from pathlib import Path


async def ingest_folder(source_dir: str, class_level: str):
    chroma_host = os.environ.get("CHROMA_HOST", "chroma")
    chroma_port = int(os.environ.get("CHROMA_PORT", "8000"))
    embed_model = os.environ.get("EMBEDDING_MODEL", "intfloat/multilingual-e5-large")

    loader = PDFLoader()
    chunker = BiologyChunker(chunk_size=512, overlap=64)
    embedder = MultilingualEmbedder(model=embed_model)
    store = ChromaVectorStore(host=chroma_host, port=chroma_port)

    pdf_files = list(Path(source_dir).glob("*.pdf"))
    if not pdf_files:
        print(f"No PDFs found in {source_dir}")
        return

    print(f"Found {len(pdf_files)} PDF(s) to ingest for Class {class_level}...")

    all_chunks = []
    for pdf_path in pdf_files:
        print(f"  Processing: {pdf_path.name}")
        metadata = extract_metadata_from_filename(str(pdf_path))
        metadata["class"] = class_level
        metadata["source"] = f"NCERT Class {class_level}"

        try:
            pages = loader.load(str(pdf_path))
        except Exception as e:
            print(f"  ERROR loading {pdf_path.name}: {e}")
            continue

        for page_num, page_text in enumerate(pages):
            page_meta = {**metadata, "page": page_num + 1}
            chunks = chunker.chunk_document(page_text, page_meta)
            all_chunks.extend(chunks)

    if not all_chunks:
        print("No chunks generated. Check that PDFs contain extractable text.")
        return

    print(f"Total chunks to embed: {len(all_chunks)}")

    batch_size = 32
    for i in range(0, len(all_chunks), batch_size):
        batch = all_chunks[i: i + batch_size]
        texts = [c["text"] for c in batch]
        embeddings = embedder.embed(texts)
        await store.add_documents(batch, embeddings)
        done = min(i + batch_size, len(all_chunks))
        print(f"  Embedded & stored {done}/{len(all_chunks)} chunks")

    print(f"\n✅ Ingestion complete! {len(all_chunks)} chunks stored in ChromaDB.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest NCERT Biology PDFs into ChromaDB")
    parser.add_argument("--source", required=True, help="Directory with PDF files")
    parser.add_argument("--class", dest="class_level", default="11", help="11 or 12")
    args = parser.parse_args()
    asyncio.run(ingest_folder(args.source, args.class_level))
