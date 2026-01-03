#!/bin/bash
# =============================================================================
# Claude 볼륨 마이그레이션 스크립트
# =============================================================================
# 기존 weavefi-private-claude 볼륨을 homelab-claude로 복사
#
# 사용법:
#   ./scripts/migrate-claude-volume.sh
# =============================================================================

set -e

SOURCE_VOLUME="weavefi-private-claude"
TARGET_VOLUME="homelab-claude"

echo "🔄 Claude 볼륨 마이그레이션 시작"
echo "   Source: $SOURCE_VOLUME"
echo "   Target: $TARGET_VOLUME"
echo ""

# 소스 볼륨 존재 확인
if ! docker volume inspect "$SOURCE_VOLUME" > /dev/null 2>&1; then
    echo "❌ 소스 볼륨이 존재하지 않습니다: $SOURCE_VOLUME"
    exit 1
fi

# 타겟 볼륨 생성 (없으면)
if docker volume inspect "$TARGET_VOLUME" > /dev/null 2>&1; then
    echo "⚠️  타겟 볼륨이 이미 존재합니다: $TARGET_VOLUME"
    read -p "덮어쓰시겠습니까? (y/N): " confirm
    if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
        echo "취소되었습니다."
        exit 0
    fi
else
    echo "📦 타겟 볼륨 생성: $TARGET_VOLUME"
    docker volume create "$TARGET_VOLUME"
fi

# 데이터 복사
echo "📋 데이터 복사 중..."
docker run --rm \
    -v "$SOURCE_VOLUME":/from:ro \
    -v "$TARGET_VOLUME":/to \
    alpine sh -c "cp -av /from/. /to/"

echo ""
echo "✅ 마이그레이션 완료!"
echo ""
echo "다음 단계:"
echo "1. homelab 서비스 시작: docker-compose -p homelab up -d"
echo "2. ai-trading-system에서 external volume 사용하도록 수정"
echo "3. 기존 볼륨 삭제 (선택): docker volume rm $SOURCE_VOLUME"