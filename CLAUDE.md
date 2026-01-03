# homelab

> 개인 유틸리티 서비스들을 도커 컨테이너로 관리하는 홈랩

---

## 날짜 확인
- 현재 날짜가 필요할 때는 항상 `date` 명령어를 실행해서 확인할 것
- 특정 연도라고 가정하지 말 것

## 프로젝트 목표

### 핵심 가치

- **단순함 우선**: 복잡하게 만들지 않는다
- **필요할 때 만든다**: 미리 설계하지 않고, 필요하면 추가
- **컨테이너 단위**: 각 서비스는 독립적인 도커 컨테이너로 격리

### 개발 철학

- 생각날 때 만들고, 필요 없으면 내린다
- 완벽보다 동작하는 것
- 각 서비스는 독립적으로 실행 가능해야 함

### 하지 않는 것

```
- 완벽한 아키텍처 설계
- 과도한 추상화/일반화
- 사용하지도 않을 기능 미리 만들기
- 복잡한 의존성 구조
```

---

## 핵심 원칙

### 개발 원칙
- **작고 단순하게 시작** (MVP 우선)
- **Code First**: 동작하는 것부터 만들고 진화
- **한 번에 하나씩** 구현하고 검증
- **과도한 추상화 지양**

### Claude 작업 방식 (필수)

> **중요**: 코드 작성 전에 반드시 설명부터. 설명 없는 코드 작성 금지.

**매 스텝마다 필수 포함:**
1. **무엇을 할 것인가** - 이번 스텝에서 만들 것
2. **왜 필요한가** - 이 코드/파일이 필요한 이유
3. **어떻게 동작하는가** - 핵심 개념과 패턴 설명
4. **코드 작성** - 설명 후 코드 작성

**예시 (좋은 예):**
```
"Step 2: API 클라이언트를 만듭니다.

**무엇을?** 백엔드 API를 호출하는 함수

**왜?** 데이터를 가져오려면 fetch 로직이 필요.
별도 파일로 분리하면 재사용 가능하고 테스트하기 쉬움.

**핵심 개념:**
- Response 타입: 백엔드 응답 구조와 1:1 매칭
- async/await: 비동기 HTTP 요청 처리

이제 코드를 작성합니다..."
```

**금지 사항:**
- ❌ 설명 없이 바로 코드 작성
- ❌ "Step 1 완료. Step 2로 넘어갑니다" (설명 없음)
- ❌ 코드만 던지고 끝

### 백로그/스토리 작성 원칙
> **핵심**: 요구사항(What)만 작성, 구현 방법(How)은 작성 안 함

- ✅ User Story, Acceptance Criteria, Why, Dependencies
- ❌ 코드 스니펫, 디렉토리 구조, 구현 방법

---

## 기술 스택

| 영역 | 기술 |
|------|------|
| 컨테이너 | Docker, Docker Compose |
| 언어 | 자유 (Python, Go, Node.js 등 상황에 맞게) |
| 배포 | NAS 또는 개인 서버 |

---

## 특수 명령어 (전문가 호출)

| 이름 | 역할 | 에이전트 |
|------|------|---------|
| **엘리** | 제품 관리, 전략 | `silicon-valley-pm-veteran` |
| **알렌** | 풀스택 개발, 시스템 아키텍처 | `silicon-valley-veteran` |
| **클로이** | 디자인, UX | `silicon-valley-design-veteran` |

---

## 백로그 관리

- **위치**: `docs/backlogs/`
- **구조**: Epic 기반 (epic0-project-setup, epic1-*, ...)
- **상태**: todo/ → in-progress/ → done/

> 상세: [.claude/rules/backlog-rules.md](.claude/rules/backlog-rules.md)

---

## 문서 관리 규칙

> **중요**: 코드 변경 시 관련 문서도 함께 업데이트

| 변경 영역 | 업데이트할 문서 |
|----------|----------------|
| 개발 프로세스/워크플로우 | `.claude/rules/workflow.md` |
| 백로그 구조 변경 | `.claude/rules/backlog-rules.md` |
| 프로젝트별 코딩 규칙 | `.claude/rules/project-rules.md` |
| 아키텍처 변경 | `docs/architecture/` |

---

## 참고 문서

| 문서 | 경로 |
|------|------|
| 워크플로우 | [.claude/rules/workflow.md](.claude/rules/workflow.md) |
| 백로그 관리 | [.claude/rules/backlog-rules.md](.claude/rules/backlog-rules.md) |
| 프로젝트 규칙 | [.claude/rules/project-rules.md](.claude/rules/project-rules.md) |
| 아키텍처 | [docs/architecture/](docs/architecture/) |

---

**Last Updated**: 2026-01-03
