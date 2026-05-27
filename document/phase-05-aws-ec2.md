# Phase 5 — AWS EC2 Setup & Manual Deploy

## Is phase mein kya hoga

Pehli baar poora stack **AWS EC2** pe — **haath se** SSH karke. CI/CD se pehle yeh zaroori hai.

---

## Step 5.1 — AWS account & EC2 launch

### Console steps

1. Login [AWS Console](https://console.aws.amazon.com/) → **EC2**
2. **Launch instance**
3. Settings:

| Setting | Value |
|---------|-------|
| Name | `assignment-api` |
| AMI | **Ubuntu Server 24.04 LTS** |
| Instance type | `t3.micro` (Free tier) ya `t3.small` |
| Key pair | Create new → download `.pem` |
| Storage | 20–30 GB gp3 |
| Security group | New — rules neeche |

### Security Group (inbound)

| Type | Port | Source | Note |
|------|------|--------|------|
| SSH | 22 | **My IP** | Sab ke liye 0.0.0.0/0 mat kholo |
| HTTP | 80 | 0.0.0.0/0 | Public API |
| HTTPS | 443 | 0.0.0.0/0 | Phase 9 optional |

**Mat kholo:** 5432 (Postgres), 6379 (Redis), 8000 (API direct)

### Elastic IP (recommended)

1. EC2 → **Elastic IPs** → Allocate
2. Associate → apni instance  
→ IP change nahi hogi restart pe — CI/CD ke liye best

---

## Step 5.2 — SSH connect

```bash
chmod 400 ~/Downloads/your-key.pem
ssh -i ~/Downloads/your-key.pem ubuntu@<EC2_PUBLIC_IP>
```

Windows: PuTTY ya WSL.

---

## Step 5.3 — Server bootstrap (ek baar)

```bash
# System update
sudo apt update && sudo apt upgrade -y

# Docker (official)
sudo apt install -y ca-certificates curl git
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Current user ko docker group (logout/login after)
sudo usermod -aG docker ubuntu

# Apply group change immediately (optional)
newgrp docker

# App directory
sudo mkdir -p /opt/app
sudo chown ubuntu:ubuntu /opt/app
```

Logout/login: `exit` → SSH dubara.

---

## Step 5.4 — Code server pe lao

### Option A — Git clone (recommended)

```bash
cd /opt/app
git clone https://github.com/doonops/workspace_aditya.git .
cp .env.example .env
nano .env   # strong passwords
```

### Option B — SCP from laptop

```bash
scp -i your-key.pem -r ./project ubuntu@<IP>:/opt/app/
```

---

## Step 5.5 — Deploy on server

```bash
cd /opt/app
docker compose up -d --build
docker compose ps
docker compose logs -f --tail=50
```

---

## Step 5.6 — Verify from browser

```text
http://<EC2_PUBLIC_IP>/health
http://<EC2_PUBLIC_IP>/
```

Agar nahi khulta:

1. Security Group — port 80 open?
2. `sudo ufw status` — agar enabled hai to `80` allow (Phase 6)
3. `docker compose ps` — sab healthy?

---

## Step 5.7 — CI/CD ke liye prep (important)

GitHub Actions workflow EC2 pe SSH karke `/opt/app` me commands chalata hai. Ensure:

- Repo path: `/opt/app` (same as `APP_PATH` secret)
- `.env` file exists at `/opt/app/.env`
- `docker compose up -d --build` manual run already done
- Security Group inbound: port **80 open** (public health check ke liye)

Quick reference: [ec2-github-config.md](./ec2-github-config.md)

---

## EC2 vs local — difference table

| | Local | EC2 |
|--|-------|-----|
| URL | localhost | Public IP |
| Firewall | Usually open | Security Group |
| Data | Laptop disk | EBS volume |
| Cost | Free | AWS billing |

---

## Server layout (end state)

```text
/opt/app/                 ← git repo root
├── docker-compose.yml
├── .env                  ← secrets, not in git
└── ...

/var/lib/docker/volumes/  ← Postgres data (automatic)
```

---

## Is phase ka output

- [ ] EC2 instance running
- [ ] Elastic IP associated (optional)
- [ ] Docker installed
- [ ] `http://<IP>/health` → 200 from phone/laptop
- [ ] Screenshot for final doc/video

---

## Agli phase

[phase-06-security.md](./phase-06-security.md) — SSH, ufw, fail2ban.

---

## Meri progress

| Step | Status | Date |
|------|--------|------|
| EC2 launched | ⬜ | |
| SSH works | ⬜ | |
| Docker installed | ⬜ | |
| compose up on server | ⬜ | |
| /health from internet | ⬜ | |

**EC2 Public IP:** `________________`

**Notes / errors:**

```text

```
