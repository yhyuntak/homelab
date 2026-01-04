# homelab 멀티 서비스 구조

> 독립적인 컨테이너 서비스들을 통합 관리하는 homelab 구조

---

## 프로젝트 구조

```
homelab/
├── docker-compose.yml              # 전체 서비스 통합 (프로덕션)
├── .env.example                    # 전체 환경 변수 예시
├── docs/                           # 루트 레벨 문서
│   ├── architecture/               # 전체 아키텍처
│   └── backlogs/                   # 홈랩 인프라 백로그 (옵션)
│
└── services/
    ├── trend-radar/
    │   ├── docker-compose.yml      # 개별 개발/테스트용
    │   ├── Dockerfile
    │   ├── src/
    │   ├── docs/
    │   │   ├── README.md
    │   │   └── backlogs/           # 서비스별 백로그 (옵션)
    │   └── .env.example
    │
    └── ping-service/
        ├── docker-compose.yml
        ├── Dockerfile
        ├── src/
        ├── docs/
        └── .env.example
```

---

## Docker Compose 구분

### 루트 `docker-compose.yml` (통합 실행)

**목적**: 모든 서비스를 한 번에 실행 (프로덕션/NAS 배포)

**특징**:
- 서비스별 포트 할당 (NAS: 61001, 61002, 61003, ...)
- 공통 네트워크 설정 (`homelab`)
- 서비스 간 통신 설정
- 환경별 설정 (dev/prod)

**예시**:
```yaml
version: '3.8'

services:
  trend-radar:
    build: ./services/trend-radar
    container_name: homelab-trend-radar
    ports:
      - "61001:8000"    # NAS 610** 번대 사용
    networks:
      - homelab
    restart: unless-stopped

  ping-service:
    build: ./services/ping-service
    container_name: homelab-ping-service
    ports:
      - "61002:8000"
    networks:
      - homelab
    restart: unless-stopped

networks:
  homelab:
    name: homelab
    driver: bridge
```

**실행**:
```bash
# 루트에서 모든 서비스 실행
docker-compose up -d

# 특정 서비스만 실행
docker-compose up -d trend-radar
```

---

### 서비스별 `docker-compose.yml` (개별 테스트)

**목적**: 해당 서비스만 독립적으로 개발/테스트

**특징**:
- 포트 8000 고정 (개발용)
- Hot reload 설정
- 개발용 환경 변수
- 볼륨 마운트 (코드 변경 즉시 반영)

**예시**:
```yaml
# services/trend-radar/docker-compose.yml
version: '3.8'

services:
  trend-radar:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ENV=development
      - DEBUG=true
    volumes:
      - ./src:/app/src    # hot reload
```

**실행**:
```bash
# 서비스 폴더에서 개별 실행
cd services/trend-radar
docker-compose up

# 또는 루트에서
docker-compose -f services/trend-radar/docker-compose.yml up
```

---

## 서비스 추가 체크리스트

새 서비스를 추가할 때:

### 1. 폴더 생성
```bash
mkdir -p services/{service-name}/{src,docs}
cd services/{service-name}
```

### 2. 필수 파일 생성
- [ ] `Dockerfile` - 컨테이너 빌드 정의
- [ ] `docker-compose.yml` - 개별 테스트용
- [ ] `src/` - 서비스 코드
- [ ] `docs/README.md` - 서비스 설명
- [ ] `.env.example` - 환경 변수 예시

### 3. 선택 파일
- [ ] `docs/backlogs/` - 복잡한 기능 개발 시
- [ ] `tests/` - 테스트 코드
- [ ] `scripts/` - 유틸리티 스크립트

### 4. 루트 docker-compose.yml 업데이트
```yaml
services:
  new-service:
    build: ./services/new-service
    container_name: homelab-new-service
    ports:
      - "6100X:8000"    # NAS 610** 번대 포트 할당
    networks:
      - homelab
    restart: unless-stopped
```

### 5. 포트 할당 규칙

**NAS 서버: 610** 번대 사용**

| 서비스 | NAS 포트 | 컨테이너 포트 |
|--------|----------|---------------|
| claude-ping | - (내부) | - |
| trend-radar | 61001 | 8000 |
| new-service | 61002 | 8000 |
| ... | 61003~ | 8000 |

**포트 할당 원칙**:
- NAS 외부: `610**` 번대 (61001부터 순차 할당)
- 컨테이너 내부: `8000` (개발 시 통일)
- 내부 전용 서비스: 포트 매핑 없음

---

## 루트 vs 서비스 구분

### 루트 레벨 (`docs/`)

**용도**: 전체 homelab 운영 문서

**내용**:
- 전체 아키텍처
- 네트워크 구성
- 공통 인프라 (모니터링, 로깅 등)
- 서비스 목록 및 포트 맵

**백로그 예시**:
- Epic: NAS 통합 배포 자동화
- Epic: 공통 모니터링 시스템
- Epic: 네트워크 보안 설정

---

### 서비스 레벨 (`services/{name}/docs/`)

**용도**: 해당 서비스만의 문서

**내용**:
- 서비스 설명 (README.md)
- API 문서 (있다면)
- 서비스별 백로그 (옵션)

**백로그 예시**:
- Epic: 트렌드 분석 기능
- Epic: 데이터 수집 최적화

---

## 서비스 독립성 원칙

### ✅ 지켜야 할 것

1. **독립 실행 가능**: 각 서비스는 단독으로 실행 가능해야 함
2. **명확한 인터페이스**: 서비스 간 통신은 API/메시지 큐 등 명확한 인터페이스 사용
3. **독립적인 데이터**: 가능하면 서비스별 DB/스토리지 분리
4. **환경 변수 관리**: 서비스별 `.env.example` 유지

### ❌ 피해야 할 것

1. **직접 파일 공유**: 서비스 간 직접 파일 시스템 공유 지양
2. **강한 결합**: 한 서비스가 다른 서비스 내부 구조에 의존
3. **포트 충돌**: 루트 compose에서 포트 중복 할당

---

## 사용 시나리오

### 시나리오 1: 새 서비스 개발

```bash
# 1. 서비스 폴더 생성
mkdir -p services/new-service/{src,docs}

# 2. 개발
cd services/new-service
# Dockerfile, docker-compose.yml 작성

# 3. 개별 테스트
docker-compose up

# 4. 잘 돌면 루트 compose에 추가
cd ../..
# docker-compose.yml에 new-service 추가

# 5. 전체 테스트
docker-compose up -d
```

### 시나리오 2: 기존 서비스 수정

```bash
# 1. 서비스만 개별 실행
cd services/trend-radar
docker-compose up

# 2. 코드 수정 (hot reload 적용)
# src/ 파일 수정

# 3. 잘 돌면 전체 재시작
cd ../..
docker-compose restart trend-radar
```

### 시나리오 3: 전체 배포 (NAS)

```bash
# 루트에서 전체 실행
docker-compose up -d

# 로그 확인
docker-compose logs -f
```

---

## 참고 문서

| 문서 | 경로 |
|------|------|
| 워크플로우 | [workflow.md](workflow.md) |
| 백로그 가이드 | [service-template/backlog-guide.md](service-template/backlog-guide.md) |
| 코딩 규칙 | [service-template/coding-standards.md](service-template/coding-standards.md) |

---

**Last Updated**: 2026-01-04
