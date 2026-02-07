"""OCR 텍스트 블록 추출 + 본문 필터링"""

import os
from collections import defaultdict
from dataclasses import dataclass, field

import pytesseract
from PIL import Image
from pytesseract import Output


@dataclass
class TextBlock:
    bbox: tuple[int, int, int, int]  # (x_min, y_min, x_max, y_max)
    text: str
    word_count: int
    line_count: int
    avg_conf: float
    translated: str = ""


def extract_text_blocks(image: Image.Image) -> list[TextBlock]:
    """Tesseract OCR로 텍스트 블록 추출 (바운딩박스 포함)"""
    data = pytesseract.image_to_data(image, lang="eng", output_type=Output.DICT)

    # 단어를 block_num으로 그룹핑
    blocks: dict[int, list[dict]] = defaultdict(list)
    for i in range(len(data["text"])):
        if (
            data["level"][i] == 5
            and data["conf"][i] > 30
            and data["text"][i].strip()
        ):
            blocks[data["block_num"][i]].append(
                {
                    "text": data["text"][i],
                    "left": data["left"][i],
                    "top": data["top"][i],
                    "width": data["width"][i],
                    "height": data["height"][i],
                    "conf": data["conf"][i],
                    "line_num": data["line_num"][i],
                    "par_num": data["par_num"][i],
                }
            )

    result = []
    for words in blocks.values():
        x_min = min(w["left"] for w in words)
        y_min = min(w["top"] for w in words)
        x_max = max(w["left"] + w["width"] for w in words)
        y_max = max(w["top"] + w["height"] for w in words)

        # 줄 단위로 텍스트 재구성
        lines: dict[tuple, list[dict]] = defaultdict(list)
        for w in words:
            lines[(w["par_num"], w["line_num"])].append(w)

        text_lines = []
        for key in sorted(lines.keys()):
            line_words = sorted(lines[key], key=lambda w: w["left"])
            text_lines.append(" ".join(w["text"] for w in line_words))

        unique_lines = set((w["par_num"], w["line_num"]) for w in words)

        result.append(
            TextBlock(
                bbox=(x_min, y_min, x_max, y_max),
                text="\n".join(text_lines),
                word_count=len(words),
                line_count=len(unique_lines),
                avg_conf=sum(w["conf"] for w in words) / len(words),
            )
        )

    return result


def filter_body_blocks(
    blocks: list[TextBlock],
    page_width: int,
    page_height: int,
) -> list[TextBlock]:
    """본문 텍스트 블록만 필터링 (라벨/주석 제외)"""
    min_width_ratio = float(os.getenv("MIN_BLOCK_WIDTH_RATIO", "0.3"))
    min_lines = int(os.getenv("MIN_BLOCK_LINES", "2"))
    min_words = int(os.getenv("MIN_BLOCK_WORDS", "5"))
    min_conf = float(os.getenv("MIN_CONFIDENCE", "40"))

    body_blocks = []
    for block in blocks:
        bw = block.bbox[2] - block.bbox[0]
        width_ratio = bw / page_width

        if width_ratio < min_width_ratio:
            continue
        if block.line_count < min_lines:
            continue
        if block.word_count < min_words:
            continue
        if block.avg_conf < min_conf:
            continue

        body_blocks.append(block)

    return body_blocks
