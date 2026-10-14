# Ticketer Backend

Ticketer is an automated incident triage, grievance management, and support routing backend built with FastAPI, SQLAlchemy, and automated classification tooling. It classifies student and faculty incident submissions into designated operational departments, assigns urgency tiers, flags emergency safety grievances, and handles automated incident summarization and SLA escalation.

---

## 1. Architecture Overview

Ticketer acts as an API backend serving clients (such as the Ticketer Web Workbench), routing requests through an AWS Application Load Balancer and Cloudflare edge network, and persisting state across managed cloud infrastructure.

```mermaid
flowchart TD
    Client["Frontend Client\n(https://ticketer.codevaults.org)"] --> Cloudflare["Cloudflare Edge / DNS\n(https://apiticketer.codevaults.org)"]
    Cloudflare --> ALB["AWS Application Load Balancer\n(Internet-Facing / Port 80, 443)"]
    ALB --> TG["Target Group: ticketer-tg-ip\n(Port 8000 / Path: /health)"]
    TG --> ECS["AWS ECS Fargate Tasks\n(Cluster: ticketer-cluster / Service: ticketer-service)"]

    subgraph ECS Container ["Container: ticketer (Python 3.14 / uv / FastAPI)"]
        direction TB
        FastAPIApp["FastAPI Server\n(Uvicorn on Port 8000)"]
        LayaModel["Laya ML Classifier\n(PyTorch CPU)"]
        LLMClient["AsyncOpenAI Summarizer\n(OpenAI / Custom Gateway)"]
    end

    ECS --> FastAPIApp
    FastAPIApp --> LayaModel
    FastAPIApp --> LLMClient

    subgraph Managed Services ["Cloud Managed Services"]
        Supabase[("PostgreSQL Database\n(Supabase)")]
        RedisCloud[("Redis Cache & Tokens\n(Redis Cloud)")]
        ResendAPI["Resend Email Service\n(OTP & Verification)"]
    end

    FastAPIApp --> Supabase
    FastAPIApp --> RedisCloud
    FastAPIApp --> ResendAPI
```

---

## 2. Core Capabilities

### Automated Incident Classification
Every created ticket passes through the Laya classification engine (`brain/laya_interface.py`), which performs zero-shot text classification and structured decision extraction:
- Department Assignment: Routes tickets to one of five internal departments:
  - `it_support`: Wi-Fi, LMS access, campus internet, hardware/software issues.
  - `facilities`: Classroom equipment, furniture, electrical, plumbing, air conditioning, dorm maintenance.
  - `academics_admin`: Student ID cards, fee payments, receipts, transcripts, certificates.
  - `student_services`: Library support, campus transport, general inquiries.
  - `safety_committee`: Ragging, harassment, physical danger, threats.
- Urgency Scoring: Sets ticket priority to `low`, `medium`, `urgent`, or `critical`.
- Safety Hazard Flagging: Evaluates whether the submission contains safety or physical danger flags (`is_safety_grievance: true`).

### Automated LLM Summarization
An asynchronous OpenAI client (`brain/llm_interface.py`) generates a concise, 1-to-2 sentence objective synopsis of the incident text. The system implements a non-blocking fallback strategy: if external LLM gateways are unreachable or challenged, the incident text is safely truncated and stored without failing ticket creation.

### Incident Bumping and SLA Escalation
Tickets track update cycles and priority bumps (`bump_count` and `last_bump_time`). Incidents that exceed resolution thresholds can be flagged and escalated in the staff triage queue.

---

## 3. Role-Based Access Control (RBAC)

The application enforces role-based authorization via JWT authentication tokens and dependency injection (`middleware/dependencies.py`):

| Role | Scope and Permissions |
| --- | --- |
| `STUDENT` | Create incidents, view personally submitted tickets, check and renew SLA subscription, view personal profile. |
| `STAFF` | Access department triage queue (unassigned incidents plus incidents assigned to own email), claim incidents, update dispatch status (`open`, `in_progress`, `resolved`, `closed`), assign tickets to staff emails. |
| `ADMIN` | Complete institutional oversight: inspect all system tickets across all departments, view and manage all users, update user subscriptions, create proxy tickets on behalf of any student. |

