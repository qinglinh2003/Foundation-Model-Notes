#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

PORT="${1:-8080}"

if [[ ! -d dist ]]; then
  echo "dist/ does not exist. Run: python3 tools/export_pdfs.py" >&2
  exit 1
fi

echo "Serving dist/ at http://localhost:${PORT}/"
python3 -m http.server "${PORT}" -d dist
