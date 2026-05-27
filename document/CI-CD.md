# CI/CD (GitHub Actions)

## Workflow

- **File:** `.github/workflows/deploy.yml`
- **Trigger:** Push to `main`, or manual `workflow_dispatch`

## Pipeline steps

1. Validate required GitHub secrets exist
2. SSH into EC2 as `ubuntu`
3. `cd $APP_PATH` → `git pull --ff-only origin main`
4. `docker compose up -d --build`
5. Poll `http://localhost/health` on the server
6. Verify `http://$EC2_HOST/health` from the GitHub runner

## Required secrets

Configure under: **Repository → Settings → Secrets and variables → Actions**

| Secret | Description | Example |
|--------|-------------|---------|
| `EC2_HOST` | Public IP or Elastic IP (no `http://`) | `54.12.34.56` |
| `EC2_USER` | SSH username | `ubuntu` |
| `EC2_SSH_KEY` | Full private key from EC2 key pair (including BEGIN/END lines) | PEM contents |
| `APP_PATH` | Absolute path to repo root on EC2 | `/opt/app/workspace_aditya` |

## First-time server requirement

CI/CD assumes the repository is already cloned on EC2 and `.env` exists. Initial setup is manual (see [DEPLOYMENT.md](./DEPLOYMENT.md)).

## Security group for CI

- Port **22** must be reachable from GitHub Actions runners (restrict to your IP for manual SSH; for Actions you may need a broader rule temporarily or use a self-hosted runner).
- Port **80** must be open for the public health check step.

## Rollback

```bash
cd $APP_PATH
git log --oneline -5
git checkout <previous-commit-sha>
docker compose up -d --build
```

## Common failures

| Error | Fix |
|-------|-----|
| `Missing secret: APP_PATH` | Add `APP_PATH` secret |
| `missing server host` | Add or fix `EC2_HOST` |
| SSH timeout | Open port 22; verify key and username |
| Health check failed | Check `.env`, `docker compose ps`, security group port 80 |
