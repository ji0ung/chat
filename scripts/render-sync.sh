#!/usr/bin/env bash
set -euo pipefail
if [[ -z "${RENDER_DEPLOY_HOOK_URL:-}" ]]; then echo "RENDER_DEPLOY_HOOK_URL 환경변수를 설정하세요." >&2; exit 1; fi
curl --fail --silent --show-error -X POST "$RENDER_DEPLOY_HOOK_URL"
echo "Render 배포를 요청했습니다. Render 대시보드에서 상태를 확인하세요."
