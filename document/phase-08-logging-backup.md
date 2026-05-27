# Phase 8 — Logging, Backup & Restart Strategy

## Is phase mein kya document hoga

Evaluator **reliability** dekhta hai — app crash / disk fail pe kya hoga?

---

## Part A — Logging strategy

### 1. Container logs (default)

```bash
# Sab services
docker compose logs -f

# Sirf API
docker compose logs -f api --tail=100

# NGINX access
docker compose logs -f nginx
```

### 2. Docker logging driver (compose)

```yaml
services:
  api:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

→ Log files rotate, disk full nahi hoti.

### 3. Application-level (FastAPI)

Production mein:

- `INFO` level requests
- `ERROR` stack traces
- Optional: JSON format for parsing

```python
import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
```

### 4. Centralized (bonus — doc only bhi chalega)

- **CloudWatch** agent on EC2 (AWS native)
- **Loki + Grafana** extra container
- Assignment ke liye: "future: ship logs to CloudWatch"

### Logging summary table (doc mein copy)

| Source | Command / Location | Retention |
|--------|-------------------|-----------|
| API | `docker compose logs api` | 3 files × 10MB |
| NGINX | `docker compose logs nginx` | same |
| Postgres | `docker compose logs db` | same |
| System | `/var/log/syslog` | OS default |

---

## Part B — Restart strategy

### Docker Compose restart policy

```yaml
services:
  api:
    restart: unless-stopped
  db:
    restart: unless-stopped
  redis:
    restart: unless-stopped
  nginx:
    restart: unless-stopped
```

| Policy | Meaning |
|--------|---------|
| `unless-stopped` | Reboot / crash pe auto start |
| `on-failure` | Sirf error pe |
| `no` | Manual only (dev) |

### EC2 reboot test

```bash
sudo reboot
# 2 min baad
curl http://<IP>/health
```

Doc: "After instance reboot, all containers come back via restart policy."

### systemd (optional extra)

Docker service already starts on boot:

```bash
sudo systemctl enable docker
```

---

## Part C — Backup strategy

### 1. PostgreSQL backup (main data)

**Manual:**

```bash
docker compose exec -T db pg_dump -U appuser appdb > backup_$(date +%Y%m%d).sql
```

**Restore:**

```bash
cat backup_20250527.sql | docker compose exec -T db psql -U appuser appdb
```

### 2. Automated cron on EC2

`/opt/app/scripts/backup.sh`:

```bash
#!/bin/bash
BACKUP_DIR=/opt/app/backups
mkdir -p "$BACKUP_DIR"
FILE="$BACKUP_DIR/db_$(date +%Y%m%d_%H%M).sql"
docker compose -f /opt/app/docker-compose.yml exec -T db pg_dump -U appuser appdb > "$FILE"
find "$BACKUP_DIR" -name "*.sql" -mtime +7 -delete
```

Crontab:

```bash
chmod +x /opt/app/scripts/backup.sh
crontab -e
# Daily 2 AM
0 2 * * * /opt/app/scripts/backup.sh >> /var/log/app-backup.log 2>&1
```

### 3. Volume backup (optional)

```bash
docker run --rm -v app_pgdata:/data -v $(pwd):/backup alpine \
  tar czf /backup/pgdata.tar.gz /data
```

### 4. AWS backup (bonus doc)

- **EBS snapshots** — weekly AMI/snapshot of disk
- **S3** — `aws s3 cp backup.sql s3://bucket/` from cron

### Backup summary table

| What | How often | Where | Retention |
|------|-----------|-------|-----------|
| Postgres SQL | Daily cron | `/opt/app/backups/` | 7 days |
| EBS snapshot | Weekly (manual) | AWS console | 4 weeks |
| `.env` | Manual encrypted copy | Password manager | N/A |

---

## Part D — Disaster recovery (short doc section)

1. **App down:** `docker compose ps` → `docker compose up -d --build`
2. **DB corrupt:** restore latest `.sql` backup
3. **Server dead:** new EC2 → install Docker → clone repo → restore backup → Elastic IP re-associate

---

## Is phase ka output

- [ ] `restart: unless-stopped` in compose
- [ ] `scripts/backup.sh` (optional but good)
- [ ] Backup/restore tested once locally or on EC2
- [ ] Tables above assignment doc / README mein

---

## Agli phase

[phase-09-ssl-no-domain.md](./phase-09-ssl-no-domain.md)

---

## Meri progress

| Item | Status | Date |
|------|--------|------|
| Logging doc + compose options | ⬜ | |
| Restart policy | ⬜ | |
| Backup script tested | ⬜ | |
| Reboot test | ⬜ | |

**Notes / errors:**

```text

```
