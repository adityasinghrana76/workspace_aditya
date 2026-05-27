#!/usr/bin/env bash
# Mac: Homebrew se PostgreSQL + Redis install/start (Docker ke bina)
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if ! command -v brew &>/dev/null; then
  echo "Homebrew chahiye: https://brew.sh"
  exit 1
fi

echo "==> Installing PostgreSQL + Redis (agar pehle se nahi)..."
brew install postgresql@16 redis

echo "==> Starting services..."
brew services start postgresql@16 2>/dev/null || brew services start postgresql
brew services start redis

# Homebrew Postgres bin path (Apple Silicon / Intel)
for PG_BIN in /opt/homebrew/opt/postgresql@16/bin /usr/local/opt/postgresql@16/bin; do
  if [[ -d "$PG_BIN" ]]; then
    export PATH="$PG_BIN:$PATH"
    break
  fi
done

echo "==> Waiting for PostgreSQL..."
for i in {1..30}; do
  if pg_isready -q 2>/dev/null; then
    break
  fi
  sleep 1
done

if ! pg_isready -q; then
  echo "PostgreSQL start nahi hua. Check: brew services list"
  exit 1
fi

echo "==> Creating app user + database..."
psql postgres -v ON_ERROR_STOP=1 <<'SQL'
DO $$
BEGIN
  IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'appuser') THEN
    CREATE ROLE appuser LOGIN PASSWORD 'change_me_strong';
  END IF;
END
$$;
SQL

if ! psql postgres -tAc "SELECT 1 FROM pg_database WHERE datname='appdb'" | grep -q 1; then
  psql postgres -v ON_ERROR_STOP=1 -c "CREATE DATABASE appdb OWNER appuser;"
else
  echo "Database appdb already exists."
fi

psql postgres -v ON_ERROR_STOP=1 -c "GRANT ALL PRIVILEGES ON DATABASE appdb TO appuser;"

if [[ ! -f .env.local ]]; then
  cp .env.local.example .env.local
  echo "Created .env.local"
fi

echo ""
echo "Setup done."
echo "  Redis:    redis-cli ping  (expect PONG)"
echo "  Postgres: psql postgresql://appuser:change_me_strong@127.0.0.1:5432/appdb -c 'SELECT 1'"
echo ""
echo "Next: ./scripts/run-local.sh"
