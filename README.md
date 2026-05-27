# Assignment AI API — Local Docker Stack

FastAPI application with PostgreSQL, Redis, and NGINX — ready for local testing before EC2 / CI/CD.

## Quick start (Docker)

```bash
cp .env.example .env
docker compose up -d --build
curl http://localhost/health
curl -X POST http://localhost/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"hello"}'
```

- API docs (via NGINX): http://localhost/docs
- Health: http://localhost/health

## Quick start (bina Docker — pehle yeh)

Docker Desktop se pehle Mac pe test:

```bash
chmod +x scripts/*.sh
./scripts/setup-local-mac.sh    # ek baar: Homebrew Postgres + Redis
./scripts/run-local.sh          # Terminal 1 — API :8000
./scripts/test-local.sh         # Terminal 2 — curl tests
```

Detail: [document/local-dev-no-docker.md](./document/local-dev-no-docker.md)

- Docs: http://127.0.0.1:8000/docs
- Health: http://127.0.0.1:8000/health

## Project layout

```text
app/                 FastAPI application
nginx/nginx.conf     Reverse proxy
document/            Phase-by-phase deployment guides
docker-compose.yml   Full local stack
```

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Service info |
| GET | `/health` | Postgres + Redis status |
| POST | `/chat` | AI chat (rules; optional OpenAI via `OPENAI_API_KEY`) |

## Documentation

See [document/README.md](./document/README.md) for EC2, security, CI/CD, and SSL guides.
