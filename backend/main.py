from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from api.routes import chat, auth, neet, upload, voice, analytics
from config import settings
import redis.asyncio as redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: init Redis
    app.state.redis = await redis.from_url(settings.REDIS_URL)

    # Auto-create DB tables
    try:
        from models.user import Base, User
        from models.chat import ChatSession, ChatMessage
        from models.progress import NEETSession, StudentProgress, Document, RetrievalLog
        from models.database import engine
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("[Startup] Database tables ready.")
    except Exception as e:
        print(f"[Startup] DB init warning: {e}")

    yield

    # Shutdown
    await app.state.redis.close()


app = FastAPI(
    title="BioGuru AI API",
    description="NEET Biology AI Tutor — Multilingual RAG System",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router,      prefix="/api/auth",      tags=["Auth"])
app.include_router(chat.router,      prefix="/api/chat",      tags=["Chat"])
app.include_router(neet.router,      prefix="/api/neet",      tags=["NEET"])
app.include_router(upload.router,    prefix="/api/upload",    tags=["Upload"])
app.include_router(voice.router,     prefix="/api/voice",     tags=["Voice"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])


@app.get("/health")
async def health():
    return {"status": "ok", "service": "BioGuru AI"}
