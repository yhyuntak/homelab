"""PDF 번역기 - 스캔 PDF의 본문 텍스트를 한국어로 번역"""

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

import pymupdf
from PIL import Image

from ocr import TextBlock, extract_text_blocks, filter_body_blocks
from renderer import assemble_pdf, process_page
from translator import translate_blocks


def parse_page_range(page_range: str, total_pages: int) -> list[int]:
    """페이지 범위 파싱 (예: '1-5', '3', '10-20')"""
    if not page_range:
        return list(range(total_pages))

    parts = page_range.split("-")
    if len(parts) == 1:
        p = int(parts[0]) - 1  # 1-indexed → 0-indexed
        return [p]
    start = int(parts[0]) - 1
    end = int(parts[1])  # inclusive → exclusive
    return list(range(start, min(end, total_pages)))


def load_cache(cache_dir: Path, page_num: int) -> list[TextBlock] | None:
    """캐시된 번역 결과 로드"""
    cache_file = cache_dir / f"page_{page_num:04d}.json"
    if not cache_file.exists():
        return None

    data = json.loads(cache_file.read_text())
    return [
        TextBlock(
            bbox=tuple(b["bbox"]),
            text=b["text"],
            word_count=b["word_count"],
            line_count=b["line_count"],
            avg_conf=b["avg_conf"],
            translated=b.get("translated", ""),
        )
        for b in data
    ]


def save_cache(cache_dir: Path, page_num: int, blocks: list[TextBlock]) -> None:
    """번역 결과 캐시 저장"""
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_file = cache_dir / f"page_{page_num:04d}.json"
    data = [asdict(b) for b in blocks]
    cache_file.write_text(json.dumps(data, ensure_ascii=False, indent=2))


def extract_page_image(doc: pymupdf.Document, page_num: int, dpi: int = 300) -> Image.Image:
    """PDF 페이지를 PIL Image로 변환"""
    page = doc.load_page(page_num)
    pix = page.get_pixmap(dpi=dpi)
    return Image.frombytes("RGB", [pix.width, pix.height], pix.samples)


def main():
    parser = argparse.ArgumentParser(description="PDF 번역기 - 스캔 PDF 본문 텍스트 한국어 번역")
    parser.add_argument("input", help="입력 PDF 파일 경로")
    parser.add_argument("output", help="출력 PDF 파일 경로")
    parser.add_argument("--pages", help="페이지 범위 (예: 1-5, 3, 10-20)", default="")
    parser.add_argument("--dpi", type=int, default=300, help="이미지 추출 DPI (기본: 300)")
    parser.add_argument("--dry-run", action="store_true", help="OCR만 실행, 번역/렌더링 스킵")
    parser.add_argument("--no-cache", action="store_true", help="캐시 사용 안 함")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    cache_dir = output_path.parent / "cache"

    if not input_path.exists():
        print(f"입력 파일 없음: {input_path}")
        sys.exit(1)

    doc = pymupdf.open(str(input_path))
    total_pages = len(doc)
    pages = parse_page_range(args.pages, total_pages)
    print(f"총 {total_pages}페이지 중 {len(pages)}페이지 처리")

    result_images = []

    for idx, page_num in enumerate(pages):
        print(f"\n[{idx + 1}/{len(pages)}] 페이지 {page_num + 1} 처리 중...")

        # 1. 이미지 추출
        image = extract_page_image(doc, page_num, args.dpi)
        print(f"  이미지 추출 완료 ({image.width}x{image.height})")

        # 2. 캐시 확인
        blocks = None
        if not args.no_cache:
            blocks = load_cache(cache_dir, page_num)
            if blocks:
                print(f"  캐시 로드: {len(blocks)}개 블록")

        # 3. OCR + 필터링
        if blocks is None:
            all_blocks = extract_text_blocks(image)
            blocks = filter_body_blocks(all_blocks, image.width, image.height)
            print(f"  OCR: 전체 {len(all_blocks)}개 블록 → 본문 {len(blocks)}개 블록")

            if args.dry_run:
                # dry-run: 블록 정보만 출력
                for i, b in enumerate(blocks):
                    print(f"  블록 {i}: bbox={b.bbox}, words={b.word_count}, "
                          f"lines={b.line_count}, conf={b.avg_conf:.1f}")
                    print(f"    텍스트: {b.text[:100]}...")
                continue

            # 4. 번역
            if blocks:
                print(f"  번역 중 ({len(blocks)}개 블록)...")
                translations = translate_blocks(blocks)
                for block, trans in zip(blocks, translations):
                    block.translated = trans

                # 캐시 저장
                if not args.no_cache:
                    save_cache(cache_dir, page_num, blocks)

        if args.dry_run:
            continue

        # 5. 렌더링
        if blocks:
            result_image = process_page(image, blocks)
            print(f"  렌더링 완료")
        else:
            result_image = image
            print(f"  본문 블록 없음, 원본 유지")

        result_images.append(result_image)

    if args.dry_run:
        print("\n[dry-run] OCR 결과만 출력했습니다. 번역/렌더링은 스킵.")
        return

    # 6. PDF 조합
    if result_images:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        assemble_pdf(result_images, str(output_path), args.dpi)
        print(f"\n완료! {len(result_images)}페이지 → {output_path}")
    else:
        print("\n처리된 페이지가 없습니다.")

    doc.close()


if __name__ == "__main__":
    main()
