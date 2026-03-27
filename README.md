# E-commerce Platform

A microservices-based ecommerce backend built to practice real DevOps workflows — Dockerized services, a DevSecOps CI/CD pipeline, and Kubernetes deployment.

Not a tutorial project. The goal was to build something that would hold up in a job interview.

---

## What's inside

Three independent Flask services, each with its own MySQL database:

- **Auth Service** (port 5001) — register, login, JWT token generation and verification
- **Product Service** (port 5002) — product catalogue, inventory CRUD
- **Order Service** (port 5003) — place and track orders

Traffic routes through an **Nginx API Gateway** as a single entry point.

---

## Tech Stack

| Layer | Tools |
|---|---|
| Services | Python, Flask, SQLAlchemy |
| Database | MySQL 8.0 |
| Containers | Docker, Docker Compose |
| Registry | Docker Hub |
| CI/CD | GitHub Actions |
| Code Quality | Flake8, Bandit |
| Security Scanning | Trivy, GitLeaks, pip-audit, Hadolint |
| Deployment | SSH + SCP to remote server |
| Orchestration | Kubernetes (coming) |
| Monitoring | Prometheus, Grafana (coming) |

---

## Running locally

**Prerequisites:** Docker and Docker Compose installed.

```bash
git clone https://github.com/Heyyprakhar1/microservices-ecommerce-devsecops.git
cd microservices-ecommerce-devsecops
docker compose up --build -d
```

All three services and MySQL start automatically. The `init.sql` script creates the three databases on the first run.

**Quick test:**

```bash
# Register
curl -X POST http://localhost:5001/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "prakhar", "email": "p@test.com", "password": "test123"}'

# Store token
TOKEN=$(curl -s -X POST http://localhost:5001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"p@test.com","password":"test123"}' | python3 -c "import sys,json; print(json.load(sys.stdin)['token'])")

# Create a product
curl -X POST http://localhost:5002/api/products/ \
  -H "Content-Type: application/json" \
  -H "Authorisation: Bearer $TOKEN" \
  -d '{"name": "Nike Shoes", "price":99.99, "stock":50, "category": "footwear"}'
```

---

## API Routes

### Auth Service — `/api/auth`

| Method | Route | Auth | Description |
|---|---|---|---|
| GET | `/health` | No | Health check |
| POST | `/register` | No | Create account |
| POST | `/login` | No | Get JWT token |
| POST | `/verify` | Bearer token | Validate token |

### Product Service — `/api/products`

| Method | Route | Auth | Description |
|---|---|---|---|
| GET | `/health` | No | Health check |
| GET | `/` | No | List all products |
| GET | `/<id>` | No | Get single product |
| POST | `/` | JWT | Add product |
| PUT | `/<id>` | JWT | Update product |
| DELETE | `/<id>` | JWT | Delete product |

### Order Service — `/api/orders`

| Method | Route | Auth | Description |
|---|---|---|---|
| GET | `/health` | No | Health check |
| POST | `/` | JWT | Place order |
| GET | `/` | JWT | Get my orders |
| GET | `/<id>` | JWT | Get single order |
| PUT | `/<id>/status` | JWT | Update order status |

---

## Project Structure

```
ecommerce-platform/
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
├── monitoring/
├── docker-compose.yml
├── init.sql
└── README.md
```

---

## DevSecOps Pipeline

Every push to `main` triggers a 7-stage pipeline. Nothing reaches the server unless all stages pass.

```
Push to main
     │
     ├── code-quality-scan   (Flake8 + Bandit)
     ├── dependency-scan     (pip-audit)
     ├── secrets-scan        (GitLeaks)
     ├── dockerfile-scan     (Hadolint)
     │
     ▼  all pass
     │
     ├── docker-build-push   (build + push to Docker Hub)
     │
     ▼
     ├── image-scan          (Trivy — HIGH/CRITICAL CVEs)
     │
     ▼
     └── deploy-to-server    (SSH → docker compose up)
```

**Pipeline stats:**
- 7 workflows, 63 total job runs
- 3m 14s average end-to-end
- No secrets leaked (GitLeaks ✅)

### Security Tools

| Tool | What it checks |
|---|---|
| Flake8 | Python code style and syntax |
| Bandit | Python security issues (hardcoded creds, debug mode) |
| pip-audit | Known CVEs in Python dependencies |
| GitLeaks | Secrets accidentally committed to git |
| Hadolint | Dockerfile best practices |
| Trivy | Docker image vulnerabilities (HIGH + CRITICAL only) |

---

## Dockerfiles

Multi-stage builds with non-root users across all three services.

```dockerfile
# Stage 1: Builder
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2: Final — non-root user
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

## Kubernetes

Coming next — services will deploy to Minikube with:

- Separate namespaces for dev and prod
- HPA on each service (scales on CPU)
- Liveness and readiness probes
- Nginx Ingress routing all traffic through one endpoint

---

## Status

- [x] Auth Service (Flask + MySQL + JWT)
- [x] Product Service
- [x] Order Service
- [x] Multi-stage Dockerfiles
- [x] Docker Compose
- [x] DevSecOps Pipeline (7 stages)
- [x] Automated server deployment
- [ ] Kubernetes manifests (HPA, Ingress, Namespaces)
- [ ] Prometheus + Grafana monitoring
- [ ] Helm Charts
