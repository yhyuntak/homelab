# 서비스별 코딩 규칙 템플릿

> 새 서비스 시작 시 `services/{name}/docs/CODING.md`로 복사 후 작성

---

## 📝 사용법

1. 새 서비스 생성 시 이 파일을 복사:
   ```bash
   cp .claude/rules/service-template/coding-standards.md \
      services/{service-name}/docs/CODING.md
   ```

2. 아래 템플릿의 `{...}` 부분을 채워서 사용

3. 불필요한 섹션은 삭제

---

## 1. 기술 스택

| 영역 | 기술 | 버전 |
|------|------|------|
| 언어 | {Python / Go / Node.js / ...} | {3.12 / 1.21 / 20 / ...} |
| 프레임워크 | {FastAPI / Gin / Express / ...} | {선택 사항} |
| 주요 라이브러리 | {requests / axios / ...} | {선택 사항} |

---

## 2. 폴더 구조

```
services/{service-name}/
├── Dockerfile
├── docker-compose.yml      # 개발/테스트용
├── requirements.txt        # Python
├── go.mod                  # Go
├── package.json            # Node.js
├── .env.example
│
├── src/
│   ├── main.{py/go/js}     # 엔트리 포인트
│   ├── {module1}/
│   ├── {module2}/
│   └── utils/
│
├── tests/                  # 테스트 (선택)
│   └── test_*.py
│
├── docs/
│   ├── README.md
│   ├── CODING.md           # 이 파일
│   └── backlogs/           # 백로그 (선택)
│
└── scripts/                # 유틸리티 스크립트 (선택)
```

---

## 3. 네이밍 규칙

### 파일명
- Python: `snake_case.py`
- Go: `snake_case.go`
- JavaScript: `camelCase.js` 또는 `kebab-case.js`

### 변수/함수
- Python: `snake_case`
- Go: `camelCase` (exported는 PascalCase)
- JavaScript: `camelCase`

### 클래스/타입
- Python: `PascalCase`
- Go: `PascalCase`
- JavaScript: `PascalCase`

---

## 4. 환경 변수 관리

### .env.example

```bash
# 서비스 설정
SERVICE_NAME={service-name}
PORT=8000

# 외부 API (필요 시)
API_KEY=your-api-key-here
API_URL=https://api.example.com

# 데이터베이스 (필요 시)
DB_HOST=localhost
DB_PORT=5432
DB_NAME={service-name}
DB_USER=user
DB_PASSWORD=password

# 로깅
LOG_LEVEL=INFO
TZ=Asia/Seoul
```

### 민감 정보 처리

- ✅ `.env.example`에 예시값 제공
- ✅ `.env`는 `.gitignore`에 추가
- ✅ 환경 변수로 주입 (docker-compose)
- ❌ 코드에 하드코딩 절대 금지

---

## 5. Docker 규칙

### Dockerfile

```dockerfile
FROM {python:3.12-slim / golang:1.21-alpine / node:20-alpine}

WORKDIR /app

# 의존성 설치
COPY {requirements.txt / go.mod / package.json} .
RUN {pip install / go mod download / npm install}

# 소스 복사
COPY src/ ./src/

# non-root 사용자
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

# 환경 변수
ENV PORT=8000

# 헬스체크 (선택)
HEALTHCHECK --interval=30s --timeout=3s \
  CMD {curl -f http://localhost:8000/health || exit 1}

CMD [{python / go run / node} src/main.{py/go/js}]
```

### docker-compose.yml (개발용)

```yaml
version: '3.8'

services:
  {service-name}:
    build: .
    ports:
      - "8000:8000"    # 개발용 고정 포트
    environment:
      - ENV=development
      - DEBUG=true
      - LOG_LEVEL=DEBUG
    volumes:
      - ./src:/app/src    # hot reload
    env_file:
      - .env
```

### 포트 규칙

| 환경 | 포트 | 설명 |
|------|------|------|
| 개발 (서비스별) | 8000 | 고정 (hot reload) |
| NAS 배포 | 610** | 루트 compose에서 할당 |

---

## 6. 코드 스타일

### Linter/Formatter

**Python**:
```bash
# pyproject.toml 또는 .flake8
black src/
flake8 src/
mypy src/
```

**Go**:
```bash
gofmt -w .
golangci-lint run
```

