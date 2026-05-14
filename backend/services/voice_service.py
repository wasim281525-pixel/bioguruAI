import openai
from config import settings
from typing import Tuple

LANG_VOICE_MAP = {
    "en": "alloy",
    "hi": "nova",
    "hinglish": "nova",
    "ur": "nova",
}


class VoiceService:
    def __init__(self):
        self.client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def transcribe(self, audio_bytes: bytes, language: str = "auto") -> Tuple[str, str]:
        lang_param = None if language == "auto" else language

        with open("/tmp/audio_upload.webm", "wb") as f:
            f.write(audio_bytes)

        with open("/tmp/audio_upload.webm", "rb") as f:
            result = await self.client.audio.transcriptions.create(
                model="whisper-1",
                file=f,
                language=lang_param,
                response_format="verbose_json",
            )

        detected = getattr(result, "language", None) or "en"
        lang_map = {"hindi": "hi", "urdu": "ur", "english": "en"}
        detected = lang_map.get(detected.lower(), "en")

        return result.text, detected

    async def synthesize(self, text: str, language: str = "en") -> bytes:
        voice = LANG_VOICE_MAP.get(language, "alloy")
        response = await self.client.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=text,
        )
        return response.content
