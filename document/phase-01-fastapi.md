# Phase 1 — FastAPI Application

## Is phase mein kya banega

Ek minimal **backend + light AI** API jo baad mein Docker mein jayegi.

### Endpoints (target)

| Method | Path | Kya karega |
|--------|------|------------|
| GET | `/` | Welcome / API info |
| GET | `/health` | **Required** — DB + Redis status (deploy health checks) |
| POST | `/chat` ya `/predict` | Simple AI: rule-based **ya** OpenAI (env se key) |

---

## Folder structure (is phase ke baad)

```text
app/
├── __init__.py
├── main.py           # FastAPI app, routes
├── config.py         # settings from env
├── database.py       # Postgres connection (optional phase 3 tak stub)
└── services/
    └── ai.py         # AI logic
requirements.txt
```

---

## Step-by-step — kaise banega

### Step 1.1 — Virtual env (local dev)

```bash
cd /path/to/workspace_aditya
python3 -m venv .venv
source .venv/bin/activate
pip install fastapi uvicorn[standard] sqlalchemy asyncpg redis httpx pydantic-settings
```

### Step 1.2 — `requirements.txt`

Dependencies list — Docker build isi se karega.

### Step 1.3 — `app/main.py` — core app

**Kya likhoge:**

1. `FastAPI()` instance
2. `GET /health` → JSON:
   ```json
   {
     "status": "ok",
     "version": "1.0.0",
     "database": "connected | disconnected",
     "redis": "connected | disconnected"
   }
   ```
3. Simple `POST /chat` — body: `{"message": "hello"}`  
   - **Without OpenAI:** echo + keyword reply (assignment ke liye enough)  
   - **With OpenAI (bonus):** `OPENAI_API_KEY` env se call

### Step 1.4 — Config from environment

`pydantic-settings` se:

- `DATABASE_URL`
- `REDIS_URL`
- `APP_ENV`

Local test ke liye `.env` file (gitignore mein).

### Step 1.5 — Local run (Docker se pehle)

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Test:

```bash
curl http://localhost:8000/health
curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"message":"hi"}'
```

---

## `/health` kyun important hai

- **Docker** `HEALTHCHECK` isi URL ko call karega
- **NGINX** upstream healthy hai ya nahi — optional advanced
- **GitHub Actions** deploy ke baad verify: `curl http://EC2_IP/health`
- **Evaluator** turant check kar sakta hai

Design tip: DB/Redis down ho to `status: "degraded"` + HTTP 503 (optional).

---

## AI endpoint — 2 options

### Option A — Simple (recommended start)

```python
# Rule-based — no API key, no cost
if "hello" in message.lower():
    return {"reply": "Hello! How can I help?"}
return {"reply": f"You said: {message}"}
```

### Option B — OpenAI (bonus marks)

- Env: `OPENAI_API_KEY`
- `httpx` se OpenAI API
- Doc mein likho: key GitHub Secrets mein, server `.env` mein

---

## Is phase ka output (deliverable)

- [ ] `app/` folder with working routes
- [ ] `requirements.txt`
- [ ] Local `uvicorn` se `/health` 200
- [ ] `document/` mein yeh file ke neeche progress update

---

## Agli phase

Jab local API chal jaye → [phase-02-docker.md](./phase-02-docker.md) — same app ko container mein pack karna.

---

## Meri progress

| Step | Status | Date |
|------|--------|------|
| venv + install | ✅ | 2026-05-27 |
| `/health` working | ✅ (code ready; Docker test pending) | 2026-05-27 |
| `/chat` working | ✅ | 2026-05-27 |
| requirements.txt | ✅ | 2026-05-27 |

**Notes / errors:**

```text

```
