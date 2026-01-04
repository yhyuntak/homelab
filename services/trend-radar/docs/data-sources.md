# 데이터 소스

---

## 개요

| 소스 | 얻을 수 있는 것 | 난이도 | Phase |
|------|----------------|--------|-------|
| arXiv | 논문 제목, 초록, 키워드 | 쉬움 | 1 |
| GitHub | 스타 수, 트렌딩 프로젝트 | 쉬움 | 2 |
| Hacker News | 핫한 토픽, 댓글 반응 | 쉬움 | 2 |
| Reddit | 서브레딧별 인기 글 | 보통 | 2 |
| Google Trends | 검색량 추이 | 보통 | 2 |
| 뉴스 (RSS) | 기사 키워드 | 보통 | 2 |
| Twitter/X | 실시간 반응 | 어려움 | 3+ |

---

## 상세

### arXiv (Phase 1)

**URL**: https://arxiv.org/

**API**: https://arxiv.org/help/api

**관련 카테고리**:
- `cs.AI` - Artificial Intelligence
- `cs.LG` - Machine Learning
- `cs.CL` - Computation and Language (NLP)
- `cs.CV` - Computer Vision
- `cs.NE` - Neural and Evolutionary Computing

**수집 가능 데이터**:
- 논문 제목
- 초록 (abstract)
- 저자
- 발행일
- 카테고리

**활용**:
- 제목/초록에서 키워드 추출
- 키워드 빈도 변화 추적
- 새로운 용어 발견

---

### GitHub (Phase 2)

**URL**: https://github.com/trending

**API**: GitHub REST API / GraphQL

**수집 가능 데이터**:
- 트렌딩 저장소
- 스타 수 변화
- 언어별 인기 프로젝트
- 토픽/태그

**활용**:
- 스타 급증 프로젝트 감지
- 새로운 프레임워크/라이브러리 발견
- 기술 채택 트렌드

---

### Hacker News (Phase 2)

**URL**: https://news.ycombinator.com/

**API**: https://github.com/HackerNews/API

**수집 가능 데이터**:
- Top stories
- 포인트 수
- 댓글 수
- 링크 도메인

**활용**:
- 개발자 커뮤니티에서 뭐가 핫한지
- 새로운 스타트업/제품 발견
- 기술 논쟁 트렌드

---

### Reddit (Phase 2)

**URL**: https://reddit.com/

**관련 서브레딧**:
- r/MachineLearning
- r/artificial
- r/LocalLLaMA
- r/technology
- r/Futurology
- r/stocks, r/investing (투자 관점)

**수집 가능 데이터**:
- 인기 게시물
- 업보트 수
- 댓글 수/내용

---

### Google Trends (Phase 2)

**URL**: https://trends.google.com/

**활용**:
- 일반 대중의 관심도 측정
- 지역별 관심도 차이
- 관련 검색어 발견

**주의**:
- 공식 API 없음 (비공식 라이브러리 사용)
- Rate limit 있음

---

### 뉴스 RSS (Phase 2)

**소스 예시**:
- TechCrunch
- The Verge
- Wired
- MIT Technology Review
- 블룸버그 테크

**활용**:
- 메인스트림 미디어 커버리지
- 기업 발표, 인수합병 뉴스

---

## 미래 소스 (Phase 3+)

| 소스 | 설명 |
|------|------|
| 특허 DB | 기업별 특허 출원 동향 |
| 채용 공고 | LinkedIn, Indeed 등 |
| VC 투자 | Crunchbase, PitchBook |
| 컨퍼런스 | NeurIPS, ICML, CES 등 발표 |
| 정부 정책 | 규제 변화, 보조금 발표 |

---

**Last Updated**: 2026-01-04
