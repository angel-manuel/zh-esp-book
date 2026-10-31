#!/bin/bash
# Cross-check pinyin against characters with pypinyin (via uv, nothing to install).
cd "$(dirname "$0")/.."
exec uv run --quiet --with pypinyin python3 scripts/check-pinyin.py "$@"
