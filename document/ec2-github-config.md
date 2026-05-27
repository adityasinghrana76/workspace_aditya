# EC2 + GitHub Configuration (Quick Reference)

Yeh doc sirf 2 cheezon pe focused hai:

1. **EC2 setup** (server pe kya install/configure karna hai)
2. **GitHub Actions setup** (kahan secrets/configure karna hai)

Isko follow karke tum 30–60 minutes mein “auto deploy” tak pahunch jaoge.

---

## Part A — EC2 setup (AWS console)

### A1. EC2 launch

AWS Console → **EC2** → **Launch instance**

- **Name**: `workspace-aditya`
- **AMI**: Ubuntu 24.04 LTS
- **Instance**: `t3.micro` / `t3.small`
- **Key pair**: create/download `.pem`
- **Storage**: 20GB+

### A2. Security Group (IMPORTANT)

EC2 → Instance → **Security** → Security Group → Inbound rules:

| Rule | Port | Source | Why |
|------|------|--------|-----|
| SSH | 22 | *My IP* | Admin access |
| HTTP | 80 | 0.0.0.0/0 | Public API via NGINX |
| HTTPS | 443 | 0.0.0.0/0 | Optional (later) |

**Never open:** `5432`, `6379`, `8000` to public internet.

### A3. Elastic IP (recommended)

EC2 → **Elastic IPs** → Allocate → Associate to instance.  
Phir `EC2_HOST` secret mein isi IP ko use karo (stable rehti hai).

---

## Part B — EC2 setup (server pe SSH)

### B1. SSH connect (Mac)

```bash
chmod 400 ~/Downloads/your-key.pem
ssh -i ~/Downloads/your-key.pem ubuntu@<EC2_PUBLIC_IP>
```

### B2. Install Docker + Compose + Git

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y ca-certificates curl git

sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo \"$VERSION_CODENAME\") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

sudo usermod -aG docker ubuntu
newgrp docker
```

### B3. Repo clone path (APP_PATH)

CI/CD workflow by default **`/opt/app`** use karta hai.

```bash
sudo mkdir -p /opt/app
sudo chown ubuntu:ubuntu /opt/app
cd /opt/app
git clone https://github.com/doonops/workspace_aditya.git .
```

### B4. `.env` create + edit

```bash
cp .env.example .env
nano .env
```

Minimum fields (production):

- `POSTGRES_USER`
- `POSTGRES_PASSWORD` (strong)
- `POSTGRES_DB`
- `DATABASE_URL=postgresql://...@db:5432/...`
- `REDIS_URL=redis://redis:6379/0`
- `APP_ENV=production`
- `SECRET_KEY` (random)

### B5. First manual start (sanity)

```bash
docker compose up -d --build
docker compose ps
curl -f http://localhost/health
```

Public test (apne laptop se):

```text
http://<EC2_PUBLIC_IP>/health
```

---

## Part C — GitHub Actions configuration

### C1. Kahan configure karna hai

Repo: `doonops/workspace_aditya` → **Settings** → **Secrets and variables** → **Actions**

### C2. Required secrets

Add these repository secrets (exact names):

| Secret | Example | Notes |
|--------|---------|------|
| `EC2_HOST` | `54.12.34.56` | **No** `http://` |
| `EC2_USER` | `ubuntu` | Ubuntu AMI default |
| `EC2_SSH_KEY` | (PEM content) | Full private key incl. BEGIN/END |
| `APP_PATH` | `/opt/app` | Repo root on EC2 |

### C3. SSH key ka source

**Simple approach:** wahi `.pem` use karo jo EC2 instance create time download hui thi.  
Uska content copy karke `EC2_SSH_KEY` me paste karo.

### C4. Run workflow

- Push to `main`, ya
- GitHub → **Actions** tab → “Deploy to EC2” → **Run workflow**

Successful run ke baad:

- `http://<EC2_HOST>/health` → 200

---

## Common failures (fast fixes)

### “missing server host”

- `EC2_HOST` secret **missing/empty** OR wrong name.

### SSH timeout / permission denied

- Security Group port `22` open? (My IP)
- Wrong key pasted in `EC2_SSH_KEY`?
- Username `ubuntu` correct?

### Health check fails (503 / 000)

- `.env` missing on EC2?
- `docker compose ps` me api healthy?
- Security Group port `80` open to 0.0.0.0/0?

