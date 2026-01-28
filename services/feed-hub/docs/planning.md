# Feed Hub 기획 문서

> 정보의 바다에서 관심 있는 콘텐츠를 자동 수집하고, 분석하고, 한 곳에서 모아보는 서비스

---

## 1. 배경 및 문제

### 현재 상황
- 정보가 **여러 곳에 산발적**으로 흩어져 있음
  - 구글 크롬 추천 게시글
  - 링크드인
  - 유튜브
  - X (Twitter)
- 각 플랫폼을 일일이 확인해야 함
- 중요한 정보를 놓치기 쉬움

### 원하는 것
- **한 곳에서 모아보기** (대시보드)
- **자동 수집** (직접 돌아다니지 않아도)
- **유튜브 영상 깊이 분석** (자막 추출 → 요약 → 사실 검증)
- **알림** (Slack/Discord로 중요한 것만)

---

## 2. 핵심 기능

### 2.1 정보 수집 (Aggregation)

다양한 소스에서 자동으로 콘텐츠 수집:

| 소스 타입 | 예시 |
|-----------|------|
| 유튜브 채널 | 조코딩, 노마드코더, Fireship, ... |
| RSS 피드 | Hacker News, TechCrunch, ... |
| X (Twitter) | AI/테크 인플루언서 계정 |
| Reddit | r/LocalLLaMA, r/MachineLearning, ... |
| 뉴스레터 | The Rundown AI, Ben's Bites, ... |
| GitHub | Trending repositories |
| 학술/연구 | arXiv (cs.AI, cs.LG) |

### 2.2 유튜브 콘텐츠 분석 (Deep Analysis)

```
유튜브 URL 입력
    ↓
자막 추출 (자동 생성 자막 포함)
    ↓
내용 요약 + 핵심 포인트 정리
    ↓
언급된 기술/서비스/출처 추출
    ↓
웹 검색으로 사실 검증 + 추가 정보
    ↓
검증된 분석 결과 제공
```

**핵심 아이디어**: 영상에서 언급된 출처들을 자동 추출 → "팔로우할 소스"로 추가 가능

### 2.3 콘텐츠 정리 (Curation)

- 중복 제거
- 관심 분야 기반 필터링
- 중요도/관련도 순 정렬

### 2.4 전달 (Delivery)

| 형태 | 설명 | 채널 |
|------|------|------|
| 웹 대시보드 | 모든 콘텐츠 모아보기 | 웹 |
| 즉시 알림 | 중요한 뉴스 (새 모델 출시 등) | Slack/Discord |
| 일일 다이제스트 | 오늘 수집된 것들 요약 | Slack/Discord |
| 주간 하이라이트 | 이번 주 핵심 정리 | 대시보드 |

---

## 3. 관심 분야

### 포함
- AI / LLM / 생성형 AI
- 코딩 도구 (Cursor, Claude Code, Copilot 등)
- 1인 개발 / 솔로프러너
- 스타트업 뉴스
- 하드웨어 (GPU, 로봇 등)
- 오픈소스 프로젝트

### 확장 가능
- 관심 분야는 **점진적으로 추가/제거** 가능해야 함
- 키워드 기반 필터링

---

## 4. 사용 시나리오

### 시나리오 1: 유튜브 영상 분석
```
1. 대시보드에서 유튜브 URL 입력
2. 시스템이 자막 추출 → 요약 → 검증
3. 결과 확인:
   - 3줄 요약
   - 핵심 포인트 5개
   - 언급된 기술/서비스 목록 (원 출처 링크 포함)
   - 자막 오류 수정 사항
4. "이 출처들 팔로우하기" 버튼 → 자동 소스 추가
```

### 시나리오 2: 일일 체크
```
1. 아침에 Discord/Slack 알림 확인
2. "오늘의 AI 뉴스 5개" 요약 읽기
3. 관심 가는 항목 클릭 → 원문 또는 상세 분석
```

### 시나리오 3: 주말 캐치업
```
1. 대시보드 접속
2. "이번 주 하이라이트" 탭
3. 놓친 중요 뉴스들 한눈에 확인
```

---

## 5. 기술 스택 (예정)

| 영역 | 후보 | 비고 |
|------|------|------|
| 언어 | Python | 크롤링/분석에 적합 |
| 웹 프레임워크 | FastAPI | API 서버 |
| 프론트엔드 | React / Next.js (또는 간단히 시작) | 대시보드 |
| DB | SQLite → PostgreSQL | 시작은 가볍게 |
| LLM | Claude API / OpenAI | 요약, 분석, 검증 |
| 자막 추출 | yt-dlp + Whisper | 유튜브 자막 |
| 알림 | Slack Webhook, Discord Webhook | |
| 배포 | Docker on NAS | homelab 통합 |

---

## 6. MVP 스코프 (제안)

### Phase 1: 유튜브 분석기
- [ ] 유튜브 URL → 자막 추출
- [ ] 자막 → 요약 + 핵심 포인트
- [ ] 언급된 기술/서비스 추출
- [ ] 웹 검색으로 사실 검증
- [ ] 간단한 웹 UI (URL 입력 → 결과 표시)

### Phase 2: 알림 연동
- [ ] Discord 웹훅 연동
- [ ] Slack 웹훅 연동
- [ ] 분석 결과 알림 전송

### Phase 3: 정보 소스 수집
- [ ] RSS 피드 수집기
- [ ] Hacker News API 연동
- [ ] Reddit API 연동
- [ ] 수집된 콘텐츠 대시보드

### Phase 4: 자동화 + 고도화
- [ ] 유튜브 채널 구독 → 신규 영상 자동 분석
- [ ] 일일/주간 다이제스트 자동 생성
- [ ] 관심 분야 필터링 고도화

---

## 7. 정보 소스 후보 목록

### 유튜브 채널 (한국)
- 조코딩
- 노마드코더
- 드림코딩
- 테크몽
- (추가 예정)

### 유튜브 채널 (해외)
- Fireship
- Theo - t3.gg
- AI Explained
- Two Minute Papers
- (추가 예정)

### RSS / 뉴스
- Hacker News (news.ycombinator.com)
- TechCrunch AI
- The Verge AI
- Ars Technica

### 뉴스레터
- The Rundown AI
- Ben's Bites
- TLDR AI
- (추가 예정)

### Reddit
- r/MachineLearning
- r/LocalLLaMA
- r/artificial
- r/singularity

### GitHub
- Trending (daily/weekly)
- 특정 토픽 (llm, ai, etc.)

### 학술
- arXiv cs.AI
- arXiv cs.LG
- Papers With Code

---

## 8. 미결정 사항

- [ ] 출력 형태 상세 (요약 길이, 알림 주기 등)
- [ ] API 비용 한도
- [ ] 대시보드 상세 UI/UX
- [ ] 관심 분야 키워드 목록 구체화

---

## 9. 참고

### 영감을 준 것
- 조코딩 유튜브 (다양한 소스에서 정보 수집)
- NotebookLM (유튜브 요약 + 분석)

### 관련 서비스
- Feedly (RSS 리더)
- Readwise Reader
- Perplexity (AI 검색)

---

**Created**: 2026-01-28
**Status**: 기획 중
