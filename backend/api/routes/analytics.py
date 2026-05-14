from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc

from api.middleware.auth_middleware import get_current_user
from models.database import get_db
from models.progress import NEETSession, StudentProgress, RetrievalLog
from models.chat import ChatMessage, ChatSession

router = APIRouter()


@router.get("/dashboard")
async def dashboard(user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    uid = user.get("sub")

    # NEET stats
    result = await db.execute(
        select(
            func.count(NEETSession.id).label("total_tests"),
            func.avg(NEETSession.score_pct).label("avg_score"),
            func.max(NEETSession.score_pct).label("best_score"),
        ).where(NEETSession.user_id == uid)
    )
    stats = result.first()

    # Recent NEET sessions
    sessions_result = await db.execute(
        select(NEETSession)
        .where(NEETSession.user_id == uid)
        .order_by(desc(NEETSession.created_at))
        .limit(5)
    )
    recent_sessions = sessions_result.scalars().all()

    # Chat count
    session_result = await db.execute(
        select(func.count(ChatSession.id)).where(ChatSession.user_id == uid)
    )
    chat_count = session_result.scalar() or 0

    return {
        "neet": {
            "total_tests": stats.total_tests or 0,
            "avg_score": round(float(stats.avg_score or 0), 2),
            "best_score": round(float(stats.best_score or 0), 2),
        },
        "chat_sessions": chat_count,
        "recent_tests": [
            {
                "id": str(s.id),
                "score_pct": float(s.score_pct or 0),
                "correct": s.correct,
                "total_q": s.total_q,
                "created_at": s.created_at.isoformat() if s.created_at else None,
            }
            for s in recent_sessions
        ],
    }
