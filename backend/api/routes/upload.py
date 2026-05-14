from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import os, uuid, shutil

from api.middleware.auth_middleware import get_current_user, require_admin
from models.database import get_db
from models.progress import Document

router = APIRouter()
UPLOAD_DIR = "/app/data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


async def ingest_pdf_background(doc_id: str, filepath: str, metadata: dict):
    """Background task to ingest a PDF into ChromaDB"""
    try:
        import sys
        sys.path.insert(0, "/app")
        from rag.ingestion.pdf_loader import PDFLoader
        from rag.ingestion.chunker import BiologyChunker
        from rag.embeddings.embedder import MultilingualEmbedder
        from rag.vector_store.chroma_store import ChromaVectorStore
        from config import settings

        loader = PDFLoader()
        chunker = BiologyChunker()
        embedder = MultilingualEmbedder(model=settings.EMBEDDING_MODEL)
        store = ChromaVectorStore()

        pages = loader.load(filepath)
        all_chunks = []
        for page_num, text in enumerate(pages):
            meta = {**metadata, "page": page_num + 1}
            chunks = chunker.chunk_document(text, meta)
            all_chunks.extend(chunks)

        batch_size = 32
        for i in range(0, len(all_chunks), batch_size):
            batch = all_chunks[i:i + batch_size]
            embeddings = embedder.embed([c["text"] for c in batch])
            await store.add_documents(batch, embeddings)

        print(f"[Upload] Ingested {len(all_chunks)} chunks for doc {doc_id}")
    except Exception as e:
        print(f"[Upload] Ingestion failed for {doc_id}: {e}")


@router.post("/pdf")
async def upload_pdf(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    source_type: str = "ncert",
    class_level: int = 11,
    chapter: str = "",
    user=Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(400, "Only PDF files accepted")

    doc_id = str(uuid.uuid4())
    save_path = os.path.join(UPLOAD_DIR, f"{doc_id}.pdf")

    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    doc = Document(
        id=doc_id,
        uploader_id=user.get("sub"),
        filename=file.filename,
        source_type=source_type,
        class_level=class_level,
        chapter=chapter,
        status="processing",
    )
    db.add(doc)
    await db.commit()

    background_tasks.add_task(
        ingest_pdf_background,
        doc_id,
        save_path,
        {"source": f"NCERT Class {class_level}", "class": str(class_level), "chapter": chapter},
    )

    return {"doc_id": doc_id, "filename": file.filename, "status": "processing"}


@router.get("/documents")
async def list_documents(user=Depends(require_admin), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Document).order_by(Document.created_at.desc()))
    docs = result.scalars().all()
    return [
        {
            "id": str(d.id),
            "filename": d.filename,
            "source_type": d.source_type,
            "class_level": d.class_level,
            "chapter": d.chapter,
            "status": d.status,
            "created_at": d.created_at.isoformat() if d.created_at else None,
        }
        for d in docs
    ]
