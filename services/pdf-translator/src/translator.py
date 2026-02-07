"""Grok API를 이용한 영→한 번역"""

import os
import time

from openai import OpenAI

client = None

SYSTEM_PROMPT = (
    "You are a professional English-to-Korean translator "
    "specializing in anatomy and kinesiology textbooks. "
    "Translate the following text naturally into Korean. "
    "Keep anatomical terms in format: 한글명(English term). "
    "Example: 승모근(Trapezius). "
    "Return ONLY the translated text, nothing else."
)

BATCH_SYSTEM_PROMPT = (
    "You are a professional English-to-Korean translator "
    "specializing in anatomy textbooks. "
    "Translate each text block separated by '---BLOCK_SEPARATOR---'. "
    "Keep the same separator between translated blocks. "
    "Keep anatomical terms in format: 한글명(English term). "
    "Return ONLY translated text with separators."
)

SEPARATOR = "---BLOCK_SEPARATOR---"


def _get_client() -> OpenAI:
    global client
    if client is None:
        client = OpenAI(
            api_key=os.environ["XAI_API_KEY"],
            base_url="https://api.x.ai/v1",
        )
    return client


def _get_model() -> str:
    return os.getenv("GROK_MODEL", "grok-3-latest")


def translate(text: str) -> str:
    """단일 텍스트 블록 번역"""
    for attempt in range(3):
        try:
            response = _get_client().chat.completions.create(
                model=_get_model(),
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": text},
                ],
                temperature=0.3,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            if attempt < 2:
                wait = 2 ** (attempt + 1)
                print(f"  API 에러, {wait}초 후 재시도: {e}")
                time.sleep(wait)
            else:
                raise


def translate_blocks(blocks: list) -> list[str]:
    """여러 블록을 한 번의 API 호출로 번역 (비용/속도 절약)"""
    if not blocks:
        return []

    if len(blocks) == 1:
        return [translate(blocks[0].text)]

    combined = f"\n{SEPARATOR}\n".join(b.text for b in blocks)

    for attempt in range(3):
        try:
            response = _get_client().chat.completions.create(
                model=_get_model(),
                messages=[
                    {"role": "system", "content": BATCH_SYSTEM_PROMPT},
                    {"role": "user", "content": combined},
                ],
                temperature=0.3,
            )
            result = response.choices[0].message.content.strip()
            translations = [t.strip() for t in result.split(SEPARATOR)]

            # 분리 개수가 안 맞으면 개별 번역으로 폴백
            if len(translations) != len(blocks):
                print(f"  배치 분리 불일치 ({len(translations)} vs {len(blocks)}), 개별 번역으로 전환")
                return [translate(b.text) for b in blocks]

            return translations
        except Exception as e:
            if attempt < 2:
                wait = 2 ** (attempt + 1)
                print(f"  API 에러, {wait}초 후 재시도: {e}")
                time.sleep(wait)
            else:
                raise
