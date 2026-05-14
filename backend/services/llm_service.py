import anthropic
from typing import AsyncGenerator, List, Dict
from config import settings


class LLMService:
    def __init__(self):
        self.client = anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.model = settings.LLM_MODEL

    async def stream(self, system: str, messages: List[Dict]) -> AsyncGenerator[str, None]:
        async with self.client.messages.stream(
            model=self.model,
            max_tokens=1500,
            system=system,
            messages=messages,
        ) as stream:
            async for text in stream.text_stream:
                yield text

    async def complete(self, system: str, messages: List[Dict]) -> str:
        response = await self.client.messages.create(
            model=self.model,
            max_tokens=1500,
            system=system,
            messages=messages,
        )
        return response.content[0].text

    async def generate_mcq(self, topic: str, count: int = 5, difficulty: str = "medium") -> List[Dict]:
        """Generate NEET-style MCQs on a Biology topic"""
        prompt = f"""Generate {count} NEET-style Biology MCQ questions on "{topic}".
Difficulty: {difficulty}
Format: Return ONLY valid JSON array, no markdown.
Each object: {{
  "question": "...",
  "options": ["A) ...", "B) ...", "C) ...", "D) ..."],
  "correct": "A",
  "explanation": "...",
  "ncert_ref": "NCERT Class 11/12, Chapter X"
}}"""
        response = await self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}],
        )
        import json, re
        text = response.content[0].text
        # Strip possible markdown fences
        text = re.sub(r"```json|```", "", text).strip()
        return json.loads(text)
