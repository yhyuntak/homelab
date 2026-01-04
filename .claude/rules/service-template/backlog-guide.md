# 서비스별 백로그 가이드

> Epic/Story 기반 백로그 시스템 (옵션)

---

## 백로그가 필요한 경우

### ✅ 백로그 사용 추천

- 복잡한 기능 개발 (3개 이상의 구현 단계)
- 여러 스텝이 필요한 작업
- 팀원과 공유가 필요한 작업
- 기획부터 구현까지 긴 프로젝트

### ⏭️ 백로그 없이 진행 가능

- 간단한 유틸리티 (1-2파일)
- 빠른 프로토타입
- 즉시 구현 가능한 작은 기능

---

## 폴더 구조

### 루트 백로그 (`docs/backlogs/`)

**용도**: 전체 homelab 인프라 관련

```
docs/backlogs/
├── README.md
└── epic{N}-{slug}/
    ├── overview.md
    ├── todo/
    ├── in-progress/
    └── done/
```

**예시**:
- Epic: NAS 통합 배포 자동화
- Epic: 공통 모니터링 시스템
- Epic: 네트워크 보안 설정

---

### 서비스별 백로그 (`services/{name}/docs/backlogs/`)

**용도**: 해당 서비스만의 기능 개발

```
services/trend-radar/docs/backlogs/
├── README.md
└── epic{N}-{slug}/
    ├── overview.md
    ├── todo/
    ├── in-progress/
    └── done/
```

**예시**:
- Epic: 트렌드 데이터 수집 기능
- Epic: 분석 API 구현
- Epic: 알림 시스템

---

## 파일명 규칙

### Epic 폴더
```
epic{N}-{slug}/

예: epic0-project-setup/
    epic1-core-feature/
    epic2-advanced-feature/
```

### Story 파일
```
story-{번호}-{slug}.md

예: story-01-setup-environment.md
    story-02-implement-auth.md
```

- 번호는 2자리 (01, 02, ... 10, 11)
- slug는 영문 소문자, 하이픈으로 연결

---

## 상태 관리

### 상태 종류

| 상태 | 폴더 | 설명 |
|------|------|------|
| Todo | `todo/` | 대기 중, 아직 시작 안 함 |
| In Progress | `in-progress/` | 현재 작업 중 |
| Done | `done/` | 완료됨 |

### 상태 변경 방법

```bash
# 작업 시작: todo → in-progress
mv epic0-project-setup/todo/story-01-*.md \
   epic0-project-setup/in-progress/

# 작업 완료: in-progress → done
mv epic0-project-setup/in-progress/story-01-*.md \
   epic0-project-setup/done/
```

### Claude 자동 처리

**작업 시작 트리거**:
- "진행한다", "시작하자", "할게", "해보자"
- → Story 파일을 `in-progress/`로 이동

**작업 완료 트리거**:
- Story의 모든 Acceptance Criteria 충족 시
- → Story 파일을 `done/`으로 이동

---

## README.md 업데이트

상태 변경 시 README.md도 함께 업데이트:

1. **현황 테이블**: Todo/In Progress/Done 개수 갱신
2. **Story 링크**: 새 경로로 업데이트
3. **상태 표시**: Todo → In Progress → Done

### 예시

```markdown
# 변경 전
| 01 | [환경 설정](epic0-project-setup/todo/story-01-setup.md) | Todo |

# 변경 후 (작업 시작)
| 01 | [환경 설정](epic0-project-setup/in-progress/story-01-setup.md) | 🔄 In Progress |

# 변경 후 (작업 완료)
| 01 | [환경 설정](epic0-project-setup/done/story-01-setup.md) | ✅ Done |
```

---

## Story 템플릿

```markdown
# Story {N}: {제목}

## User Story

사용자가 [행동]하면, [결과]를 얻는다.

## Acceptance Criteria

- [ ] 기준 1
- [ ] 기준 2
- [ ] 기준 3

## 비기능 요구사항

- 성능: ...
- 보안: ...

## Dependencies

- Story XX 완료 후 시작 가능

---

## 구현 노트 (작업 중 추가)

### 기술 결정
- ...

### 이슈/해결
- ...

---

**Last Updated**: YYYY-MM-DD
```

---

## Epic 추가 시

1. 폴더 생성: `docs/backlogs/epic{N}-{slug}/`
2. 하위 폴더 생성: `todo/`, `in-progress/`, `done/`
3. `overview.md` 작성
4. `README.md`에 Epic 섹션 추가

---

## 백로그 작성 원칙

> CLAUDE.md의 "백로그 작성 원칙" 참조

### 포함할 것
- User Story (As a user, I want to...)
- Acceptance Criteria
- 비기능 요구사항
- 우선순위
- 의존성

### 포함하지 말 것
- 구체적인 코드 예시
- 세부 아키텍처
- 기술 스택 선택
- 구현 방법
- 파일/폴더 구조

### 이유
```
"설계와 구현은 함께 고민하면서 성장하는 과정"

미리 다 정해놓으면:
- 고민할 기회가 없어짐
- 상황에 맞지 않는 결정이 될 수 있음
- 유연성이 떨어짐

구현 시점에 결정하면:
- 최선의 선택 가능
- 현재 상황에 맞는 결정
- 학습과 성장 기회
```

---

## 서비스별 백로그 예시

### Trend Radar 서비스

```
services/trend-radar/docs/backlogs/
├── README.md
├── epic0-data-collection/
│   ├── overview.md
│   ├── todo/
│   │   └── story-01-github-api.md
│   ├── in-progress/
│   └── done/
└── epic1-analysis/
    ├── overview.md
    ├── todo/
    ├── in-progress/
    └── done/
```

### Ping Service 백로그 없이 진행

```
services/ping-service/
├── docs/
│   └── README.md        # 백로그 없이 간단한 문서만
├── src/
└── Dockerfile
```

---

## 참고 문서

| 문서 | 경로 |
|------|------|
| homelab 구조 | [../homelab-structure.md](../homelab-structure.md) |
| 워크플로우 | [../workflow.md](../workflow.md) |
| 코딩 규칙 | [./coding-standards.md](./coding-standards.md) |

---

**Last Updated**: 2026-01-04