**JavaScript**:
```bash
# .eslintrc.js, .prettierrc
eslint src/
prettier --write src/
```

### Import 순서

**Python**:
```python
# 1. 표준 라이브러리
import os
import sys

# 2. 서드파티
import requests
from fastapi import FastAPI

# 3. 로컬 모듈
from .utils import helper
```

**Go**:
```go
// 1. 표준 라이브러리
import (
    "fmt"
    "net/http"
)

// 2. 서드파티
import (
    "github.com/gin-gonic/gin"
)

// 3. 로컬 모듈
import (
    "{module}/utils"
)
```

### 주석 작성 원칙

- 복잡한 로직에만 주석 작성
- 자명한 코드는 주석 불필요
- TODO, FIXME 태그 활용

```python
# ✅ 좋은 예
def calculate_trend_score(data):
    # 가중 평균 계산: 최근 데이터에 더 높은 가중치
    weights = [0.5, 0.3, 0.2]
    return sum(d * w for d, w in zip(data, weights))

# ❌ 나쁜 예
def add(a, b):
    # 두 숫자를 더함
    return a + b
```

---

## 7. 에러 핸들링

### 기본 패턴

**Python**:
```python
import logging

logger = logging.getLogger(__name__)

try:
    result = fetch_data()
except RequestException as e:
    logger.error(f"API 호출 실패: {e}")
    raise
except Exception as e:
    logger.exception(f"예상치 못한 에러: {e}")
    raise
```

**Go**:
```go
if err != nil {
    log.Printf("API 호출 실패: %v", err)
    return fmt.Errorf("fetch failed: %w", err)
}
```

### 로깅 레벨

| 레벨 | 용도 |
|------|------|
| DEBUG | 개발 중 상세 정보 |
| INFO | 일반 실행 흐름 |
| WARNING | 주의 필요 (복구 가능) |
| ERROR | 에러 발생 (복구 시도) |
| CRITICAL | 치명적 에러 (서비스 중단) |

---

## 8. 테스트 규칙 (선택)

### 테스트 파일 위치

```
tests/
├── test_main.py
├── test_api.py
└── test_utils.py
```

### 테스트 실행

```bash
# Python
pytest tests/

# Go
go test ./...

# JavaScript
npm test
```

### 테스트 커버리지 목표

- 핵심 로직: 80% 이상
- 유틸리티: 60% 이상
- 간단한 서비스: 테스트 생략 가능

---

## 9. API 설계 (해당 시)

### 엔드포인트 규칙

```
GET    /health              # 헬스체크 (필수)
GET    /api/v1/resources    # 목록 조회
GET    /api/v1/resources/:id    # 단일 조회
POST   /api/v1/resources    # 생성
PUT    /api/v1/resources/:id    # 수정
DELETE /api/v1/resources/:id    # 삭제
```

### 응답 형식

```json
{
  "status": "success",
  "data": {...},
  "message": "optional message"
}
```

---

## 10. 보안 규칙

### 필수 체크리스트

- [ ] 환경 변수로 민감 정보 관리
- [ ] API 키/토큰 노출 방지
- [ ] 입력 값 검증 (XSS, SQL Injection)
- [ ] HTTPS 사용 (프로덕션)
- [ ] 에러 메시지에 민감 정보 포함 금지

### .gitignore

```
.env
*.log
__pycache__/
node_modules/
dist/
build/
```

---

## 11. 서비스 통합 (homelab)

### 루트 docker-compose.yml 추가

```yaml
services:
  {service-name}:
    build: ./services/{service-name}
    container_name: homelab-{service-name}
    ports:
      - "610XX:8000"    # NAS 포트 할당
    networks:
      - homelab
    restart: unless-stopped
    env_file:
      - ./services/{service-name}/.env
```

### 네트워크 통신

- 서비스 간 통신: `http://{container-name}:8000`
- 외부 접근: `http://{NAS-IP}:610XX`

---

## 참고 문서

| 문서 | 경로 |
|------|------|
| homelab 구조 | [../../homelab-structure.md](../homelab-structure.md) |
| 워크플로우 | [../../workflow.md](../workflow.md) |
| 백로그 가이드 | [./backlog-guide.md](./backlog-guide.md) |

---

**Last Updated**: 2026-01-04
