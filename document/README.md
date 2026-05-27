# Deployment Assignment — Documentation Index

Yeh folder assignment ka **step-by-step guide** hai. Har phase alag file mein hai — jaisa-jaisa kaam complete karo, us file ke end mein **“Status”** section update karo.

## Project kya banega (ek line mein)

**FastAPI** app → **Docker** containers → **Docker Compose** (API + PostgreSQL + Redis + NGINX) → **AWS EC2** pe deploy → **GitHub Actions** se auto deploy.

## Domain nahi hai?

Theek hai. Pehle **EC2 Public IP** se chalega (`http://<IP>/health`). SSL ke liye alag doc: [phase-09-ssl-no-domain.md](./phase-09-ssl-no-domain.md).

---

## Phases — order follow karo

| Phase | File | Kya banega | Approx time |
|-------|------|------------|-------------|
| 0 | [00-overview.md](./00-overview.md) | Architecture, folder structure, checklist | 15 min padhna |
| 1 | [phase-01-fastapi.md](./phase-01-fastapi.md) | Python API, `/health`, simple AI endpoint | 2–4 hrs |
| 2 | [phase-02-docker.md](./phase-02-docker.md) | `Dockerfile`, local image build | 1–2 hrs |
| 3 | [phase-03-docker-compose.md](./phase-03-docker-compose.md) | Postgres, Redis, networks, volumes | 2–3 hrs |
| 4 | [phase-04-nginx-env.md](./phase-04-nginx-env.md) | NGINX reverse proxy, `.env` | 2–3 hrs |
| 5 | [phase-05-aws-ec2.md](./phase-05-aws-ec2.md) | EC2 launch, SSH, Docker on server | 2–4 hrs |
| 6 | [phase-06-security.md](./phase-06-security.md) | Firewall, SSH hardening, secrets | 1–2 hrs |
| 7 | [phase-07-cicd.md](./phase-07-cicd.md) | GitHub Actions → EC2 deploy | 2–4 hrs |
| 8 | [phase-08-logging-backup.md](./phase-08-logging-backup.md) | Logs, backup, restart strategy | 1–2 hrs |
| 9 | [phase-09-ssl-no-domain.md](./phase-09-ssl-no-domain.md) | HTTP / self-signed / future HTTPS | 1 hr |
| 10 | [phase-10-final-deliverables.md](./phase-10-final-deliverables.md) | Repo checklist, video, evaluation | 2–3 hrs |

**Total (rough):** 5–7 din part-time.

---

## Repo folder structure (end state)

Jab sab complete ho, repo aisa dikhega:

```text
workspace_aditya/
├── app/                    # FastAPI code
│   ├── main.py
│   └── ...
├── nginx/
│   └── nginx.conf
├── document/               # Yeh guides (assignment explanation)
├── scripts/                # backup.sh, deploy helpers (optional)
├── .github/workflows/
│   └── deploy.yml
├── docker-compose.yml
├── Dockerfile
├── .env.example
├── requirements.txt
├── README.md               # Quick start evaluators ke liye
└── .gitignore
```

---

## Har phase ke baad kya karna hai

1. Us phase ki file ke **bottom** mein `## Meri progress` update karo (date, done/pending).
2. Agar koi command fail hui — `## Notes / errors` mein likho (evaluator ko debugging dikhati hai).
3. Phase complete → agli file kholo.

---

## Quick links

- Architecture diagram: [00-overview.md#architecture-diagram](./00-overview.md#architecture-diagram)
- AWS EC2 setup: [phase-05-aws-ec2.md](./phase-05-aws-ec2.md)
- CI/CD: [phase-07-cicd.md](./phase-07-cicd.md)
- EC2 + GitHub configuration (fast): [ec2-github-config.md](./ec2-github-config.md)
- Assignment deliverables: [phase-10-final-deliverables.md](./phase-10-final-deliverables.md)
