"""화이트아웃 + 한글 텍스트 렌더링 + PDF 조합"""

import io
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# 한글 폰트 경로 후보 (Docker 컨테이너 내)
FONT_CANDIDATES = [
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/noto/NotoSansKR-Regular.ttf",
]

_font_path: str | None = None


def _find_font() -> str:
    """사용 가능한 한글 폰트 경로 탐색"""
    global _font_path
    if _font_path:
        return _font_path
    for path in FONT_CANDIDATES:
        if Path(path).exists():
            _font_path = path
            return path
    raise FileNotFoundError(f"한글 폰트를 찾을 수 없습니다: {FONT_CANDIDATES}")


def whiteout_block(image: Image.Image, bbox: tuple, padding: int = 3) -> None:
    """바운딩박스 영역을 흰색으로 덮기"""
    draw = ImageDraw.Draw(image)
    x_min, y_min, x_max, y_max = bbox
    draw.rectangle(
        [x_min - padding, y_min - padding, x_max + padding, y_max + padding],
        fill="white",
    )


def _wrap_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    font: ImageFont.FreeTypeFont,
    max_width: int,
) -> str:
    """텍스트를 max_width에 맞게 줄바꿈"""
    paragraphs = text.split("\n")
    result_lines = []

    for paragraph in paragraphs:
        if not paragraph.strip():
            result_lines.append("")
            continue

        current_line = ""
        for char in paragraph:
            test_line = current_line + char
            line_width = draw.textlength(test_line, font=font)
            if line_width > max_width and current_line:
                result_lines.append(current_line)
                current_line = char
            else:
                current_line = test_line
        if current_line:
            result_lines.append(current_line)

    return "\n".join(result_lines)


def render_korean_text(image: Image.Image, bbox: tuple, text: str) -> None:
    """바운딩박스 영역에 한글 텍스트 렌더링 (폰트 크기 자동 조절)"""
    draw = ImageDraw.Draw(image)
    x_min, y_min, x_max, y_max = bbox
    box_width = x_max - x_min
    box_height = y_max - y_min

    font_path = _find_font()

    # 초기 폰트 크기: 박스 높이 기반 추정
    estimated_lines = max(text.count("\n") + 1, 3)
    initial_size = max(14, box_height // estimated_lines)

    # 폰트 크기를 줄여가며 박스에 맞는 크기 탐색
    for font_size in range(initial_size, 8, -1):
        font = ImageFont.truetype(font_path, font_size)
        wrapped = _wrap_text(draw, text, font, box_width)
        text_bbox = draw.multiline_textbbox((0, 0), wrapped, font=font)
        text_height = text_bbox[3] - text_bbox[1]
        if text_height <= box_height:
            break
    else:
        # 최소 크기로도 안 맞으면 그냥 최소 크기로 렌더링
        font = ImageFont.truetype(font_path, 8)
        wrapped = _wrap_text(draw, text, font, box_width)

    # 세로 중앙 정렬
    text_bbox = draw.multiline_textbbox((0, 0), wrapped, font=font)
    text_height = text_bbox[3] - text_bbox[1]
    y_offset = y_min + max(0, (box_height - text_height) // 2)

    draw.multiline_text(
        (x_min, y_offset),
        wrapped,
        font=font,
        fill="black",
        spacing=4,
    )


def process_page(image: Image.Image, blocks: list) -> Image.Image:
    """페이지 이미지에 번역된 블록들을 오버레이"""
    result = image.copy()
    for block in blocks:
        if not block.translated:
            continue
        whiteout_block(result, block.bbox)
        render_korean_text(result, block.bbox, block.translated)
    return result


def assemble_pdf(images: list[Image.Image], output_path: str, dpi: int = 300) -> None:
    """이미지 리스트를 PDF로 조합"""
    if not images:
        raise ValueError("이미지가 없습니다")

    images[0].save(
        output_path,
        "PDF",
        save_all=True,
        append_images=images[1:],
        resolution=dpi,
    )
    print(f"PDF 저장 완료: {output_path}")
