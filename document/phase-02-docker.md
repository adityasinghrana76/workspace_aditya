# Phase 2 — Dockerize the Application

## Is phase mein kya banega

Sirf **FastAPI** ka ek Docker image — abhi Postgres/Redis alag containers nahi (wo Phase 3).

### Files

```text
Dockerfile
.dockerignore
```

---

## Dockerfile — structure (samajhne ke liye)

```dockerfile
# Stage 1: base
FROM python:3.12-slim

WORKDIR /app

# System deps (if needed for psycopg2 etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl && rm -rf /var/lib/apt/lists/*

# Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App code
COPY app/ ./app/

# Non-root user (security — Phase 6 mein doc)
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Har line ka matlab

| Part | Kyun |
|------|------|
| `python:3.12-slim` | Chhota image, fast pull |
| `WORKDIR /app` | Saari commands is folder mein |
| `COPY requirements` pehle | Layer cache — code change pe deps dubara install nahi |
| `HEALTHCHECK` | Docker ko pata — container zinda hai ya nahi |
| `USER appuser` | Root se app mat chalao (production habit) |

---

## `.dockerignore`

Git / local junk image mein na jaye:

```text
.venv
__pycache__
.git
.env
document/
*.md
```

---

## Build & run (sirf API container)

```bash
docker build -t myapp-api:latest .

docker run --rm -p 8000:8000 \
  -e APP_ENV=development \
  myapp-api:latest
```

Test: `curl http://localhost:8000/health`

---

## Common errors

| Error | Fix |
|-------|-----|
| `curl not found` in HEALTHCHECK | Dockerfile mein `curl` install |
| Module not found | `COPY app/` path check; `uvicorn app.main:app` |
| Permission denied | `USER` se pehle `chown` |

---

## Is phase ka output

- [ ] `docker build` success
- [ ] `docker run` → `/health` OK
- [ ] Image size reasonable (`docker images`)

---

## Agli phase

[phase-03-docker-compose.md](./phase-03-docker-compose.md) — API + PostgreSQL + Redis ek saath.

---

## Meri progress

| Step | Status | Date |
|------|--------|------|
| Dockerfile | ✅ | 2026-05-27 |
| .dockerignore | ✅ | 2026-05-27 |
| build + run test | ✅ | 2026-05-27 |

**Notes / errors:**

```text

```
