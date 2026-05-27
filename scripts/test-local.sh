#!/usr/bin/env bash
# API tests (server alag terminal mein ./scripts/run-local.sh chal raha ho)
set -euo pipefail

BASE="${1:-http://127.0.0.1:8000}"

echo "==> GET $BASE/"
curl -sf "$BASE/" | python3 -m json.tool

echo ""
echo "==> GET $BASE/health"
curl -sf "$BASE/health" | python3 -m json.tool

echo ""
echo "==> POST $BASE/chat"
curl -sf -X POST "$BASE/chat" \
  -H "Content-Type: application/json" \
  -d '{"message":"hello"}' | python3 -m json.tool

echo ""
echo "All local tests passed."
