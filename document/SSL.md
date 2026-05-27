# SSL / HTTPS Setup

## Current state (no custom domain)

The deployment is served over **HTTP** on the EC2 public IP:

```text
http://13.126.41.46/health
```

This is acceptable for the assignment demo when no domain is available. TLS termination is designed to sit on **NGINX** when a domain is added.

## Approach without a domain

### Option A — HTTP only (current)

- NGINX listens on port 80
- Document that production would enforce HTTPS after domain setup

### Option B — Self-signed certificate (demo only)

Generate on EC2 and mount into the NGINX container. Browsers will show a security warning; encryption exists but trust is not established.

### Option C — Free DNS + Let's Encrypt (recommended when possible)

1. Use a free subdomain (e.g. DuckDNS) pointing to the Elastic IP
2. Install Certbot on EC2
3. Obtain certificates for the subdomain
4. Configure NGINX for port 443 and redirect HTTP → HTTPS
5. Automate renewal with cron

## Production plan (with domain)

1. Register or use an existing domain
2. Create an **A record** → Elastic IP
3. (Optional) Cloudflare proxy for CDN and DDoS protection
4. Let's Encrypt via Certbot with NGINX
5. Enable HSTS and force HTTPS on port 80

## Related configuration

- NGINX config: `nginx/nginx.conf` (currently HTTP on port 80)
- Security group: allow port 443 when HTTPS is enabled

See also: [DEPLOYMENT.md](./DEPLOYMENT.md), [SECURITY.md](./SECURITY.md)
