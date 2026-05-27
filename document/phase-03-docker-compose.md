# Phase 3 — Docker Compose (Full Stack)

## Is phase mein kya banega

Ek `docker-compose.yml` jo **4 services** ek network pe chalayega:

```text
┌─────────┐     ┌─────────┐
│  NGINX  │────▶│   API   │
└─────────┘     └────┬────┘
                     │
              ┌──────┴──────┐
              ▼             ▼
         ┌────────┐   ┌────────┐
         │ Postgres│   │ Redis  │
         └────────┘   └────────┘
```

*(NGINX Phase 4 mein detail; abhi API+DB+Redis bhi enough hai test ke liye)*

---

## `docker-compose.yml` — conceptual

```yaml
services:
  api:
    build: .
    env_file: .env
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    networks: [appnet]
  # ports: "8000:8000"  ← production mein mat kholo, sirf NGINX expose

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER}"]
      interval: 10s
      retries: 5
    networks: [appnet]

  redis:
    image: redis:7-alpine
    networks: [appnet]

volumes:
  pgdata:

networks:
  appnet:
```

---

## Service names = hostname

Compose network mein:

- `DATABASE_URL=postgresql://user:pass@db:5432/appdb` → host **`db`** = service name
- `REDIS_URL=redis://redis:6379/0` → host **`redis`**

Yeh local `localhost` se different hai — containers ke beech DNS Compose deta hai.

---

## `.env.example` (git mein commit)

```env
POSTGRES_USER=appuser
POSTGRES_PASSWORD=change_me_strong
POSTGRES_DB=appdb
DATABASE_URL=postgresql://appuser:change_me_strong@db:5432/appdb
REDIS_URL=redis://redis:6379/0
APP_ENV=production
SECRET_KEY=generate_random_string
# OPENAI_API_KEY=sk-...   # optional
```

Server pe: `cp .env.example .env` → values edit.

---

## FastAPI ↔ DB connect

Phase 1 mein stub tha; ab:

1. Startup pe Postgres ping (SQLAlchemy / asyncpg)
2. Redis ping (`redis.ping()`)
3. `/health` mein real status

---

## Commands

```bash
# Start
docker compose up -d --build

# Status
docker compose ps

# Logs
docker compose logs -f api

# Stop
docker compose down

# Stop + delete DB volume (careful!)
docker compose down -v
```

---

## Health checks — 2 levels

| Level | Kahan | Kya |
|-------|-------|-----|
| Container | `HEALTHCHECK` in Dockerfile | Docker restart policy |
| Compose | `healthcheck` on `db` | `depends_on: condition` |

---

## Is phase ka output

- [ ] `docker compose up` — api, db, redis **healthy**
- [ ] `/health` shows database + redis connected
- [ ] Data persist — restart ke baad DB data rahe (volume)

---

## Agli phase

[phase-04-nginx-env.md](./phase-04-nginx-env.md) — bahar se sirf port 80, andar API.

---

## Meri progress

| Step | Status | Date |
|------|--------|------|
| compose.yml | ✅ | 2026-05-27 |
| .env.example | ✅ | 2026-05-27 |
| DB connect in /health | ✅ | 2026-05-27 |
| compose up healthy | ✅ | 2026-05-27 |

**Notes / errors:**

```text

```
