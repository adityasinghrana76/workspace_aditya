# Phase 4 — NGINX Reverse Proxy & Environment

## Is phase mein kya banega

- **NGINX** container — duniya ko sirf yeh dikhe (port 80)
- **FastAPI** internal — `api:8000` (public port map nahi)
- Final `docker-compose.yml` with 4 services

---

## Kyun NGINX?

| Without NGINX | With NGINX |
|---------------|------------|
| API directly :8000 | Single entry :80 |
| SSL har app mein alag | SSL NGINX pe (Phase 9) |
| No static files / rate limit | Easy to add later |

---

## `nginx/nginx.conf` (minimal)

```nginx
upstream api_backend {
    server api:8000;
}

server {
    listen 80;
    server_name _;   # koi bhi host / IP

    client_max_body_size 10M;

    location / {
        proxy_pass http://api_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /health {
        proxy_pass http://api_backend/health;
        access_log off;
    }
}
```

---

## Compose mein NGINX service

```yaml
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      # - "443:443"   # Phase 9 SSL
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/conf.d/default.conf:ro
    depends_on:
      - api
    networks: [appnet]
```

**Important:** `api` service se `ports: "8000:8000"` **hata do** — sirf NGINX expose.

---

## Test (local laptop)

```bash
docker compose up -d --build
curl http://localhost/health
curl http://localhost/
```

Browser: `http://localhost/`

---

## Environment variables — production rules

1. **`.env`** — server pe only, `chmod 600`
2. **`.env.example`** — repo mein, fake values
3. **GitHub Secrets** — CI/CD SSH key, optional API keys
4. **Compose** `env_file: .env` ya `${VAR}` substitution

### Compose + env flow

```text
.env file → docker compose → container env → pydantic Settings → app
```

---

## Logging (preview — detail Phase 8)

- NGINX access log: `/var/log/nginx/access.log` (container内)
- API: structured JSON logs `APP_ENV=production` pe
- View: `docker compose logs -f nginx api`

---

## Is phase ka output

- [ ] `http://localhost/health` works (port 80)
- [ ] Port 8000 externally closed
- [ ] `nginx/nginx.conf` in repo
- [ ] `.env.example` complete

---

## Agli phase

[phase-05-aws-ec2.md](./phase-05-aws-ec2.md) — yahi stack EC2 pe.

---

## Meri progress

| Step | Status | Date |
|------|--------|------|
| nginx.conf | ✅ | 2026-05-27 |
| nginx in compose | ✅ | 2026-05-27 |
| API port not public | ✅ | 2026-05-27 |
| local :80 test | ✅ | 2026-05-27 |

**Notes / errors:**

```text

```
