# 개발 워크플로우

> Git 브랜치 전략 + 태그 기반 릴리즈 + 백로그 관리

---

## Git 브랜치 전략

프로젝트 시작 시 두 가지 옵션 중 선택:

### 옵션 A: 단순 (main only)

**추천 대상**: 개인 프로젝트, 소규모 프로젝트

```
feature/xxx ──→ main ──→ 태그 (v0.1.0)
```

**작업 플로우**:
```bash
# 1. 작업 브랜치 생성 (선택)
git checkout -b feature/new-feature

# 2. 작업 + 커밋
git add .
git commit -m "feat: 새 기능 구현"

# 3. main에 머지
git checkout main
git merge feature/new-feature
git push origin main

# 4. 브랜치 정리
git branch -d feature/new-feature
```

---

### 옵션 B: 표준 (develop/main/태그)

**추천 대상**: 팀 프로젝트, 배포 환경 분리 필요

```
v0.1.0 (태그) ──→ Production
    │
main (릴리즈 준비 완료)
    ↑
develop (개발 중)
    ↑
feature/xxx (작업 브랜치)
```

**브랜치 타입**:
| 타입 | 용도 | 머지 대상 | 예시 |
|------|------|----------|------|
| `feature/*` | 새 기능 | `develop` | `feature/user-auth` |
| `fix/*` | 버그 수정 | `develop` | `fix/login-error` |
| `hotfix/*` | 긴급 수정 | `main` + `develop` | `hotfix/security-patch` |

**작업 플로우**:
```bash
# 1. develop에서 브랜치 생성
git checkout develop
git pull origin develop
git checkout -b feature/new-feature

# 2. 작업 + 커밋
git add .
git commit -m "feat: 새 기능 구현"

# 3. develop에 머지
git checkout develop
git merge feature/new-feature
git push origin develop

# 4. 브랜치 정리
git branch -d feature/new-feature
```

---

## 버전 관리 (Semantic Versioning)

```
v{MAJOR}.{MINOR}.{PATCH}

MAJOR: 호환성 깨지는 변경 (v1.0.0 → v2.0.0)
MINOR: 새 기능 추가 (v0.1.0 → v0.2.0)
PATCH: 버그 수정 (v0.1.0 → v0.1.1)
```

### 서비스별 태그 vs 전체 태그

**서비스별 태그** (개별 서비스 릴리즈):
```bash
# 형식: {service-name}-v{version}
git tag -a trend-radar-v0.1.0 -m "Trend Radar: 첫 번째 릴리즈"
git tag -a ping-service-v0.2.0 -m "Ping Service: 알림 기능 추가"
git push origin --tags
```

**전체 홈랩 태그** (모든 서비스 통합 릴리즈):
```bash
# 형식: homelab-v{version}
git tag -a homelab-v1.0.0 -m "Homelab: 전체 서비스 통합 릴리즈"
git push origin homelab-v1.0.0
```

### 릴리즈 절차

**옵션 A (단순):**
```bash
# 서비스별 릴리즈
git tag -a trend-radar-v0.1.0 -m "Trend Radar: 첫 번째 릴리즈"
git push origin trend-radar-v0.1.0

# 전체 릴리즈 (모든 서비스 안정화 후)
git tag -a homelab-v1.0.0 -m "Homelab 전체 릴리즈"
git push origin homelab-v1.0.0
```

**옵션 B (표준):**
```bash
# 1. develop을 main에 머지
git checkout main
git pull origin main
git merge develop
git push origin main

# 2. 서비스별 태그 생성
git tag -a trend-radar-v0.1.0 -m "Trend Radar: 첫 번째 릴리즈"
git push origin trend-radar-v0.1.0

# 3. (선택) GitHub Release 생성
gh release create trend-radar-v0.1.0 --title "Trend Radar v0.1.0" --notes "릴리즈 노트..."
```

---

## 커밋 메시지 규칙

### 기본 형식

```
<type>(<scope>): <description>

# 타입
feat:     새 기능
fix:      버그 수정
refactor: 리팩토링
docs:     문서 변경
chore:    기타 (의존성, 설정 등)
style:    코드 스타일
test:     테스트 추가/수정
```

### 스코프 (Scope)

**서비스별 변경**:
```bash
feat(trend-radar): 트렌드 분석 API 추가
fix(ping-service): 헬스체크 타임아웃 수정
refactor(trend-radar): 데이터 수집 로직 개선
```

**전체 홈랩 변경**:
```bash
chore(homelab): docker-compose 네트워크 설정 변경
docs(homelab): 아키텍처 문서 업데이트
feat(homelab): 공통 모니터링 추가
```

**스코프 생략 가능** (작은 변경):
```bash
docs: README 오타 수정
chore: .gitignore 업데이트
```

### 예시

```bash
# 서비스 기능 추가
feat(trend-radar): 기술 트렌드 데이터 수집 기능 추가

# 서비스 버그 수정
fix(ping-service): 연결 실패 시 재시도 로직 수정

# 인프라 변경
chore(homelab): NAS 배포용 환경 변수 추가

# 문서 업데이트
docs(trend-radar): API 사용법 문서 작성
```

---

**Last Updated**: 2026-01-04
