from fastapi import APIRouter, HTTPException, Depends, Header, status
from fastapi.responses import Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
import scipy.io.wavfile as wavfile
import io
import numpy as np
from typing import Optional

from config import (
    logger,
    ALLOWED_KEYS,
    AVAILABLE_MODELS,
    AVAILABLE_VOICES,
    SUPPORTED_FORMATS,
    get_model,
    generate_audio,
)

router = APIRouter()


class TTSRequest(BaseModel):
    model: str = Field(..., description="Model name to use for speech generation")
    input: str = Field(..., description="The text to generate audio for")
    voice: str = Field(..., description="The voice to use")
    response_format: str = Field(default="wav", description="Audio format")
    speed: float = Field(default=1.0, ge=0.25, le=4.0, description="Speed of the generated audio")


class ModelObject(BaseModel):
    id: str
    object: str = "model"
    created: int


class VoiceObject(BaseModel):
    name: str
    language: str = "en"


security = HTTPBearer()


async def verify_api_key(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    authorization: Optional[str] = Header(None)
):
    if not ALLOWED_KEYS:
        return None

    if not credentials and not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API key"
        )

    api_key = credentials.credentials if credentials else None

    if authorization and authorization.startswith("Bearer "):
        api_key = authorization[7:]

    if api_key not in ALLOWED_KEYS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )

    return api_key


def convert_to_wav(audio_array: np.ndarray, sample_rate: int = 24000) -> bytes:
    buffer = io.BytesIO()
    wavfile.write(buffer, sample_rate, audio_array)
    buffer.seek(0)
    return buffer.getvalue()


@router.get("/v1/audio/models")
async def list_models():
    return {
        "models": [
            {"id": model_key, "name": model_key}
            for model_key in AVAILABLE_MODELS.keys()
        ]
    }


@router.get("/v1/audio/voices")
async def list_voices():
    return {
        "voices": [
            {"name": voice, "id": voice}
            for voice in AVAILABLE_VOICES
        ]
    }


@router.post("/v1/audio/speech")
async def create_speech(request: TTSRequest, api_key: Optional[str] = Depends(verify_api_key)):
    if request.model not in AVAILABLE_MODELS:
        raise HTTPException(
            status_code=400,
            detail=f"Model '{request.model}' not found. Available: {list(AVAILABLE_MODELS.keys())}"
        )

    if request.voice not in AVAILABLE_VOICES:
        raise HTTPException(
            status_code=400,
            detail=f"Voice '{request.voice}' not found. Available: {AVAILABLE_VOICES}"
        )

    if not request.input.strip():
        raise HTTPException(status_code=400, detail="Input text cannot be empty")

    if request.response_format not in SUPPORTED_FORMATS:
        raise HTTPException(
            status_code=400,
            detail=f"Format '{request.response_format}' not supported. Available: {SUPPORTED_FORMATS}"
        )

    logger.info(f"Generating audio | Model: {request.model} | Voice: {request.voice}")

    try:
        audio_array = generate_audio(request.model, request.voice, request.input)
        if audio_array is None:
            raise HTTPException(status_code=500, detail="Failed to generate audio")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating audio: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate audio")

    content_type_map = {
        "wav": "audio/wav",
        "mp3": "audio/mpeg",
        "flac": "audio/flac",
        "opus": "audio/opus",
        "pcm": "audio/pcm"
    }

    audio_bytes = convert_to_wav(audio_array)

    return Response(
        content=audio_bytes,
        media_type=content_type_map.get(request.response_format, "audio/wav"),
        headers={
            "Content-Disposition": f'attachment; filename="speech.{request.response_format}"'
        }
    )
