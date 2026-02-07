# PDF Translator

스캔 PDF의 본문 텍스트를 한국어로 번역하는 배치 도구.

## 사용법

```bash
# 1. .env 설정
cp .env.example .env
# XAI_API_KEY 입력

# 2. PDF를 data/input/에 넣기

# 3. 빌드 + 실행
docker-compose build
docker-compose run pdf-translator python src/main.py \
    /app/data/input/book.pdf \
    /app/data/output/book-kr.pdf

# 테스트 (5페이지만)
docker-compose run pdf-translator python src/main.py \
    /app/data/input/book.pdf \
    /app/data/output/book-kr.pdf \
    --pages 1-5

# OCR 결과만 확인 (번역 없이)
docker-compose run pdf-translator python src/main.py \
    /app/data/input/book.pdf \
    /app/data/output/book-kr.pdf \
    --dry-run --pages 1-3
```

## 옵션

| 옵션 | 설명 |
|------|------|
| `--pages 1-5` | 특정 페이지만 처리 |
| `--dry-run` | OCR만 실행, 번역/렌더링 스킵 |
| `--dpi 300` | 이미지 추출 해상도 |
| `--no-cache` | 캐시 사용 안 함 |
