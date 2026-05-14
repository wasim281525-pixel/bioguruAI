from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func as sqlfunc
import uuid

from services.llm_service import LLMService
from api.middleware.auth_middleware import get_current_user
from models.database import get_db
from models.progress import NEETSession, StudentProgress

router = APIRouter()
llm = LLMService()

CHAPTERS_11 = [
    "The Living World", "Biological Classification", "Plant Kingdom",
    "Animal Kingdom", "Morphology of Flowering Plants", "Anatomy of Flowering Plants",
    "Structural Organisation in Animals", "Cell: The Unit of Life",
    "Biomolecules", "Cell Cycle and Cell Division", "Transport in Plants",
    "Mineral Nutrition", "Photosynthesis", "Respiration in Plants",
    "Plant Growth and Development", "Digestion and Absorption",
    "Breathing and Exchange of Gases", "Body Fluids and Circulation",
    "Excretory Products", "Locomotion and Movement",
    "Neural Control and Coordination", "Chemical Coordination",
]
CHAPTERS_12 = [
    "Reproduction in Organisms", "Sexual Reproduction in Flowering Plants",
    "Human Reproduction", "Reproductive Health",
    "Principles of Inheritance and Variation", "Molecular Basis of Inheritance",
    "Evolution", "Human Health and Disease", "Strategies for Food Production",
    "Microbes in Human Welfare", "Biotechnology: Principles and Processes",
    "Biotechnology and Its Applications", "Organisms and Populations",
    "Ecosystem", "Biodiversity and Conservation", "Environmental Issues",
]


class GenerateMCQRequest(BaseModel):
    topic: str
    count: int = 10
    difficulty: str = "medium"


class SubmitAnswersRequest(BaseModel):
    session_id: str
    questions: List[dict]
    answers: List[str]
    time_taken: int


@router.get("/chapters")
async def get_chapters(class_level: int = 11, user=Depends(get_current_user)):
    chapters = CHAPTERS_11 if class_level == 11 else CHAPTERS_12
    return {"class_level": class_level, "chapters": chapters}


@router.post("/generate")
async def generate_mcq(req: GenerateMCQRequest, user=Depends(get_current_user)):
    questions = await llm.generate_mcq(
        topic=req.topic, count=req.count, difficulty=req.difficulty
    )
    session_id = str(uuid.uuid4())
    return {"session_id": session_id, "questions": questions, "topic": req.topic}


@router.post("/submit")
async def submit_answers(
    req: SubmitAnswersRequest,
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    correct = 0
    wrong = 0
    skipped = 0
    details = []

    for i, (q, user_ans) in enumerate(zip(req.questions, req.answers)):
        correct_ans = q.get("correct", "")
        if not user_ans:
            skipped += 1
            result = "skipped"
        elif user_ans == correct_ans:
            correct += 1
            result = "correct"
        else:
            wrong += 1
            result = "wrong"

        details.append({
            "question": q.get("question"),
            "user_answer": user_ans,
            "correct_answer": correct_ans,
            "result": result,
            "explanation": q.get("explanation", ""),
        })

    total = len(req.questions)
    score_pct = (correct / total * 100) if total > 0 else 0
    neet_score = correct * 4 - wrong * 1  # NEET marking scheme

    # Persist session
    session = NEETSession(
        user_id=user.get("sub"),
        total_q=total,
        correct=correct,
        wrong=wrong,
        skipped=skipped,
        score_pct=score_pct,
        time_taken=req.time_taken,
    )
    db.add(session)
    await db.commit()

    return {
        "session_id": req.session_id,
        "total": total,
        "correct": correct,
        "wrong": wrong,
        "skipped": skipped,
        "score_pct": round(score_pct, 2),
        "neet_score": neet_score,
        "details": details,
    }


@router.get("/progress")
async def get_progress(user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(NEETSession).where(
            NEETSession.user_id == user.get("sub")
        ).order_by(NEETSession.created_at.desc()).limit(20)
    )
    sessions = result.scalars().all()
    return {
        "sessions": [
            {
                "id": str(s.id),
                "total_q": s.total_q,
                "correct": s.correct,
                "wrong": s.wrong,
                "score_pct": float(s.score_pct or 0),
                "time_taken": s.time_taken,
                "created_at": s.created_at.isoformat() if s.created_at else None,
            }
            for s in sessions
        ]
    }
