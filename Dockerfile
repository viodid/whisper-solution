FROM python:3.11-slim-bullseye

RUN apt update && apt install ffmpeg -y

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./src .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]