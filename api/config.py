import logging
import os
import numpy as np
from kittentts import KittenTTS

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
)

logger = logging.getLogger("kitten_tts")

AVAILABLE_MODELS = {
    "kitten-tts-mini": "KittenML/kitten-tts-mini-0.8",
    "kitten-tts-micro": "KittenML/kitten-tts-micro-0.8",
    "kitten-tts-nano": "KittenML/kitten-tts-nano-0.8",
}

AVAILABLE_VOICES = ['Bella', 'Jasper', 'Luna', 'Bruno', 'Rosie', 'Hugo', 'Kiki', 'Leo']

SUPPORTED_FORMATS = ["wav", "mp3", "flac", "opus", "pcm"]

DEFAULT_TEXT = (
    "Hello and welcome to the Kitten TTS demo. "
    "This example shows how to convert text into natural sounding speech. "
    "You can choose different voices and models from the interface. "
    "Feel free to experiment with your own text."
)

API_KEY = os.getenv("KITTEN_TTS_API_KEY", "sk-kitten-default-key")
ALLOWED_KEYS = [API_KEY] if API_KEY else []

loaded_models = {}


def get_model(model_key: str) -> KittenTTS:
    if model_key not in loaded_models:
        logger.info(f"Loading model: {model_key}")
        loaded_models[model_key] = KittenTTS(AVAILABLE_MODELS[model_key])
        logger.info(f"Model loaded: {model_key}")
    return loaded_models[model_key]


def generate_audio(model_key: str, voice: str, text: str) -> np.ndarray:
    if not text.strip():
        logger.warning("Empty text input received.")
        return None
    
    logger.info(f"Generating audio | Model: {model_key} | Voice: {voice}")
    model = get_model(model_key)
    audio = model.generate(text, voice=voice)
    logger.info("Audio generation completed.")
    return np.array(audio)
