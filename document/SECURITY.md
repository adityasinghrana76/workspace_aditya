# Security Measures

## Network (AWS Security Group)

| Port | Exposure | Purpose |
|------|----------|---------|
| 22 | Restricted (prefer “My IP”) | SSH administration |
| 80 | Public | HTTP via NGINX |
| 443 | Public (optional) | Future HTTPS |
| 5432, 6379, 8000 | **Not public** | Database, cache, API must stay internal |

## Host firewall (UFW on Ubuntu)

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow OpenSSH
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
sudo ufw status verbose
```

## SSH hardening

- Authenticate with EC2 key pair only
- Disable password authentication:

```bash
sudo sed -i 's/^#*PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config
sudo systemctl restart sshd
```

## Application and containers

- API container runs as non-root user (`appuser` in Dockerfile)
- PostgreSQL and Redis have no published host ports in `docker-compose.yml`
- Only NGINX publishes port `80` to the host
- Secrets in `.env`, excluded via `.gitignore`

## CI/CD secrets

- SSH private key and EC2 host stored in GitHub Actions secrets
- Never log secret values in workflow output

## Optional enhancements (bonus)

- `fail2ban` for SSH brute-force protection
- AWS WAF or Cloudflare when a domain is available
- Regular `apt upgrade` on the EC2 instance
