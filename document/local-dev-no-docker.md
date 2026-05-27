# Local Test — Bina Docker (Mac)

Docker Desktop se pehle API test karne ke liye:

1. **Homebrew** se PostgreSQL + Redis (same logic, localhost pe)
2. **Python venv** se FastAPI directly port `8000`

NGINX is step skip hota hai local pe — baad mein Docker compose mein add hoga.

---

## Step 1 — Ek baar setup

```bash
cd /Users/rishabhdabral/workspace_aditya
chmod +x scripts/*.sh
./scripts/setup-local-mac.sh
```

Yeh karega:
- `brew install postgresql@16 redis`
- Services start
- User `appuser`, database `appdb`
- `.env.local` file create

---

## Step 2 — API chalao (Terminal 1)

```bash
./scripts/run-local.sh
```

Browser: http://127.0.0.1:8000/docs

---

## Step 3 — Test (Terminal 2)

```bash
./scripts/test-local.sh
```

---

## Manual curl

```bash
curl http://127.0.0.1:8000/health
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"namaste"}'
```

---

## Docker vs local — farq

| | Bina Docker | Docker Compose |
|--|-------------|----------------|
| URL | `http://127.0.0.1:8000` | `http://localhost` (port 80) |
| NGINX | ❌ | ✅ |
| Postgres host | `127.0.0.1` | `db` |
| Env file | `.env.local` | `.env` |

---

## Common errors

| Error | Fix |
|-------|-----|
| `connection refused` Postgres | `brew services start postgresql@16` |
| `connection refused` Redis | `brew services start redis` |
| `/health` 503 | `./scripts/setup-local-mac.sh` dubara |
| Port 8000 busy | `lsof -i :8000` → process kill |

---

## Homebrew nahi hai?

Install: https://brew.sh

Ya sirf chat test (health fail hoga):

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --port 8000
curl http://127.0.0.1:8000/        # OK
curl http://127.0.0.1:8000/chat ... # OK (rules)
# /health → 503 until Postgres+Redis running
```
