# Phase 6 — Server Security (EC2)

## Is phase mein kya document + implement hoga

Assignment **security awareness** check karta hai — sirf app nahi, server bhi.

---

## Layer 1 — AWS Security Group (primary firewall)

Already Phase 5 mein:

- ✅ 22 from **My IP only**
- ✅ 80, 443 public
- ❌ DB ports closed

**Review:** EC2 → Instance → Security → Inbound rules screenshot doc mein.

---

## Layer 2 — UFW on Ubuntu (host firewall)

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow OpenSSH
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
sudo ufw status verbose
```

**Warning:** SSH (22) allow kiye bina `enable` mat karo — lock out ho sakte ho.

---

## Layer 3 — SSH hardening

`/etc/ssh/sshd_config` (sudo nano):

```text
PasswordAuthentication no
PermitRootLogin no
PubkeyAuthentication yes
```

```bash
sudo systemctl restart sshd
```

Sirf **key pair (.pem)** se login — password SSH band.

---

## Layer 4 — Docker / app security

| Practice | Kya karo |
|----------|----------|
| Non-root container | Dockerfile `USER appuser` |
| No secrets in image | `.env` + env vars |
| DB not exposed | Compose mein db ke `ports` na ho |
| Updates | `sudo apt upgrade` monthly |
| `.env` permissions | `chmod 600 .env` |

---

## Layer 5 — fail2ban (bonus)

```bash
sudo apt install -y fail2ban
sudo systemctl enable fail2ban
```

Default jail SSH brute-force ke liye — doc mein likho: "installed for SSH protection".

---

## Layer 6 — GitHub / CI secrets

| Secret | Store |
|--------|-------|
| SSH private key | GitHub → Settings → Secrets |
| DB password | Server `.env` only |
| OpenAI key | Secrets + server `.env` |

**Kabhi commit mat:** `.pem`, `.env`, API keys.

---

## Security checklist (evaluator)

- [ ] Security Group screenshot / description in doc
- [ ] ufw enabled, only 22/80/443
- [ ] SSH password auth off
- [ ] Postgres/Redis not public
- [ ] `.env` in `.gitignore`
- [ ] Non-root Docker user (Phase 2)

---

## Agli phase

[phase-07-cicd.md](./phase-07-cicd.md) — GitHub Actions automated deploy.

---

## Meri progress

| Item | Status | Date |
|------|--------|------|
| Security group verified | ⬜ | |
| ufw configured | ⬜ | |
| SSH hardened | ⬜ | |
| fail2ban (bonus) | ⬜ | |

**Notes / errors:**

```text

```
