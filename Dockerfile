FROM pytorch/pytorch:2.7.0-cuda12.8-cudnn9-devel

RUN pip install gradio soundfile

# for api.py
RUN pip install fastapi uvicorn scipy

RUN pip install https://github.com/KittenML/KittenTTS/releases/download/0.8/kittentts-0.8.0-py3-none-any.whl

WORKDIR /app

COPY ./api/ /app

EXPOSE 7860

ENTRYPOINT [ "python3", "/app/main.py" ]
