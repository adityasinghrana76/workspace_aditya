#!/usr/bin/env bash
# FastAPI bina Docker — port 8000
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [[ ! -f .env.local ]]; then
  echo "Missing .env.local — run: ./scripts/setup-local-mac.sh"
  echo "Or: cp .env.local.example .env.local"
  exit 1
fi

if [[ ! -d .venv ]]; then
  echo "Creating virtualenv..."
  python3 -m venv .venv
fi

# shellcheck disable=SC1091
source .venv/bin/activate
pip install -q -r requirements.txt

echo "Starting API at http://127.0.0.1:8000"
echo "  Docs:   http://127.0.0.1:8000/docs"
echo "  Health: http://127.0.0.1:8000/health"
echo ""
exec uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
