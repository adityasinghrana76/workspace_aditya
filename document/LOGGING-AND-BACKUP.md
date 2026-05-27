# Logging, Restart, and Backup Strategy

## Logging

### Container logs (Docker)

View logs:

```bash
docker compose logs -f
docker compose logs -f api
docker compose logs -f nginx
```

### Log rotation

`docker-compose.yml` configures the `json-file` driver with rotation for the API service:

- `max-size: 10m`
- `max-file: 3`

### Application logs

FastAPI/uvicorn logs requests at `INFO` level to stdout (collected by Docker).

### Future enhancement

- Ship logs to Amazon CloudWatch Logs or a self-hosted stack (Loki/Grafana)

## Restart strategy

All services use:

```yaml
restart: unless-stopped
```

Containers automatically restart after crashes or EC2 reboot (once the Docker daemon is running).

Verify after reboot:

```bash
sudo reboot
# after reconnect
curl http://localhost/health
```

## Backup strategy

### PostgreSQL (primary data)

**Manual backup:**

```bash
cd /opt/app/workspace_aditya   # or your APP_PATH
docker compose exec -T db pg_dump -U appuser appdb > backups/db_$(date +%Y%m%d_%H%M).sql
```

**Restore:**

```bash
cat backups/db_YYYYMMDD_HHMM.sql | docker compose exec -T db psql -U appuser appdb
```

### Automated backup script

Use `scripts/backup.sh` on EC2 with cron:

```bash
chmod +x scripts/backup.sh
crontab -e
# Daily at 02:00
0 2 * * * /opt/app/workspace_aditya/scripts/backup.sh >> /var/log/app-backup.log 2>&1
```

The script retains SQL dumps for 7 days by default.

### Disaster recovery (summary)

| Scenario | Action |
|----------|--------|
| Container crash | `docker compose up -d` |
| Bad deploy | `git checkout <prev>` + `docker compose up -d --build` |
| Database loss | Restore latest `pg_dump` |
| Lost EC2 | New instance, clone repo, restore backup, re-associate Elastic IP |

## Configuration backup

- Keep `.env` backed up securely (password manager or encrypted storage), not in Git
- Document Elastic IP and security group settings in your submission notes
