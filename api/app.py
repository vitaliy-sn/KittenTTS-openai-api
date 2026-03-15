import gradio as gr
from fastapi import FastAPI

from config import (
    logger,
    AVAILABLE_MODELS,
    AVAILABLE_VOICES,
    DEFAULT_TEXT,
    generate_audio,
)
from openai_api import router as openai_api_router


def generate_audio_ui(text, voice, model_key):
    audio_array = generate_audio(model_key, voice, text)
    if audio_array is None:
        return None
    return (24000, audio_array)


with gr.Blocks(title="KittenTTS Demo") as gradio_app:
    gr.Markdown("## KittenTTS Text-to-Speech Demo")

    model_dropdown = gr.Dropdown(
        choices=list(AVAILABLE_MODELS.keys()),
        value="kitten-tts-mini",
        label="Select Model"
    )

    text_input = gr.Textbox(
        label="Enter Text",
        value=DEFAULT_TEXT,
        lines=5
    )

    voice_dropdown = gr.Dropdown(
        choices=AVAILABLE_VOICES,
        value="Jasper",
        label="Select Voice"
    )

    generate_button = gr.Button("Generate Speech")

    audio_output = gr.Audio(
        label="Generated Audio",
        type="numpy"
    )

    generate_button.click(
        fn=generate_audio_ui,
        inputs=[text_input, voice_dropdown, model_dropdown],
        outputs=audio_output
    )


app = FastAPI(
    title="KittenTTS API",
    version="1.0.0",
    description="Text-to-Speech API compatible with OpenAI TTS API format",
    docs_url="/swagger"
)

app.include_router(openai_api_router)

app = gr.mount_gradio_app(app, gradio_app, path="/")
