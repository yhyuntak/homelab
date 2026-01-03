# Epic 1: Claude Usage Ping Service

## 목표

Claude Max 플랜의 5시간 사용량 리셋 사이클을 관리하기 위한 독립적인 도커 서비스 구축

## 배경

- Claude Max 플랜은 5시간마다 사용량이 리셋됨
- 개발 시간에 맞춰 리셋 사이클을 조정하면 효율적인 사용 가능
- 기존 weaveFI 프로젝트에 있던 로직을 독립 서비스로 분리

## 범위

### 포함
- Claude API ping 스케줄러
- Slack 알림 연동
- Docker 컨테이너화

### 제외
- 복잡한 모니터링 대시보드
- 다른 LLM 서비스 연동

## Stories

| # | Story | 설명 |
|---|-------|------|
| 01 | Ping Service 구현 | 스케줄러 + API 호출 + Slack 알림 + Docker |

---

**Last Updated**: 2026-01-03
