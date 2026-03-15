FROM pytorch/pytorch:2.7.0-cuda12.8-cudnn9-devel

WORKDIR /app

COPY ./requirements.txt /app/
RUN pip install -r requirements.txt

COPY ./api/ /app

EXPOSE 7860

ENTRYPOINT [ "python3", "/app/main.py" ]
