<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:2496ED,100:326CE5&height=160&section=header&text=Microservices%20E-Commerce%20Platform&fontSize=32&fontColor=ffffff&fontAlignY=45&desc=Flask%20%7C%20MySQL%20%7C%20Docker%20%7C%20Kubernetes%20%7C%20DevSecOps%20%7C%20Google%20OAuth&descSize=13&descAlignY=68&descColor=d0e8ff" width="100%"/>

# 🛒 Microservices E-Commerce Platform
### DevSecOps · Kubernetes · Google OAuth · 7-Stage CI/CD Pipeline

[![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)](.)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=flat-square&logo=kubernetes&logoColor=white)](.)
[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat-square&logo=githubactions&logoColor=white)](.)
[![Trivy](https://img.shields.io/badge/Trivy-1904DA?style=flat-square&logo=aquasecurity&logoColor=white)](.)
[![Gitleaks](https://img.shields.io/badge/Gitleaks-181717?style=flat-square&logo=github&logoColor=white)](.)
[![Hadolint](https://img.shields.io/badge/Hadolint-2496ED?style=flat-square&logo=docker&logoColor=white)](.)

</div>

---

## What this is

Three Flask microservices — Auth, Product, Order — each with its own MySQL database, running behind an Nginx API gateway. Built to practice real DevOps workflows, not follow a tutorial.

Every push to `main` goes through a 7-stage DevSecOps pipeline. Nothing reaches the server unless all stages pass. Auth supports both password login and Google OAuth.

Not a toy project. The goal was something that would hold up in a job interview.

---

## Services

| Service | Port | What it does |
|---|---|---|
| Auth Service | 5001 | Register, login, Google OAuth, JWT tokens |
| Product Service | 5002 | Product catalog, inventory CRUD |
| Order Service | 5003 | Place and track orders |
| Nginx Gateway | 80 | Single entry point for all traffic |

---

## Tech stack

| Layer | Tools |
|---|---|
| Services | Python, Flask, SQLAlchemy |
| Auth | JWT + Google OAuth 2.0 (Authlib) |
| Database | MySQL 8.0 |
| Containers | Docker, Docker Compose |
| Registry | Docker Hub |
| CI/CD | GitHub Actions (7 workflows) |
| Security | Trivy, Gitleaks, Hadolint, Bandit, pip-audit |
| Orchestration | Kubernetes (kind — local), EKS (planned) |
| GitOps | Argo CD (planned) |
| Monitoring | Prometheus + Grafana (planned) |

---

## Auth — two ways to log in

Standard email/password registration and login. Plus Google OAuth — hit `/api/auth/google/login` in a browser, sign in with Google, get a JWT back. Same token format either way, so the rest of the system doesn't care how you authenticated.

```
GET  /api/auth/google/login      → redirects to Google
GET  /api/auth/google/callback   → Google returns here → JWT issued
```

Google users get created automatically on first login. Password field stays null for them — trying to log in via password with a Google account returns 401.

---

## API routes

### Auth — `/api/auth`

| Method | Route | Auth | Description |
|---|---|---|---|
| GET | `/health` | No | Health check |
| POST | `/register` | No | Create account |
| POST | `/login` | No | Get JWT token |
| POST | `/verify` | Bearer | Validate token |
| GET | `/google/login` | No | Start Google OAuth |
| GET | `/google/callback` | No | Google OAuth callback |

### Product — `/api/products`

| Method | Route | Auth | Description |
|---|---|---|---|
| GET | `/health` | No | Health check |
| GET | `/` | No | List all products |
| GET | `/<id>` | No | Get single product |
| POST | `/` | JWT | Add product |
| PUT | `/<id>` | JWT | Update product |
| DELETE | `/<id>` | JWT | Delete product |

### Order — `/api/orders`

| Method | Route | Auth | Description |
|---|---|---|---|
| GET | `/health` | No | Health check |
| POST | `/` | JWT | Place order |
| GET | `/` | JWT | Get my orders |
| GET | `/<id>` | JWT | Get single order |
| PUT | `/<id>/status` | JWT | Update order status |

---

## DevSecOps pipeline

```
Push to main
     │
     ├── code-quality-scan   (Flake8 + Bandit)
     ├── dependency-scan     (pip-audit)
     ├── secrets-scan        (Gitleaks)
     ├── dockerfile-scan     (Hadolint)
     │
     ▼  all pass
     │
     ├── docker-build-push   (build + push to Docker Hub)
     │
     ▼
     ├── image-scan          (Trivy — HIGH/CRITICAL CVEs block deploy)
     │
     ▼
     └── deploy-to-server    (SSH → docker compose up)
```

**Stats:** 7 workflows · 69+ commits · ~3m 14s average end-to-end · zero secrets leaked

---

## Dockerfiles

Multi-stage builds, non-root users across all three services.

```dockerfile
# Stage 1 — builder
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2 — runtime, non-root
FROM python:3.12-slim
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser
WORKDIR /app
COPY --from=builder /install /usr/local
COPY app/ ./app/
COPY run.py .
RUN chown -R appuser:appgroup /app
USER appuser
```

---

## Running locally

**Prerequisites:** Docker and Docker Compose installed.

```bash
git clone https://github.com/Heyyprakhar1/microservices-ecommerce-devsecops.git
cd microservices-ecommerce-devsecops
docker compose up --build -d
```

All three services and MySQL start automatically. `init.sql` creates the three databases on first run.

**Quick test:**

```bash
# Register
curl -X POST http://localhost:5001/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"prakhar","email":"p@test.com","password":"test123"}'

# Login
TOKEN=$(curl -s -X POST http://localhost:5001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"p@test.com","password":"test123"}' | python3 -c "import sys,json; print(json.load(sys.stdin)['token'])")

# Google OAuth (open in browser)
# http://localhost:5001/api/auth/google/login

# Create a product
curl -X POST http://localhost:5002/api/products/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"name":"Nike Shoes","price":99.99,"stock":50,"category":"footwear"}'
```

---

## Project structure

```
microservices-ecommerce-devsecops/
├── services/
│   ├── auth-service/
│   │   ├── app/
│   │   │   ├── __init__.py
│   │   │   ├── config.py
│   │   │   ├── models.py
│   │   │   └── routes.py
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── run.py
│   ├── product-service/
│   └── order-service/
├── k8s/
│   ├── auth-service/
│   ├── product-service/
│   ├── order-service/
│   ├── mysql/
│   └── ingress.yaml
├── .github/
│   └── workflows/
│       ├── DevSecOps-pipeline.yml
│       ├── code_quality.yml
│       ├── dependency_scan.yml
│       ├── secrets-scan.yml
│       ├── dockerfile-scan.yml
│       ├── docker-build-push.yml
│       ├── image-scan.yml
│       └── deploy_to_server.yml
├── terraform/
├── docker-compose.yml
└── init.sql
```

---

## Status

- ✅ Auth Service (Flask + MySQL + JWT + Google OAuth)
- ✅ Product Service
- ✅ Order Service
- ✅ Multi-stage Dockerfiles (non-root users)
- ✅ Docker Compose
- ✅ DevSecOps Pipeline (7 stages, 69+ runs)
- ✅ Kubernetes manifests (HPA, Ingress, Namespaces)
- ✅ Terraform (AWS EC2 provisioning)
- ⏳ EKS deployment
- ⏳ Helm Charts
- ⏳ Argo CD (GitOps)
- ⏳ Prometheus + Grafana monitoring
- ⏳ AI Chatbot service (Ollama)

---

<div align="center">

**Built by [Prakhar Srivastava](https://github.com/Heyyprakhar1)**
· [Portfolio](https://prakharsrivastavadevops.netlify.app/)
· [LinkedIn](https://linkedin.com/in/heyyprakhar1)

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:326CE5,100:2496ED&height=100&section=footer&text=Not%20a%20tutorial%20project&fontSize=20&fontColor=ffffff&fontAlignY=65&desc=Built%20to%20break%2C%20debug%2C%20and%20understand%20why.&descSize=12&descColor=d0e8ff&descAlignY=85" width="100%"/>

</div>
