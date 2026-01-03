# =============================================================================
# Claude Ping Service
# =============================================================================
FROM python:3.12-slim

# 시스템 패키지 설치 (Node.js for Claude CLI)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Claude CLI 설치
RUN npm install -g @anthropic-ai/claude-code

# 작업 디렉토리
WORKDIR /app

# Python 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY main.py .

# non-root 사용자 생성
RUN useradd -m -u 1000 appuser && \
    mkdir -p /home/appuser/.claude && \
    chown -R appuser:appuser /home/appuser /app

USER appuser

# 환경변수
ENV PYTHONUNBUFFERED=1

CMD ["python", "main.py"]
