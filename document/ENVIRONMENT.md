# Environment Variables

Configuration is loaded from `.env` (not committed to Git). Use `.env.example` as a template.

## Variables

| Variable | Required | Description | Example (Docker Compose) |
|----------|----------|-------------|-------------------------|
| `POSTGRES_USER` | Yes | PostgreSQL username | `appuser` |
| `POSTGRES_PASSWORD` | Yes | PostgreSQL password | Strong random string |
| `POSTGRES_DB` | Yes | Database name | `appdb` |
| `DATABASE_URL` | Yes | SQLAlchemy connection URL | `postgresql://appuser:PASS@db:5432/appdb` |
| `REDIS_URL` | Yes | Redis connection URL | `redis://redis:6379/0` |
| `APP_ENV` | Yes | Environment name | `production` on EC2, `development` locally |
| `SECRET_KEY` | Yes | Application secret (random string) | Generate with `secrets.token_urlsafe(32)` |
| `OPENAI_API_KEY` | No | Enables OpenAI responses on `POST /chat` | `sk-...` |

## Docker Compose hostnames

Inside the Compose network, services resolve by **service name**:

- PostgreSQL host: `db` (not `localhost`)
- Redis host: `redis`

## Example `.env` (production on EC2)

```env
POSTGRES_USER=appuser
POSTGRES_PASSWORD=<strong-password>
POSTGRES_DB=appdb

DATABASE_URL=postgresql://appuser:<strong-password>@db:5432/appdb
REDIS_URL=redis://redis:6379/0

APP_ENV=production
SECRET_KEY=<random-32+-char-string>
```

## Generating `SECRET_KEY`

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

## Security

- Never commit `.env` to Git
- On EC2: `chmod 600 .env`
- Store production secrets only on the server and in GitHub Actions secrets (for SSH/deploy, not app DB passwords unless required)
