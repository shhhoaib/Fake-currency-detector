FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 libglib2.0-0 libsm6 libxext6 libxrender-dev wget && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cpu -r requirements.txt

COPY . .

RUN mkdir -p uploads app/ml

ENV DATABASE_URL=sqlite+aiosqlite:///./pakshield.db
ENV SECRET_KEY=pakshield-ai-secret-key-change-in-production-2026
ENV CORS_ORIGINS_REGEX=https?://(localhost:[0-9]+|.*\.vercel\.app|.*\.huggingface\.space)
ENV MODEL_PATH=./app/ml/yolo_cls.pt
ENV UPLOAD_DIR=./uploads

EXPOSE 7860

CMD uvicorn main:app --host 0.0.0.0 --port 7860