---

## 4. API Reference

All protected routes require an HTTP Authorization header formatted as `Bearer <access_token>`.

### Health Check Endpoints
| Method | Endpoint | Access | Description |
| --- | --- | --- | --- |
| `GET` | `/` | Public | Root probe returning server status. |
| `GET` | `/health` | Public | Target group and container health probe. Returns `{"status":"healthy"}`. |
| `GET` | `/api/v1/health` | Public | Versioned health check endpoint. |

### Authentication Endpoints
| Method | Endpoint | Access | Description |
| --- | --- | --- | --- |
| `POST` | `/api/v1/auth/signup` | Public | Register user account and trigger verification OTP. |
| `POST` | `/api/v1/auth/verify-otp` | Public | Verify OTP code and activate account. |
| `POST` | `/api/v1/auth/signin` | Public | Authenticate credentials and return JWT access and refresh tokens. |
| `POST` | `/api/v1/auth/refresh` | Public | Exchange valid refresh token for a new access token. |
| `POST` | `/api/v1/auth/signout` | Authenticated | Invalidate and revoke current session refresh token in Redis. |

### Student / Client Endpoints
| Method | Endpoint | Access | Description |
| --- | --- | --- | --- |
| `POST` | `/api/v1/client/tickets/create` | `STUDENT`, `ADMIN` | Submit an incident description. Triggers classification and LLM summary. |
| `GET` | `/api/v1/client/tickets/all` | `STUDENT`, `ADMIN` | Retrieve all tickets created by the authenticated user. |
| `GET` | `/api/v1/client/user/details` | Authenticated | Retrieve authenticated user profile. |
| `PUT` | `/api/v1/client/user/update` | Authenticated | Update user name, password, or institute. |
| `GET` | `/api/v1/client/user/subscription` | Authenticated | Retrieve active SLA subscription status. |
| `PUT` | `/api/v1/client/user/subscription/update` | Authenticated | Toggle or renew subscription status. |

### Staff Triage Endpoints
| Method | Endpoint | Access | Description |
| --- | --- | --- | --- |
| `GET` | `/api/v1/staff/tickets/all` | `STAFF`, `ADMIN` | Fetch triage queue (unassigned incidents plus incidents assigned to the caller). |
| `PUT` | `/api/v1/staff/tickets/update/{ticket_id}` | `STAFF`, `ADMIN` | Update ticket status (`open`, `in_progress`, `resolved`, `closed`) and assigned staff email. |

### Administration Endpoints
| Method | Endpoint | Access | Description |
| --- | --- | --- | --- |
| `GET` | `/api/v1/admin/tickets/all` | `ADMIN` | Retrieve all tickets in the system across all departments. |
| `POST` | `/api/v1/admin/tickets/create` | `ADMIN` | Create a proxy ticket on behalf of a specific student email. |
| `GET` | `/api/v1/admin/user/all` | `ADMIN` | List all registered users and their roles. |
| `GET` | `/api/v1/admin/user/subscription/{user_id}` | `ADMIN` | Check subscription status for a specific user ID. |
| `PUT` | `/api/v1/admin/user/subscription/update/{user_id}` | `ADMIN` | Update subscription status for a specific user ID. |

---

## 5. Technology Stack

- Language & Runtime: Python 3.14
- Web Framework: FastAPI 0.141+ with Starlette
- ASGI Server: Uvicorn
- Package Manager: Astral `uv`
- ORM & Migrations: SQLAlchemy 2.0+ with Alembic
- Primary Database: PostgreSQL (hosted on Supabase)
- Cache & Session Store: Redis (hosted on Redis Cloud)
- Email Provider: Resend API
- Machine Learning: Laya, PyTorch (CPU-only build), Hugging Face Hub
- LLM Interface: AsyncOpenAI client
- Containerization: Multi-stage Docker build on Debian Slim
- Cloud Infrastructure: AWS ECS Fargate, AWS ALB, AWS SSM Parameter Store, Amazon ECR
- Edge & DNS: Cloudflare

