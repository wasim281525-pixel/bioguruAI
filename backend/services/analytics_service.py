from sqlalchemy.ext.asyncio import AsyncSession
from models.progress import RetrievalLog
import uuid


class AnalyticsService:
    async def log_retrieval(
        self,
        db: AsyncSession,
        user_id: str,
        query: str,
        language: str,
        chunks_retrieved: int,
        top_score: float,
        latency_ms: int,
    ):
        log = RetrievalLog(
            id=str(uuid.uuid4()),
            user_id=user_id,
            query=query,
            language=language,
            chunks_retrieved=chunks_retrieved,
            top_score=top_score,
            response_latency_ms=latency_ms,
        )
        db.add(log)
        await db.commit()
