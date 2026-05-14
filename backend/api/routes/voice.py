from fastapi import APIRouter, UploadFile, File, Depends
from fastapi.responses import Response
from services.voice_service import VoiceService
from api.middleware.auth_middleware import get_current_user

router = APIRouter()
voice_svc = VoiceService()


@router.post("/transcribe")
async def transcribe(
    audio: UploadFile = File(...),
    language: str = "auto",
    user=Depends(get_current_user),
):
    audio_bytes = await audio.read()
    transcript, detected_lang = await voice_svc.transcribe(audio_bytes, language)
    return {"transcript": transcript, "detected_language": detected_lang}


@router.post("/speak")
async def text_to_speech(
    text: str,
    language: str = "en",
    user=Depends(get_current_user),
):
    audio_bytes = await voice_svc.synthesize(text, language)
    return Response(content=audio_bytes, media_type="audio/mpeg")