---

## 6. Environment Configuration

The application reads configuration from environment variables. For local execution, define these in a `.env` file in the project root:

| Variable | Description | Required | Example |
| --- | --- | --- | --- |
| `MODE` | Runtime mode (`dev` or `prod`). In `dev`, token authentication is bypassed with default admin context. | Yes | `prod` |
| `PORT` | Port for the ASGI server to bind. Default is `8000`. | No | `8000` |
| `DEVICE` | PyTorch execution device (`cpu` or `cuda`). Defaults to `cpu`. | No | `cpu` |
| `AUTO_MIGRATE` | Run `alembic upgrade head` automatically on container start. | No | `true` |
| `POSTGRES_URL` | PostgreSQL connection string. Must use compatible driver format. | Yes | `postgresql+psycopg://user:password@host:5432/postgres` |
| `JWT_SECRET_KEY` | Symmetric key for signing and verifying JWT access tokens. | Yes | `<64-char-random-string>` |
| `REDIS_HOST` | Hostname for Redis Cloud instance. | Yes | `redis-12534.c330.asia-south1-1.gce.cloud.redislabs.com` |
| `REDIS_PORT` | Port for Redis instance. | Yes | `12534` |
| `REDIS_PASSWORD` | Password for Redis authentication. | Yes | `<redis-password>` |
| `OPENAI_API_KEY` | API key for OpenAI or compatible gateway. | Yes | `sk-...` |
| `OPENAI_BASE_URL` | Base URL for the OpenAI client. Defaults to `https://api.openai.com/v1`. | No | `https://freellm.codevaults.org/v1` |
| `RESEND_API_KEY` | API key for Resend email verification service. | Yes | `re_...` |

---

## 7. Local Development Setup

### Prerequisites
- Python 3.14
- Astral `uv` package manager (`curl -LsSf https://astral.sh/uv/install.sh | sh` on Linux/macOS or `powershell -c "irm https://astral.sh/uv/install.ps1 | iex"` on Windows)
- Git

### Installation Steps

1. Clone repository:
   ```bash
   git clone https://github.com/VinayakFTW/Ticketer.git
   cd Ticketer
   ```

2. Configure environment:
   ```bash
   cp .env.example .env
   # Edit .env and populate database connection strings and API keys
   ```

3. Install dependencies using uv:
   ```bash
   uv sync
   ```

4. Run database migrations:
   ```bash
   uv run alembic upgrade head
   ```

5. Start the development server:
   ```bash
   uv run uvicorn main:server --reload --port 8000
   ```

The API documentation will be accessible at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## 8. Docker and Containerization

The repository contains a production-ready, multi-stage `Dockerfile`:
- Stage 1 (Builder): Uses `ghcr.io/astral-sh/uv` to install dependencies into `/app/.venv` with layer caching enabled.
- Stage 2 (Runner): Minimal `python:3.14-slim` base image. Copies the pre-compiled virtual environment, adds a non-privileged system user (`appuser`, UID 10001), configures `HF_HOME` cache directories, and runs container health checks.

### Running with Docker Compose
The `docker-compose.yml` runs the backend application container directly, connecting to your remote Supabase PostgreSQL and Redis Cloud instances:

```bash
docker compose up --build -d
```

Check logs:
```bash
docker compose logs -f app
```

Shutdown:
```bash
docker compose down
```

---

## 9. Production Deployment Architecture

Production deployment runs on AWS serverless container infrastructure in region `ap-southeast-1`.

### 1. AWS Systems Manager (SSM) Parameter Store
All sensitive credentials are stored as `SecureString` parameters under the `/ticketer/` namespace in AWS SSM:
- `/ticketer/POSTGRES_URL`
- `/ticketer/JWT_SECRET_KEY`
- `/ticketer/OPENAI_API_KEY`
- `/ticketer/OPENAI_BASE_URL`
- `/ticketer/REDIS_HOST`
- `/ticketer/REDIS_PORT`
- `/ticketer/REDIS_PASSWORD`
- `/ticketer/RESEND_API_KEY`

