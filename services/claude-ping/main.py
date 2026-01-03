"""
Claude Usage Ping Service

Claude Max 플랜의 5시간 사용량 리셋 사이클을 관리하기 위한 스케줄러.
08:00, 13:00, 18:00 KST에 Claude API를 호출하여 사이클을 맞춤.
"""

import asyncio
import subprocess
import os
import json
from datetime import datetime
from zoneinfo import ZoneInfo

import httpx
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

# 환경변수
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL", "")
TZ = ZoneInfo("Asia/Seoul")


def log(message: str) -> None:
    """타임스탬프와 함께 로그 출력"""
    now = datetime.now(TZ).strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now}] {message}", flush=True)


async def send_slack_message(text: str) -> None:
    """Slack Webhook으로 메시지 전송"""
    if not SLACK_WEBHOOK_URL:
        log("Slack Webhook URL not configured, skipping notification")
        return

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                SLACK_WEBHOOK_URL,
                json={"text": text},
                timeout=10.0,
            )
            if response.status_code != 200:
                log(f"Slack notification failed: {response.status_code}")
    except Exception as e:
        log(f"Slack notification error: {e}")


async def claude_ping() -> None:
    """
    Claude API에 간단한 ping 요청 전송

    Claude Code CLI를 사용하여 OAuth 인증으로 API 호출
    """
    current_time = datetime.now(TZ).strftime("%Y-%m-%d %H:%M:%S KST")
    log(f"Starting Claude ping at {current_time}")

    try:
        # Claude CLI로 간단한 요청 전송
        result = subprocess.run(
            [
                "claude",
                "-p", "안녕! 간단히 '확인' 이라고만 답해줘.",
                "--output-format", "json",
            ],
            capture_output=True,
            text=True,
            timeout=60,
        )

        if result.returncode == 0:
            # 성공
            try:
                output = json.loads(result.stdout)
                response_text = output.get("result", "")[:50]
                log(f"Claude ping success: {response_text}")

                # Slack 알림
                await send_slack_message(
                    f"🏓 Claude Ping 완료 ({current_time})\n"
                    f"• 응답: {response_text}\n"
                    f"• 5시간 후 사용량 리셋 예정"
                )
            except json.JSONDecodeError:
                log(f"Claude ping success (raw): {result.stdout[:100]}")
                await send_slack_message(
                    f"🏓 Claude Ping 완료 ({current_time})\n"
                    f"• 5시간 후 사용량 리셋 예정"
                )
        else:
            # 실패
            error_msg = result.stderr[:200] if result.stderr else "Unknown error"
            log(f"Claude ping failed: {error_msg}")
            await send_slack_message(
                f"❌ Claude Ping 실패 ({current_time})\n"
                f"• 에러: {error_msg}"
            )

    except subprocess.TimeoutExpired:
        log("Claude ping timeout")
        await send_slack_message(f"⏰ Claude Ping 타임아웃 ({current_time})")
    except Exception as e:
        log(f"Claude ping error: {e}")
        await send_slack_message(f"❌ Claude Ping 에러 ({current_time})\n• {e}")


async def main() -> None:
    """메인 스케줄러 실행"""
    log("Starting Claude Ping Service")
    log(f"Slack notifications: {'enabled' if SLACK_WEBHOOK_URL else 'disabled'}")

    scheduler = AsyncIOScheduler(timezone=TZ)

    # 08:00, 13:00, 18:00 KST에 실행
    for hour in [8, 13, 18]:
        scheduler.add_job(
            claude_ping,
            CronTrigger(hour=hour, minute=0, timezone=TZ),
            id=f"claude_ping_{hour}",
            name=f"Claude Ping at {hour}:00 KST",
        )
        log(f"Scheduled: Claude ping at {hour:02d}:00 KST")

    scheduler.start()
    log("Scheduler started, waiting for jobs...")

    # 시작 알림
    await send_slack_message(
        "🚀 Claude Ping Service 시작됨\n"
        "• 스케줄: 08:00, 13:00, 18:00 KST"
    )

    # 무한 대기
    try:
        while True:
            await asyncio.sleep(3600)  # 1시간마다 체크
    except (KeyboardInterrupt, SystemExit):
        log("Shutting down...")
        scheduler.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
