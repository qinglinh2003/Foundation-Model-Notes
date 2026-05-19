#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEPLOY_ROOT="${DEPLOY_ROOT:-/var/www/html/capstone}"

cd "$PROJECT_ROOT"

python3 tools/export_pdfs.py

if [[ ! -d "$(dirname "$DEPLOY_ROOT")" ]]; then
  echo "Parent deploy root does not exist: $(dirname "$DEPLOY_ROOT")" >&2
  exit 1
fi

mkdir -p "$DEPLOY_ROOT"
rsync -av --delete "$PROJECT_ROOT/dist/" "$DEPLOY_ROOT/"

echo "Deployed Foundation Model Notes to $DEPLOY_ROOT"
