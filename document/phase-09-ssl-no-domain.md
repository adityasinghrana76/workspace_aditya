# Phase 9 — SSL Setup (Domain Nahi Hai)

## Situation

- Tumhare paas abhi **domain nahi**
- Assignment phir bhi **SSL approach document** maangta hai

Yeh file evaluator ko dikhati hai: tum HTTPS samajhte ho, bas abhi IP pe ho.

---

## 3 approaches — comparison

| Approach | URL example | Browser | Assignment |
|----------|-------------|---------|------------|
| **A. HTTP only** | `http://54.x.x.x/health` | ✅ No warning | ✅ Minimum OK |
| **B. Self-signed cert** | `https://54.x.x.x/` | ⚠️ "Not secure" warning | ✅ Shows SSL knowledge |
| **C. Free subdomain + Let's Encrypt** | `https://myapp.duckdns.org` | ✅ Green lock | ⭐ Bonus |

---

## Approach A — HTTP only (start here)

NGINX sirf port 80 — Phase 4 jaisa.

**Doc mein likho:**

> Production mein domain ke saath HTTPS mandatory hai. Development/demo ke liye EC2 public IP pe HTTP use kiya. TLS termination NGINX pe hogi jab domain attach ho.

**Evaluator test:** `http://<EC2_IP>/health`

---

## Approach B — Self-signed certificate (no domain)

### Generate on EC2

```bash
sudo mkdir -p /opt/app/nginx/ssl
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /opt/app/nginx/ssl/selfsigned.key \
  -out /opt/app/nginx/ssl/selfsigned.crt \
  -subj "/CN=ec2-assignment/O=Dev/C=IN"
```

### NGINX snippet

```nginx
server {
    listen 443 ssl;
    server_name _;
    ssl_certificate     /etc/nginx/ssl/selfsigned.crt;
    ssl_certificate_key /etc/nginx/ssl/selfsigned.key;

    location / {
        proxy_pass http://api:8000;
        # ... proxy headers ...
    }
}

server {
    listen 80;
    return 301 https://$host$request_uri;
}
```

Compose volume:

```yaml
volumes:
  - ./nginx/ssl:/etc/nginx/ssl:ro
```

Security Group: port **443** open.

**Doc warning:** Self-signed = encryption hai, trust nahi — sirf demo.

---

## Approach C — Free subdomain + Let's Encrypt (bonus)

### Step 1 — Free DNS

- [DuckDNS](https://www.duckdns.org/) → `myapp.duckdns.org` → EC2 IP
- Ya [nip.io](http://nip.io) → `54-123-45-67.nip.io`

### Step 2 — Certbot on EC2

```bash
sudo apt install -y certbot
# Stop nginx container temporarily OR use webroot plugin
sudo certbot certonly --standalone -d myapp.duckdns.org
```

Certificates: `/etc/letsencrypt/live/myapp.duckdns.org/`

### Step 3 — Mount in NGINX container

```yaml
volumes:
  - /etc/letsencrypt:/etc/letsencrypt:ro
```

**Auto-renew cron:**

```bash
0 3 * * * certbot renew --quiet && docker compose -f /opt/app/docker-compose.yml restart nginx
```

---

## Production SSL (jab domain mile) — doc paragraph

```text
1. Domain registrar → A record → Elastic IP
2. (Optional) Cloudflare proxy — DDoS + CDN
3. Certbot with NGINX plugin OR AWS ACM + ALB (advanced)
4. Force HTTPS, HSTS header
5. Renew every 90 days (automated)
```

---

## Cloudflare (bonus — domain chahiye)

1. Domain Cloudflare nameservers pe
2. A record → EC2 IP (orange cloud = proxy)
3. SSL mode: Full (strict) agar origin pe valid cert ho

Bina domain: Cloudflare skip — doc mein "future step" likh do.

---

## Assignment mein kya submit karo (SSL section)

README ya `document/` mein ek section:

### SSL & HTTPS

- **Current:** HTTP on `http://<EC2_IP>/` — no domain
- **Demo HTTPS (optional):** self-signed on 443 — browser warning expected
- **Production plan:** domain → Let's Encrypt → NGINX 443 → redirect 80→443

---

## Meri progress

| Approach | Status | Date |
|----------|--------|------|
| A HTTP working | ⬜ | |
| B self-signed (optional) | ⬜ | |
| C DuckDNS + LE (bonus) | ⬜ | |

**Notes / errors:**

```text

```
