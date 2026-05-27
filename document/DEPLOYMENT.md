# Deployment Guide (AWS EC2)

## Prerequisites

- AWS account with EC2 access
- GitHub repository: `doonops/workspace_aditya`
- Local SSH key pair (`.pem`) for the EC2 instance

## 1. Launch EC2

| Setting | Recommended value |
|---------|-------------------|
| AMI | Ubuntu 24.04 LTS |
| Instance type | `t3.micro` or `t3.small` |
| Key pair | Create and download `.pem` |
| Storage | 20 GB+ |

### Security group (inbound)

| Port | Protocol | Source | Purpose |
|------|----------|--------|---------|
| 22 | TCP | Your IP | SSH administration |
| 80 | TCP | 0.0.0.0/0 | HTTP (NGINX) |
| 443 | TCP | 0.0.0.0/0 | HTTPS (optional, future) |

Do **not** expose ports `5432`, `6379`, or `8000` to the public internet.

Associate an **Elastic IP** so the public address remains stable for CI/CD and documentation.

## 2. Bootstrap the server

```bash
ssh -i /path/to/key.pem ubuntu@<EC2_PUBLIC_IP>

sudo apt update && sudo apt upgrade -y
sudo apt install -y ca-certificates curl git

# Docker Engine + Compose plugin
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

sudo usermod -aG docker ubuntu
newgrp docker
```

## 3. Clone application

```bash
sudo mkdir -p /opt/app
sudo chown ubuntu:ubuntu /opt/app
cd /opt/app
git clone https://github.com/adityasinghrana76/workspace_aditya.git workspace_aditya
cd workspace_aditya
```

> **Note:** If the repository is cloned into a subdirectory, set GitHub secret `APP_PATH` to that path (e.g. `/opt/app/workspace_aditya`).

## 4. Configure environment

```bash
cp .env.example .env
nano .env
chmod 600 .env
```

See [ENVIRONMENT.md](./ENVIRONMENT.md) for variable descriptions.

## 5. Start stack

```bash
docker compose up -d --build
docker compose ps
curl -f http://localhost/health
```

Public verification from your machine:

```text
http://13.126.41.46/health
http://13.126.41.46/docs
```

## 6. Troubleshooting

| Symptom | Likely cause | Action |
|---------|--------------|--------|
| Connection refused on :80 | Security group | Allow inbound TCP 80 |
| `permission denied` on `.env` | Wrong ownership | `sudo chown -R ubuntu:ubuntu /opt/app` |
| `no configuration file` | Wrong directory | `cd` to folder containing `docker-compose.yml` |
| `/health` returns 503 | DB/Redis down | `docker compose logs api db redis` |

## Related

- [CI-CD.md](./CI-CD.md) — automated deployment
- [SECURITY.md](./SECURITY.md) — hardening checklist
- [WALKTHROUGH.md](./WALKTHROUGH.md) — submission walkthrough