The ECS Task Execution Role (`ecsTaskExecutionRole`) is granted permissions to read these parameters and inject them as container environment variables on task launch.

### 2. AWS ECS Fargate
- Task Definition (`aws/task-definition.json`):
  - Family: `ticketer-backend`
  - Compute: 2048 CPU units (2 vCPU) and 8192 MB Memory (to ensure sufficient headroom for PyTorch classification inference).
  - Network Mode: `awsvpc`
  - Platform: Linux x86_64
  - Logging: AWS CloudWatch logs via `awslogs` driver to group `/ecs/ticketer`.
  - Health Check: `curl -f http://localhost:8000/health || exit 1` (30s interval, 5s timeout, 3 retries).
- Cluster & Service:
  - Cluster: `ticketer-cluster`
  - Service: `ticketer-service` (Maintains desired count of 2 replicas across availability zones).
  - Security Group: `sg-09f8dd93a7fa67a9b` allows incoming TCP port 8000 traffic originating from the ALB Security Group (`sg-04f9b651414b9df16`).

### 3. AWS Application Load Balancer (ALB)
- The internet-facing Application Load Balancer distributes traffic across active ECS Fargate task IP addresses.
- Target Group: `ticketer-tg-ip`
  - Target type: `ip`
  - Port: 8000
  - Health check path: `/health` (HTTP 200 required).

### 4. Cloudflare Edge and DNS
- Public Hostname: `https://apiticketer.codevaults.org`
- DNS: Cloudflare CNAME record pointing `apiticketer.codevaults.org` to the AWS ALB DNS hostname.
- SSL / TLS: Full (Strict) encryption between Cloudflare edge and AWS ALB.
- CORS Configuration: Handled in `main.py` allowing requests from `https://ticketer.codevaults.org`, `https://apiticketer.codevaults.org`, and local development origins.

### 5. Automated CI/CD Pipeline
Deployment is fully automated using GitHub Actions workflows:

1. Pull Request Verification (`.github/workflows/ci.yml`):
   - Triggers on pull requests to `master` and `main`.
   - Checks Python syntax and builds Docker image dry-run using GitHub Actions cache.
2. Production Deployment (`.github/workflows/deploy.yml`):
   - Triggers on push to `master` or `main`.
   - Assumes AWS IAM Role via GitHub OIDC federation (`AWS_ROLE_ARN`).
   - Logs into Amazon Elastic Container Registry (ECR).
   - Builds the Docker image, tags it with the Git commit SHA and `latest`, and pushes to ECR repository `ticketer-backend`.
   - Renders the updated container image into `aws/task-definition.json`.
   - Registers a new task definition revision with AWS ECS.
   - Deploys the revision to `ticketer-service` in `ticketer-cluster` with `wait-for-service-stability: true`, executing a zero-downtime rolling update.

---

## 10. Operations and Troubleshooting

### Viewing CloudWatch Logs
To stream production logs from ECS tasks:
```bash
aws logs tail /ecs/ticketer --follow --region ap-southeast-1
```

To filter for runtime errors:
```bash
aws logs filter-log-events \
  --log-group-name "/ecs/ticketer" \
  --filter-pattern "ERROR" \
  --region ap-southeast-1
```

### Checking Target Group Health
Verify that task IP targets are registered and passing health checks:
```bash
aws elbv2 describe-target-health \
  --target-group-arn "arn:aws:elasticloadbalancing:ap-southeast-1:944921953100:targetgroup/ticketer-tg-ip/a7490e5293dc17d4" \
  --region ap-southeast-1
```

### Database Migrations
Database migrations execute automatically on container startup when `AUTO_MIGRATE=true` via `docker-entrypoint.sh`. To manually apply Alembic migrations against the production database:
```bash
alembic upgrade head
```
To generate a new migration revision after modifying models in `schemas/postgredb_schema.py`:
```bash
alembic revision --autogenerate -m "describe_migration_changes"
```
