#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

UV_CACHE_DIR=.uv-cache uv run python gemini_generate_test_images.py \
  --model "${GEMINI_IMAGE_MODEL:-gemini-3.1-flash-image}" \
  --output-dir ../ref/gemini-generated-diagrams/batch-001 \
  --start "${START:-0}" \
  --limit "${LIMIT:-20}" \
  --workers 1 \
  --rate-limit-seconds "${RATE_LIMIT_SECONDS:-45}" \
  --retries "${RETRIES:-12}" \
  --retry-initial-delay "${RETRY_INITIAL_DELAY:-60}" \
  --retry-max-delay "${RETRY_MAX_DELAY:-600}" \
  --skip-existing
