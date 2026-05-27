# Deployment Walkthrough (Written Instructions)

Step-by-step guide for evaluators. Replace `<EC2_IP>` with your instance public IP.

## 1. Architecture

See [ARCHITECTURE.md](./ARCHITECTURE.md). Traffic enters on port 80 (NGINX) and is proxied to FastAPI; PostgreSQL and Redis are internal only.

## 2. Local verification (optional)

```bash
git clone https://github.com/adityasinghrana76/workspace_aditya.git
cd workspace_aditya
cp .env.example .env
docker compose up -d --build
curl http://localhost/health
```

Expected: `"status":"ok"`, `"database":"connected"`, `"redis":"connected"`.

## 3. EC2 setup

1. Launch Ubuntu EC2 with key pair and security group (ports 22, 80).
2. SSH: `ssh -i key.pem ubuntu@<EC2_IP>`
3. Install Docker (see [DEPLOYMENT.md](./DEPLOYMENT.md)).
4. Clone repo to `/opt/app/workspace_aditya` (or chosen path).
5. Create `.env` from `.env.example`.
6. Run: `docker compose up -d --build`
7. Verify: `curl http://localhost/health`

**Screenshot:** EC2 security group inbound rules.

## 4. Public access

Open in browser:

```text
http://<EC2_IP>/health
http://<EC2_IP>/docs
```

Test chat:

```bash
curl -X POST http://<EC2_IP>/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"hello"}'
```

**Screenshot:** Browser showing health JSON.

## 5. CI/CD configuration

1. GitHub → repo → Settings → Secrets → Actions
2. Add: `EC2_HOST`, `EC2_USER`, `EC2_SSH_KEY`, `APP_PATH`
3. Push to `main` or run workflow manually

**Screenshot:** GitHub Actions run with green checkmark.

## 6. Security and SSL

- Security: [SECURITY.md](./SECURITY.md) (UFW, SSH, closed DB ports)
- SSL without domain: [SSL.md](./SSL.md)

## 7. Logging and backup

- Logs: `docker compose logs -f api`
- Backup: `scripts/backup.sh` and [LOGGING-AND-BACKUP.md](./LOGGING-AND-BACKUP.md)

## Submission checklist

- [ ] GitHub repository link
- [ ] Live `http://<EC2_IP>/health` works
- [ ] CI/CD workflow passes
- [ ] This walkthrough or equivalent video
- [ ] Architecture diagram in README or ARCHITECTURE.md

## Repository links

- **Code:** https://github.com/adityasinghrana76/workspace_aditya
- **Workflow:** `.github/workflows/deploy.yml`
- **Docs index:** [README.md](./README.md)
