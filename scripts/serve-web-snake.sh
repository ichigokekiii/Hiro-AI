#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
PORT="${PORT:-8080}"

echo "Snake web game: http://127.0.0.1:${PORT}/"
echo "Open this URL from Cursor mobile web if tunneled/public."
python3 -m http.server "$PORT" --directory docs
