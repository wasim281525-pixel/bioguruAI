from fastapi import APIRouter, Depends, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional
import json

from services.rag_service import RAGService
from services.llm_service import LLMService
from utils.lang_detect import detect_language
from utils.prompt_builder import build_biology_prompt
from api.middleware.auth_middleware import get_current_user
from api.middleware.rate_limiter import rate_limit

router = APIRouter()
rag = RAGService()
llm = LLMService()


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str
    history: List[ChatMessage] = []
    chapter: Optional[str] = None
    language: Optional[str] = None
    stream: bool = True


@router.post("/message")
async def chat_message(
    req: ChatRequest,
    user=Depends(get_current_user),
    _=Depends(rate_limit),
):
    lang = req.language or detect_language(req.message)

    retrieved_chunks = await rag.retrieve(
        query=req.message,
        chapter_filter=req.chapter,
        top_k=5,
        lang=lang,
    )

    system_prompt = build_biology_prompt(
        language=lang,
        context_chunks=retrieved_chunks,
        user_class=str(user.get("class_level", "11")),
    )

    messages = [{"role": m.role, "content": m.content} for m in req.history[-8:]] + [
        {"role": "user", "content": req.message}
    ]

    if req.stream:
        async def generate():
            async for token in llm.stream(system=system_prompt, messages=messages):
                yield f"data: {json.dumps({'token': token})}\n\n"
            yield f"data: {json.dumps({'done': True, 'sources': [c['source'] for c in retrieved_chunks]})}\n\n"

        return StreamingResponse(generate(), media_type="text/event-stream")

    response = await llm.complete(system=system_prompt, messages=messages)
    return {
        "response": response,
        "language": lang,
        "sources": [c["source"] for c in retrieved_chunks],
        "retrieved_chunks": len(retrieved_chunks),
    }
