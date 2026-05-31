# Warehouse Management System (Project B)

[![Django](https://img.shields.io/badge/Django-6.0-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.16-red.svg)](https://www.django-rest-framework.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-blue.svg)](https://www.docker.com/)
[![Coverage](https://img.shields.io/badge/Coverage-84%25-brightgreen.svg)](https://coverage.readthedocs.io/)
[![CI/CD](https://github.com/yourusername/projectb-warehouse/actions/workflows/project_b.yml/badge.svg)](https://github.com/yourusername/projectb-warehouse/actions/workflows/project_b.yml)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📋 Overview

**Warehouse Management System (Project B)** is a production-ready microservice that handles inventory management, stock movements, real-time stock tracking, and analytics. It seamlessly communicates with **Project A (Bookstore)** via REST API to provide accurate, real-time inventory data.

This project demonstrates a **microservices architecture** where two independent Django applications communicate via REST API, each with its own database, cache, and task queue.

### Business Value

- **Real-time inventory tracking** across multiple warehouses
- **Automated stock alerts** when products reach critical levels
- **Analytics and reporting** for data-driven decisions
- **Secure API communication** between Bookstore and Warehouse services
- **Async task processing** for heavy operations (daily reports, low stock checks)

---

## 🏗 Architecture Diagram

```text
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                                    PROJECT B                                        │
│                              (Warehouse Service)                                    │
│                                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────────────┐    │
│  │                           INGRESS (NGINX :8443)                             │    │
│  │                         (Reverse Proxy / SSL)                               │    │
│  └─────────────────────────────────────┬───────────────────────────────────────┘    │
│                                        │                                            │
│                                        ▼                                            │
│  ┌─────────────────────────────────────────────────────────────────────────────┐    │
│  │                         GUNICORN (Django Application)                       │    │
│  │                                                                             │    │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐            │    │
│  │  │Worker 1 │  │Worker 2 │  │Worker 3 │  │Worker 4 │  │Worker 5 │            │    │
│  │  │ (API)   │  │ (API)   │  │ (API)   │  │ (API)   │  │ (API)   │            │    │
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘  └─────────┘            │    │
│  └─────────────────────────────────────┬───────────────────────────────────────┘    │
│                                        │                                            │
│                    ┌───────────────────┼───────────────────┐                        │
│                    │                   │                   │                        │
│                    ▼                   ▼                   ▼                        │
│  ┌─────────────────────────┐  ┌─────────────────┐  ┌─────────────────────────┐      │
│  │       PostgreSQL        │  │      Redis      │  │        Celery           │      │
│  │       (Database)        │  │  (Cache/Broker) │  │     (Task Queue)        │      │
│  │                         │  │                 │  │                         │      │
│  │  ┌─────────────────────┐│  │  ┌─────────────┐│  │  ┌─────────────────────┐│      │
│  │  │   Persistent Data   ││  │  │  Fast Cache ││  │  │  Async Workers      ││      │
│  │  │   ACID Compliant    ││  │  │  Message    ││  │  │  Scheduled Tasks    ││      │
│  │  └─────────────────────┘│  │  │    Broker   ││  │  │  (Beat Scheduler)   ││      │
│  └─────────────────────────┘  │  └─────────────┘│  │  └─────────────────────┘│      │
│                               └─────────────────┘  └─────────────────────────┘      │
│                                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────────────┐    │
│  │                         MONITORING & LOGGING                                │    │
│  │                                                                             │    │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │    │
│  │  │   Sentry    │  │   Flower    │  │   Logs      │  │   Metrics   │         │    │
│  │  │  (Errors)   │  │  (Celery)   │  │  (Files)    │  │  (Custom)   │         │    │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘         │    │
│  └─────────────────────────────────────────────────────────────────────────────┘    │
│                                                                                     │
│                                    │                                                │
│                                    │ HTTPS / REST API / API Key                     │
│                                    ▼                                                │
└─────────────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                    PROJECT A                                    │
│                              (Bookstore Service)                                │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐    │
│  │                              API ENDPOINTS                              │    │
│  │                                                                         │    │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │    │
│  │  │   Orders    │  │   Books     │  │  Payments   │  │   Stock     │     │    │
│  │  │   API       │  │   API       │  │   API       │  │   API       │     │    │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘     │    │
│  │                                                                         │    │
│  │  Communication: GET /api/stock/{id}/ - POST /api/stock/{id}/reserve/    │    │
│  └─────────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────────┘


## 🔗 Inter-Service Communication

### How Project B Communicates with Project A

Project B communicates with Project A via REST API endpoints:

| Method | Endpoint | Purpose | Authentication |
|--------|----------|---------|----------------|
| GET | `/api/stock/{id}/` | Check product stock availability | API Key |
| POST | `/api/stock/{id}/reserve/` | Reserve stock for an order | API Key |

### Client Implementation

```python
# inventory/services.py
class ProjectAClient:
    def __init__(self):
        self.base_url = settings.PROJECTA_URL
        self.api_key = settings.PROJECTA_API_KEY
    
    def check_product_stock(self, product_id):
        response = requests.get(
            f"{self.base_url}/api/stock/{product_id}/",
            headers={'X-API-Key': self.api_key},
            verify=False
        )
        return response.json()


Project B (Warehouse)                    Project A (Bookstore)
       │                                        
       │  1. GET /api/stock/1/                  │
       │     Headers: X-API-Key                 │
       │ ──────────────────────────────────────►│
       │                                        │
       │  2. Verify API Key                     │
       │                                        │
       │  3. Check product stock                │
       │                                        │
       │  4. Response: {stock: 25}              │
       │ ◄──────────────────────────────────────│
       │                                        │
       │  5. POST /api/stock/1/reserve/         │
       │     Body: {quantity: 1, order_id: 123} │
       │ ──────────────────────────────────────►│
       │                                        │
       │  6. Reserve stock                      │
       │                                        │
       │  7. Response: {success: true}          │
       │ ◄──────────────────────────────────────│



### 2. 📊 Error Handling & Logging

```markdown
## 📊 Error Handling & Logging

### Logging Levels

| Level | File | Use Case |
|-------|------|----------|
| DEBUG | `logs/all.log` | Development debugging |
| INFO | `logs/all.log` | General operations |
| ERROR | `logs/error.log` | Failures and exceptions |

### Error Handling Strategy

| Scenario | Handling |
|----------|----------|
| **Project A unavailable** | Log error, return None, don't block operations |
| **Product not found** | Return None with warning log |
| **Timeout** | Retry up to 3 times, then fail gracefully |
| **Invalid API Key** | Log error, return 401 equivalent |

### View Logs

```bash
# View all logs
docker compose exec app tail -f logs/all.log

# View errors only
docker compose exec app tail -f logs/error.log



### 3. 🔄 CI/CD Pipeline (Detallada)

```markdown
## 🔄 CI/CD Pipeline (GitHub Actions)

### Pipeline Jobs

| Job | Description | Dependencies |
|-----|-------------|--------------|
| **Lint** | Flake8 code style check | None |
| **Test** | Run all tests with PostgreSQL and Redis | None |
| **Security** | Bandit security scan | None |
| **Docker** | Build and test Docker image | Lint, Test |
| **Deploy** | Automatic deployment to production | Docker |

### Pipeline Configuration

The pipeline runs automatically on:
- `push` to `main` branch
- `pull_request` to `main` branch
- Manual trigger (`workflow_dispatch`)

### Required GitHub Secrets

| Secret | Purpose |
|--------|---------|
| `DEPLOY_HOST` | Production server IP |
| `DEPLOY_USER` | SSH username |
| `DEPLOY_KEY` | SSH private key |


### 4. 🚀 Production Deployment

```markdown
## 🚀 Production Deployment

### Requirements

| Component | Requirement |
|-----------|-------------|
| **OS** | Ubuntu 22.04 / Debian 12 |
| **Docker** | Version 24.0+ |
| **RAM** | Minimum 2GB |
| **Storage** | Minimum 20GB |

### Deployment Steps

```bash
# 1. Connect to server
ssh user@your-server.com

# 2. Clone repository
git clone https://github.com/yourusername/projectb-warehouse.git
cd projectb-warehouse

# 3. Configure environment
cp .env.example .env
nano .env

# 4. Deploy
docker compose up -d --build

# 5. Run migrations
docker compose exec web python manage.py migrate

# 6. Create superuser
docker compose exec web python manage.py createsuperuser

# 7. Verify deployment
curl https://yourdomain.com/api/inventory/warehouses/



### 5. 📈 Sentry Monitoring

```markdown
## 📈 Sentry Monitoring

### Configuration

```python
# settings.py
sentry_sdk.init(
    dsn=os.getenv('SENTRY_DSN'),
    integrations=[DjangoIntegration(), CeleryIntegration()],
    environment='production',
    traces_sample_rate=0.1,
)



### 6. 🔒 Security Features (Ampliar)

```markdown
## 🔒 Security Features

| Feature | Implementation | Purpose |
|---------|----------------|---------|
| **JWT Authentication** | `rest_framework_simplejwt` | Stateless token-based auth |
| **Role-Based Access Control** | Django groups + custom permissions | Granular access per endpoint |
| **API Key** | `X-API-Key` header | Secure inter-service communication |
| **CORS Configuration** | `django-cors-headers` | Controlled cross-origin requests |
| **Rate Limiting** | Nginx + Django | Prevent abuse (100 req/minute) |
| **HTTPS** | Nginx SSL termination | TLS encryption |
| **SQL Injection Protection** | Django ORM | Parameterized queries |
| **XSS Protection** | Django templates | Auto-escaping |
| **CSRF Protection** | `CsrfViewMiddleware` | CSRF prevention |
| **Secure Headers** | Django SecurityMiddleware | X-Frame-Options, HSTS |
