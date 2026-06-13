# cloud-lab

Minimal cloud SaaS lab: REST APIs (FastAPI), health checks, event ingest, Prometheus-style metrics, Docker.

One codebase, honest framings for **cloud software / backend / platform / developer tooling** roles (not data ETL).

| Module | Demo | JD fit |
|--------|------|--------|
| REST service | `GET /health`, `GET /api/v1/sessions`, `POST /api/v1/events` | Spring Boot–style service design (Python/FastAPI) |
| **Secrets / CLI** | `python run_secrets_cli.py list/get/mount-env` | Client secrets, developer platform, `.env` mounting |
| **Agentic workflows** | `python run_agent.py` | GenAI agents, prompt grounding, hallucination checks |
| Observability | `GET /metrics` (Prometheus text) | Prometheus, SLO/ops, low-latency monitoring |
| Containers | `Dockerfile`, `docker-compose.yml` | Docker, containerized microservices |

## Quick start

```bash
cd labs/cloud-lab
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# NVIDIA / cloud SaaS interview
python run_service.py          # prints honest stats for resume bullets
pytest tests/test_api.py -q      # 5 passing

# 1Password / developer platform interview
python run_secrets_cli.py list --project web-app
python run_secrets_cli.py mount-env --project web-app --output .env.local
pytest tests/test_secrets.py -q  # 8 passing

# Campbell's / agentic AI interview
python run_agent.py
pytest tests/test_agent.py -q    # 6 passing

pytest -q                      # full suite
uvicorn cloudlab.app:app --reload --port 8000

docker compose up --build      # optional: container demo
```

## Push to GitHub (separate repo)

```bash
cd labs/cloud-lab
git add .
git commit -m "feat: secrets CLI module for developer platform demos"
git push origin main
```

**Note:** Python/FastAPI only — do not claim Java/Spring Boot, Rust, or Go on the resume.
