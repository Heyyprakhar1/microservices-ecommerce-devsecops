# Ecommerce Platform

A microservices-based ecommerce backend built to practice real DevOps workflows — Dockerized services, a DevSecOps CI/CD pipeline, and Kubernetes deployment.

Not a tutorial project. The goal was to build something that would hold up in a job interview.

---

## What's inside

Three independent Flask services, each with its own MySQL database:

- **Auth Service** (port 5001) — register, login, JWT token generation and verification
- **Product Service** (port 5002) — product catalog, inventory CRUD
- **Order Service** (port 5003) — place and track orders

Traffic routes through an **Nginx API Gateway** as a single entry point.

---

## Tech Stack

| Layer | Tools |
|---|---|
| Services | Python, Flask, SQLAlchemy |
| Database | MySQL 8.0 |
| Containers | Docker, Docker Compose |
| CI/CD | GitHub Actions |
| Security | Trivy, Semgrep, GitLeaks, SonarQube |
| Orchestration | Kubernetes (Minikube) |
| Monitoring | Prometheus, Grafana |

---

## Running locally

**Prerequisites:** Docker and Docker Compose installed.

```bash
git clone https://github.com/<your-username>/ecommerce-platform.git
cd ecommerce-platform
docker compose up --build -d
```

All three services and MySQL start automatically. The `init.sql` script creates the three databases on first run.

---

## Auth Service — API Routes

| Method | Route | Auth | Description |
|---|---|---|---|
| GET | `/api/auth/health` | No | Health check |
| POST | `/api/auth/register` | No | Create account |
| POST | `/api/auth/login` | No | Get JWT token |
| POST | `/api/auth/verify` | Bearer token | Validate token |

**Register:**
```bash
curl -X POST http://localhost:5001/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"prakhar","email":"p@test.com","password":"test123"}'
```

**Login:**
```bash
curl -X POST http://localhost:5001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"p@test.com","password":"test123"}'
```

---

## Project Structure

```
ecommerce-platform/
├── services/
│   ├── auth-service/
│   ├── product-service/
│   └── order-service/
├── k8s/
│   ├── auth-service/
│   ├── product-service/
│   ├── order-service/
│   └── ingress.yaml
├── .github/
│   └── workflows/
│       └── devsecops.yml
├── monitoring/
├── docker-compose.yml
├── init.sql
└── README.md
```

---

## DevSecOps Pipeline

Every push to `main` runs:

```
Push → GitHub Actions
         ├── Trivy       (Docker image vulnerability scan)
         ├── Semgrep     (static code analysis)
         ├── GitLeaks    (secret detection)
         ├── SonarQube   (code quality)
         └── Push to ECR (only if all checks pass)
```

---

## Kubernetes

Services deploy to a local Minikube cluster with:

- Separate namespaces for dev and prod
- HPA on each service (scales on CPU)
- Liveness and readiness probes
- Nginx Ingress routing all traffic through one endpoint

---

## Status

- [x] Auth Service
- [x] Dockerfile + Docker Compose
- [ ] Product Service
- [ ] Order Service
- [ ] DevSecOps pipeline
- [ ] Kubernetes manifests
- [ ] Monitoring dashboards
