FROM python:3.12-slim-bookworm

WORKDIR /app

# Tesseract OCR + Korean fonts
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        tesseract-ocr \
        tesseract-ocr-eng \
        fonts-noto-cjk \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Source code
COPY src/ ./src/

# non-root user
RUN useradd -m -u 1000 appuser && \
    mkdir -p /app/data/input /app/data/output && \
    chown -R appuser:appuser /app
USER appuser

ENV PYTHONUNBUFFERED=1

CMD ["python", "src/main.py", "--help"]
