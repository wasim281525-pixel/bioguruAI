from services.llm_service import LLMService
from typing import List, Dict


class NEETService:
    def __init__(self):
        self.llm = LLMService()

    async def generate_questions(
        self, topic: str, count: int = 10, difficulty: str = "medium"
    ) -> List[Dict]:
        return await self.llm.generate_mcq(topic, count, difficulty)

    def score_answers(self, questions: List[Dict], answers: List[str]) -> Dict:
        correct = wrong = skipped = 0
        for q, ans in zip(questions, answers):
            if not ans:
                skipped += 1
            elif ans == q.get("correct", ""):
                correct += 1
            else:
                wrong += 1

        total = len(questions)
        score_pct = (correct / total * 100) if total else 0
        neet_score = correct * 4 - wrong * 1

        return {
            "correct": correct,
            "wrong": wrong,
            "skipped": skipped,
            "total": total,
            "score_pct": round(score_pct, 2),
            "neet_score": neet_score,
        }
