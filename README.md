# cloud-lab

Minimal cloud SaaS lab: REST APIs (FastAPI), health checks, event ingest, Prometheus-style metrics, Docker.

One codebase, honest framings for **cloud software / backend / platform** roles (not data ETL).

| Module | Demo | JD fit |
|--------|------|--------|
| REST service | `GET /health`, `GET /api/v1/sessions`, `POST /api/v1/events` | Spring Boot–style service design (Python/FastAPI) |
| Observability | `GET /metrics` (Prometheus text) | Prometheus, SLO/ops, low-latency monitoring |
| Containers | `Dockerfile`, `docker-compose.yml` | Docker, containerized microservices |

## Quick start

```bash
cd labs/cloud-lab
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python run_service.py          # prints honest stats for resume bullets
pytest -q                      # 5 passing
uvicorn cloudlab.app:app --reload --port 8000

docker compose up --build      # optional: container demo
```

## Push to GitHub (separate repo)

```bash
cd labs/cloud-lab
git init
git add .
git commit -m "feat: initial cloud-lab REST and metrics service"
git remote add origin git@github.com:mkm-007/cloud-lab.git
git push -u origin main
```

**Note:** Python/FastAPI only — do not claim Java/Spring Boot on the resume.
