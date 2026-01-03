# Story 01: Claude Usage Ping Service 구현

**우선순위**: P1
**Status**: 🔄 In Progress

---

## User Story

Claude Max 플랜 사용자가 5시간 사용량 리셋 사이클을 개발 시간에 맞춰 관리하고 싶다.

---

## Why

- weaveFI 프로젝트와 무관한 Claude API 사용량 관리 로직
- 여러 프로젝트에서 공통으로 사용할 수 있는 유틸리티 서비스
- 독립적인 스케줄러로 분리하여 관리 용이성 향상

**스케줄 전략**:
- 08:00 KST → 5시간 후 13:00 리셋
- 13:00 KST → 5시간 후 18:00 리셋
- 18:00 KST → 5시간 후 23:00 리셋
- 20:00 개발 시작 시 fresh한 사용량 확보 (18:00 사이클 활용)

---

## Acceptance Criteria

- [ ] Claude API에 간단한 ping 요청 전송 (08:00, 13:00, 18:00 KST)
- [ ] Slack 알림 전송 (토큰 사용량, 다음 리셋 시간)
- [ ] Docker Compose로 간편하게 실행 가능
- [ ] 환경변수로 API 키, Webhook URL 설정

---

## 비기능 요구사항

- 경량 컨테이너 (NAS 또는 클라우드에서 실행 가능)
- 장애 발생 시 Slack으로 에러 알림

---

## Dependencies

- 없음 (독립 서비스)

---

## 구현 노트

> 구현 시 작성

---

**Last Updated**: 2026-01-03
