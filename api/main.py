import uvicorn
from config import logger
from app import app as api_app
from gradio_app import app as gradio_app
import gradio as gr

# Mount API under /api prefix, Gradio will be at /
app = gr.mount_gradio_app(api_app, gradio_app, path="/")

if __name__ == "__main__":
    logger.info("Starting KittenTTS server on 0.0.0.0:7860")
    logger.info("Gradio UI: http://0.0.0.0:7860/")
    logger.info("API endpoints: http://0.0.0.0:7860/v1/...")
    logger.info("API docs: http://0.0.0.0:7860/swagger")
    uvicorn.run(app, host="0.0.0.0", port=7860)
