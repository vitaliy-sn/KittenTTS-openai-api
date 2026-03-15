import gradio as gr
import numpy as np
from config import logger, AVAILABLE_MODELS, AVAILABLE_VOICES, DEFAULT_TEXT, generate_audio


def generate_audio_ui(text, voice, model_key):
    audio_array = generate_audio(model_key, voice, text)
    if audio_array is None:
        return None
    return (24000, audio_array)


with gr.Blocks(title="KittenTTS Demo") as app:
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
