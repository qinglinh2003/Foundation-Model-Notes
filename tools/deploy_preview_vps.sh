#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

REMOTE="${REMOTE:-user@YOUR_VPS_IP}"
SSH_PORT="${SSH_PORT:-22}"
REMOTE_DIR="${REMOTE_DIR:-/workspace/preview}"

python3 tools/export_pdfs.py

rsync -az \
  -e "ssh -p ${SSH_PORT}" \
  dist/ "${REMOTE}:${REMOTE_DIR}/"

echo "Preview files synced to ${REMOTE}:${REMOTE_DIR}"
echo
echo "On this Vast profile, the existing Jupyter file server is the easiest preview path."
echo "Open Jupyter, then browse:"
echo "  /files/workspace/preview/index.html"
echo
echo "If you want to use an SSH tunnel instead:"
echo "  ssh -p ${SSH_PORT} ${REMOTE} -L 8081:localhost:8081"
echo "  ssh -p ${SSH_PORT} ${REMOTE} \"cd ${REMOTE_DIR} && python3 -m http.server 8081\""
echo "  http://localhost:8081/"
