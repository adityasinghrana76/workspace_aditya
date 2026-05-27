# Deployment Documentation (Reviewer)

English documentation for evaluators. For step-by-step learning notes (Hinglish), see the [`guide/`](../guide/) folder.

## Documents

| Document | Description |
|----------|-------------|
| [ARCHITECTURE.md](./ARCHITECTURE.md) | System diagram and component roles |
| [DEPLOYMENT.md](./DEPLOYMENT.md) | EC2 provisioning and manual deploy |
| [CI-CD.md](./CI-CD.md) | GitHub Actions pipeline and secrets |
| [ENVIRONMENT.md](./ENVIRONMENT.md) | Environment variables reference |
| [SECURITY.md](./SECURITY.md) | Server and network security measures |
| [SSL.md](./SSL.md) | HTTPS approach without a custom domain |
| [LOGGING-AND-BACKUP.md](./LOGGING-AND-BACKUP.md) | Logging, restart, and backup strategy |
| [WALKTHROUGH.md](./WALKTHROUGH.md) | End-to-end deployment instructions (submission) |

## Repository

- **GitHub:** https://github.com/adityasinghrana76/workspace_aditya
- **CI/CD workflow:** `.github/workflows/deploy.yml`
- **Live health (replace with your EC2 IP):** `http://<EC2_PUBLIC_IP>/health`

## Quick verification

```bash
curl http://<EC2_PUBLIC_IP>/health
curl -X POST http://<EC2_PUBLIC_IP>/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"hello"}'
```
